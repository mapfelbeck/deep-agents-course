# Sample Technical Interview Summary Email 1 [KEEP]

I recommend we **PROCEED** with the candidate as an engineer for the **\<build\-center\-name\> \<capability name\>** team.

The candidate was strong in coding, and had excellent ideas when problem solving, however, their modelling and database answers were just ok. Overall, I believe we should PROCEED with them at the engineer level, giving them the time to learn and grow their modeling and database experience.

# Overall:

* **Technical Proficiency**: Excellent
* **Consulting Presence**: Good
* **Persistence and Curiosity:** Good

# Details:

* **Communication (Good)**


	+ Clear and concise
	+ Not too expressive or enthusiastic, but seemed to loosen up near the end of the convo and asked a lot of questions about our working style and teaming and opportunity to work on different stacks
* **Code Writing (Good/Excellent)**


	+ Was able to write the code for the SuperEven coding exercise fairly easily
	
	
		- Wanted to use Python, but we agreed on using JavaScript instead
	+ Added a few modifications when asked
	
	
		- Typed the parameters
		
		
			* (and suggested checking the types and throwing an error as needed)
		- Added validations for the parameters so that startNum \> endNum
		- Changed from printing\-to\-console to adding a return type instead
* **Unit Testing (Good/Excellent)**


	+ Good test cases
	
	
		- Had to prompt them for performance based test cases (like max/min numbers)
	+ Was able to refactor the code for testability
	
	
		- Moved the if\-else logic out on its own so it's more testable
* **Problem Solving (Excellent)**


	+ CPU constraints
	
	
		- Came up with caching as a solution very quickly
		- Suggested slicing the array based on start/end params, instead of retrieving each value
	+ Memory constraints
	
	
		- Suggested using a hash table, then quickly realized an array is all that's needed
		- Suggestion 1
		
		
			* Store 10 numbers only in cache
			* Mod the starting number by 10, and use that to know where to start counting down from in the cache and then calculate how many iterations on the array you'll need to reach the end, and keep hitting the cache for each iteration
		- Suggestion 2
		
		
			* Start with
			
			
				+ Calculate how many "blocks" of 10 there are in the range specified
				+ Calculate how many number above the first 10 block there are
				+ Calculate how many numbers below the last 10 block there are
			* Hit the cache once to retrieve the whole 10\-number array
			* Print out the mod of the few numbers above the 10\-block
			* Print out as many 10\-blocks are needed for the range, no need to hit the cache again
			* Print out the mod of the last few numbers below the 10\-block
* **Object Modelling (Fair)**


	+ Mentioned a lot of things quickly and I had to ask them to scale back the scope of the requirements and start simpler
	
	
		- e.g. mentioned payment systems, and gates, and tickets, and cars…etc.
	+ Once we simplified it, they came up with Lot and Spot as the main entities, but went too simplistic and started leaning towards putting everything in  a single object for Lot
	+ Essentially, they’re able to do some stuff here, but it doesn't seem that they have much experience in this area
* **Data Modelling / SQL (Fair)**


	+ Was able to come up with the correct 2 tables, and the PK and FK correctly
	+ Used a right\-join, so I questioned them a bit about the different types of joins, which took some time to think of, but in the end they got it, and switched back to an inner join
	+ They had the right ideas and concepts, but the syntax wasn't perfect
* **Front end / Backend (Not Covered)**


	+ N/A
* **GenAI (Not Covered)**


	+ N/A
* **Questions for me:**


	+ a couple of questions about projects and how teams collaborate each week

trueupdatesAdd a table with key/value pairs in order to display its data on another page using the Page Properties Report macro.



| **2024 GenAI Update** | 1 1 complete Update Sample Skills\-Screen Summary Email 1 to reflect SE Technical Interview script to (including GenAI topics) |
| --- | --- |
| **2024 SE Capability Update** | 2 2 complete Update Summary Email to reflect SE Technical Interview script   3 3 complete Update Summary Email to reflect SE Purpose, Core Values, How\- and What we Do. |

