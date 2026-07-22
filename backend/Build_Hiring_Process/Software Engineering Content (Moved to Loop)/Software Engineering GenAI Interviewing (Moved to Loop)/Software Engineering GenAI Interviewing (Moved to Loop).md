# Software Engineering GenAI Interviewing  (Moved to Loop)

This page is for discussion purposes only. Location and guidelines TBD.

# How to use this question bank

The GenAI interview is designed as a supplement to the technical interview process for candidates who are being interviewed for GenAI\-specific roles or who have knowledge of GenAI that we need to assess. 

This question bank contains a questions and represents the competencies and skills that successful candidates will exhibit around Generative AI. Unless the candidate is specifically being hired for a GenAI focused role, do not try to use all of these questions in an interview.

Question Bank



| **Question** | **Core answer** | **Bonus points:** |
| --- | --- | --- |
| What technical knowledge is useful to know when interacting with an LLM? | Answer should include:* Tokens * Prompt Engineering * Context | The candidate’s answer does not need to include these, but mentioning these would show a deeper understanding of the subject:* Temperature, top\_p, top\_k, and/or stop sequence * Parameters * Tuning / Base Models * Auto\-regression (looping over the prompt/answer) |
| What is RAG? | Answer should include a significant discussion of how to provide context to an LLM and what prompt engineering techniques are appropriate to getting responses from a RAG system. Answer should also include discussion of vector search. | Not required, but ideally candidate will mention citations.Be aware that technically, RAG does not need to include vector databases. Any system that initiates a search and uses the results of that search in the context of a prompt to an LLM is a RAG system. 95% of the time, “RAG” means vector search, and so the candidate should discuss this, but calling out that it is technically not a requirement for RAG is accurate. |
| In the discussion of LLMs, what is a vector, why is it important, and how do we use it? | Answer should include a discussion of * How LLMs represent semantic meaning * Parameters/variables/etc. * N\-dimensional space and vector math * The use of vectors in vector search * Which use cases are best for vector search, vs more traditional search | Extra credit for mentioning:* Different vector databases/vendors * Which use cases are best for vector search * How LLMs identify parameters and how they relate to human semantics * How an LLM uses vectors to respond to prompts. |
| What is an Agent or an “Agentic Workflow” | Generally: an Agent is a system that uses an LLM (or LLMs) to execute multiple steps to perform a complex task.The answer should probably include discussion of at least two: * self\-reflection/introspection * planning * task breakdown * orchestration | Extra credit for:* Discussing the role of chaining and tools. * Discussing different types of agents, such as flow, conversation, and orchestration * Tooling or prompt engineering discussions |
| What is prompt engineering, and what are some good techniques for prompt engineering? | Overview should be straight forward (?)Candidate should include at least three of these approaches in their answer:* Zero\-shot/few\-shot * Roles * Chain\-of\-thought * Generated Knowledge * Prompt Modifiers * Reflection | Bonus if they include five or more approaches/techniques.And more if they include real\-world examples |
| What is fine tuning? | Answer should include some discussion of base models, minimum data quantity, and cost. |  |
| What types of Generative AI Models are there? | This answer has a lot of different possible answers, and the specific answer will give you insight into the candidate’s depth of knowledge.A perfectly acceptable answer would be:* Text\-based * Image\-based * Audio\- or Video\-based * multi\-modal | A more in\-depth answer might group all of the above under “Transformers” or “LLMs” and also differentiate some or all:* GAN * Transformer Encoder * Diffusion * VAE * NeRF * Action\-based (Large Action Models * BERT  A candidate who dives into the details of transformers, transformer encoders, BERT, etc, may have very deep knowledge. (But do make sure they are not going inappropriately deep for the level of question you asked.) |
|  |  |  |

