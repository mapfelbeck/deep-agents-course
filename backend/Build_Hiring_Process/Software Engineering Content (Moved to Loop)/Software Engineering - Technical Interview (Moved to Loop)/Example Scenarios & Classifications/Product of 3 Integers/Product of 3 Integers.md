# Product of 3 Integers



| **Career Skill** | Expertise |
| --- | --- |
| **Skill Classification** | Algorithm |
| **Primary Capability** | Software Engineering |
| **Scenario Description** | Evaluates a candidate's ability to work through a problem that is simple from a programatic perspective, but difficult from a logic perspective. |
| **Status** | ActiveGreen Green \- Active; Red \- Don't Use; Yellow \- Needs Review |
| **Beginner Expectation** | Will attempt to solve the project with brute force nested loops. May choose to guard against arrays of fewer than 3 integers. |
| **Foundational Expectation** | Attempts to optimize loops using absolute values (this won’t work, but shows a basic understanding of the inefficiency of using nested loops) |
| **Intermediate Expectation** | Is aware that positive and negative numbers will have an effect on whether the product is large or small. Realizes that the largest product may be negative. May attempt to handle positive and negative numbers independently. |
| **Advanced Expectation** | Will sort the array in order to group large and small numbers together in order to avoid analyzing the entire array. |
| **Expert Expectation** | Is able to see the pattern of the optimal solution and solve the problem without any loops (aside from the sorting algorithm) |

## Scenario

### Overview

Given an array of at least integers, what is the largest product that can be made from multiplying any three numbers in the array.

The numbers can be positive, negative, or zero, but they are all integers. The array must contain at least 3 integers in order to be able to multiply them.

Here is an example array, where the largest product is **120** (6 \* \-10 \* \-2\):  
\[ 3, \-10, 6, 0, \-2 ]

For convenience, here is the array sorted:  
\[\-10, \-2, 0, 3, 6 ]

### Expectations

The goal of this problem is not necessarily for the candidate to arrive at the perfect answer. The goal is to observe the candidate try multiple solutions, and continue to refine their solution. They should, at the very least, move beyond the obvious brute\-force nested loops solution.

The ultimate, simplest solution is:

1. Sort the array from smallest to largest
2. Multiply the largest 3 numbers
3. Multiply the smallest 2 numbers with the largest number
4. Return the max of those 2 results

Because of the negative numbers, the solution will always be one of those 2 results.

## Solutions

js* Add links to supporting reference materials that can be used by the interviewer to ensure they understand the scenario and the backing skill that is being measured.
