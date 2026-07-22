# Sample Technical Interview Summary Email 3 [KEEP]

I recommend that we  **PROCEED** with candidate as a **Senior Engineer** in the **\<build\-center\-name\> \<**capability\-name\> team.

I enjoyed my chat with the candidate, they were nice and personable. They had some gaps/experience\-mismatches for some of the work we do, but their strength with GenAI topics indicates that they can perform at the Senior Engineer level.

I thought their code\-writing and problem solving skills were strong. However, they were only willing to write the code in Python, and weren’t comfortable doing the coding in .NET, Java.

We skipped the object/data modelling/SQL sections in favor of GenAI questions, due to candidate’s experience in that area. They were able to come up with a pretty good architecture for a RAG application, and showed a good understanding of the strengths and weaknesses of different LLM models.

While I think they can perform as a Senior Engineer on back\-end or GenAI projects, I would suggest that they will need to focus on getting more full\-stack experience (especially with a more modern tech\-stack), and getting more exposure to the design/modelling decisions in larger applications and databases.

# Overall

* **Technical Proficiency**: Good
* **Consulting Presence**: Fair
* **Persistence and Curiosity:** Fair

# Details

**Communication (Fair/Good)**

* Nice and personable
* Interview was a bit frenetic paced: talked quickly and bounced between incorrect solutions before arriving at the correct answers
* They were easy to understand, but I had to repeat/rephrase my questions a couple of times when asked

**Code Writing (Good)**

* Had to use Python, wasn't comfortable coding in Java, .NET, or JavaScript
* Was able to write the code for the SuperEven exercise correctly


	+ but had the extra mod 10 condition
* Was able to add start/end parameters, and a validation (when prompted)

**Unit Testing (Fair/Good)**

* Came up with many test conditions


	+ had to prompt them for performance related test\-cases, but they got the right answer then
* When asked about testability of the code, they didn't initially think of outputting an array of strings, and was gonna test the *cout* output directly


	+ Talked about outputting a single file with results, then using that as a "golden file" and comparing the outputs against it..
	
	
		- Seems like a legacy system approach
* Didn't come up with the correct code refactor into 2 methods to make it more easily testable

**Problem Solving (Good)**

* Came up with a few ideas for optimizing CPU and memory


	+ including
	
	
		- caching
		- using counters to track progress instead of use the mod operator
		- use a smaller but repeatable range of numbers to cache
		- moved to using arrays at some point
* Didn't optimize memory storage or what's being stored in the arrays

**Object Modelling (Poor)**

* Not very familiar it seemed, took a lot of hints to come up with a basic entity or two
* Not familiar with the word entity,
* Didn't come up with a way to connect the two entities

**Data Modelling (Fair)**

* Took some time and a couple of hints, but eventually came up with the 2\-tables needed
* Used string/bool…etc. as the types instead of the SQL types

**SQL (Not Covered)**

* N/A

**Front end / Backend (Not Covered)**

* N/A

**GenAI (Good)**

* Described a RAG architecture well, including chunking and optimization approaches
* Provided good prompt approaches and (with prompting) described guard rails and safety approaches.
* Selected good models for embeddings and chat completions, and was able to describe reasoning for and against use of particular models for particular challenges
* Suggested tooling for agentic workflows, but was unable to fully explain the advantages and disadvantages of using tools/function calls over chains for this use case.

**Questions for me:**

* A couple of questions about projects and how teams collaborate each week

trueupdatesAdd a table with key/value pairs in order to display its data on another page using the Page Properties Report macro.



| **2024 GenAI Update** | 1 1 complete Update Summary email (3\) to reflect SE Technical Interview script to (including GenAI topics) |
| --- | --- |

