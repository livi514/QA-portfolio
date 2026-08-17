# Equivalence Class Partitioning (ECP) and Boundary Value Analysis (BVA)

# Overview

Test cases require input values in order to check the behaviour of the software being tested. However, the range of possible test data values can be extremely large, and writing test cases for every potential value can be both impractical and error-prone. Testers therefore need systematic techniques for selecting effective test inputs without introducing unnecessary redundancy.

Two widely-used techniques for choosing effective test data values are Equivalence Class Partitioning (ECP) and Boundary Value Analysis (BVA). ECP selects representative values from groups of inputs that the system treats equivalently, while BVA focuses on the boundary values at the edges of these groups. Both are black-box test design techniques, meaning that they are based only on software requirements and external user behaviour, rather than internal code structure. Testers supply inputs and verify whether the outputs match the expected behaviour defined by the specification.

ECP and BVA are used to reduce redundant tests while maintaining strong coverage. They are especially effective for numeric ranges, input validation, and APIs with strict parameter rules.

## Equivalence Class Partitioning (ECP)

Equivalence Class Partitioning divides input data into groups of values (known as equivalence classes) that the system processes in the same way. If two values follow the same logical path through the code and trigger the same validation rules, transformations, or outputs, they are considered equivalent.  The tester selects one representative value from each class. If the system behaves correctly for that representative, the entire class is assumed to behave correctly under the same conditions.

### Example

If an application allows the user to enter a password of length 8-12 characters inclusive, the input domain can be divided into 3 separate equivalence classes:
- Invalid equivalence class: <8 characters
- Valid equivalence class: 8-12 characters
- Invalid equivalence class: >12 characters

### Goals of ECP

The purpose of ECP is to remove redundant tests, ensure coverage of all meaningful input categories, and guarantee that every distinct logic path is exercised at least once.

### Properties of a good equivalence class

A well-defined equivalence class is:
- **Complete:** it covers all meaningful categories of input defined by the requirements
- **Non-Overlapping:** no value belongs to more than one class
- **Representative:** all values in the class follow the same logic path
- **Behaviourally consistent:** all values in the class produce the same output or error

### Determining whether two values belong in the same class

To confirm that two values belong in the same equivalence class, the tester checks whether the system applies identical validation rules, transformations, or business logic to both. If the values trigger different branches or produce different outputs, they are not equivalent and must be separated into distinct classes.

### Types of equivalence classes

Equivalence classes may be:
- Valid functional classes
- Invalid functional classes
- Format classes (e.g. email with/without '@')
- Structural classes (e.g. empty vs non-empty)
- Special-case classes (null, zero, max length)
- Error-handling classes (missing fields, wrong types)

### Why one representative per class is usually enough

All values in the class follow the same logic path, so testing one value exercises the entire behaviour. If two values behave differently, the class was grouped incorrectly and must be refined.

### When ECP is not enough 

ECP is insufficient when inputs interact, when logic is multi‑step, or when rules depend on combinations of conditions. For example, a discount rule requiring a customer to be VIP and have a cart total above £100 and supply a valid coupon cannot be captured by ECP alone; decision tables or state‑transition testing are required.

## Boundary Value Analysis (BVA)

Boundary Value Analysis (BVA) focuses on testing the boundary values (edges) of valid and invalid input ranges, where defects are most likely to occur. Errors frequently arise at boundaries due to off‑by‑one mistakes, confusion between inclusive and exclusive limits, floating‑point precision issues, and ambiguous natural‑language requirements.

BVA typically tests:
- The minimum boundary value
- The value just above the minimum
- A nominal value
- The value just below the maximum
- The maximum boundary value
- Invalid values just outside the valid range

### Example 

If a form accepts ages from 20 to 50 inclusive, BVA would test:
- Just below the minimum: 19
- Minimum: 20
- Just above the minimum: 21
- A nominal value: 35
- Just below the maximum: 49
- Maximum: 50
- Just above the maximum: 51

## How ECP and BVA complement each other

ECP identifies meaningful input categories, while BVA ensures that the boundaries of those categories are thoroughly tested. Using both techniques together allows testers to compress large input domains into manageable sets of test cases while still detecting off‑by‑one errors and edge‑case defects.

This combined approach is particularly effective for calculation‑heavy systems, numeric ranges, and validation logic.

## Best Practices for ECP and BVA

To apply ECP and BVA effectively:
- map the input domain by identifying valid, invalid, and special‑case partitions
- test both sides of each boundary to detect off‑by‑one errors
- combine ECP/BVA with decision tables or state‑transition testing when logic is complex
- automate boundary tests by parameterising values so they run consistently in regression suites
