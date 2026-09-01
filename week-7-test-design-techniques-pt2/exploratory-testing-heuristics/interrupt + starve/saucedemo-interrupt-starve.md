# Exploratory Testing Using Interrupt / Starve: SauceDemo Checkout

## Heuristics

**Interrupt:** Deliberately interrupt a workflow while it is in progress, then
check whether the application recovers without losing data or creating an
invalid result.

**Starve:** Limit the time, network, space, or other resources available to
the application, then check how it behaves under those constrained
conditions.

## Test charter

**Objective:** Determine whether SauceDemo preserves cart and checkout
integrity when checkout is interrupted or delayed.

**Site:** https://www.saucedemo.com/

**Account:** `standard_user` for normal behaviour; `performance_glitch_user`
for delayed behaviour.

**Feature:** Inventory -> Cart -> Checkout

**Data to monitor:**

- Cart item names and count
- Cart badge
- Checkout information
- Item total, tax, and final total
- Visible completion confirmations and other evidence of repeated processing
- Current page and available controls
- (Added after investigation) `cart-contents` in `localStorage` — the actual
  underlying data store for cart state, once discovered — see Session 1,
  Scenario E and Session 2, Scenario B.

## Session 1: Interrupt checkout

### Baseline

1. Log in as `standard_user`.
2. Add the Sauce Labs Backpack and Sauce Labs Bike Light.
3. Open the cart and record the items and cart badge.
4. Start checkout and enter valid customer information.

Expected state before interrupting:

| Observation | Expected value | Actual value |
|---|---|---|
| Cart items | Backpack, Bike Light | Backpack, Bike Light |
| Cart badge | `2` | `2` |
| Checkout information | Entered values | Entered values |
| Checkout totals | Item total + tax + total, matching the two items added | Item total: $39.98, Tax: $3.20, Total: $43.18 |

### Interrupt scenarios

| Scenario | Interruption | Recovery action |
|---|---|---|
| A | Refresh the checkout information page | Continue checkout |
| B | Press browser Back after entering customer information | Return to checkout and inspect the fields |
| C | Navigate away from checkout before pressing **Continue** | Reopen the cart and start checkout again |
| D | Open the application in another tab and return to the first tab | Continue the original checkout |
| E | Double-click **Continue** or **Finish** | Check for duplicate submissions, repeated navigation, or other visible evidence of repeated processing |

------------------

#### Scenario A

**Action:** The user reloads the checkout overview page.

**Actual Result:**
On the page "www.saucedemo.com/checkout-step-two.html", the user reloads the page.
The cart items ("Sauce Labs Backpack", "Sauce Labs Bike Light") are preserved, along with their quantities, descriptions, and prices.
The cart icon is preserved; it still reads `2`.
The price total is preserved, and still matches the combined prices of the two items.
The same level of tax is still applied.
Total price still matches item total + tax.
The website does not show an error, loading state, or misleading success message.
The user can continue without restarting the entire session.

**Expected Result:**
The expected result was that the program would handle the reload gracefully, allowing the user to continue the checkout process.

**Finding:**
The actual result matches the expected result.

--------------

#### Scenario B

**Actual Result:**
The cart items were preserved.
The entries in the First Name, Last Name, and Zip/Postal Code input fields were not preserved.
The application does not show an error, loading state, or misleading success message.
The user can recover without restarting the entire session; however, they have to re-enter these details.

**Expected Result:**
The cart items should be preserved.
The checkout details may be preserved or cleared after navigating back, but
they should not be partially or incorrectly changed. If the fields are
cleared, the user should be able to re-enter them and continue normally.
No error, loading state, or misleading success message should be displayed.

**Finding:**
The result meets the minimum recovery expectation, although clearing the
entered checkout details introduces minor user friction. The user can recover
from this interruption without having to restart the entire session.

#### Scenario C

**Actual Result:**
The cart items were preserved.
The entries in the First Name, Last Name, and Zip/Postal Code input fields were not preserved.
The application does not show an error, loading state, or misleading success message.
The user can recover without restarting the entire session; however, they have to re-enter these details.

**Expected Result:**
The cart items should be preserved.
The checkout details may be preserved or cleared after navigating back, but
they should not be partially or incorrectly changed. If the fields are
cleared, the user should be able to re-enter them and continue normally.
No error, loading state, or misleading success message should be displayed.

**Finding:**
Result identical to Scenario B — cart items preserved, checkout fields
cleared, no error or misleading message shown, recovery possible without
restarting the session. As this is a separate
interruption point to scenario B (navigating away before Continue, rather than pressing
Back after entering details), the matching outcome reflects the app
consistently clearing the checkout-details form on any navigation away from
it, not a copy-paste artifact between these two scenario write-ups.

#### Scenario D

**Actual Result:**
The cart items, as well as the entries in the First Name, Last Name, and Zip/Postal Code input fields, were all preserved.
The application does not show an error, loading state, or misleading success message.
The user can continue from where they left off.

**Expected Result:**
The cart items and checkout details should be preserved.
No error, loading state, or misleading success message should be displayed.

**Finding:**
The actual result matches the expected result.

#### Scenario E

**Action:** Double-click the **Continue** button, and separately the
**Finish** button, as rapidly as possible.

**Actual Result:**
No network requests are involved at any point in the checkout flow (see
Session 2, Scenario B finding below) — the entire flow, including Continue
and Finish, is handled client-side via JavaScript state changes, so
"duplicate submission" in the traditional network-request sense does not
apply here.

The actual state under test is `cart-contents` in `localStorage`
(`https://www.saucedemo.com`), which was inspected directly via DevTools →
Application → Local Storage:
- Before adding items: no `cart-contents` key exists.
- After adding the Backpack: `cart-contents: [4]`.
- After also adding the Bike Light: `cart-contents: [4,0]` — correctly
  appended, not overwritten or duplicated.
- After reaching "Checkout: Complete!" via a **single** click on Finish:
  `cart-contents` is removed entirely, matching the pre-cart baseline.
- After repeating the same flow and reaching "Checkout: Complete!" via a
  **rapid double-click** on Finish (and separately, on Continue), across
  several repeated attempts: `cart-contents` is cleared identically to the
  single-click case each time.

**Expected Result:**
The application should process the action once, with no duplicate or
partial state left behind regardless of click count.

**Finding:**
No evidence of a double-click integrity issue. Repeated testing (multiple
attempts) showed identical `cart-contents` behaviour between single-click
and double-click submission — the key is cleanly removed either way, with
no stale, duplicated, or partial entries observed. This is consistent with
the flow being entirely client-side: since there's no network request to
race, and the state-clearing logic appears to run the same way regardless
of how many times the button handler fires, there's little surface area
left for a classic double-submit bug in this specific implementation.

**Note on architecture (cross-reference to CRUD testing session):** this
investigation confirmed SauceDemo's cart is implemented as an array of
product indices in `localStorage`, keyed as `cart-contents` — e.g. `[4,0]`
for two added items. This closely matches the mental model used when
applying the CRUD heuristic to the same feature in a separate session
(treating the cart as "a collection of cart-item records"). 

The CRUD session's model was
chosen for testing-design reasons, before this implementation detail was
known, but it turned out to describe the real underlying structure closely.

## Session 2: Starve the application

### Baseline

Repeat the baseline steps from Session 1 using `standard_user`. Apply the
resource constraint during the cart or checkout workflow, not during login.

`performance_glitch_user` is not included here because the observable delay
for that account occurs during login. It can be tested separately as a
login-focused starvation session.

### Starvation scenarios

| Scenario | Constraint | What to observe |
|---|---|---|
| A | Throttle the network in browser DevTools before clicking **Continue** | Loading indicators, delayed controls, timeouts, and recovery after loading finishes |
| B | Block or delay the checkout request in browser DevTools | Error handling, disabled controls, and stale or partial data |
| ~~C~~ | ~~Click **Continue** repeatedly while the response is delayed~~ | *Cut from scope — see Scenario C below* |
| D | Refresh while checkout content is still loading | Lost data, blank content, or stale totals |

For each scenario, answer:

- Did the page eventually finish loading?
- Did all products and prices appear?
- Were controls disabled while the operation was pending?
- Could one user action produce more than one result?
- Did the application explain what the user should do next?
- Was the final cart and order state correct?

#### Scenario A

**Constraint applied:** Network throttled to 3G during checkout process.

**Actual result:**
The next page loads after a brief delay.
The cart items, as well as the entries in the First Name, Last Name, and Zip/Postal Code input fields, were all preserved.
The application does not show an error, loading state, or misleading success message.
The user can continue from where they left off.

**Expected result:**
The page should load after a brief delay.
The cart items and checkout details should be preserved.
The application should not show an error, loading state, or misleading success message.

**Finding:**
The actual result matches the expected result.
The user can continue through the rest of the checkout process.

**Follow-up note (added after confirming the app makes no network requests
during checkout — see Scenario B below):** since checkout involves no actual
network request, the delay observed here under 3G throttling was not caused
by a slowed-down request/response cycle. It's more likely attributable to
rendering/transition time, or possibly the throttling setting affecting
initial asset loading rather than the checkout action itself. Worth a
follow-up check on exactly what "3G" was actually delaying, since the
original assumption (a slowed network request) doesn't hold given what was
later confirmed.

#### Scenario B

**Constraint applied:** Attempted to block the checkout request via DevTools
→ Network → Request Blocking.

**Confirmed finding:** Checked the Network tab directly, filtered to
Fetch/XHR only, with the log cleared beforehand. Went through the full
checkout flow (Continue, then Finish). Result: **0 of 93 total requests**
were Fetch/XHR type — the 93 requests recorded were entirely CSS, JS,
fonts, and images loaded on page load, not anything triggered by the
checkout actions themselves.

This confirms **SauceDemo's checkout flow makes no network requests at
all** — it is implemented entirely client-side. Cart and checkout state is
held in `localStorage` (see Session 1, Scenario E for the confirmed
`cart-contents` key and its behaviour) and page transitions are handled via
client-side routing, not server calls.

**Revised finding:** Scenario B, as originally scoped ("block or delay the
checkout request"), is **not applicable** to this application — there is no
request to block. This isn't a gap in testing skill or DevTools usage; it's
a genuine architectural fact about the app under test, confirmed rather than
assumed. Recorded here as a confirmed non-applicable result rather than
"inconclusive," since the original uncertainty has been fully resolved.

#### Scenario C — cut from scope

*Originally scoped as "click Continue repeatedly while the response is
delayed." Not testable as written: Scenario B confirmed checkout makes no
network requests, so there is no response to delay in the first place.
See Scenario B for the underlying
finding that makes this scenario inapplicable.*

#### Scenario D

**Constraint applied:** Network throttled to 3G; page refreshed while
checkout content was expected to still be loading/transitioning.

**Actual result:**
No observable impact — no lost data, blank content, or stale totals were
seen. However, this result comes with a caveat: 3G throttling in
this app is not slow enough to reliably catch the page mid-load. The
transition completes quickly enough that hitting the exact moment of
"still loading" is difficult to land consistently, so a "no impact" result
here is less conclusive than the other scenarios — it may reflect the app
genuinely handling this well, or it may simply mean the interruption
window was too narrow to actually exercise the loading state in the first
place.

**Expected result:**
No lost data, blank content, or stale totals should occur if the page is
refreshed while loading.

**Finding:**
No issue observed, but confidence in this result is lower than other
scenarios in this document due to difficulty reliably timing the refresh
within the loading window. Given that checkout makes no network requests
(see Scenario B), the "loading" state being targeted here is likely just
a brief client-side render/transition rather than a genuine
network-wait state — which may explain why there's so little window to
actually interrupt. Worth revisiting only if a slower, more deliberate
throttling profile (e.g. "Slow 3G" rather than "Fast 3G," if not already
used) becomes available, or with a scripted/automated approach that can
time the refresh more precisely than manual clicking allows.

## Scope limitations

- SauceDemo is a demo application and does not expose real payment or order
	processing systems, order history, or order identifiers. Therefore, the
	actual number of orders created cannot be verified through the UI alone.
	However, direct inspection of `localStorage` (see Session 1, Scenario E)
	provided a reliable, confirmed way to check for duplicate or stale cart
	state, which partially closes this gap for cart integrity specifically —
	though it does not address order-level duplication beyond the cart data
	structure itself.
- Network throttling and browser-history tests should record the browser,
	viewport, and throttling settings used.
- A delayed response is not automatically a defect; the finding should show
	data loss, incorrect state, unavailable recovery, or misleading feedback.
- **Confirmed during this session:** SauceDemo's checkout flow makes no
  network requests at all (see Session 2, Scenario B). Several of the
  original scenarios (Session 2, B and C) were scoped around
  network-request behaviour that doesn't apply to this app's actual
  architecture. Original scenario definitions have been kept in this
  document rather than deleted, with confirmed findings and revised framing
  added alongside them, so the investigation process — including the
  incorrect initial assumption that a request existed to test — remains
  visible rather than edited out.