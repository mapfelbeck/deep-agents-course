# Constructing And Selecting Technical Interview Questions

**DRAFT** This is draft content that is currently under construction.

We are best when we draw from the experiences of our interviewers to create a pool of questions that are consistently structured. This page outlines considerations for contributing a Technical Interview question or scenario.

# Technical Interview Question Libraries

We manage a set of technical interview scenarios and problems on Miro. These should be ready to use and adhere to the considerations laid out on this page.

* [https://miro.com/app/board/o9J\_lDwySeY\=/](https://miro.com/app/board/o9J_lDwySeY=/)
* [https://miro.com/app/board/o9J\_lDytZbg\=/](https://miro.com/app/board/o9J_lDytZbg=/)

## Miro Problem Conventions

When you add a technical interview question to either of the above boards, you can streamline the process by following these conventions

* Use a frame to hold the entire question and any interviewer notes
* Use a child frame to hold the candidate view of the question


	+ Interviewers can select the Candidate View frame and copy/paste that into the Miro board that is used for the candidate interview
* Add notes via stickies of specific attributes that the candidate should be able to express: what are you looking for?

# Technical Interview Question Structure

The most important consideration for a technical interview question is that it is set up in a way that the candidate can be successful in solving the problem. We are looking to assess their skills in a relatively realistic scenario, we are not looking to trick the candidate. We should be wary of questions that are overly abstract or those that use esoteric comp sci language. Asking someone to ‘traverse a binary tree’ is less desirable than asking someone to ‘find an employee in an organization where every manager has at most two direct reports’

In order to ensure other interviewers can use a shared interview problem, a technical interview question should be set up in a manner that is easy for another interviewer to pick up and use. The following structure will support a meaningful exercise with the candidate.

## Setup

Set the stage: This helps the candidate orient and frame their solution in a way that they will be most successful.

* What are we going to ask them to do? What are we looking for? 


	+ “We’d like you to write some code in \[language]… We are looking for how you work, so think about the whole process of writing code to solve a user story.” \[this includes clean code, tests, etc]
* Frame the question context


	+ “Imagine our client is building an eCommerce site, and they have a really large customer base. They are preparing a marketing campaign targeting customers by age.”

## Core Problem

The core problem and directions for what you are looking for. 

* Ask the core question:


	+ “We need a **function** that will take a collection of customers as **input** and will **return** the collection sorted by customer age”

## Problem Complications

More experienced candidates may address these types of additional considerations on their own. Lay out different complications to the core problem.

* Exception Handling


	+ “What happens if one of the customer records is null?”
	+ “What happens if the collection is empty?”
* Add additional business rules


	+ “Modify the function to remove any customers who are not at least 18 years old.”

## Completeness of solution

Include in the problem specification notes for an interviewer to consider as they are working with the candidate. 

* What are your expectations of testing?
* What types of approaches that you are looking for?

## Progressive Enhancement

A great question or scenario is one that follows the principles of [progressive enhancement](https://en.wikipedia.org/wiki/Progressive_enhancement). We work in an iterative delivery environment \- creating a question that can be answered simply, but then iterated on and improved will help us understand the candidate’s ability to think and work iteratively. There are a number of ways we could accomplish this:

* Start with a base problem
* Add additional considerations that push out toward the edge
