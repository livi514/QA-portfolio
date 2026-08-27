# Exploratory Testing Using CRUD: SauceDemo Cart and Checkout

CRUD means testing the four basic operations on a piece of data:

- **C**reate
- **R**ead
- **U**pdate
- **D**elete

For SauceDemo, I am treating the cart as a collection of cart-item records.
The test checks whether each CRUD operation leaves the cart, its badge, and
the checkout summary in a consistent state.

For each operation, I compare the expected cart state with the item list,
cart badge, product buttons, and checkout totals.

| CRUD operation | SauceDemo action | What to verify |
|---|---|---|
| Create | Click **Add to cart** | A cart-item record is created; the item appears in the cart and the badge becomes `1` |
| Read | Open the cart or checkout overview | The same item data is displayed correctly: name, quantity, price, and totals |
| Update | Not supported for cart items; enter checkout information as a separate data entity | SauceDemo has no quantity-edit or product-edit control; checkout details can be entered and discarded |
| Delete | Click **Remove** | The cart-item record is deleted; the item disappears, the badge updates, and totals recalculate |

**Limitation:** SauceDemo does not support changing the quantity of one item.
The Update operation is therefore not demonstrated for cart-item records.
Checkout information is a separate data entity, which is entered during this
session but is not tested for persistence after cancellation. Each product
can only exist once in the cart, so adding an already-added product does not
test an additional quantity.

A practical exploratory session could look like this:

## Step 1 - Logging in as standard_user *(Setup - not CRUD)*

**Action:** The user logs in using the username "standard_user" and the password "secret_sauce".

**Result:** The user is authenticated successfully, and navigated to the inventory page.

## Step 2 - Adding the Sauce Labs Backpack *(Create)*

**Action:** The user adds the "Sauce Labs Backpack" to their cart.

**Result:** Cart icon updates to show "1"; the item's button changes from "Add to Cart" to "Remove".

## Step 3 - Opening and inspecting cart *(Read)*

**Action:** The user clicks on the cart icon.

**Result:** The user is taken to the cart page. The cart page shows the "Sauce Labs Backpack", with the following details:

QTY: 1

Description:
- "Sauce Labs Backpack"
- "carry.allTheThings() with the sleek, streamlined Sly Pack that melds uncompromising style with unequaled laptop and tablet protection."*
- $29.99

## Step 4 - Navigating back to the inventory page *(Read)*

**Action:** The user clicks on the "Continue Shopping" button.

**Result:** The user is taken back to the inventory page. The button for the "Sauce Labs Backpack" still reads "Remove", while the buttons for the other 5 items read "Add to cart".

## Step 5 - Adding two more items *(Create)*

**Action:** The user adds the "Sauce Labs Bike Light" and the "Sauce Labs Bolt T-Shirt" to their cart.

**Result:** Cart icon updates to show "3"; the buttons for "Sauce Labs Backpack", "Sauce Labs Bike Light", and "Sauce Labs Bolt T-Shirt" all read "Remove".


## Step 6 - Returning to cart *(Read)*

**Action:** The user clicks on the cart icon.

**Result:** The user is taken to the cart page, which shows all 3 items along with their names, quantities, descriptions, and prices.

## Step 7 - Removing Sauce Labs Backpack *(Delete)*

**Action:** The user removes the "Sauce Labs Backpack" from their cart by clicking the "Remove" item on the tile.

**Result:** The "Sauce Labs Backpack" is no longer displayed on the cart page. The icon next to the cart now shows "2". 

## Step 8 - Starting Checkout *(Read)*

**Action:** User clicks "Checkout" button.

**Result:** The user is taken to the first page in the checkout process, which has input fields for their "First Name", "Last Name" and "Zip/Postal Code".

## Step 9 - User Enters Checkout Details, then Clicks "Cancel" *(Update checkout data + navigation)*

**Action:** The user enters the first name "Standard", the last name "User", and the postal code "12345", then clicks the cancel button.

**Result:** The user is taken back to their cart, which shows the items "Sauce Labs Bike Light" and "Sauce Labs Bolt T-Shirt". The cart state is preserved; persistence of the entered checkout details was not tested.

## Step 10 - User Removes Sauce Labs Bike Light *(Delete)*

**Action:** The user presses the "Remove" button for the "Sauce Labs Bike Light". 

**Result:** The "Sauce Labs Bike Light" is no longer displayed in the user's cart.

## Step 11 - User Clicks "Checkout" Button *(Read)*

**Action:** User clicks "Checkout" button.

**Result:** The user is taken to the first page in the checkout process, which has input fields for their "First Name", "Last Name" and "Zip/Postal Code".

## Step 12 - User Enters Checkout Details, then Clicks "Continue" *(Update checkout data + Read cart)*

**Action:** The user enters the first name "Standard", the last name "User", and the postal code "12345", then clicks the "Continue" button.

**Result:** The user is taken to the second page in the checkout process, which shows the items in their cart - currently just "Sauce Labs Bolt T-Shirt". The price total reflects the price of just the t-shirt: none of the previous items are counted.

## Step 13 - User Presses "Cancel" Button *(Read)*

**Action:** The user presses the "Cancel" button.

**Result:** The user is taken back to the inventory page. The "Sauce Labs Bolt T-Shirt" is still selected.

## Step 14 - User Presses "Cart" icon *(Read)*

**Action:** User presses cart icon and views their items.

**Result:** The cart shows the "Sauce Labs Bolt T-Shirt".

## Step 15 - User Removes the Sauce Labs Bolt T-Shirt *(Delete)*

**Action:** The user presses the "Remove" button for the Sauce Labs Bolt T-Shirt.

**Result:** The user's cart is now shown as being empty.

## Step 16 - User Presses "Checkout" *(Read + empty-state boundary)*

**Action:** The user presses the "Checkout" button.

**Result:** The user is taken to the first page in the checkout process.

## Step 17 - User enters details and presses "Continue" *(Update checkout data + Read cart)*

**Action:** The user enters the first name "Standard", the last name "User", and the postal code "12345", then clicks the "Continue" button.

**Result:** The user is taken to the second page in the checkout process, which shows that they are checking out with no items in their cart.

## Step 18 - User presses "Continue" to reach the overview *(Read)*

**Action:** The user presses the "Continue" button.

**Result:** The user is taken to the Payment Information screen, showing that the Price Total is $0.00.

## Step 19 - User Presses "Finish" Button *(Outside cart CRUD: order creation)*

**Action:** The user presses the "Finish" button.

**Result:** The user is shown the "Checkout: Complete!" screen.

## Step 20 - User Presses "Back Home" Button *(Read/reset)*

**Action:** The user presses the "Back Home" Button.
**Result:** The user is taken back to the inventory page, with an empty cart.

---------------------

**CRUD finding:** After the final cart item is deleted, SauceDemo still allows
checkout to proceed and complete with a `$0.00` total. Delete succeeds, but
the empty collection is not validated before the checkout workflow creates a
successful order state. See the dedicated empty-cart bug report.

**Scope limitation:** Items cannot be removed from the cart during checkout.
They can only be removed from the inventory page or the cart page.
