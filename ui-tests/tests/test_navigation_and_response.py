from urllib import response

def test_navigation_and_response(page):
    # page() is a fresh browser tab
    # goto() navigates to the specified URL
    response = page.goto("https://www.saucedemo.com/") 
    # test response status code
    assert response.status == 200
