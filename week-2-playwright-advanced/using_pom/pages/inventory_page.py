class InventoryPage:
    def __init__(self, page):
        self.page = page
        self.title = page.locator(".title")
        self.cart_icon = page.locator(".shopping_cart_link")
        self.cart_badge = page.locator(".shopping_cart_badge")
        self.sort_dropdown = page.locator("[data-test='product_sort_container']")

        # Product-specific selectors
        self.backpack_add_button = page.locator("[data-test='add-to-cart-sauce-labs-backpack']")
        self.backpack_remove_button = page.locator("[data-test='remove-sauce-labs-backpack']")
        self.bike_light_add_button = page.locator("[data-test='add-to-cart-sauce-labs-bike-light']")
        self.bike_light_remove_button = page.locator("[data-test='remove-sauce-labs-bike-light']")

        # Generic product selectors
        self.product_names = page.locator(".inventory_item_name")
        self.product_prices = page.locator(".inventory_item_price")

    # Actions
    def add_backpack(self):
        self.backpack_add_button.click()

    def add_bike_light(self):
        self.bike_light_add_button.click()

    def remove_backpack(self):
        self.backpack_remove_button.click()

    def remove_bike_light(self):
        self.bike_light_remove_button.click()

    def open_cart(self):
        self.cart_icon.click()

    def sort_by(self, option_text):
        self.sort_dropdown.select_option(option_text)

    # Accessors
    def get_cart_count(self):
        if self.cart_badge.is_visible():
            return int(self.cart_badge.inner_text())
        return 0

    def get_product_names(self):
        return self.product_names.all_inner_texts()

    def get_product_prices(self):
        return self.product_prices.all_inner_texts()

    def is_loaded(self):
        return self.title.inner_text() == "Products"
