# Exploratory Testing Heuristics

## What is Exploratory Testing?

Exploratory testing is a hands-on testing approach that combines test design and execution simultaneously. Rather than following predefined test scripts, testers actively explore the software, learning its behavior and identifying defects through investigation and experimentation. It complements automated testing by catching issues that scripted tests miss.

## Why Use Exploratory Testing?

**Key benefits:**
- Finds defects that scripted tests cannot catch (assumptions, undocumented behaviors, edge cases)
- Requires minimal upfront planning — scope is clear, but test cases emerge during execution
- Builds a deeper understanding of the application through hands-on exploration
- Effective at all development stages, especially early iterations when features are still unstable

**When to apply:**
- Early development phases (rapid feedback on new features)
- Regression testing (exploring existing features for unintended changes)
- Risk-based testing (targeting high-impact areas)
- Post-deployment validation (real-world usage scenarios)

## What Are Heuristics in Exploratory Testing?

Heuristics are mental shortcuts or "rules of thumb" that guide the testing process. They provide a framework for discovering and testing new areas of the application systematically, helping testers know where to look and what to test without prescribing exact steps.

## Exploratory Testing Heuristics

### CRUD (Create, Read, Update, Delete)

Tests the four fundamental data operations on entities, verifying consistency across all surfaces that display that data.

- **Create:** Add a new item/record and verify it appears everywhere it should (inventory grid, detail page, cart, summary)
- **Read:** Retrieve and display the same item on multiple surfaces and verify data matches across all of them
- **Update:** Modify an existing item/record and verify changes are reflected consistently everywhere
- **Delete:** Remove an item and verify it disappears from all surfaces and totals recalculate

**Use case:** Find data inconsistency bugs, cascade failures, and missing refresh logic.

**Practical example: SauceDemo cart operations**
- **Create (Add to cart):** Add Sauce Labs Backpack from inventory grid. Verify: cart badge shows "1", button changes to "Remove", item appears on cart page with correct name/price/description.
- **Read (Cart visibility):** Same item displays consistently on inventory grid, product detail page, cart page, and checkout summary. Prices and descriptions match across all surfaces.
- **Update (Not supported):** SauceDemo cart doesn't support quantity editing or product modification. No quantity selector exists in UI.
- **Delete (Remove from cart):** Remove Sauce Labs Backpack from cart page. Verify: item disappears immediately, cart badge updates from "1" to hidden, button on inventory page changes back to "Add to cart", checkout totals recalculate.
- **Additional finding (bug discovered):** checkout can be completed with an empty cart, reaching a $0.00 order with no validation or warning at any step.

---

### SFDPOT (Structure, Function, Data, Platform, Operations, Time)

A systematic heuristic for exploring all dimensions of an application.

- **Structure:** How is the data organized? What are the data relationships?
- **Function:** What can the user do? What behaviors does the app perform?
- **Data:** What data types are accepted? How are edge cases handled (empty, null, huge, negative)?
- **Platform:** How does it work on different browsers, devices, OS versions?
- **Operations:** What happens during normal operation? During server issues? Network latency?
- **Time:** How does it behave over time? With old data? New data? After long periods of inactivity?

**Use case:** Get a comprehensive overview of the application's behaviour space.

**Practical example: SauceDemo login page**
- **Structure:** Input fields grouped in a white container with high contrast; no dividers between elements
- **Function:** Valid logins with `standard_user` + `secret_sauce` work; invalid credentials show generic "do not match" error (security practice); `locked_out_user` shows specific "locked out" message
- **Data:** Whitespace is not trimmed; `' OR 1=1--` is rejected like any other invalid input; long strings (1000+ chars) scroll horizontally without breaking layout; special characters accepted at input level
- **Platform:** Consistent across Firefox, Chrome, Edge, Opera on Windows and Chrome on Android; mobile layout adapts cleanly to single column
- **Operations:** Typing, pasting, and autofill all work; Enter key submits from either field; no field-level validation (errors only on submit); leading/trailing whitespace causes rejection
- **Time:** Typing speed has no effect; arbitrary delays between credential entry and login work fine; `performance_glitch_user` experiences intentional login delay, which is expected behavior

---

### HICCUPS (History, Image, Claims, Comparable Products, User Expectations, Product, Statutes)

Focuses on spotting inconsistencies and misalignments with expectations.

- **History:** Does behavior differ from previous versions? Are there regressions?
- **Image:** Does the product match its brand and reputation promises?
- **Claims:** Do features work as documented? Does marketing match reality?
- **Comparable Products:** How does it compare to competitor products? Missing features? Unexpected behavior?
- **User Expectations:** What do users expect based on similar apps? Where are the surprises?
- **Product:** Does the actual product meet the stated requirements?
- **Statutes:** Does it comply with relevant laws, standards, and regulations?

**Use case:** Validate that the product meets user and business expectations.

**Practical example: SauceDemo login behavior**
- **Claims:** "Locked out accounts cannot log in" [✓] Confirmed—`locked_out_user` with correct password shows "Sorry, this user has been locked out."
- **User Expectations:** Empty fields should show "required" errors [✓] Matches expectation. Blank username: "Username is required"; blank password: "Password is required"
- **Comparable Products:** Most e-commerce login flows validate fields before submission. [✗] SauceDemo validates only on submit, not during typing.
- **Product:** Should reject invalid credentials consistently. [✓] All invalid combos show same generic "Username and password do not match" error (security practice—doesn't leak whether username exists).

---

### Goldilocks (Boundary Testing with Relativity)

Tests inputs at "too small," "too big," and "just right" boundaries to find edge-case bugs.

- **Too small:** Minimum valid input, empty string, single character, 0, negative numbers
- **Just right:** Normal, expected input that should work
- **Too big:** Maximum field lengths, huge numbers, very long strings, maximum allowed quantity

**Example:** Test a price field with $0.01, $9,999.99, and $1,000,000,000.

**Use case:** Find validation and field-length bugs, overflow errors, and formatting failures.

**Practical example: SauceDemo login fields**
- **Too small (empty):** Blank username shows "Username is required." Blank password shows "Password is required." [✓]
- **Just right:** `standard_user` + `secret_sauce` logs in successfully. [✓]
- **Too big (1000+ characters):** Very long strings in username/password fields are accepted. No truncation occurs. Field allows horizontal scrolling. No layout breakage. [✓] (Validation happens on backend, not at input level)

---

### Zero, One, Many

Tests boundary limits by operating with zero, one, or many items in a collection or workflow.

- **Zero:** Empty cart, no filters, no search results, no user accounts
- **One:** Single item in cart, one filter applied, one file uploaded
- **Many:** Maximum or near-maximum items (100+ products, 50 items in cart, 1000 results)

**Example:** Add 0, 1, 5, 50, and 500 items to a shopping cart and verify checkout works at each level.

**Use case:** Find scaling bugs, loop errors, off-by-one bugs, and performance degradation.

**Practical example: SauceDemo checkout**
- **Zero items:** [✗] User can proceed through entire checkout flow with empty cart, reaching a $0.00 order confirmation. **Bug found:** no validation at any step prevents this. System should either disable checkout when cart is empty, show a warning, or block at final step.
- **One item:** [✓] Normal flow with Sauce Labs Backpack ($29.99 + $2.40 tax = $32.39). No issues.
- **Many items:** [✓] All 6 items checkout successfully ($129.94 + $10.40 tax = $140.34). Cart state is correctly reflected across inventory page, cart page, and checkout summary. Note: SauceDemo does not support adding multiple quantities of the same item—each product can only exist once in the cart.

---

### Never and Always

Targets behaviors the software claims it will never or always do, then violates those claims.

- **Never:** "Users can never delete an admin account" → Try deleting one
- **Always:** "Confirmation emails are always sent within 2 minutes" → Check timing and edge cases
- **Always:** "The system always validates email format" → Test invalid formats

**Use case:** Uncover broken guarantees and defensive programming gaps.

**Practical example: SauceDemo checkout**
- **Claim (implicit):** "Checkout should always require at least one item" [✗] Bug found: Checkout succeeds with zero items, creating a $0.00 order
- **Claim (implicit):** "Cart state is always preserved during checkout" [✓] Confirmed — cart items persist even if user navigates away or reloads pages
- **Claim (implicit):** "Checkout details should always be cleared if the user navigates back" [✓] Confirmed—first/last name and zip are cleared when user presses Back, forcing re-entry (acceptable UX tradeoff)

---

### Beginning, Middle, End

Varies the sequence, timing, or position of operations in a workflow to find state-management bugs.

- **Beginning:** Perform actions at the start of a workflow (before prerequisites are satisfied)
- **Middle:** Perform actions during normal workflow progression
- **End:** Perform actions at the end (after workflow should be complete)

**Example:** Try logging out at the beginning of a checkout, in the middle (after adding items), and after completing an order.

**Use case:** Find state-machine violations, race conditions, and workflow sequencing bugs.

**Practical example: SauceDemo checkout interruptions**
- **Beginning (Before Continue):** [✓] User enters checkout details, then navigates away before clicking "Continue". Cart is preserved when they return. Checkout details are cleared. Recovery: smooth, user just re-enters info.
- **Middle (At Overview):** [✓] User reloads the checkout overview page while reviewing items. Cart items, quantities, prices, and totals are all preserved. No errors.
- **End (After pressing Finish):** [✓] User completes checkout and sees "Thank you for your order!" Attempting to re-submit by double-clicking Finish rapidly doesn't create duplicate orders. System handles rapid input gracefully. 

---

### Interrupt / Starve (Resilience Testing)

Forces the system to handle resource shortages and sudden operational breaks.

- **Interrupt:** Kill network connection mid-upload, close browser tab, cancel a request
- **Starve:** Slowly reduce resources (bandwidth, memory, CPU) to trigger failures
- **Restart:** Restart operations after interruption and verify recovery

**Example:** Submit a form, interrupt network halfway through, then reconnect to see how it handles the partial submission.

**Use case:** Uncover crash bugs, data corruption, improper error handling, and lack of retry logic.

**Practical example: SauceDemo checkout**
- **Reload during checkout:** [✓] User reloads the checkout overview page mid-flow. Cart items preserved, totals preserved, no error shown. User can continue without restarting.
- **Browser Back button during checkout:** [✓] User enters customer info, then presses Back. Cart items preserved, but checkout fields are cleared (minor friction, but acceptable). User can restart checkout without losing cart.
- **Navigate away before submission:** [✓] User exits checkout before pressing "Continue." Cart items preserved when they return to cart. Checkout fields are cleared on re-entry.
- **Open in another tab:** [✓] User starts checkout in Tab A, opens the site in Tab B. Returning to Tab A, both cart and checkout info are preserved and user can continue. (Browser session data is shared across tabs)
- **Double-click submission buttons:** [✓] User double-clicks "Continue" or "Finish" rapidly. No duplicate submissions or repeated processing observed. System handles the rapid input gracefully. 

---

## Quick Reference: Heuristics at a Glance

| Heuristic | Best for | Typical bugs found |
|-----------|----------|-------------------|
| SFDPOT | Comprehensive exploration | Missing features, undocumented behaviors |
| HICCUPS | Expectation alignment | Feature gaps, regression, spec mismatches |
| Goldilocks | Input validation | Field overflow, format errors, bounds failures |
| Zero, One, Many | Scaling & loops | Off-by-one bugs, performance drop, crashes |
| Never/Always | Guarantee validation | Broken invariants, defensive code gaps |
| Beginning/Middle/End | Workflow state | Race conditions, state violations, sequencing bugs |
| Interrupt/Starve | Resilience | Hangs, data loss, incomplete recovery |

---

## What's Covered: Practical Examples and Bug Reports

All heuristics in these notes are grounded in real exploratory testing work on SauceDemo and documented with practical examples.

### CRUD Testing
- [CRUD operations on SauceDemo cart](CRUD/saucedemo-crud.md) — Full lifecycle: Create (add items), Read (display consistency), Delete (remove items), including discovery of empty-cart checkout bug

### SFDPOT Testing
- [SFDPOT analysis of SauceDemo login](SFDPOT/SFDPOT-saucedemo-login.md) — Systematic exploration across all 6 dimensions with findings on structure, function, data handling, platform consistency, operations, and timing behavior
- [Bug report: Login error message overflow](SFDPOT/saucedemo-login-bug-report.md) — Detailed reproduction steps and screenshots

### Zero, One, Many Testing
- [Zero/One/Many checkout scenarios](zero-one-many/saucedemo-zero-one-many.md) — Three test scenarios demonstrating boundary limits with 0 items, 1 item, and all 6 available items
- [Bug report: Empty cart checkout](zero-one-many/bug-report-empty-cart-checkout.md) — Critical finding: checkout succeeds with $0.00 order and no validation

### Interrupt/Starve Testing
- [Interrupt/Starve checkout resilience](interrupt%20+%20starve/saucedemo-interrupt-starve.md) — Five scenarios testing reload, back button, tab switching, and rapid submissions

---

## Tips for Exploratory Testing Success

- **Time-box your sessions:** Set a clear duration (30 min, 1 hour) to maintain focus
- **Take notes:** Document what you tested, what you found, and what you want to test next
- **Vary your approach:** Mix random exploration with targeted heuristic-driven testing
- **Collaborate:** Pair exploratory testing with colleagues to catch blind spots
- **Integrate with automation:** Use automation for regression coverage, exploratory testing for new discoveries
