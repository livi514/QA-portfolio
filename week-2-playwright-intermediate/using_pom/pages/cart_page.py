from playwright.sync_api import expect


class CartPage:
    def __init__(self, page):
        self.page = page
        self.title = page.locator(".title")
        self.cart_items = page.locator(".cart_item")
        self.item_names = page.locator(".inventory_item_name")
        self.item_prices = page.locator(".inventory_item_price")

        self.remove_backpack_button = page.locator(
            "[data-test='remove-sauce-labs-backpack']"
        )
        self.remove_bike_light_button = page.locator(
            "[data-test='remove-sauce-labs-bike-light']"
        )

        self.continue_shopping_button = page.locator("[data-test='continue-shopping']")
        self.checkout_button = page.locator("[data-test='checkout']")

    def wait_until_loaded(self):
        # The title and checkout button exist on the cart page whether
        # or not it has items, so this works for empty carts too.
        expect(self.title).to_have_text("Your Cart")
        expect(self.checkout_button).to_be_visible()

    # Actions
    def remove_backpack(self):
        self.remove_backpack_button.click()

    def remove_bike_light(self):
        self.remove_bike_light_button.click()

    def continue_shopping(self):
        self.continue_shopping_button.click()

    def checkout(self):
        self.checkout_button.click()

    # Accessors
    def get_item_count(self):
        self.wait_until_loaded()
        return self.cart_items.count()

    def get_item_names(self):
        self.wait_until_loaded()
        return self.item_names.all_inner_texts()

    def get_item_prices(self):
        self.wait_until_loaded()
        return self.item_prices.all_inner_texts()

    def get_title_text(self):
        self.wait_until_loaded()
        return self.title.inner_text()
