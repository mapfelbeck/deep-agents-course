from presidio_analyzer import AnalyzerEngine, PatternRecognizer, Pattern, RecognizerResult
from presidio_anonymizer import AnonymizerEngine
from presidio_analyzer.nlp_engine import SpacyNlpEngine
import re
import hashlib
from typing import Dict, List, Tuple

# 1) Set up Presidio
# python -m spacy download en_core_web_lg
nlp_engine = SpacyNlpEngine(models=[{"lang_code": "en", "model_name": "en_core_web_lg"}])
# a trained model would work better but blank should be fine
# nlp_engine = SpacyNlpEngine(models=[{"lang_code": "en", "model_name": "blank:en"}])
analyzer = AnalyzerEngine(nlp_engine=nlp_engine, supported_languages=["en"])
anonymizer = AnonymizerEngine()

# 2) Add custom resume-focused recognizers (LinkedIn, GitHub, personal URLs)
linkedin_pattern = Pattern(
    name="linkedin_pattern",
    regex=r"(?:https?://)?(?:www\.)?linkedin\.com/in/[A-Za-z0-9\-_]+/?",
    score=0.8
)
github_pattern = Pattern(
    name="github_pattern",
    regex=r"(?:https?://)?(?:www\.)?github\.com/[A-Za-z0-9\-_]+/?",
    score=0.8
)
personal_site_pattern = Pattern(
    name="personal_site_pattern",
    # Tighter than a generic URL to avoid over-redacting; tune as needed
    regex=r"(?:https?://)?(?:www\.)?(?:[A-Za-z0-9\-]+\.)+(?:dev|io|app|me|com|net|org)(?:/[^\s]*)?",
    score=0.4
)

linkedin_recognizer = PatternRecognizer(
    supported_entity="LINKEDIN",
    patterns=[linkedin_pattern]
)
github_recognizer = PatternRecognizer(
    supported_entity="GITHUB",
    patterns=[github_pattern]
)
personal_site_recognizer = PatternRecognizer(
    supported_entity="PERSONAL_SITE",
    patterns=[personal_site_pattern]
)

analyzer.registry.add_recognizer(linkedin_recognizer)
analyzer.registry.add_recognizer(github_recognizer)
analyzer.registry.add_recognizer(personal_site_recognizer)

# 2b) Helpers to keep non-PII "years of experience" / skill mentions intact.
# Presidio's default recognizers frequently misclassify experience durations
# (e.g. "5 years", "3+ years") as DATE_TIME, and tool/technology names
# (e.g. "Python", "AWS") as ORGANIZATION. Neither is actually PII, so we
# filter these out before redacting.
EXPERIENCE_DURATION_RE = re.compile(
    r"^\d+(?:\.\d+)?\+?\s*(?:years?|yrs?|months?|mos?)$", re.IGNORECASE
)

SKILL_CONTEXT_RE = re.compile(
    r"(?:"
    r"(?:experience|expertise|proficiency|proficient|skilled|skill|knowledge|"
    r"familiar|hands-on|exposure|certified|certification)\s+(?:with|in|using|of)"
    r"|"
    r"\d+(?:\.\d+)?\+?\s*(?:years?|yrs?|months?|mos?)\s+(?:with|in|using|of)"
    r")\s*\Z",
    re.IGNORECASE,
)


def _is_experience_duration(entity_type: str, matched_text: str) -> bool:
    """True for DATE_TIME matches that are really a duration of experience
    (e.g. "5 years", "3+ years", "18 months") rather than a calendar date."""
    return entity_type == "DATE_TIME" and bool(
        EXPERIENCE_DURATION_RE.match(matched_text.strip())
    )


def _is_skill_mention(entity_type: str, matched_text: str, text: str, start: int, window: int = 40) -> bool:
    """True for matches that look like a tool/technology named directly in a
    skills/experience phrase (e.g. "experience with Python", "3 years using
    AWS", "familiar with Docker") rather than real PII. Requires one of the
    skill-indicating phrases to appear immediately before the match so that
    generic mentions like "worked at Acme Corporation" are left alone.

    spaCy's NER sometimes misclassifies tool/technology names as ORGANIZATION
    or even PERSON (e.g. "Docker"). For PERSON/NRP/MISC we only exempt
    single-token matches, since real personal names in this context almost
    always contain a space (e.g. "John Smith")."""
    if entity_type in ("PERSON", "NRP", "MISC") and " " in matched_text.strip():
        return False
    if entity_type not in ("ORGANIZATION", "ORG", "PERSON", "NRP", "MISC"):
        return False
    preceding = text[max(0, start - window):start]
    return bool(SKILL_CONTEXT_RE.search(preceding))


# 3) Helper to build consistent tokens and preserve reversibility
def token_for(entity: str, value: str, counter: Dict[str, int]) -> str:
    # Option A: deterministic hash per value per entity
    digest = hashlib.sha1(value.encode("utf-8")).hexdigest()[:8]
    return f"[{entity}_{digest}]"

def redact_with_mapping(text: str, language: str = "en", score_threshold: float = 0.35):
    # Analyze
    results: List[RecognizerResult] = analyzer.analyze(
        text=text,
        language=language,
        score_threshold=score_threshold
    )

    # Sort results by start offset to build deterministic replacements
    results = sorted(results, key=lambda r: (r.start, -r.score))

    # Create mapping and perform manual replacement so we can control tokens
    mapping: Dict[str, str] = {}  # token -> original
    reverse_spans: List[Tuple[int, int, str]] = []  # spans used to replace later
    used_spans = []

    # Avoid overlapping replacements by tracking taken intervals
    def overlaps(a, b):
        return not (a[1] <= b[0] or b[1] <= a[0])

    counters: Dict[str, int] = {}

    for r in results:
        span = (r.start, r.end)
        if any(overlaps(span, s) for s in used_spans):
            continue
        original = text[r.start:r.end]
        entity = r.entity_type.upper()

        if _is_experience_duration(entity, original) or _is_skill_mention(entity, original, text, r.start):
            continue

        token = token_for(entity, original, counters)

        mapping[token] = original
        reverse_spans.append((r.start, r.end, token))
        used_spans.append(span)

    if not reverse_spans:
        return text, mapping

    # Apply replacements from end to start to avoid index shifts
    redacted_text = []
    last_idx = 0
    for start, end, token in sorted(reverse_spans, key=lambda x: x[0]):
        redacted_text.append(text[last_idx:start])
        redacted_text.append(token)
        last_idx = end
    redacted_text.append(text[last_idx:])
    redacted = "".join(redacted_text)

    return redacted, mapping

def redact(text: str, language: str = "en", score_threshold: float = 0.35) -> str:
    """Redact PII in `text` and return only the redacted text (no mapping).

    This is a convenience wrapper over `redact_with_mapping` for callers that
    do not need to reverse the redaction.

    Args:
        text: The text to redact.
        language: Presidio language code (default "en").
        score_threshold: Minimum confidence score for a detection to be
            redacted (default 0.35).

    Returns:
        The redacted text.
    """
    redacted, _mapping = redact_with_mapping(
        text, language=language, score_threshold=score_threshold
    )
    return redacted

def unredact(text: str, mapping: Dict[str, str]) -> str:
    # Replace tokens back to original
    # Sort by length to avoid partial overlaps
    for token in sorted(mapping.keys(), key=len, reverse=True):
        text = text.replace(token, mapping[token])
    return text

if __name__ == "__main__":
    sample1 = """John Q. Public
    Email: john.public@example.com
    Phone: (555) 123-4567
    LinkedIn: https://www.linkedin.com/in/johnpublic
    GitHub: github.com/jpublic
    Address: 1234 Main St, Seattle, WA 98101
    """

    sample2 = """ANTHONY RIVERA
    Email: anthony.rivera@gmail.com
    Phone: (312) 884-2019
    LinkedIn: https://www.linkedin.com/in/anthonyrivera
    GitHub: github.com/arivera-dev
    Address: 4820 N Kedzie Ave, Chicago, IL 60625
    """

    sample3 = """DIEGO TREVIÑO FERRER
    Email: diego.trevino.ferrer@outlook.com
    Phone: (786) 401-5573
    LinkedIn: https://www.linkedin.com/in/diegotrevinoferrer
    GitHub: github.com/dtrevino
    Address: 2115 SW 22nd St, Miami, FL 33145
    """

    sample4 = """Juan Sebastian Cabra
    Email: js.cabra@protonmail.com
    Phone: (469) 233-7148
    LinkedIn: https://www.linkedin.com/in/juansebastiancabra
    GitHub: github.com/jscabra
    Address: 908 Elm St, Dallas, TX 75202
    """

    all_samples = [sample1, sample2, sample3, sample4]
    for i, sample in enumerate(all_samples, start=1):
        print(f"Processing sample{i}...")
        redacted, mapping = redact_with_mapping(sample)
        print("Redacted:\n", redacted)
        print("Mapping:\n", mapping)
        print("Restored:\n", unredact(redacted, mapping))

    # Remove the redundant processing of 'sample' outside the loop