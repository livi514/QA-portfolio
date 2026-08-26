# Exploratory Testing Heuristics — Zero / One / Many

**Chosen heuristic:** Zero / One / Many

**Chosen demo site:** https://www.saucedemo.com/

**Chosen feature:** Inventory → Cart → Checkout flow

**Method:** Black-box testing through interaction with the UI, varying the number of items in the cart at checkout (Zero, One, Many)

---

## Scenario 1: Checkout with ZERO items in cart

| Step | Action | Result |
|---|---|---|
| 1 | Log in with valid credentials | Successfully authenticated, navigated to inventory page. |
| 2 | Navigate to cart without adding any items | Empty cart is displayed correctly. |
| 3 | Press "Checkout" with an empty cart | Proceeds to the checkout information step (First Name / Last Name / Zip). **No warning or error shown about the empty cart.** |
| 4 | Enter First Name: "Standard", Last Name: "User", Zip: "123456", press "Continue" | Proceeds to the checkout overview step. Price total shown: Item total $0, Tax $0.00, Total $0.00 |
| 5 | Press "Finish" | Checkout completes successfully. "Thank you for your order!" confirmation is shown. |

### Finding:

The system allows a full checkout to complete with
zero items in the cart: no validation blocks this at any step, and the
user reaches a normal order confirmation for a $0.00 order.

**See dedicated bug report.**

---

## Scenario 2: Checkout with ONE item in cart

| Step | Action | Result |
|---|---|---|
| 1 | Log in with valid credentials | Successfully authenticated, navigated to inventory page. |
| 2 | Add "Sauce Labs Backpack" to cart | Cart icon updates to show "1"; the item's button changes from "Add to cart" to "Remove" |
| 3 | Navigate to cart page | Cart correctly displays the Sauce Labs Backpack. |
| 4 | Press "Checkout" | Proceeds to the checkout information step, no errors shown. |
| 5 | Enter First Name: "Standard", Last Name: "User", Zip: "123456", press "Continue" | Proceeds to checkout overview. Price total: Item total $29.99, Tax $2.40, Total $32.39 |
| 6 | Press "Finish" | Checkout completes successfully. "Thank you for your order!" confirmation is shown. |

No issues found in this flow — this represents the expected, unremarkable
baseline case.

---

## Scenario 3: Checkout with MANY items in cart (all 6 available)

| Step | Action | Result |
|---|---|---|
| 1 | Log in with valid credentials | Successfully authenticated, navigated to inventory page. |
| 2 | Add all 6 available items to cart | Cart icon updates to show "6"; every item's button changes from "Add to cart" to "Remove". |
| 3 | Navigate to cart page | Cart correctly displays one of each of the 6 items. |
| 4 | Press "Checkout" | Proceeds to the checkout information step, no errors shown. |
| 5 | Enter First Name: "Standard", Last Name: "User", Zip: "123456", press "Continue" | Proceeds to checkout overview. Price total: Item total $129.94, Tax $10.40, Total $140.34 |
| 6 | Press "Finish" | Checkout completes successfully. "Thank you for your order!" confirmation is shown. |

---

## Note: "Many of the same item" is not a testable scenario here

SauceDemo does not support adding multiple quantities of the same item to the cart: each item can only be added once, and the button toggles
between "Add to cart" and "Remove" rather than offering a quantity
selector. This axis of Zero/One/Many (quantity *per item*, as opposed to number of *distinct* items) simply doesn't apply to this system as built.
