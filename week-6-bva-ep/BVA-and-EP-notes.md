# Equivalence Class Partitioning (ECP) and Boundary Value Analysis (BVA)

# Overview

Equivalence Class Partitioning (ECP) and Boundary Value Analysis (BVA) are black-box test design techniques, meaning that they are based only on software requirements and external user behaviour, without looking at the internal code. Testers put in data and check if the output matches what the system promised to do.

ECP and BVA are used to reduce redundant tests while still achieving strong coverage. They are especially useful for numeric ranges, input validation, and APIs with strict parameter rules.

## Equivalence Class Partitioning (ECP)

Equivalence Partitioning (also called Equivalence Class Partitioning or ECP) is a black-box technique that divides input data into groups of values that the system treats the same. 

Each group is called an equivalence class.

The tester picks one representative per class, assuming the software behaves the same for every member.

### Goals of ECP:

- Remove redundant tests
- Cover all meaningful input categories
- Ensure every logic path is tested at least once

### Properties of a good equivalence class:

- **Complete:** covers all possible inputs
- **Non-Overlapping:** no value belongs to two classes
- **Representative:** all values in the class follow the same logic path
- **Behaviourally consistent:** all values produce the same output or error

### How to prove two values belong in the same class

You check whether the system applies the same validation rules, transformations, or business logic to both.
If two values trigger different branches, errors, or outputs, they are not equivalent and must be split into separate classes.

### Types of equivalence classes

- Valid functional classes
- Invalid functional classes
- Format classes (e.g. email with/without '@')
- Structural classes (e.g. empty vs non-empty)
- Special-case classes (null, zero, max length)
- Error-handling classes (missing fields, wrong types)

### Why one representative per class is usually enough

All values in the class follow the same logic path, so testing one value exercises the entire behaviour.
If two values behave differently, the class was grouped incorrectly and must be split.

### When ECP is not enough 

ECP fails when:
- inputs interact (e.g., start date + end date)
- logic is multi-step
- rules depend on combinations of inputs

Example:
A discount applies only if VIP AND total > £100 AND coupon valid.
ECP alone cannot capture this - you need decision tables.

## Boundary Value Analysis (BVA)

Boundary Value Analysis (BVA), also called range checking, validates the extreme ends of each equivalence class. Because defects cluster at range limits, BVA targets five key points:
1. minimum 
2. just above the minimum 
3. a nominal value
4. just below the maximum 
5. maximum 

## How ECP and BVA complement each other

BVA complements Equivalence Partitioning: once classes are defined, their boundary values surface off-by-one and edge bugs. 

Why use equivalence partitioning and BVA?
1. Compress large test case volumes into manageable chunks.
2. Provide clear rules for choosing test data, without sacrificing effectiveness.
3. Suit calculation-intensive apps with many numeric variables.

Best Practices for Equivalence Partitioning and BVA

Follow these practices to keep coverage strong while controlling test counts:

- Map every domain: List valid, invalid, and special-case partitions first.
- Test both sides of each limit: Include values just inside and outside to catch off-by-one errors.
- Combine techniques: Pair with decision tables or state-transition testing for complex logic.
- Automate edge cases: Parameterize boundary values so regression suites run consistently.
