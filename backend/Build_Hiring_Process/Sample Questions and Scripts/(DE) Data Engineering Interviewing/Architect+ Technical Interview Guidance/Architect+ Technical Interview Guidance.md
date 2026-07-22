# Architect+ Technical Interview Guidance

## Overview

We currently have a standardized approach for Engineer/Senior Engineer initial screen and following technical interview. The technical interview approach for Architect\+ roles has largely been interviewer\-specific and inconsistent across candidates. Standardizing the approach for Architect\+ technical interviews will facilitate candidate evaluation, role leveling, and the onboarding of new interviewers. It will also create a better candidate experience as we iterate on the approach as a team and improve it for the future.

DATA ENGINEERING  
COMMUNICATION

Score a 1 \- 2 \- 3 (within the context of the role they are interviewing for)  
1 \- person would need significant ramp/up or mentoring to be successful. not ready

2 \- TBD \- most people will likely end up here. ready for project work, may need some ramp up/coaching/support

3 \- can handle complex, multi\-pod projects, they are ready to go. solid, staff them immediately.

## Approach

The technical interview process consists of an Initial Screen followed by a Technical Interview. The Initial Screen is performed virtually through a phone call or Teams meeting. Previously, the Technical Interview was performed in\-person with an option to use the whiteboard. It has switched to a virtual format with white boarding software starting in 2020\.

### Initial Screen

The purpose of the initial screen is to ensure the candidate has the right level of technical skills to lead teams at the project or program level, aligned with the role’s requirements defined by the Slalom Build CDF. The areas covered in the initial screen consist of Engineering Proficiency, Cloud Knowledge, Industry Points of View, and Learning Potential. Any skill gaps noted during the interview process should be minor and not prohibitive to the candidate being staffed within 2 weeks of hire date at Slalom.

The interviewer should come out of the Initial Screen with a Proceed or Do Not Proceed decision along with a role leveling recommendation. Our previous mindset has centered around “A Maybe means No”. If the interviewer is undecided about a candidate and feels they should continue on with the process, make the case for a Yes and highlight the candidate’s strong suits.

#### Engineering Proficiency

This section of the interview ensures that the candidate can support Engineers and Senior Engineers on a project, and perform the Delivery work themselves when necessary. It also ensures the candidate has the right technical skills to lead during a Discovery phase, including making the correct technical recommendations for the solution.

##### Programming/Scripting

Start with the "SQL customer orders" problem and the "Python word count" problem (see Interview Question Bank ). These are the core foundational skills required to do the work. If you can deduplicate datasets with SQL and process data with a programming language, you are capable of building DE solutions. The candidate has to solve one of the problems confidently in order to proceed. Ideally, they solve both. You can provide some coaching, but they need to arrive at the solution on their own.

* Data processing with SQL \- SQL customer orders deduplication, find the most recent order for every customer
* Programming language proficiency \- Python (or other) word count, given a text file, return a list of each word and the number of times it appears in the file

See the Interview Question Bank page for details

##### Development Toolset

Assess familiarity with the DE toolset. Can they be hands on? They should be able to answer all of these questions. It is OK if they have only used one shell, such as bash. A solid understanding of Git, proficiency at the shell prompt, and enough development experience to have an opinion about code editors is required.

* Tell me about a (Git) merge conflict, how does that happen?
* What's your favorite code editor (e.g. VS Code, Jetbrains tools, vim) and why?
* What's your favorite shell (e.g. bash, fish, zsh) and why?

#### Skills Validation

Focus on the candidate’s most recent roles within the past 5\-7 years. Explore their skills profile.

* Ask questions based on skills they list in their profile.
* Validate they know what they say they know.
* Make sure they understand the work and are not just managing teams that do the work
* Explore their experience with agile and team leadership

#### Points of View (Communication)

Ask about points of view, get their opinions and thoughts. Try to relate it to their past 5\-7 years experience. There needs to be an engaging discussion here. Some example topics include:

* TARGETED
* Tell me about data lake vs data warehouse vs delta lake (ie lakehouse)
* What are your DOs and DON’Ts around data modeling
* Tell me about a recent decision related to an architecture that you would revisit. What would you change? What worked well?
* HIGH LEVEL OVERARCHING
* Did they answer the question they were asked.
* Did they ask clarifying questions

### Tech Rounds

Focus on the cloud in Tech Rounds. At this point, we have leveled the appropriately and determined that they have the potential to be a successful Architect\+ in Build DE. Consider the following

* Which cloud do they know best and at what level?


	+ Can they learn other cloud platforms besides the ones they know
* Do we think they can lead a team and participate in agile ceremonies


	+ Will their adoption of PEM be feasible?
	+ Are they new at team leadership, what is the experience level?
* Can we staff them within 2 weeks as a Sr Engineer?


	+ Can they transition to Architect\+ for their next project? If not, what would that take?
