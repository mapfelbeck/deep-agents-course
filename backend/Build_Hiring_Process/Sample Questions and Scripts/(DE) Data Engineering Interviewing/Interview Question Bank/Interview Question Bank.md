# Interview Question Bank

Data Storage Concepts

| **Type of Question (fundamentals, problem solving, etc)** | **Area** | **Question** | **Notes** |
| --- | --- | --- | --- |
| Fundamentals | Databases | * What is a NoSQL database? * How is it different from a RDBMS? * What are different kind of NoSQL databases? 	+ Key Value database (AWS DynamoDB, Azure CosmosDB, etc.) 	+ Document databases (MogonDB, AWS DocumentDB, Azure CosmosDB) 	+ Graph databases (Neo4j, AWS Nepture, Azure CosmosDB Gremlin API, etc.) | RDBMS scales up whereas NoSQL databases scales out |
| Advanced | Databases | * What are trade\-offs of NoSQL Databases? * What is CAP theorem? 	+ Most NoSQL databases trade\-off “Consistency” against Performance and Availability according to CAP theorem |  |
| Fundamentals | Databases | * What are MPP databases and how are they different from traditional databases? * What are some design considerations when designing a data model in a MPP database? * How to enforce unique key constraints in a MPP database? * What are the use cases for noSQL databases? |  |
| Fundamentals | Database Design | * What is the difference between Primary Key, Surrogate Key and a Natural Key? * Describe the benefit of dimensional modeling * What is a Star Schema and what are its benefits? * What are Slowly Changing Dimensions? * Why do we use surrogate keys, do we always need to? * What is the benefit of primary keys? * How do we decide to make a set of columns one dimension or two? * Give an overview of an ETL system you built * What is an index and how does it work? * What are some differences between a transactional and analytical database? 	+ Provide an example of each (ie SQL Server, Oracle \= transactional  ...  Redshift, Teradata, Netezza \= analytical) |  |
| Fundamentals | Big Data / Hadoop | * What is Big Data? * What types of problems does it help to solve? * What defines a big data project? * What are some Big Data platforms? (Hadoop, Spark, Redshift, Cassandra, and many others) * If you had to define "Big Data" with a data volume, what would it be? (near 100TB and up is an acceptable answer) * What is a Hadoop cluster? * What are the various components that make up a Hadoop cluster, and what do they do? (Hive, Pig, Oozie, Zookeeper, YARN, HBase, Tez, etc) * What types of nodes does a Hadoop cluster have? (Primary and secondary name node, data nodes, edge nodes) * What is different from a primary and secondary name node? * Describe a scenario where you would/wouldn't use Hadoop for data processing * How does Hadoop store data (HDFS / S3\), and what makes it different from a regular computer file system? (Scalable, Distributed, Replicated) * What are some of the differences between the Hadoop distributions? (Hortoworks HDP, Amazon EMR, Cloudera CDH, MapR) |  |
| Fundamentals | Data Lake | * What is a data lake and how can they be organized? * What is the difference between a Data Lake and Data Warehouse? |  |
| Fundamentals | Streaming | * How would you collect, store and analyze a real time stream of data? |  |
| Problem Solving | Troubleshooting | * You are a Developer working on a Data Warehouse/ETL project. One day you notice one of the jobs that usually takes 15 minutes to run is taking 4 hours.  	+ How would you troubleshoot this? 	+ What if there has been no change in the incoming data volume? * You are a Developer working on a Data Warehouse/ETL project. One day you notice that a few of your incremental data jobs just pulled back full sets of data.  	+ What could some of the reasons be? (source system restated, ETL metadata table got corrupted) |  |

Data Comprehension (SQL)

| **Type of Question (fundamentals, problem solving, etc)** | **Area** | **Question** | **Notes** |
| --- | --- | --- | --- |
| Problem Solving | SQL | * What is the difference between where vs having in a SQL statement * Table A has 2 rows. Table B has 4 rows 	+ Someone Writes a join but the query returned 8 rows. What could have happened? Cartesian Product due to Cross join, duplicate data, incorrect join condition 	+ Someone writes a join but the query returned 6 rows. What could have happened? Full Outer Join * You have a database table with Customer Orders. Columns are as follows: 	+ **Columns** 		- Customer Id \- unique identifier for each individual customer 		- Customer Name \- First name and last name 		- Order Timestamp \- Order date and time, down to the millisecond 		- Order Number \- unique identifier for each individual order 		- Sales Amount \- dollar amount for the order 	+ **Questions** 	+ How do you get the Sales Amount for each Customer's most recent order using SQL?  		- What's another way you can do that in SQL? (you can join to a derived table with customer id and max timestamp, or use a windowing function with rank/sort) 		- Which way do you think will be faster? |  |
| Fundamentals | SQL Best Practice | * Share any SQL best practices you have employed/ |  |
| Fundamentals | SQL \- semi structured querying | * You have some JSON data loaded into a column. How would query this in a database of your choice. |  |
| Fundamentals | SQL Basics | * What is the difference between a Table and a View? |  |
| Fundamentals | SQL Basics | * What is the difference between a SQL DDL vs DML statement? |  |
| Intermediate | Window function | * What is a Window Function in SQL? * How is it different from Group By clause? |  |
| Fundamentals | Sub queries | * What are sub\-queries in SQL? When do you use a sub\-query? |  |
| Advanced | Sub queries | * What is the difference between a corelated subquery vs non\-corelated sub query? * What is the performance implication of using a corelated subquery? | Co\-related Sub queries execute multiple times for outer query whereas non\-corelated sub queries are executed once in an outer query. |
| Intermediate | Stored Procedures | * What are stored procedures in SQL? * What are the use\-cases of using Stored Procedures? | Stored Procedures encapsulate complex logic and allow re\-usability. |
| Intermediate | Materialized Views | * What are Materialized Views? * How are they different from regular Views? |  |
| Fundamentals | Spark | * What is Spark and how is it different than Map Reduce? * What is an RDD and what are some if its characteristics (distributed, can rebuild from lineage, read\-only) * What is a DataFrame, and how is it different than an RDD? * Describe the following Spark concepts: Driver application, Master node, Executors |  |
| Intermediate | Spark | * What is a Spark DAG? * What are transformations and actions in Spark? 	+ Focus on lazy evaluation vs eager evaluation * What are the advantages of lazy evaluation? |  |
| Advanced | Spark | * What is the difference between narrow vs wide transformations in Spark? 	+ Narrow transformations do NOT shuffle data across executors (Filter, Drop) 	+ Wide transformation may shuffle data across executors (GroupBy, Distinct) * What is a Shuffle operation in Spark? * How is data shared across executors? * What is Tungsten Binary Format in Spark? |  |
| Advanced | Spark | * What is the function of Catalyst Optimizer in Spark? 	+ Catalyst is Spark SQL optimization engine. It optimizes Spark SQL and generates Java byte code. * What are two kind of optimizations Catalyst performs? 	+ Rule based 	+ Cost based |  |
| Advanced | Spark trouble shooting | * You have a Spark ETL job that reads Apache Parquet data file, performs various transformations and then writes the result to another Parquet file. A developer on the team has enhanced the code and introduced “collect()” method at the end. The job was running fine initially but is now consistently failing. What could be problem with the code? 	+ The collect method brings all the data from Executor nodes on to the Driver node. The Driver node may not have enough memory to hold the data. |  |

 

Engineering (Programming)

| **Type of Question (fundamentals, problem solving, etc)** | **Area** | **Question** | **Notes** |
| --- | --- | --- | --- |
| Fundamentals | General | Class vs Object |  |
| Fundamentals | General | Inheritance / Polymorphism / Encapsulation |  |
| Fundamentals | General | REST and HTTP Response Codes | * Informational responses (100–199\), * Successful responses (200–299\), * Redirects (300–399\), * Client errors (400–499\), * Server errors (500–599\). |
| Fundamentals | Python | What is the difference between a List and a Dictionary |  |
| What is the difference between list, set and tuple |  |
| How would you performance optimize your python code |  |
| What are Asynchronous functions? |  |
| What are recursive functions? |  |
| Problem Solving | * Given a 1 GB CSV file with words in it. Identify count of word occurrences? * How do you scale the solution to a 100 GB CSV file? 	+ File Split? 	+ Database? 	+ Big Data framework? |  |
| Given a list of numbers\- 1. Give me all the duplicate values 2. Give me the list without duplicates |  |
| How would you scrape data from the web? |  |
| list1 \= \[12, 15, 32, 40]display numbers divisible by 4 |  |
| Write a script to display:1 1 2  1 2 3 1 2 3 4 1 2 3 4 5 |  |
| Intermediate | List comprehension | What is list comprehension used for in Python?`numbers = [1,2,3,4,5]``newnumbers = [ x*2 for x in numbers]` | To create a list by performing operation on an existing list |
| Intermediate | Lambda Function | What are Lambda functions in Python? | Anonymous function |
| Advanced | Problem solving | Given a Python list as following, create another list where each number of first list is multiplied by 2 without using loop or list comprehension`numbers = [1,2,3,4,5]``newnumbers = list(map(lambda x: x * 2 , numbers ))` | Use Lambda function with in map function |
| Advanced | Problem solving | Given a Python list as following, create another list where each number of first list is an even number without using loop or list comprehension`numbers = [1, 2, 3, 4, 5]` `even_numbers = list(filter(lambda x: (x % 2 == 0), numbers ))` | Use Lambda function within a filter function |
| Fundamentals | Bash | How to reference positional arguments in a script? | $1 $2 |
| Problem Solving | How to get 3rd element from each line from a file ? | awk '{print $3}' |
| Problem Solving | How to check if file exist on filesystem ? | bashif \[ \-f /var/log/messages ] then echo "File exists" fi |
| Problem Solving | How to get 10th line from the text file ? | head \-10 file\|tail \-1 |
| Problem Solving | How to run a script in background ? | add "\&" to the end of script |
| Fundamentals | What does "chmod 500 script" do ? |  |
| Fundamentals | Security | What is the difference between authentication and authorization? |  |
| Advanced | Security | What is SSO? What are some advantages of using SSO? | SSO helps in streamlining enterprise wide authentication and authorization with many applications |
| Intermediate | Security | What is the difference between data masking \& data encryption? |  |

Cloud

| **Type of Question (fundamentals, problem solving, etc)** | **Area** | **Question** | Notes |
| --- | --- | --- | --- |
| Fundamentals | Cloud basics | * What is the difference between IaaS vs PaaS vs SaaS? * Can you give an example of each of the above? | IaaS \- Infrastructure as servicePaaS \- Platform as a serviceSaas \- Software as a service |
| Fundamentals | Cloud basics | * What does it mean by the term “Serverless”? |  |
| Fundamentals | Cloud basics | * What is a REST API? What is the underlying technology used by REST APIs? | http |
| Fundamentals | Client tools | * What are some AWS client tools have you used? * How does AWS client tools interact with AWS platform? * What kind of operations can you do with AWS Client tools? Provide examples. | AWS CLI/Powershell use AWS APIs to interact with AWS platform such as create S3 bucket/EC2 instance, etc. |
| Fundamentals | S3 | * Client wants to build file system in the cloud. Is S3 a good fit? * Performance optimizing PUTs on S3 * What is lifecycle management in S3 * What is versioning in S3? How would you access a file that is versioned * What is VPC endpoint for S3 |  |
| Fundamentals | IAM | * What is ARN * Sections of a policy | “Effect”: “Allow”,“Action”: \[“iam:Get\*”,“iam:List\*”],“Resource”: “\*” |
| Fundamentals | Lambda | * What is cold start in Lambda functions * How would you access a resource in a private subnet through a lambda function * What are Lambda Layers. How else can you manage dependencies? * What is a trigger? You want to spawn a lambda when file lands in S3 |  |
| Fundamentals | Redshift | * What is it? How is it different from SQL Server * How to Performance Tune in Redshift * Data Distribution 	+ Sort Keys? How do they work 		- Compound (in the order they are listed) vs Interleaved (equal weights) Sort Key 	+ Distribution Keys? How do they work – EVEN, KEY, ALL * Best way to load data from S3? What are some best practices to follow? 	+ COPY command 		- Data Formats – CSV, Delimiter, JSON 		- IgnoreHeader 		- Remove Quotes 		- Time Format 		- Truncate Column 		- COMPUPDATE – Find compression and bake it in * Query concurrency \- Workload Management’s queues to increase throughput 	+ Handle surprise and anticipated bursts of activity * Amazon Redshift’s default table structure uses EVEN distribution with no column encoding. This data structure is suboptimal for many types of queries. * Improve performance with Analyze and Vacuum * Compression Encoding 	+ Types of encoding – RAW vs LZO * What is Amazon Redshift Spectrum – what is it used for? * What services would you use to build a streaming solution for analytics? |  |
|  | Athena | * What are some considerations should be made while using Athena? * What limitations you have encountered with using Athena 	+ Max partitions 100 	+ No Stored procs * Distinguish Athena from Redshift Spectrum |  |
|  | Glue | * What are the use cases for AWS Glue service? * What are the considerations for selecting between executing a Spark job with AWS Glue vs AWS EMR? |  |

ML Mathematics \& Statistics

| **Type of Question (fundamentals, problem\-solving, etc)** | **Area** | **Question** | **Notes** |
| --- | --- | --- | --- |
| fundamental | P\-VALUE | What is p\-value? What does it mean? How is it calculated? | Probability that the result is at least as extreme as the one we saw compared to the hypothesis. If the p\-value is 0\.04, it means that there's a 4% chance we would see this result assuming that what we have hypothesized as true. Any further examples should indicate a strong grasp. |
|  |  | How is p\-value used in the context of machine learning algorithms? | Look for examples here. One helpful guide comes from linear regression where the null is that the slope is zero while the alternative is that it is NOT |
| fundamental | LINEARITY | Suppose we are analyzing some two\-dimensional data \[provide an example\- e.g. total sales in y and sale price in x]. The graph looks "curved" and looks like it could be fit with an exponential model. what kind of regression would you performing, linear or non\-linear? | Look for an understanding of linearity between parameters vs non\-linearity between parameters. The exponential regression is an interesting case\- the ability to use a log transform implies it is in fact linear in parameters |
|  |  | Suppose you had to explain to the client why you chose the model you chose. Say the exponential model. The model has certain parameters. How would you describe to the client why you thought the model was linear from the POV of hypothesis testing. | Look for answers along the lines of hypothesizing the slope of the linearized (log transformed) exponential equation |
| problem\-solving | DIMENSIONALITY REDUCTION | what is a high dimensional problem? | Look for answers that relate sample size requirement to the number of dimensions (features), distance function calculations, and their uselessness in nearest neighbours, similarity calculations. Also probe for examples from recent experiences |
| problem\-solving |  | How does one mitigate it and can you give examples of this in your work experience? \[Any ML engineer has to have experienced this at some point] | Look for examples of experience using PCA, non\-negative matrix factorization, LDAs etc. |
| problem\-solving |  | What is PCA? | Answers along the lines of transforming existing data to a new set of fewer dimensions by associating the greatest variance to the "first component", the second greatest variance to "second component" |
| problem\-solving |  | What is LDA? How is it different from PCA? | PCA assumes no classes vs LDA is supervised. It also assumes normality of distribution. PCA is used for components that maximize variance while LDA looks for components that maximize class separation |
| fundamental | BIAS VARIANCE TRADEOFF | What is bias vs what is variance? | Variance refers to the amount by which predictions would change if we estimated it using a different a completely different dataset.Bias refers to the error that is introduced by predictions by using a much simpler model |
| general |  | Can you give me examples where your models exhibited either one scenario and your attempts to tackle either. | Look for answers that relate simplicity with interpretability. Another way to gauge a candidate's experience is to probe for a holistic experience\- "how would you pick a model with 5 parameters and 80% accuracy vs a model with 100 parameters and 90% accuracy"? |
| general | PERFORMANCE | What is precision? What is recall? | Simple formula regurgitation isn’t enough. Probe for when either could be more important than the other. e.g. in cancer detection, recall is far more important\[ false negatives are disastrous]. Good answers are those that display an understanding of the cost of false\-positive vs false\-negative. |
| general | PERFORMANCE | what is a confusion matrix? | A table of performance of a ML classification algorithm. Use in conjunction with precsion\-recall question above. |
| general | STATS | Explain bayes' theorem | This one is too vast to have an explanation of a “Good answer”. In expecting interviewers themselves to know this well enough to guage the candidate. But, the following are good guidelines:Understanding of prior and posterior probabilitiesUnderstanding of likelihood functions |
| general | STATS | what is a likelihood function? | Probabililty that the data will be fit by a certain model **given** the pameters. Probe for understanding of MLEs |
| general | PERFORMANCE | How do you avoid overfitting a model? Can you give an example of this from your own experience? | Looking for regularization, model simplicty \[fewer params], cross validation |
| general | PERFORMANCE | How do you handle an imbalanced dataset | Look for examples from work experience\- sine there is no one size fits all approach here look for up\-sampling, downsampling, synthetic samples \[SMOTE], |
| fundamental | NEURAL NETS | Explain what a neural network is and your experience with them \[for junior candidates\- look if they have deployed one simply to learn , compete in kaggle, practice with datasets, etc.] | Look for an answer along the lines of the use of a gradient descent method to update weights in inputs that are passed through an activation function to simulate a probability measure of predictions. Probe deeper for bonus points on the inner workings of Gradient descent, why a neural network overtrains, the fundamental reasoning behind their usage \[universal function approximators], etc. |
| fundamental | NEURAL NETS | How would you explain a neural network to a client? | No right answer here\- look for answers from experience and ask for the type of neural nets they have deployed and how they impacted the business? |
| problem\-solving | PERFORMANCE | Vanishing gradient Problem:What is it and how does one resolve it \[give me one or two examples] | The gradients\- as computed using partial derivatives of the loss function, sometimes become extremely small. This implies that the weights do not update at all and training all but stops. This happens typically with deeper networks since initial layers need updates. But with many layers and many chain rules, the weights sometimes do not update since the activation function itself places a limit on the range of values.A good way to resolve is to use rectifiers\- like RelU but even that isn't enough since it is only effective for positive inputs |
| fundamental | PERFORMANCE | What is cross\-validation and can you give me an example of some of the challenges you faced regarding cross\-validation with a recent project? | Taking n\-subsamples of the data, shuffling them, and using n\-1 subsets as the training set. This reduces variance \[essentially a bagging technique] and bias since it uses most of the data |
| fundamental |  | Tell me about a project where ensemble learning featured prominently and why? | Look for experience with tree based methods \[Random forests, xgboost, etc.] |
| fundamental |  | What are recommendation systems? What are the various types? What's the high\-level difference? | Look for definition within the realms of a system that predicts the ratings users/consumers give to items and/or the likelihood of users consuming \[buying, liking, etc.] various products, services etc.Collaborative filtering makes assumptions about users with similar traits will continue sharing the traits. Requires a lot of data to start with \["cold start"]Content\-based filtering technique relies on attributes of the items/products themselves and a history of affinity towards these products |

Visual Analytics Concepts

| **Type of Question (fundamentals, problem solving, etc)** | **Area** | **Question** | **Notes** |
| --- | --- | --- | --- |
| Fundamentals | Visual Analytics Concepts | What is a wireframe? What is your process for building a wireframe? |  |
| Fundamentals | Visual Analytics Concepts | Describe a use case for when you would use data visualization? |  |
| Fundamentals | Visual Analytics Concepts | What are some scenarios that you’d use a data visualization tool over a tool like excel? |  |
| Fundamentals | Visual Analytics Concepts | What makes a well\-constructed visualization? |  |
| Fundamentals | Visual Analytics Concepts | If you were to create one dashboard for a high\-level executive audience and another for a group of operational managers, how might the dashboards be different? |  |
| Fundamentals | Visual Analytics Concepts | What are some common elements of design for dashboards (Experience Design)? |  |
| Fundamentals | Visual Analytics Concepts | What is the concept of row level security and why is it important for reports/dashboards? |  |
| Problem Solving | Visual Analytics Concepts | How can you visualize more than three dimensions in a single chart? |  |
| Problem Solving | Visual Analytics Concepts | What visuals could best display* relationships? * distributions? * comparisons? |  |
| Problem Solving | Visual Analytics Concepts | Describe a dashboard that could present analysis that is:* descriptive? * prescriptive? * predictive? |  |

Data Vizualization Tools

| **Type of Question (fundamentals, problem solving, etc)** | **Area** | **Question** | **Notes** |
| --- | --- | --- | --- |
| Fundamentals | Power BI | Are there any updates to the Power BI platform in the past year that you have been particularly excited to see? |  |
| Fundamentals | Power BI | What is the difference between a Report vs Dashboard |  |
| Fundamentals | Power BI | What is the difference between a Measure vs Column |  |
| Fundamentals | Power BI | Data Connections: What are the various methods to connect to data, and describe a use case for each one? | Direct Query, Import, Live Connection, Composite |
| Fundamentals | Power BI | What does “modelling” refer to, and can you describe what an optimal model looks like for Power BI? |  |
| Fundamentals | Power BI | Can you describe what publishing refers to, and how an end user typically access a report? |  |
| Fundamentals | Power BI | When would you use Power BI desktop over the Service? |  |
| Fundamentals | Power BI | Suppose you had a report that wasn’t performing up to standards. What are some performance optimization techniques that could be applied? |  |
| Problem Solving | Power BI | If you wanted to limit a user to view data only for the region they are in, how would you go about doing that? | Row Level Security |
| Problem Solving | Power BI | What options are available to link to another page in the report? | bookmarks, drillthrough |
| Problem Solving | Power BI | What options are available to change interaction behavior visuals in a report? | highlight vs filter vs none |
| Fundamentals | Tableau | Are there any updates to the Tableau platform in the past year that you have been particularly excited to see? |  |
| Fundamentals | Tableau | Product Offerings: Can you describe the various components of tableau and their functions? | Reader, Public, Server, Online, Desktop |
| Fundamentals | Tableau | What is the difference between a Set vs Group |  |
| Fundamentals | Tableau | What is a Story in Tableau, and when may stories be used in a business scenario? |  |
| Fundamentals | Tableau | What is the difference between a Join vs Blend |  |
| Fundamentals | Tableau | What is the difference between Discrete vs Continuous |  |
| Fundamentals | Tableau | What is the difference between a Measure vs Dimension |  |
| Fundamentals | Tableau | Data Connections: What are the various methods to connect to data, and describe a use case for each one? |  |
| Problem Solving | Tableau | What does a primary data source refer to when on the topic of data blending? |  |
| Problem Solving | Tableau | Do you usually use layout containers? Why or why not? |  |
| Problem Solving | Tableau | If you wanted to restrict data that a user sees based on the region they belong to, how could you go about doing that? |  |

Orchestration/Data pipelines

| **Type of Question (fundamentals, problem solving, etc)** | **Area** | **Question** | **Notes** |
| --- | --- | --- | --- |
| Fundamentals | Tools | Name of a few data orchestration tools you have used for automating data pipeline steps | AirFlow, Azure Data Factory, AWS StepFunctions, BMC Control\-M, etc. |
| Intermediate | Concept | What does it mean by “idempotent” data pipeline? | Running an idempotent data pipeline multiple times with the same input will always produce the same output |
| Fundamentals | AirFlow | Define core components of Apache AirFlow architecture | Metadata DB, Workers, Scheduler |
| Fundamentals | AirFlow | What is an Airflow DAG? What does it mean by “Acyclic” in DAG? | Acyclic means that there can NOT be a closed loop in a graph. |
| Intermediate | AirFlow | Describe is the difference between an Operator and Sensor? | * [Operators](https://airflow.apache.org/docs/apache-airflow/stable/core-concepts/operators.html), predefined task templates that you can string together quickly to build most parts of your DAGs. * [Sensors](https://airflow.apache.org/docs/apache-airflow/stable/core-concepts/sensors.html), a special subclass of Operators which are entirely about waiting for an external event to happen |
| Intermediate | AirFlow | You have two tasks in a DAG, the output parameter of task1 is an input parameter to task2\. Which AirFlow construct would would allow you to define this parameter passing? | XCOM is Airflow construct that allows parameter passing between tasks of a DAG. |
| Advanced | AirFlow | What is the AirFlow CLI command to list DAGs? | `airflow dags list` |
| Advanced | AirFlow | You have a group of tasks that are used multiple times in a DAG. How would you re\-use the same functionality without copying same task definitions. | TaskGroup |

