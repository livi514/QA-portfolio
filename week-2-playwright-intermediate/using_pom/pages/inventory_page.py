from playwright.sync_api import expect


class InventoryPage:
    def __init__(self, page):
        self.page = page

        # Static elements
        self.title = page.locator("span.title")
        self.cart_icon = page.locator("a.shopping_cart_link")
        self.cart_badge = page.locator("span.shopping_cart_badge")

        # Sort dropdown (actual <select> element)
        self.sort_dropdown = page.locator("select[data-test='product-sort-container']")

        # Product containers
        self.product_items = page.locator("div.inventory_item")
        self.product_names = page.locator("div.inventory_item_name")
        self.product_prices = page.locator("div.inventory_item_price")

        # Specific product buttons
        self.backpack_add_button = page.locator(
            "[data-test='add-to-cart-sauce-labs-backpack']"
        )
        self.backpack_remove_button = page.locator(
            "[data-test='remove-sauce-labs-backpack']"
        )

        self.bike_light_add_button = page.locator(
            "[data-test='add-to-cart-sauce-labs-bike-light']"
        )
        self.bike_light_remove_button = page.locator(
            "[data-test='remove-sauce-labs-bike-light']"
        )

    # Navigation
    def navigate(self):
        self.page.goto("https://www.saucedemo.com/inventory.html")

    # Page load wait
    def wait_until_loaded(self):
        # Wait for the page title to appear
        self.page.wait_for_selector("span.title")
        # Wait for at least one product to render
        self.page.wait_for_selector("div.inventory_item")

    # Generic product actions
    def add_item(self, item_name):
        self.page.locator(f"[data-test='add-to-cart-{item_name}']").click()

    def remove_item(self, item_name):
        self.page.locator(f"[data-test='remove-{item_name}']").click()

    # Specific product actions
    def add_backpack(self):
        self.backpack_add_button.click()

    def add_bike_light(self):
        self.bike_light_add_button.click()

    def remove_backpack(self):
        self.backpack_remove_button.click()

    def remove_bike_light(self):
        self.bike_light_remove_button.click()

    # Cart helpers
    def get_cart_count(self):
        if self.cart_badge.is_visible():
            return int(self.cart_badge.inner_text())
        return 0

    def is_cart_badge_visible(self):
        return self.cart_badge.is_visible()

    def open_cart(self):
        self.cart_icon.click()

    # Sorting helpers
    def sort_by(self, option):
        self.sort_dropdown.select_option(option)

    def sort_by_price_low_to_high(self):
        self.sort_dropdown.select_option("lohi")

    def sort_by_price_high_to_low(self):
        self.sort_dropdown.select_option("hilo")

    def sort_by_name_ascending(self):
        self.sort_dropdown.select_option("az")

    def sort_by_name_descending(self):
        self.sort_dropdown.select_option("za")

    # Product accessors
    def get_product_names(self):
        return self.product_names.all_inner_texts()

    def get_product_prices(self):
        return self.product_prices.all_inner_texts()

    def get_product_count(self):
        return self.product_items.count()

    def get_price_of(self, product_name):
        locator = (
            self.page.locator(f"text={product_name}")
            .locator("..")
            .locator(".inventory_item_price")
        )
        return locator.inner_text()

    # Visibility helpers
    def is_loaded(self):
        return self.title.inner_text() == "Products"

    def is_sort_dropdown_visible(self):
        return self.sort_dropdown.is_visible()

    def is_cart_icon_visible(self):
        return self.cart_icon.is_visible()

    def are_product_names_visible(self):
        for i in range(6):
            expect(self.product_names.nth(i)).to_be_visible()

    def are_product_prices_visible(self):
        for i in range(6):
            expect(self.product_prices.nth(i)).to_be_visible()
