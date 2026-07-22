# Architect+ Initial Interview Script

### Overview

Technically focused discussion, additional emphasis on communication and ability to lead DE team members, be a velocity multiplier, work with clients from a technical perspective. This is not intended to assess their ability to be a DE capability leader (ie. take on direct reports, participate in pursuits).

There are a total of six screening questions with time boxes. A Q\&A session will follow. Example questions are included in this candidate's evaluation.

Introduction: 5 minutes, who we are, what we do, why we’re going to ask the questions we have for them today

**Data Engineering Skill 1 to 3**  
Question 1: Data Processing SQL (5 min)  
Question 2: Data Processing w/Python (5 min)  
Question 3: Data Modeling POV (5\-8 min)  
Question 4: Data Pipeline POV (5\-8 min)  
Question 5: Git / Repo / SDLC POV (5 min)  
Question 6: Serverless / Containers POV (5 min)

Side note: Have them refer to work they’ve done during the answer

**Communication 1 to 3**  
Evaluate communication style across all the responses.  
Questions are designed to engage with the candidate and have a meaningful discussion  
Are they clear, concise or are they rambling and taking up time.

### Details

#### Question 1: Data Processing SQL (5 min)

”The SQL Customer Orders Problem”

See: Interview Question Bank 

Expected responses

* The subquery approach \- select max timestamp grouped by customer id, self\-join back to the main table on customer id \= customer id, and max timestamp \= timestamp to filter out the most recent order for each customer
* The window function approach \- rank orders by customer id and timestamp, select all the ones with rank \= 1
* Some will struggle to arrive at the solution, but they know there needs to be a subquery used to filter the results, try to coach them. If they talk about a sub select with an inner join, they are probably able to solve it with some coaching

Unexpected responses

* Trying to order by the customer id or order id, we state the ids are random and not sequential. They should be using the timestamp column to determine recency.
* Using the TOP function to pick the most recent, this will not give you anything at a customer level
* General rambling, bouncing around different techniques, not really landing on any approach

#### Question 2: Data Processing w/Python (5 min)

“The Word Count Problem”

See: Interview Question Bank 

* Given a 1 GB CSV file with words in it. Identify count of word occurrences?
* How do you scale the solution to a 100 GB CSV file?

Expected responses

* Implementing word count from scratch \- breaking up the text using whitespace as the separator. Loading each word into a dictionary, incrementing the count as you traverse the list of words
* Using a scaled out approach using Spark and Dataframes \- using Dataframe functionality to break up the words and increment the counts
* Any other answers using distributed processing framework, maybe Python Dask or Ray
* Similar solution using Java, for candidates not familiar with Python.

Unexpected responses

* Talking through the problem at too high of a level, they are basically re wording the question another way, and not really talking about the solution with enough detail
* Talking about adding more memory or CPU for the scaled out solution. We’re looking for a solution that can scale out more than that.

#### Question 3: Data Modeling POV (5\-8 min)

Not yet added to Interview Question Bank

You have raw clickstream data ingested from an ecommerce site and landed in in Azure Blob/S3/Google storage. Client wants to analyze the data with SQL and also run predictive analysis for a recommendation engine. How would you approach the data modeling?

Expected responses:

* A good example from one of our candidates is listed below, there can be a lot of variability in this answer. We want to see that they were the person doing the modeling, and it was not done by another team or by another architect along side them.

*They provided a great answer, leading with first understanding the clickstream data and producing a data dictionary of known entities/attributes after a preliminary analysis of the source data. They also understand the users of the BI app, their requirements and business cases. The users may need computed columns or the data laid out in a different manner to support analyst tasks. They mentioned possibly creating snapshot tables to support preditcive analysis.*

*They then went on to describe the dimensional modeling process, including facts, dimensions, scd type 2 dimensions and a few of the other types of scds. They prefer scd2 of all the scd types for the historical view. They also mentioned partitioning and indexing to improve performance, and called out the denormalized nature of dimensional models as an advantage for fast performance (vs 3nf)*

Unexpected responses

* High\-level speak around “adding business value” without discussing the actual modeling techniques used.
* No awareness of dimensional modeling terms: facts, dimensions, star schema

#### Question 4: Data Pipeline POV (5\-8 min)

Not yet added to question bank

Your customer wants to implement a net\-new cloud platform on Snowflake\*. Client has raw data initially landed in cloud object storage. Your first step is to enable analytics in Snowflake using Tableau dashboards. How would you design the architecture? How would you automate and orchestrate it?

* Change to BigQuery, Redshift, Synapse, Databricks as applicable for candidate

Expected responses

* Solution is driven by an automated framework that supports logging, monitoring and alerting.
* Solutions involving Apache Airflow, Azure Data Factory, AWS Step Functions, Google Dataflow, or any other type of data orchestration framework
* Automated testing and deployment are addressed

Unexpected responses

* Solution involves only manual steps
* Candidate led a team who built the solution, and they were not involved.

#### Question 5: Git / Repo / SDLC POV (5 min)

Not yet added to question bank

Tell me about the last Pull Request you approved or the last Merge Conflict you helped to resolve

Expected responses

* Experience with Pull Request code reviews, discussion of criteria for accepting or rejecting the review
* Description of the merge conflict challenges, working with the engineer to resolve the merge

Unexpected responses

* No experience using source control on their project
* Candidate was too far removed from the building process to get involved with the code repositories

 

#### Question 6: Serverless / Containers POV (5 min)

What is your point of view on using Serverless vs Containers for building data pipelines?

Expected responses

* Serverless is good for short\-running jobs, less than 15 minutes.
* It’s a convenient approach with low management overhead, need to watch the invocation costs though
* It can be challenging to bundle the DE frameworks into Serverless environment
* Containers are great for long\-running batch jobs. Docker images make it easy to package up the DE frameworks.

Unexpected responses

* Using a Virtual Machine over Serverless or Containers. This is a legacy cloud pattern, although suitable for small\-scale and proofs of concept.
* Candidate preferring VMs because they are more scalable and easier to maintain. It’s a lot of overhead to keep the VMs patched and up\-to\-date.
