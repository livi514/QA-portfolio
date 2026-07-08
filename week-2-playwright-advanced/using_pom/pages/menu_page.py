class MenuPage:
    def __init__(self, page):
        self.page = page
        self.menu_button = page.locator("#react-burger-menu-btn")
        self.logout_link = page.locator("#logout_sidebar_link")

    def open_menu(self):
        self.menu_button.click()

    def logout(self):
        self.logout_link.click()