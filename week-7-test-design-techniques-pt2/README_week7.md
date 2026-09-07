# QA Summer Roadmap – Week 7

## Introduction:

In Week 7 of my QA Summer Roadmap, I explored three test design techniques: decision table testing, state transition testing, and exploratory testing heuristics. My aim was to develop a more systematic approach to designing test cases, as well as to try something new to me: exploratory testing. I applied decision table testing to CommitQuality, state transition testing to ParaBank, and exploratory testing heuristics to SauceDemo.

By the end of the week, I had a clearer understanding of the thinking behind designing effective test cases, and how these techniques can help both to reduce redundancy and to improve test coverage.

## What I did:

### Decision Table Testing:

I started with decision table testing. Software systems are made up of a series of decisions. Decision table testing answers the question: “How can we test all the possible combinations of inputs in a systematic way?” I applied this concept to the “Add Product” page on the CommitQuality demo site, starting by extracting all possible input conditions for the input fields “Name”, “Price”, and “Date Stocked”, and determining the valid and invalid values for each. I then created a full decision table for each combination. This table ended up having 24 rows, but I was able to collapse it into 7 meaningful rules. Finally, I converted each rule into an automated test.

Along the way, I discovered an oversight in my own test suite: my `years_ago()` (used to test the "Date Stocked" field) simply changed the year of the current date to be 100 years ago, without checking the boundary values (i.e. tomorrow's date, 100 years ago, and yesterday's date, 100 years ago). After adding these test cases, I was able to confirm that the system works as expected for these boundary values.

My key takeaway from this exercise is how much more organised using a decision table felt compared to just trying to come up with all possible scenarios while you’re writing the automated tests. Planning scenarios systematically up front mitigates both the risk of redundant tests, and the risk of missing crucial ones.

### State Transition Testing:

Next, I moved onto state transition testing, which checks how a system moves between the states it can occupy. I started by creating a state transition diagram showing the states for ParaBank’s loan application system, and the transitions between them. Next, I converted this into a state transition table, and, finally, converted both into automated tests.

A key insight from this exercise was figuring out when to build a diagram, and when to build a table. The best approach is usually to build both, as they serve different purposes. Diagrams provide a quick visual picture of the lifecycle, and can be used to communicate the flow to non-technical teams. On the other hand, tables can be helpful for checking all valid and invalid state-event combinations, and ensuring you have exhaustive transition coverage.

Another key takeaway from this exercise was that state transition testing is not just about happy paths. It is about proving that the system behaves correctly as it moves through every meaningful state, while also identifying transitions that should not exist, should be blocked, or currently fail unexpectedly.

### Exploratory Testing Heuristics:

Finally, I moved onto exploratory testing, a hands-on testing approach that combines test design and execution simultaneously. I tried out several heuristics, including CRUD, Interrupt / Starve, SFDPOT, and Zero / One / Many.

Exploratory testing was very different to what I had done before, which was either automation or following detailed manual test plans. However, it taught me that not all bugs can be found through these strategies: some only show up when you look past what’s documented or expected of the system. 

Using DevTools inspection on SauceDemo, I confirmed a CSS overflow bug with error messages that are 3 or more lines long. I traced the cause to a fixed `height: 45px` on the container, which clips longer content instead of expanding to fit it. Changing this to `min-height: 45px` (or removing the fixed height entirely and letting the flex container size its content) lets the box grow for longer messages while still keeping the original height as a minimum for short ones. I confirmed that this fix worked directly in DevTools before including my proposed suggestion in the bug report.

Using the Zero/One/Many heuristic, I also confirmed something I'd first noticed during my UI tests in Weeks 1-3: SauceDemo allows checkout with a $0.00 empty cart, reproducible across 3 of 5 test accounts. Digging further, I found that SauceDemo's checkout is entirely client-side, with cart state held in a `localStorage` array. Because the checkout flow makes no network requests, there is no server-side validation involved in this demo flow; the client-side checkout contains no guard against an empty cart.

### CI/pipeline debugging

Aside from exploring test design techniques this week, I also had to fix an issue with my UI tests pipeline. I discovered a silently hanging Windows CI job and added timeouts and reruns to surface the real error. Rather than being caused by an error in my own code, this issue was due to a Firefox-on-Windows resource-contention crash that only surfaced once the timeout was in place to reveal it.

## Key takeaways from this week:

This week taught me that testing can’t be limited to one technique, and that looking at a system through a new angle can help you discover unexpected bugs. It also reinforced that even automated tests rely on good design. Automation without good design is just running bad tests faster.