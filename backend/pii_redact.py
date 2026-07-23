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
#nlp_engine = SpacyNlpEngine(models=[{"lang_code": "en", "model_name": "blank:en"}])
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

def unredact(text: str, mapping: Dict[str, str]) -> str:
    # Replace tokens back to original
    # Sort by length to avoid partial overlaps
    for token in sorted(mapping.keys(), key=len, reverse=True):
        text = text.replace(token, mapping[token])
    return text

if __name__ == "__main__":
    sample = """John Q. Public
    Email: john.public@example.com
    Phone: (555) 123-4567
    LinkedIn: https://www.linkedin.com/in/johnpublic
    GitHub: github.com/jpublic
    Address: 1234 Main St, Seattle, WA 98101
    """

    redacted, mapping = redact_with_mapping(sample)
    print("Redacted:\n", redacted)
    print("Mapping:\n", mapping)
    print("Restored:\n", unredact(redacted, mapping))