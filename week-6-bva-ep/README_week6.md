# QA Summer Roadmap – Week 6

## Introduction

Week 6 of my QA Summer Roadmap focuses on two core black‑box test design techniques: **Equivalence Class Partitioning (ECP)** and **Boundary Value Analysis (BVA)**. Whilst I had briefly covered these concepts in my studies, I wanted to review my knowledge, as well as applying my knowledge to a practical system. This week's goal was to develop a more systematic approach to selecting test inputs, especially for validation‑heavy APIs.

My aim was to review the theory behind ECP and BVA, then apply both techniques to the Open‑Meteo API (https://open-meteo.com/). By the end of the week, I had a clearer understanding of how to map input domains, identify meaningful partitions, and choose boundary values deliberately.

## What I tested

I started by reviewing the rules for three Open‑Meteo parameters: latitude, longitude, and date ranges. For each parameter, I identified the valid and invalid equivalence classes based on the documented constraints. Once the classes were defined, I selected representative values from each class and wrote tests around them.

After that, I applied BVA to test the edges of each range. For latitude and longitude, this meant checking values like `-90`, `-89.9`, `90`, `90.1`, `-180`, and `180`. For dates, the process was more involved because the API uses a sliding window of allowed dates. I wrote fixtures to calculate the current minimum and maximum allowed dates dynamically so the tests would remain valid over time.

While implementing these tests, I noticed a few behaviours that weren’t mentioned in the documentation. For example, longitude values of `180` were normalised internally to `-180`, and invalid longitude values sometimes returned `400` and sometimes `503`. I updated my tests to account for these inconsistencies.

By combining ECP and BVA, I was able to create a small set of tests that still covered the full input domain. Instead of testing dozens of random values, I focused on representative and boundary values that were more likely to reveal issues.

## What I learned

### Choosing Test Data Systematically

ECP made me think more deliberately about how inputs should be grouped. Instead of treating latitude or longitude as a continuous range, I had to identify the exact partitions the API uses and choose values that represent each one. This made my tests more structured and predictable.

### Why Boundary Values Matter

BVA highlighted how important edge cases are. Many validation issues only appear at the limits of a range, due to off-by-one errors, confusion over whether ranges should be inclusive or exclusive, floating-point precision issues, and ambiguous requirements. Testing values just inside and just outside the boundaries helped me catch behaviours that wouldn’t be visible with typical inputs.

### Real‑World Behaviour Doesn’t Always Match Documentation

Working with the Open‑Meteo API showed me that real systems often have quirks or inconsistencies. Some invalid inputs returned different error codes, and certain values were normalised internally. This reinforced the importance of testing both valid and invalid boundaries rather than assuming the system behaves exactly as described.

### Interdependent Inputs Need Combined Testing

Date ranges were a good example of this. Testing the start date and end date independently isn’t enough, because the two values need to make sense together. BVA helped me identify cases where the end date was before the start date or where one date fell outside the allowed window.

## Key takeaways from this week

This week highlighted the value of being systematic when choosing test inputs. ECP helped me reduce unnecessary tests by grouping inputs into meaningful categories, while BVA ensured that the edges of those categories were properly tested. Together, they made my test design more intentional and less reliant on guesswork.

I also learned that documentation is only a starting point. Real APIs may behave slightly differently, and boundary testing is often the quickest way to uncover those differences. Finally, I saw how important it is to consider interactions between inputs, especially when they define a range or depend on each other.

## How to Run the Tests

or full setup and installation instructions, see the main [README](../README.md).

Ensure you are running commands from the `week-6-bva-ep` folder.

Use `cd week-6-bva-ep` to navigate to the folder if necessary.

Run all tests:
```
pytest
```

Run a specific test file:
```
pytest tests/test_latitude.py