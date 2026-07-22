# General Initial Interview Script

This page provides an example script for conducting an initial interview of a candidate interviewing for the Engineer or Senior Engineer role. That being said, the script can serve as a framework for interviewing Architects, Senior Architects, Principals and beyond, by feathering into each section more in\-depth or architecturally\-relevant questions. You can find role\-specific questions by using the **CDF Role** column to filter/sort questions found at Sample Technical Screening Questions. 

As described on Engineer Technical Leveling Criteria, the depth of your questions and your expectation for the candidate’s answers are proportional to the role for which the candidate is interviewing. The more senior the role, the more you expect from the candidate.

noteRemember: We are primarily looking for **Technical Proficiency** while getting a sense of their **consulting presence** and **persistence and curiosity** in this interview. The Script will reflect those outcomes.


Remember: We are primarily looking for **Technical Proficiency** while getting a sense of their **consulting presence** and **persistence and curiosity** in this interview. The Script will reflect those outcomes.


## Initial Interview Script

#### Intro:

* Hi, this is \[your name] from Slalom.
* \[Recruiter’s name] set up a half\-hour phone call.
* Is now still a good time?
* Goal of today’s call is to get to know you and get a feeling for your **technical proficiency** in a lot of different areas to get a better understanding for where you would fit in here.
* We use Generative AI in our day\-to\-day work here at Slalom, but for this conversation I’m looking to learn more about YOU and so I request that you do **not** use an LLM or search engine.
* I have to issue a disclaimer of sorts: I may interrupt ya or cut you off at points.  That is in no way intended to convey a lack of interest in you or what you have to say, but interruptions are sometimes necessary to ensure we're able to cover the maximum amount of content.  Please don't take offense!  And know that, if we had extended time, I would love to talk at length about today's subject matter.

#### Foundational Skills:

* Propose a problem and ask how they might solve it.  Look for the data structures and search algorithms they suggest.  Ask about pros and cons of their answers.


	+ Example: I've got a million phone numbers to store and search through.  
	
	
		- What are some data structures that come to your mind for solving this problem?
		- What are some search algorithms that come to your mind?
* Ask/look for understanding of Big O


	+ Big O is a very CS\-oriented view \- really looking to know if they understand what will make a code block run slow. While resources (like database connections) are a component, we are looking for a more fundamental understanding e.g. nested loops across massive arrays.
* Define/describe iteration and recursion


	+ Ask for pros and cons of each
* Define/describe interface vs abstract base class.


	+ Why choose one over the other
* Define/describe generics.


	+ When would you use them?
* Describe callbacks


	+ Ask/look for examples in various languages
* Ask about features of a language, platform, or framework they claim on their resume


	+ Ex: delegates, lambdas, LINQ, etc.
	+ Ex: AWS services (EC2/ECS/RDS/Dynamo/Lambda etc)
* *You can find more sample questions for this section of the interview at this link:* [https://slalom.atlassian.net/wiki/spaces/NDTS/pages/1811677269/Sample\+Technical\+Screening\+Questions\#Category%3A\-Fundamentals](https://slalom.atlassian.net/wiki/spaces/NDTS/pages/1811677269/Sample+Interviewing+Questions+Moved+to+Loop#Category%3A-Fundamentals)

#### Front End:

* Propose a situation that would require validation and ask how they would handle validation


	+ Look for server and client side validation \- value of both
	+ Look for understanding of RegEx
	+ Pros and cons of various approaches
* Propose a visual change to a website that would be site\-wide.  Ask how they would handle?
* Look for understanding of HTML, CSS, JavaScript
* Look for understanding of APIs \- REST? GraphQL?
* Look for basic understanding of security


	+ What is OAuth? Federation? JWT?
	+ What is CORS?
* If applicable, Look for understanding of mobile frameworks and approaches
* *You can find more sample questions for this section of the interview at this link:* [https://slalom.atlassian.net/wiki/spaces/NDTS/pages/1811677269/Sample\+Technical\+Screening\+Questions\#Category%3A\-Front\-End](https://slalom.atlassian.net/wiki/spaces/NDTS/pages/1811677269/Sample+Interviewing+Questions+Moved+to+Loop#Category%3A-Front-End)

#### Database:

* Propose a table and ask the candidate to write queries to obtain data from the table
* Look for an understanding of SELECT, WHERE, COUNT, ORDER BY, GROUP BY, DISTINCT
* If the candidate is capable and time allows, ask about JOINs
* If time allows: Differentiate document databases and Relational databases
* *You can find more sample questions for this section of the interview at this link:* [https://slalom.atlassian.net/wiki/spaces/NDTS/pages/1811677269/Sample\+Technical\+Screening\+Questions\#Category%3A\-Data](https://slalom.atlassian.net/wiki/spaces/NDTS/pages/1811677269/Sample+Interviewing+Questions+Moved+to+Loop#Category%3A-Data)

**Generative AI**:

* Ask if/how they use Generative AI as a tool in their software development work.


	+ Example: Do you regularly use GitHub Copilot or Amazon Q Developer? 
	
	
		- If they do, ask **how** they use it.
		- If they do not, ask why (be aware this may be because of limits set by their employer.)

*If their resume indicates they have GenAI experience:*

* What is Prompt Engineering?
* What do LLMs do well at, and what do they not do well at?
* *You can find more sample questions for this section of the interview at this link:* [https://slalom.atlassian.net/wiki/spaces/NDTS/pages/1811677269/Sample\+Technical\+Screening\+Questions\#Category%3A\-Generative\-AI](https://slalom.atlassian.net/wiki/spaces/NDTS/pages/1811677269/Sample+Interviewing+Questions+Moved+to+Loop#Category%3A-Generative-AI)

#### Operations/Troubleshooting \[if time allows]:

* Working with code


	+ Why are branches useful?
	+ How do you handle a merge conflict?
	+ How do you set aside your work so you can work on an urgent bug?
* What are the compute/storage services in AWS (or Azure or GCP)? 


	+ When would you use relational vs bucket storage?
	+ When would you use a VM vs a container?
	+ What is cloud formation (or terraform) used for?
* Ask if they know what ports 80 and 443 are used for
* How would they connect to a remote Linux/Unix or Windows box?
* How would they diagnose a connectivity issue?


	+ Look for ping, tracert, firewall
* How would you diagnose a problem with a web server?
* *You can find more sample questions for this section of the interview at this link:* [https://slalom.atlassian.net/wiki/spaces/NDTS/pages/1811677269/Sample\+Technical\+Screening\+Questions\#Category%3A\-Operating](https://slalom.atlassian.net/wiki/spaces/NDTS/pages/1811677269/Sample+Interviewing+Questions+Moved+to+Loop#Category%3A-Operating)

#### Conclusion:

* \[If time allows or it's a strong candidate] We have time for a question or two, is there anything you’d like to ask me?
* Thank you for your time today!
* \[Recruiter’s name] will be in touch with you in a couple days about next steps.  Have a great day!

*If you have any feedback or questions related to the content on this page, send us an email at* [*build\-interviewing\-feedback@twodegrees1\.onmicrosoft.com*](mailto:build-interviewing-feedback@twodegrees1.onmicrosoft.com)*.*

# Markdown Template

noteThis note\-taking template is representative of the core “what we do’s” as software engineers (Advise, Analyze, Design, Develop, Test, Deploy, Run)


This note\-taking template is representative of the core “what we do’s” as software engineers (Advise, Analyze, Design, Develop, Test, Deploy, Run)


none20241028\-TechInterview\-candidate.notes.md

I recommend that we \*\*\[DO\|DO NOT]\*\* move forward with candidate as \[Engineer\|Sr. Engineer\|Architect\|Sr. Architect]. \[add detailed summary here]

\# Brief History

\*Scale: None/Poor/Fair/Good/Excellent\*

\# Overall:

\* Technical Proficiency: None/Poor/Fair/Good/Excellent
\* Consulting Presence: None/Poor/Fair/Good/Excellent
\* Persistence and Curiosity: None/Poor/Fair/Good/Excellent


\# Details

\#\# Design/foundational skills: None/Poor/Fair/Good/Excellent

\* Design Patterns
\* Data structures
\* Algorithms
\* Recursion
\* Structured/OOP vs Functional
\* Callbacks


\#\# Develop: None/Poor/Fair/Good/Excellent

\#\#\# Front End: None/Poor/Fair/Good/Excellent

\* Page Structure
\* Input Validation
\* Modern Web Frameworks
\* REST vs GraphQL
\* Serverless
\* Security
 \- JWT
 \- CORS


\#\#\# Database: None/Poor/Fair/Good/Excellent

\* Data Access
\* Indexes
\* Joins \- Inner vs Outer
\* NoSQL vs RDBMS
\* Queries

\#\#\# Language Specific: None/Poor/Fair/Good/Excellent

\* Javascript
\* Python
\* .Net
\* Java


\#\# Test: None/Poor/Fair/Good/Excellent

\* Test Pyramid
\* Unit Testing vs Integration Testing
\* Testing
 \* Three Laws of TDD


\#\# Deploy: None/Poor/Fair/Good/Excellent

\* Cloud Providers 
 \- Azure
 \- AWS
 \- GCP
\* Continuous Integration
\* Continuous Delivery


\#\# Run: None/Poor/Fair/Good/Excellent

\* System Operations
\* Source Management
\* Troubleshooting technique
\* Depth of fact finding


\#\# Advise: None/Poor/Fair/Good/Excellent

\* Agile
 \- Team
 \- Work Estimation
\* Project Ramp Up/Learning 


\#\# Analyze: None/Poor/Fair/Good/Excellent

\* Break down a monolith (for Sr Arch \+)




\# Questions About Slalom, Interview, Next Steps

\*
trueupdatesAdd a table with key/value pairs in order to display its data on another page using the Page Properties Report macro.



| **2024 GenAI Update** | 1 1 complete Update script to include GenAI guidance   2 2 complete Add reference to sample questions related to GenAI |
| --- | --- |
| **2024 SE Capability Update** | 3 3 complete Update script to reflect SE Purpose, Core Values, How\- and What we Do.   4 4 complete Ensure appropriate coverage of applicable non\-technical topics to ensure ‘consulting\-minded engineers’ |

