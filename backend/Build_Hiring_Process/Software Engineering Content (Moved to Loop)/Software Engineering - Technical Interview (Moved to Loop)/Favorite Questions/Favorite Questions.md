# Favorite Questions

A list of questions that have been used in the past, or are currently in use, that you can use or draw inspiration from. 

# Programming Questions

## One\-To\-Ten

**Do Not Use \- this has been posted to glass door.**

Question:

1. Write a function that returns the numbers 1\-10 in a collection.
2. Refactor the function to take parameters a, b and return all of the numbers between them, inclusive.
3. List all the test cases you can think of for this function
4. Refactor the function to take a function/predicate that filters in the numbers that are returned. For example, numbers(1, 10, n \=\> n % 2 \=\= 0\) should return the collection 2, 4, 6, 8, 10

c\#var n \= numbers(1, 10, p \=\> p % 2 \=\= 0\); 
// n \~\= { 2, 4, 6, 8, 10 }

public IEnumerable\<int\> numbers(int a, int b, Func\<int, bool\> p) {
 for (int i \= Math.Min(a, b), i \<\= Math.Max(a, b); i\+\+) {
 if (p(i))
 yield return i;
 }
}## Peak Finder

jssurveyData \= \[0,4,2,9,2,3,5,0]
// peaks: ^ ^ ^

function countPeaks(surveyData) {
 var peaksFound \= 0;
 for (var i \= 1; i \< surveyData.length\-2; i\+\+) {
 if (surveyData\[i] \> surveyData\[i\-1] \&\& surveyData\[i] \> surveyData\[i\+1]) {
 peaksFound\+\+;
 }
 }
 return peaksFound;
}* Consider boundary case if using a for\-loop.


	+ If a "peak" contains two points of the same height it will not be detected with the naive approach above.
* Elaboration: Update function to return positions of peaks instead of the count.
* Elaboration count plateaus instead of peaks?


	+ May require a state machine to detect plateaus.
* Sample java solution:

## Meeting Booking

Write a function which takes a calendar and a meeting, and if the new meeting does not conflict with the calendar, add the new meeting to the calendar.

scalaimport com.github.nscala\_time.time.Imports.\_

case class Meeting(startTime: DateTime, duration: Duration) {
 lazy val endTime \= startTime \+ duration
}
//The calendar starts sorted (code to enforce this doesn't need to be part of the solution it can be assumed)

type Calendar \= List\[Meeting]

def scheduleMeeting(calendar: Calendar, newMeeting: Meeting): Option\[Calendar] \=
 calendar match {
 case Nil \=\> Some(List(newMeeting))
 case m :: ms \=\> {
 if (m.endTime \<\= newMeeting.startTime) scheduleMeeting(ms, newMeeting).map(m :: \_)
 else if (newMeeting.endTime \<\= m.startTime) Some(newMeeting :: m :: calendar)
 else None
 }
 }* Encourage the candidate to use Doubles or Ints if they get stuck on DateTime math
* The common edge case is a meeting inside of another meeting

Variation:

* Given a calendar which is represented as List\[Boolean] 24 long; answer the question.  This variation removes the modeling complexity, and greatly simplifies the logic.

## Find Sum

Write a function which takes a list of integers, finds two numbers in that list that sum up to 2022, and returns their product. 

typescriptsumfinder1function solveProblem(numbers: number\[]): number {
 const targetSum \= 2022;
 numbers.find((someNumber, index) \=\> {
 const restOfNumbers \= 
 });
}# Data Modeling Questions

## IMDB (Now with optional GenAI!)

Question: Design a database that stores information about

* tv shows
* their episodes
* the directors that direct them
* the actors that play them

Targeting something that looks like this:

**(GenAI)** Elaboration: how would you adjust this to allow semantic search?  
**(GenAI)** Elaboration: How would architect a solution to allow an interactive bot to help build a playlist?

Question: Write a query to get the names of every person that acted and directed in the same episode.

## Parking Garage

Question: Design a database that stores information about a parking garage

An ideal solution would have:

* Garage
* Level/floor
* Space
* Vehicle

Check the candidate knows the relationship between garage, level, space. As a way to test a many to many relationship, suggest a large vehicle (big truck) can take up multiple spaces and a space can fit multiple motorcycles in it.

## Chatbot

Question: Write a prompt for a chatbot that helps a user shop for cruise line vacations and presents items that can be added to a shopping cart.

Their prompt should include:

* Role setting
* Guard rails
* One\-shot
* Prompt modifiers

As well as direct guidance, initial salutation instructions, and steps for the AI to follow.

*If you have any feedback or questions related to the content on this page, send us an email at* [*build\-interviewing\-feedback@twodegrees1\.onmicrosoft.com*](mailto:build-interviewing-feedback@twodegrees1.onmicrosoft.com)*.*

trueupdatesAdd a table with key/value pairs in order to display its data on another page using the Page Properties Report macro.



| **2024 GenAI Update** | 1 1 complete Update Favorite Questions to include GenAI topics |
| --- | --- |

