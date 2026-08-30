# Exploratory Testing Using CRUD: SauceDemo Cart and Checkout

CRUD means testing the four basic operations on a piece of data:

- **C**reate
- **R**ead
- **U**pdate
- **D**elete

For SauceDemo, the cart is treated as a collection of cart-item records. Each operation is checked for consistency across every surface that displays cart state: the inventory page (grid tiles), the product detail page, the cart page, and the checkout summary.

For each operation, I compare the expected cart state with the item list, cart badge, product buttons, and checkout totals.

| CRUD operation | SauceDemo action | What to verify |
|---|---|---|
| Create | Click **Add to cart** (from the inventory grid or a product's detail page) | A cart-item record is created; the item appears in the cart and the badge becomes `1` |
| Read | View the inventory grid, a product's detail page, the cart page, or the checkout overview | The same item data (name, quantity, price) is displayed consistently across all four surfaces |
| Update | Not supported for cart items; checkout information is a separate data entity and is tested for update behaviour instead | SauceDemo has no quantity-edit or product-edit control for cart items; checkout details, however, can be entered, cancelled, and re-entered with different values - see Session 2 |
| Delete | Click **Remove** (from the inventory grid, the product detail page, or the cart page) | The cart-item record is deleted; the item disappears from all views, the badge updates, and totals recalculate |

**Limitations:**
- SauceDemo does not support changing the quantity of a single item. Update is therefore not demonstrable for cart-item records themselves.
- Each product can only exist once in the cart (no quantity selector).
- Items cannot be removed from the cart during the checkout flow itself. Removal is only possible from the inventory page, a product's detail page, or the cart page, before checkout begins.

## Session 1: Core cart lifecycle (Create, Read, Delete), via cart-page removal

### Step 1 - Logging in as standard_user *(Setup - not CRUD)*

**Action:** Log in using the username "standard_user" and the password "secret_sauce".

**Result:** Authenticated successfully, and navigated to the inventory page.

### Step 2 - Adding the Sauce Labs Backpack *(Create)*

**Action:** Add the "Sauce Labs Backpack" to the cart from the inventory grid.

**Result:** Cart icon updates to show "1"; the item's button changes from "Add to Cart" to "Remove".

### Step 3 - Opening and inspecting cart *(Read)*

**Action:** Click on the cart icon.

**Result:** Taken to the cart page. The cart page shows the "Sauce Labs Backpack", with the following details:

QTY: 1

Description:
- "Sauce Labs Backpack"
- "carry.allTheThings() with the sleek, streamlined Sly Pack that melds uncompromising style with unequaled laptop and tablet protection."*
- $29.99

This matches the inventory-page listing.

### Step 4 - Navigating back to the inventory page *(Read)*

**Action:** Click on the "Continue Shopping" button.

**Result:** Taken back to the inventory page. The button for the "Sauce Labs Backpack" still reads "Remove", while the buttons for the other 5 items read "Add to cart", meaning the cart state is correctly reflected on the grid.

### Step 5 - Adding two more items *(Create)*

**Action:** Add the "Sauce Labs Bike Light" and the "Sauce Labs Bolt T-Shirt" to cart.

**Result:** Cart icon updates to show "3"; the buttons for "Sauce Labs Backpack", "Sauce Labs Bike Light", and "Sauce Labs Bolt T-Shirt" all read "Remove".

### Step 6 - Returning to cart *(Read)*

**Action:** Click on the cart icon.

**Result:** Taken to the cart page, which shows all 3 items correctly, along with their names, quantities, descriptions, and prices.

### Step 7 - Removing Sauce Labs Backpack *(Delete - via cart page)*

**Action:** Remove the "Sauce Labs Backpack" via the cart page, by clicking the "Remove" item on the tile.

**Result:** The "Sauce Labs Backpack" is no longer displayed on the cart page. The icon next to the cart now shows "2". 

### Step 8 - Starting Checkout *(Read)*

**Action:** Click "Checkout" button.

**Result:** Taken to the first page in the checkout process, which has input fields for "First Name", "Last Name" and "Zip/Postal Code".

### Step 9 - Entering checkout details, then clicking "Cancel" *(navigation - checkout data not committed)*

**Action:** Enter the first name "Standard", the last name "User", and the postal code "12345", then click the cancel button.

**Result:** Taken back to the cart page, which shows the items "Sauce Labs Bike Light" and "Sauce Labs Bolt T-Shirt". The cart state is preserved through a cancelled checkout attempt. (Whether the enterd checkout details persist anywhere was not tested in this session - see Session 2 for the follow-up.)

### Step 10 - Removing Sauce Labs Bike Light *(Delete - via cart page)*

**Action:** Press the "Remove" button for the "Sauce Labs Bike Light". 

**Result:** The "Sauce Labs Bike Light" is no longer displayed in the cart.

### Step 11 - Starting Checkout again *(Read)*

**Action:** Click the "Checkout" button.

**Result:** Taken to the first page in the checkout process, which has input fields for their "First Name", "Last Name" and "Zip/Postal Code".

### Step 12 - Entering Checkout Details, then clicking "Continue" *(Update checkout data + Read cart)*

**Action:** Enter the first name "Standard", the last name "User", and the postal code "12345", then click the "Continue" button.

**Result:** Taken to the second page in the checkout process, which shows the items in the cart - currently just "Sauce Labs Bolt T-Shirt". The price total reflects the price of just the t-shirt: none of the previous items are counted.

### Step 13 - Clicking "Cancel" Button *(Read)*

**Action:** Click the "Cancel" button.

**Result:** Taken back to the inventory page. The "Sauce Labs Bolt T-Shirt" is still selected.

### Step 14 - Clicking "Cart" icon *(Read)*

**Action:** Click cart icon.

**Result:** The cart shows the "Sauce Labs Bolt T-Shirt", as expected.

### Step 15 - Removing the Sauce Labs Bolt T-Shirt *(Delete - via cart page)*

**Action:** Click the "Remove" button for the Sauce Labs Bolt T-Shirt.

**Result:** Cart is now empty.

### Step 16 - Starting Checkout with an empty cart *(Read + empty-state boundary)*

**Action:** Click the "Checkout" button.

**Result:** First checkout page shown, with no warning that the cart is empty.

### Step 17 - Entering details and clicking "Continue" *(Read - empty cart crried into checkout)*

**Action:** Enter the first name "Standard", the last name "User", and the postal code "12345", then click the "Continue" button.

**Result:** Second checkout page shows no items in the cart, with no error shown.

### Step 18 - Click "Continue" to reach the overview *(Read)*

**Action:** Click the "Continue" button.

**Result:** Taken to the Payment Information screen, which shows that the Price Total is $0.00.

### Step 19 - Finishing Checkout *(Order creation - outside cart CRUD)*

**Action:** Click the "Finish" button.

**Result:** Shown the "Checkout: Complete!" screen.

### Step 20 - Returning home *(Read/reset)*

**Action:** Click the "Back Home" Button.
**Result:** Taken back to the inventory page, with an empty cart.

---------------------

## Session 2 (Product-page pathways, and a genuine Update test)

Session 1 tested Create/Read/Delete exclusively via the inventory grid and cart page. 

Session 2 fills two gaps: whether the same operations behave consistently when performed from a product's own detail page, and whether checkout information genuinely supports being updated, i.e. entering one set of values, discarding them, then entering and committing a different set, rather than only ever re-entering the same values twice.

### Step 1 - Logging in as standard_user *(Setup - not CRUD)*

**Action:** Log in using the username "standard_user" and the password "secret_sauce".

**Result:** Authenticated successfully, and navigated to the inventory page.

### Step 2 - Viewing Sauce Labs Backpack Product Page *(Read)*

**Action:** From the inventory page, click on the "Sauce Labs Backpack" product name / text to view the product page for the backpack.

**Result:** The product page for the "Sauce Labs Backpack" is displayed, including the photo, name, description, and price of the product, as well as an "Add to cart" button. The text on the button ("Add to cart") matches the button's text for the backpack on the inventory page, and reflects the fact that the backpack has not been added to the user's cart.

### Step 3 - Adding Sauce Labs Backpack to Cart *(Create - via product page)*

**Action:** From the backpack's product page, the user presses the "Add to cart" button.

**Result:** The button now reads "Remove" and the cart icon shows "1". We can therefore conclude that Create behaves consistently regardless of entry point (inventory grid vs. product page).

### Step 4 - Opening and inspecting Cart *(Read)*

**Action:** Click the cart icon.

**Result:** Taken to the cart page, which shows the "Sauce Labs Backpack", with the following details:

QTY: 1

Description:
- "Sauce Labs Backpack"
- "carry.allTheThings() with the sleek, streamlined Sly Pack that melds uncompromising style with unequaled laptop and tablet protection."*
- $29.99

This matches Session 1's result for the same item, confirming consistent data across sessions and entry points.

### Step 5 - Returning to the Inventory Page *(Read)*

**Action:** Click the "Continue Shopping" button.

**Result:** Taken back to the inventory page. The button for the Sauce Labs Backpack still reads "Remove", while the buttons for the other 5 items read "Add to cart".

### Step 6 - Re-navigating to the Sauce Labs Backpack Product Page *(Read)*

**Action:** Click the "Sauce Labs Backpack" text.

**Result:** Taken to the cart page, which shows the "Sauce Labs Backpack", with the same details as before.

### Step 7 - Removing the Backpack from its product page *(Delete - via product page)*

**Action:** Click "Remove" on the product detail page.

**Result:** The text on the button now reads "Add to cart" and the cart icon showing the number is hidden (correctly reflects an empty cart). Delete behaves consistently when performed from the product page, matching the cart-removal behaviour tested in Session 1.

### Step 8 - Returning to the Inventory page *(Read)*

**Action:** Click the "Back to products" button.

**Result:** Returns to the inventory grid; all 6 items correctly shown as unselected.

### Step 9 - Adding Sauce Labs Fleece Jacket to Cart *(Create - via inventory grid)*

**Action:** Click on the "Add to cart" button for the fleece jacket.

**Result:** The text on the button now reads "Remove" and the cart icon shows "1".

### Step 10 - Opening and Inspecting Cart *(Read)*

*Action:** Click on the cart icon.

**Result:** Taken to the cart page, which shows the "Sauce Labs Fleece Jacket", with the following details:

QTY: 1

Description:
- "Sauce Labs Fleece Jacket"
- "It's not every day that you come across a midweight quarter-zip fleece jacket capable of handling everything from a relaxing day outdoors to a busy day at the office."
- $49.99

### Step 11 - Starting Checkout process *(Read)*

**Action:** Click on "Checkout" button.

**Result:** Taken to the first page in the checkout process, showing input fields for First Name, Last Name, and Zip/Postal Code.

### Step 12 - Entering the first set of checkout details 

**Action:** Enter the first name "Standard", the last name "User", and the postal code "12345".

**Result:** The values are correctly displayed in the form fields.

### Step 13 - Cancelling the checkout attempt

**Action:** Click on the "Cancel" button.

**Result:** Returns to the cart. The cart contents are preserved.

### Step 14 - Restarting checkout

**Action:** Click on the "Checkout" button again.

**Result:** The checkout form is shown with blank fields. The previously entered values ("Standard"/"User"/"12345") values are not retained. This confirms that the form does not silently persist stale data from a cancelled attempt.

### Step 15 - Entering a second, different set of checkout details *(Update - confirmed)*

**Action:** Enter "Jane" / "Doe" / "54321". These are deliberately different values from Step 12, to test whether the second entry genuinely overrides the first rather than merging with or being ignored in favour of it.

**Result:** The new values ("Jane" / "Doe" / "54321") are correctly displayed on screen, replacing the earlier discarded entry.

### Step 16 - Continuing to the payment overview *(Read)*

**Action:** Click the "Continue" button.

**Result:** Payment Information screen shown correctly, with the Fleece Jacket and its price reflected in the total.

### Step 17 - Finishing checkout *(order creation - outside cart CRUD)*

**Action:** Click the "Finish" button.

**Result:** The "Checkout: Complete!" confirmation message shown. As with the payment overview in Step 16, only item and price information is shown. The First Name, Last Name, and Postal Code entered earlier are not displayed anywhere on this screen either.

### Update Finding (confirmed):

Session 2 confirms that checkout information supports being updated, not just re-entered identically as shown in Session 1. Cancelling a checkout attempt and starting over correctly clears the form (Step 14), and a second, deliberately different set of values (Step 15) is used cleanly, with no evidence of the first, discarded entry being retained, merged, or silently reused.

This is a positive result: the "Update" pathway for checkout data works as expected.

### Observation (not necessarily a bug, but worth documenting):

The First Name, Last Name, and Postal Code entered by the user are never shown again after the page on which they're entered. Confirmed absent from both the payment overview screen (Step 16, which shows only item and price information) and the final "Checkout: Complete!" confirmation screen (Step 17). The user has no way to review the shipping details they submitted before or after confirming the order. Worth flagging as a UX gap even though it isn't a functional defect.


---------------------

**CRUD finding:** After the final cart item is deleted, SauceDemo still allows
checkout to proceed and complete with a `$0.00` total. Delete succeeds, but
the empty collection is not validated before the checkout workflow creates a
successful order state. See the dedicated empty-cart bug report.

**Scope limitation:** Items cannot be removed from the cart during checkout.
They can only be removed from the inventory page or the cart page.
