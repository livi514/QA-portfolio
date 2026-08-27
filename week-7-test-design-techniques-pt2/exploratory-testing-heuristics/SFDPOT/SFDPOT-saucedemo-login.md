# Exploratory Testing Heuristics — SFDPOT

**Chosen heuristic:** SFDPOT (Structure, Function, Data, Platform, Operations, Time)
**Chosen demo site:** https://www.saucedemo.com/
**Chosen feature:** Login page
**Method:** Black-box testing through interaction with the UI

---

## S — Structure

**Elements present:**
- Heading: "Swag Labs"
- Username and password input fields, each with a visible label indicating its purpose
- Login button, labelled "Login"
- A section listing valid usernames and passwords for testing purposes (would not be present on a production site)

**Aesthetic and structural observations:**
- The username field, password field, and login button are visually grouped within a single white container, with no dividing lines. This keeps the page's key interactive elements presented as one coherent unit, supporting usability.
- Strong contrast between the container and background draws attention to the input fields and button, reinforcing the visual grouping above.
- Typography is minimal and unobtrusive.
- The colour scheme is simple and consistent throughout.
- The page scales cleanly when zooming in and out; no elements overlap.

**Known issue:**
- An overflow bug occurs on the red error-message box when certain error messages are displayed. *(See dedicated bug report.)*

**Open questions (accessibility):**
- No obvious built-in support for colour-blind users or dyslexia-friendly fonts. Unclear whether the page would support third-party overrides (browser extensions, OS-level accessibility tools) without conflict.
- Screen reader compatibility not yet tested.

> **Note on accessibility scope:** accessibility testing (keyboard navigation, screen reader behaviour, colour contrast) is intentionally out of scope for this exercise — it's covered as its own dedicated topic in Week 8 of the roadmap, using WCAG 2.2 and Axe DevTools. This was a deliberate scoping decision, not an oversight. See the Week 8 accessibility testing notes for that follow-up once complete.

---

## F — Function

**Valid login behaviour:**
- Logging in with any of `standard_user`, `problem_user`, `performance_glitch_user`, `error_user`, or `visual_user` alongside the password `secret_sauce` correctly navigates to the inventory page.
- `performance_glitch_user` experiences an intentional delay on login. This is expected behaviour, not a defect.
- `locked_out_user` with the correct password displays: *"Epic sadface: Sorry, this user has been locked out."*

**Error handling:**
- Invalid username, invalid password, or both, all display the same generic message: *"Epic sadface: Username and password do not match any user in this service."* The system does not indicate which field is incorrect. This is reasonable from a security standpoint (avoids confirming valid usernames to an attacker), worth noting either way.
- Blank username (regardless of password): *"Epic sadface: Username is required."*
- Blank password only: *"Epic sadface: Password is required."*
- Both fields blank: *"Epic sadface: Username is required."*. This indicates the username field is validated first.
- Clicking the cross on an error message dismisses it correctly.

**Case sensitivity:**
- Case variations of otherwise-valid credentials (e.g. `Standard_User`, `STANDARD_USER`) are rejected. Only exact-case `standard_user` is accepted. Consistent, expected behaviour for credential matching.

**Unauthenticated access:**
- Navigating directly to `/inventory.html` while logged out shows a blank page rather than redirecting to login. Functionally safe (no content is exposed), but a redirect to the login page would be more user-friendly and consistent with the rest of the site.
- Navigating directly to the cart page or any checkout step while logged out correctly redirects to the login page, which inconsistent with the inventory page's blank-page behaviour above.

**Summary:** Validation logic is functionally sound and consistent across the tested paths. The one inconsistency worth flagging is that unauthenticated access is handled differently across pages (blank page vs. redirect). This is worth standardising for a better user experience.

---

## D — Data

*(Some valid/invalid credential handling is also covered under Function above.)*

**Whitespace:**
- Leading or trailing whitespace around otherwise-valid credentials is rejected. It is rejected equally regardless of which side the whitespace is on. Result: *"Epic sadface: Username and password do not match any user in this service."* The system does not trim whitespace automatically.

**Special characters and injection attempts:**
- The username/password fields accept special characters without restriction at the input level (no client-side character filtering).
- Common SQL injection payloads (e.g. `' OR 1=1--`) are rejected identically to any other invalid credential. The same generic error message is shown, with no indication of a different code path being hit.
- A basic XSS probe (`<script>alert(1)</script>`) is also rejected cleanly, with no script execution and no reflection of the raw input anywhere on the page.
- **Caveat on interpretation:** rejection alone doesn't prove the backend is specifically hardened against injection. SauceDemo is a static demo frontend with no real backend database to query against, so there's no live injection surface to actually exploit in the first place. What this confirms is that malicious-looking input is treated the same as any other invalid input, and nothing is reflected unsafely into the DOM.

**Long input:**
- Entering very long strings (1000+ characters) into either field is accepted without truncation. The field allows horizontal scrolling through the entered text, and the page layout is unaffected: no overflow or breakage observed here (distinct from the error-message overflow bug noted under Structure).

**Rate limiting / repeated failed attempts (Pass 1):**
- No change in behaviour observed after 5, 10, or 20 consecutive failed login attempts: no lockout, delay, or CAPTCHA appeared during testing, suggesting there is no rate-limiting in place.
- **Limitation of this finding:** this can't be fully confirmed through black-box UI testing alone. It's possible a rate limit exists at a much higher threshold than tested, or is enforced server-side in a way that wouldn't surface as a visible UI change (e.g. a silent flag on the account, or IP-based throttling that wouldn't trigger from a low volume of manual attempts).

---

## P — Platform

**Platforms tested:**
- Firefox, Chrome, Edge, and Opera on Windows 11 (laptop)
- Chrome on Android (phone)

**Findings:**
- Functionality is consistent across all tested browsers and devices.
- Page scaling is consistent across all platforms.
- Mobile layout adapts appropriately: username and password fields display in a single column rather than two, at 100% zoom.

---

## O — Operations

### Input operations
- Typing username then password: allowed.
- Typing password then username: allowed.
- No field-level validation is performed before submission, errors are only checked on submit.
- Pasting values instead of typing: allowed.
- Selecting a previously-entered value from the browser's autofill/history dropdown: allowed for the username field, but this history does not appear to be available for the password field.
- Using a saved credential pair (browser password manager): allowed.
- Leading/trailing whitespace around otherwise-valid credentials: not accepted, and not automatically trimmed. An error is shown (see Data section for full detail).

### Submission operations
- Clicking the Login button: allowed, redirects to the inventory page on success.
- Pressing Enter while focused in the username field: allowed, submits successfully.
- Pressing Enter while focused in the password field: allowed, submits successfully.
- Submitting with empty fields displays the appropriate error message (see Function section for exact wording per case).

### Navigation operations
- After logging in and navigating back to the login page, input fields are cleared.
- Exception: if the credentials were populated via the browser's saved-credential autofill, they remain visible on returning to the page.
- Logging in, closing the tab, and reopening the site in a new tab shows the login page with empty fields (no persisted session state observed at this level).

---

## T — Time

- Typing speed has no effect on validation. The system does not validate fields as the user types, only on submission.
- Rapidly-typed and pasted input are both handled without issue.
- Arbitrary delays between entering credentials and pressing Login are handled correctly, with no timeout observed during testing.

---

## Next steps

1. Write up the error-message overflow bug as a standalone report (repro steps, screenshot, affected platforms, severity).
2. Accessibility testing (keyboard navigation, screen reader behaviour, colour contrast) scoped separately as Week 8: Accessibility Testing, using WCAG 2.2 and Axe DevTools. Not covered in this exercise; see week 8's notes once complete.