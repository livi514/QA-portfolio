# Bug Report: Checkout Completes Successfully With Zero Items In Cart

## Summary
SauceDemo allows a user to complete the entire checkout flow (including
reaching the final "Thank you for your order!" confirmation) with an
empty cart. No validation at any step blocks or warns about checking out
with zero items, and the order summary displays a $0.00 total as if it
were a normal, valid order.

## Environment
- **Site:** https://www.saucedemo.com/
- **All available accounts tested, reproducibility varies by account:**

| Account | Empty-cart checkout reproduces? | Notes |
|---|---|---|
| `standard_user` | **Yes:** bug confirmed | Full flow completes as described below |
| `performance_glitch_user` | **Yes:** bug confirmed | Identical to `standard_user` aside from the expected login delay; not a factor in this specific bug |
| `visual_user` | **Yes:** bug confirmed | Some layout issues observed during checkout, but none block completion, so the empty-cart bug still reproduces |
| `problem_user` | **No:** cannot test | Blocked before reaching the point where this bug would matter: cannot fill in the "Last Name" field at all (a separate, pre-existing issue with this account), so checkout cannot be completed regardless of cart contents |
| `error_user` | **No** cannot test | Gets stuck at the final step and cannot press "Finish" (a separate, pre-existing issue with this account), so this account never reaches order confirmation regardless of cart contents |

**Interpretation:** the empty-cart bug is confirmed reproducible for 3 of the 5 standard test accounts. The other 2 don't reproduce it, but only because those accounts have unrelated, separate defects that block
checkout before the empty-cart issue would ever come into play. This is
not evidence the bug is fixed or doesn't apply to them, just that it
couldn't be tested there.

## Steps to Reproduce
1. Log in with valid credentials.
2. From the inventory page, do **not** add any items to the cart.
3. Click the cart icon to navigate to the cart page (it will be empty).
4. Click "Checkout."
5. Enter any values into First Name, Last Name, and Zip/Postal Code
   (e.g. "Standard" / "User" / "123456").
6. Click "Continue."
7. Click "Finish."

## Expected Result
At minimum, one of the following should occur:
- The "Checkout" button should be disabled or hidden when the cart is
  empty, preventing the flow from starting at all, **or**
- An error/warning should be shown at some point in the flow (e.g. on
  reaching the checkout overview with a $0.00 total) telling the user
  their cart is empty and they cannot proceed, **or**
- At minimum, checkout should still be blocked at the final "Finish" step.

## Actual Result
None of the above occur. The user can:
- Reach the checkout information step with an empty cart, no warning.
- Reach the checkout overview step, which displays Item total: $0,
  Tax: $0.00, Total: $0.00. This is styled identically to a normal order
  summary, with no indication anything is unusual.
- Click "Finish" and receive the same "Thank you for your order!"
  confirmation shown for a legitimate order.

## Severity / Impact
**Medium.** This isn't a security issue or data-loss risk on a demo site, but it represents a genuine logic gap: a system knowingly allows a
"successful" transaction that has no actual content. Confirmed across 3
of the 5 standard test accounts (the other 2 are blocked by unrelated,
pre-existing account-specific bugs before this issue can even be
reached — see Environment table above), so this isn't an account-specific quirk, it's a gap in the checkout flow's core validation logic. In a real e-commerce context, this class of bug could mean empty orders reaching a fulfilment or payment system, confusing order-tracking metrics, or a poor user experience for someone who ends up here by accident (e.g. removed their last cart item mid-checkout without realising, then continued through muscle memory). Worth fixing regardless of whether it causes visible harm on this specific demo, since the underlying pattern — no server- or client-side guard against a degenerate/empty state — is the kind of gap that tends to matter more once real payment or fulfilment logic sits behind it.