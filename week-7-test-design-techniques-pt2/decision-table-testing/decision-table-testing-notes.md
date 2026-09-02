# Decision Table Testing

## Overview

Software systems are made up of a series of decisions. The more complex the system, the more decisions it makes, and the more critical it becomes to test every possible combination of inputs that drives those decisions. So, how can we test all the possible combinations of inputs in a systematic way?

Decision table testing is a black-box software testing technique designed specifically for this purpose. It organises the various combinations of inputs into a decision table: a tabular representation of inputs versus rules, cases, or test conditions. Decision tables are a highly effective tool for both complex software testing and requirements management. A decision table helps check all possible combinations of conditions, and testers can easily identify missing conditions. Conditions are indicated using True (T) and False (F) values. It is also called a Cause-Effect table, because it records causes and effects for better test coverage.

## When to use Decision Table Testing

Decision tables are most useful when:
- A system has multiple input conditions that interact with each other.
- The result depends on a combination of conditions, not a single input on its own.
- The business rules are complex and need to be validated systematically.
- We need to reduce the number of tests without losing coverage.

Examples include:
- Login validation rules
- Loan approval logic
- Pricing and discount rules
- Form validation for product creation, checkout, or user registration

Decision table testing is less useful when:
- The system is mainly driven by free-text or exploratory behaviour.
- There are very few conditions and outcomes to check.
- The logic is simple enough to test effectively with equivalence partitioning or boundary value analysis alone.

## Key Components of a Decision Table

A decision table generally contains the following elements:
- **Conditions:** Conditions are based on business rules, for example "Credit Score Category" with the rules "High" and "Low" in a Loan Approval System.
- **Condition alternatives:** Condition alternatives are the specific values assigned to each condition within a rule, such as Yes/No, True/False, or range values.
- **Actions:** Actions are the system's expected responses when a particular combination of conditions is met. They describe what the system does, not what it evaluates, for example "Approve loan" or "Reject loan".
- **Rules:** Rules are the columns of the decision table. Each rule defines one unique combination of condition values and the corresponding action.
- **Action entries:** Action entries indicate which actions are triggered for each rule.

| Component | What it means | Example (Loan App) |
| ----------- | ----------- | ----------- |
| Condition | The input your system checks | Credit Score, Income Level, Existing Debts |
| Actions | What the system does | Approve, Reject, Flag for Review |
| Rule | One combination of conditions: one action | Good score + High income + No debt = Approve |

Each column in your decision table represents one rule, and each rule becomes one test case.

## Full Decision Table vs Collapsed Decision Table

A full decision table includes every possible combination of conditions. This is useful for understanding the complete logic, but it can become very large very quickly.

For example, if we have 3 conditions with 2 values each, we could end up with 8 possible combinations. If we add more conditions, the number rises fast. This is where decision table testing becomes especially valuable: we can identify redundant combinations and collapse the table.

A collapsed decision table groups rules that have the same outcome. We can do this by marking irrelevant conditions as "don't care".

### Don’t Care values
A "don't care" value means the condition does not affect the outcome for that rule. We usually mark it with a dash (-) or the words "don’t care".

This reduces unnecessary test cases without reducing coverage. For example:
- If the username is invalid, the password may not matter for that rule.
- If a price is empty, the date value may not affect the outcome of the validation message.

This helps simplify the decision table while still preserving the important business logic.

## Worked Example: Add Product Page (CommitQuality)

(**NOTE:** See "decision-table-for-commitquality.md" and "test_add_product.py" for my practical application of the concepts covered in these notes. My practical work will be referenced below.)

In the Add Product form on the CommitQuality demo site, the validation outcome depends on several conditions interacting together:

### Conditions
- **Name:** less than 2 characters or at least 2 characters
- **Price:** empty, too long, or valid
- **Date:** empty, future/today, over 100 years ago, or within the valid range

### Full table (all combinations)

| Rule | Name | Price | Date | Outcome |
|------|-------|--------|--------|----------|
| R1 | < 2 chars | Empty | Empty | Invalid |
| R2 | < 2 chars | Empty | Future | Invalid |
| R3 | < 2 chars | Empty | Over 100 years ago | Invalid |
| R4 | < 2 chars | Empty | Past 100 years | Invalid |
| R5 | < 2 chars | > 10 digits | Empty | Invalid |
| R6 | < 2 chars | > 10 digits | Future | Invalid |
| R7 | < 2 chars | > 10 digits | Over 100 years ago | Invalid |
| R8 | < 2 chars | > 10 digits | Past 100 years | Invalid |
| R9 | < 2 chars | Valid | Empty | Invalid |
| R10 | < 2 chars | Valid | Future | Invalid |
| R11 | < 2 chars | Valid | Over 100 years ago | Invalid |
| R12 | < 2 chars | Valid | Past 100 years | Invalid |
| R13 | ≥ 2 chars | Empty | Empty | Invalid |
| R14 | ≥ 2 chars | Empty | Future | Invalid |
| R15 | ≥ 2 chars | Empty | Over 100 years ago | Invalid |
| R16 | ≥ 2 chars | Empty | Past 100 years | Invalid |
| R17 | ≥ 2 chars | > 10 digits | Empty | Invalid |
| R18 | ≥ 2 chars | > 10 digits | Future | Invalid |
| R19 | ≥ 2 chars | > 10 digits | Over 100 years ago | Invalid |
| R20 | ≥ 2 chars | > 10 digits | Past 100 years | Invalid |
| R21 | ≥ 2 chars | Valid | Empty | Invalid |
| R22 | ≥ 2 chars | Valid | Future | Invalid |
| R23 | ≥ 2 chars | Valid | Over 100 years ago | Invalid |
| R24 | ≥ 2 chars | Valid | Past 100 years | Valid |

This shows every combination, but it is quite repetitive.

### Collapsed table

| Rule | Name | Price | Date | Outcome |
|------|-------|--------|--------|----------|
| R1 | < 2 characters | don’t care | don’t care | Invalid |
| R2 | ≥ 2 characters | Empty | don’t care | Invalid |
| R3 | ≥ 2 characters | > 10 digits | don’t care | Invalid |
| R4 | ≥ 2 characters | Valid (≤ 10 digits) | Empty | Invalid |
| R5 | ≥ 2 characters | Valid (≤ 10 digits) | Future *(includes Today)* | Invalid |
| R6 | ≥ 2 characters | Valid (≤ 10 digits) | Over 100 years ago | Invalid |
| R7 | ≥ 2 characters | Valid (≤ 10 digits) | Past 100 years | Valid |

This collapsed table shows the meaningful business behaviours while keeping coverage intact. It allows us to design fewer tests without missing the logic that matters.

## How does Decision Table Testing work?

1. **Identify the input conditions:** List all factors that affect your app's behaviour, such as user inputs, system states, or external conditions.
2. **Define possible actions or outcomes:** Determine the possible results based on different input conditions.
3. **Construct a decision table:** Write the conditions and the expected actions for each combination.
4. **Analyse and optimise test cases:** Identify redundant rules and remove duplicate combinations where the outcome is the same.
5. **Simplify if possible:** Some conditions may be irrelevant for certain rules. If the outcome is the same regardless of the condition's value, mark it with a dash or “don’t care”.
6. **Convert rules to test cases:** Each column (rule) becomes one test case. Define the specific test data, expected result, and preconditions for each. This traceability from business rule to test case is one of decision table testing's greatest advantages.

## Converting Rules into Test Cases

Once the decision table is built, each rule can be turned into a concrete test case.

For the Add Product example:
- **R1:** Name too short → validation error expected
- **R2:** Empty price → validation error expected
- **R3:** Price exceeds max length → validation error expected
- **R4:** Empty date → validation error expected
- **R5:** Future or today date → validation error expected
- **R6:** Date over 100 years ago → validation error expected
- **R7:** Valid name, valid price, valid date → submission accepted

This makes the link between the business rule and the automated tests clear and easy to maintain.

## Common Mistakes to Avoid

- Including too many conditions at once, which makes the table difficult to read and maintain.
- Not grouping logically equivalent rules together.
- Writing duplicate rules that test the same scenario twice.
- Forgetting to define the expected action clearly.
- Ignoring important boundary conditions, such as today, exactly 100 years ago, or just over the maximum allowed value.
- Treating every combination as unique when some are logically impossible or irrelevant.

## Strengths and Limitations of Decision Table Testing

### Strengths
- Helps test combinations of conditions systematically
- Good for business-rule validation and form logic
- Makes missing conditions easy to spot
- Easy to trace from requirement to test case
- Reduces redundant test cases without losing valuable coverage

### Limitations
- Can become large if too many conditions are included
- Requires careful definition of conditions and expected results
- Not always the most natural choice for exploratory or highly dynamic systems
- Can be harder to maintain if requirements change often

## Summary

Decision table testing is a powerful way to test logic-heavy systems where outcomes depend on combinations of inputs. It helps testers move from vague requirements to structured, traceable test cases. By using full tables, identifying redundant rules, and collapsing them into meaningful scenarios, we can achieve better coverage with fewer, clearer tests.

For real-world work, such as the Add Product validation example, decision tables are especially useful because they connect business rules directly to test cases and allow us to test edge conditions like boundary dates and invalid field combinations systematically.