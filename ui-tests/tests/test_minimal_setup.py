# In PlayWright, this is the minimal setup for a test. 
# It navigates to the specified URL and can be expanded with additional test steps as needed.
def test_minimal_setup(page):
    # page() is a fresh browser tab
    # goto() navigates to the specified URL
    page.goto("https://www.saucedemo.com/") 
    # playwright automatically waits for the page to load before proceeding to the next step


