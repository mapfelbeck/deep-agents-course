# Peak Finder



| **Career Skill** | Expertise |
| --- | --- |
| **Skill Classification** | Algorithm |
| **Primary Capability** | Software Engineering |
| **Scenario Description** | Evaluates a candidates ability to work with data in collections |
| **Status** | ActiveGreen Green \- Active; Red \- Don't Use; Yellow \- Needs Review |
| **Beginner Expectation** | Might have difficulty differentiating the graphical representation from the data representation |
| **Foundational Expectation** | Can create a simple looping algorithm that shows the function |
| **Intermediate Expectation** | Elaboration: Update function to return positions of peaks instead of the count. |
| **Advanced Expectation** | Elaboration count plateaus instead of peaks?* May require a state machine to detect plateaus. |
| **Expert Expectation** | Can tackle all other elaborations; Offers insights into how to test and exercise the algorithm. |

## Scenario

### Overview

We have a collection of data that is gathered by a sensor and rendered as in the following graph:

### Expectations

Create a function that will find the peaks of data between a collection of points.

## Solutions

jssurveyData \= \[0,4,2,9,2,3,5,0]
// peaks: ^ ^ ^

function countPeaks(surveyData) {
 var peaksFound \= 0;
 for (var i \= 1; i \< surveyData.length\-1; i\+\+) {
 if (surveyData\[i] \> surveyData\[i\-1] \&\& surveyData\[i] \> surveyData\[i\+1]) {
 peaksFound\+\+;
 }
 }
 return peaksFound;
}* Consider boundary case if using a for\-loop.


	+ If a "peak" contains two points of the same height it will not be detected with the naive approach above.

### Java Solution

## Reference

* Add links to supporting reference materials that can be used by the interviewer to ensure they understand the scenario and the backing skill that is being measured.
