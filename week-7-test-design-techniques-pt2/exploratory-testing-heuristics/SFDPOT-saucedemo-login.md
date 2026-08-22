# Exploratory Testing Heuristics - Practical Exercise 1

**Chosen heuristic:** SFDPOT

**Chosen demo site:** https://www.saucedemo.com/

**Chosen feature:** login page

Black-box testing through interaction with the UI

## S - Structure

- Elements:
    - Heading: "Swag Labs"
    - Username and Password input fields with label text showing their purpose
        - Visually clean and minimalistic. Labels help users to understand the purposes of the input fields.
    - Login button with text: "Login", stating its purpose
    - Section displaying valid usernames and passwords (for testing purposes -> wouldn't be visible on a real website)
- Aesthetic and structural choices:
    - Username and password fields and login button are visually 'grouped together': they are both within the same container, with the white background. There are no lines or visual breaks separating these elements. This design choice means that there is one key container containing the crucial elements of the page, contributing to the page's useability.
    - The contrast between the background and main content helps the user to focus on the input fields and login button. This contributes to the visual grouping described above, and to the useability of the page.
    - Typography is minimalistic and not distracting.
    - The page uses a simple and consistent colour scheme.
    - Thoughts -> I don't know how to test this, but is there any way to change colours for colour blind users, edit the font to be dyslexia-friendly, etc.? The page doesn't seem to directly include this feature, but would it support other programs overriding it, plugins, etc.? Also idk how to test its functionality with screen readers.
    - The page scales well when zooming in and out, no elements overlap.
    - The main issue I identified is an overflow error on the red box when error messages are displayed.

## F - Function

- Entering any of the usernames 'standard_user', 'problem_user', 'performance_glitch_user', 'error_user', and 'visual_user' with the password 'secret_sauce' correctly navigates the user to the inventory page.
- 'performance_glitch_user' experiences a delay with this (intentional feature).
- Entering 'locked_out_user' and 'secret_sauce' displays the error message 'Epic sadface: Sorry, this user has been locked out'.
- Clicking on the cross displayed with the error message hides the error message.
- Entering an invalid username, password, or both, displays the error message 'Epic sadface: Username and password do not match any user in this service'. 
    - The system does not specify which of the two is invalid.
- Leaving the username field blank displays the error message "Epic sadface: Username is required."
- Leaving the password field blank displays the error message "Epic sadface: Password is required."
- Leaving both blank displays the error message "Epic sadface: Username is required." suggesting the username field is checked first.
- Changing the URL to www.saucedemo.com/inventory displays a blank page if the user is not logged in, so the system correctly doesn't allow any content to be viewed. However redirecting back to the login page would be more user-friendly.
- Redirecting to the login page is implemented when attempting to access the cart page or any step in the checkout workflow, without being logged in.

In summary: the validation logic is overall functional and effective. However, ensuring all pages redirect to the login page for an unauthenticated user would improve the user experience.

## D - Data

(I have already covered some valid and invalid credentials in the previous section, as well as the locked_out_user)

- Whitespace around otherwise correct credentials is not accepted. The system displays the error message "Epic sadface: Username and password do not match any user in this service."
- The system appears to be well-guarded against SQL injection. In all my attempts, the system displayed the error message "Epic sadface: Username and password do not match any user in this service."

## P - Platform

Platforms tested:
- Firefox, Chrome, Edge, Opera on Windows 11 laptop
- Chrome on Android phone

- Functionality is consistent across all platforms.
- Page scales consistently across all platforms.
- UI adapted for mobile: usernames and passwords are displayed in one column rather than two (when screen is scaled at 100%).

## O - Operations

### Input Operations

- Typing username, then password -> allowed
- Typing password, then username -> allowed
- Not errors are checked for / displayed before submitting
- Pasting values instead of typing -> allowed
- Selecting values from history dropdown (probably not the 'official' name of this feature lmao) -> allowed
    - However, the history only seems to be available for the username field, but not for the password field.
- Using saved credential (both username and password) -> allowed
- Whitespace before / after otherwise valid credentials -> not allowed, not removed automatically -> error message shown

### Submission Operations 

- Clicking login button -> allowed -> user redirected to inventory page
- Pressing enter in the username field -> allowed -> user redirected to inventory page
- Pressing enter in the password field -> allowed -> user redirected to inventory page
- Clicking login with empty fields displays error messages:
    - Username / both: "Epic sadface: Username is required."
    - Password only: "Epic sadface: Password is required."

### Navigation Operations

- Typing credentials, logging in, navigating back to login page -> input fields are now blank
- However, if using saved credentials, these will be shown when you navigate back
- Login -> close tab -> open site in new tab -> shows login page with empty fields 

## T - Time 

- Typing speed has no effect on error validation, as the system does not validate fields as you type. Fields are only validated after the "Login" button is pressed.
- The system also handles quickly-typed and pasted input with no issues.
- The system handles time delays between entering credentials and pressing the "Login" button.