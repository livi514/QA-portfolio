# Decision Table Testing

## Overview

Software systems are made up of a series of decisions. The more complex the system, the more decisions it makes, and the more critical it becomes to test every possible combination of inputs that drives those decisions. So, how can we test all the possible combinations of inputs in a systematic way?

Decision table testing is a black-box software testing technique designed specifically for this purpose. It organises the various combinations of inputs into a decision table: a tabular representation of inputs versus rules, cases, or test conditions. Decision tables are a highly effective tool for both complex software testing and requirements management. A decision table helps check all possible combinations of conditions, and testers can easily identify missing conditions. Conditions are indicated using True (T) and False (F) values. It is also called a Cause-Effect table, because it records causes and effects for better test coverage.

## Key Components of a Decision Table 

A decision table general contains the following elements:
- **Conditions:** Conditions are based on business rules, for example "Credit Score Category" with the rules "High" and "Low" in a Loan Approval System.
- **Condition alternatives:** Condition alternatives are the specific values assigned to each condition within a rule, such as Yes/No, True/False, or range values.
- **Actions:** Actions are the system's expected responses when a particular combination of conditions is met. They descibe what the system does, not what it evaluates, for example "Approve loan" or "Reject loan".
- **Rules:** Rules are the columns of the decision table. Each rule defines one unique combination of condition values and the corresponding action. 
- **Action entries:** Action entries indicate which actions are triggered for each rule.

| Component      | What it means | Example (Loan App) |
| ----------- | ----------- | ----------- |
| Condition    | The input your system checks | Credit Score, Income Level, Existing Debts |
|  Actions  | What the system does | Approve, Reject, Flag for Review |
| Rule | One combination of conditions: one action | Good score + High income + No debt = Approve |

Each column in your decision table = one Rule = one test case

## How does Decision Table Testing work?

1. **Identify the input conditions:** List all factors that affect your app's behaviour, such as user inputs, system states, or external conditions.
2. **Define possible actions or outcomes:** Determine the possible results based on different input conditions.
3. **Construct a decision table**
4. **Analyse and optimise test cases:** Now that you have all the possible scenarios your app would have to deal with, identify and eliminate the ones that are redundant. For example, if two of the test cases deliver the same outcome, remove one from the process.
5. **Simplify if possible:** Some conditions may be irrelevant for certain rules. If the outcome is the same regardless of a condition's value, mark it with a dash. This reduces redundancy without sacrificing coverage.
6. **Convert rules to test cases:** Each column (rule) becomes one test case. Define the specific test data, expected results, and preconditions for each. This traceability from business rule to test case is one of decision table testing’s greatest advantages.