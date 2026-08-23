# Bug Report: Error Message Box Overflows When Message Exceeds Two Lines

## Summary

On the SauceDemo login page, the red error-message container has a fixed
height that only accommodates two lines of text. When a triggered error
message wraps onto a third line, the container does not grow to fit it.
Instead, the third line is clipped/hidden behind the "Login" button below, making part of the message unreadable. 

Confirmed via DevTools inspection: the container is set to a fixed `height: 45px` rather than `min-height`
(see Root Cause section below).

## Environment
- **Site:** https://www.saucedemo.com/
- **Zoom level:** Confirmed present at all tested zoom levels (not
  specific to any one zoom setting).
- **Platforms confirmed:**
  - Desktop (Windows 11): see `error-overflow-screenshot.png`
  - Chrome on Android (mobile): see `error-overflow-screenshot-mobile.jpg`

  Confirmed on both the two-column desktop layout and the single-column
  mobile layout, so this is not a platform- or layout-specific rendering
  quirk, the fixed-height container issue is consistent across both.

## Steps to Reproduce
1. Go to https://www.saucedemo.com/
2. Enter any credentials that trigger the three-line error message,
   e.g. a username/password combination that doesn't match any valid
   user (produces: *"Epic sadface: Username and password do not match
   any user in this service"*).
3. Click "Login".

## Expected Result
The red error-message container expands vertically to fit the full
message, regardless of how many lines it wraps to. The message should be
fully readable, and should not overlap the "Login" button.

## Actual Result
The error-message container stays a fixed height that only fits two
lines. When the message wraps to a third line, that line is clipped: 
visually cut off by the top edge of the "Login" button, which sits
directly below the error box and does not shift down to make room.

See screenshots: the third line ("this service") is only partially
visible in both, overlapped by the "Login" button. Identical behaviour
on desktop and mobile.

## Severity / Impact
**Low–Medium.** Cosmetic rather than functional. The user can still
dismiss the message (the close button remains visible and clickable) and
retry the login, so this doesn't block the workflow. However, part of the
actual error text is unreadable, which matters for a message whose whole
purpose is to tell the user what went wrong. Confirmed reproducible on
both desktop and mobile, so this isn't an edge case limited to one
platform. Worth fixing for polish and usability, not urgent from a
functional standpoint.

## Root Cause (confirmed via browser DevTools)

Inspected via Chrome DevTools → Computed styles for `.error-message-container`:

```css
.error-message-container {
  height: 45px;       /* fixed, not min-height -- cannot grow with content */
  display: flex;
  align-items: center; /* vertically centers content within the fixed 45px box */
  justify-content: center;
  margin-bottom: 5px;
  margin-top: -10px;
  padding-left: 10px;
  padding-right: 10px;
  position: relative;
}
```

`height: 45px` is a fixed value rather than `min-height`, so the
container cannot expand to fit a third line of wrapped text, it's
capped regardless of content length. Combined with `display: flex` and
`align-items: center`, the text is vertically centered *within* that
fixed 45px box, which is why the overflow specifically pushes the third
line downward (rather than, say, clipping from the top). The flex
centering shifts the whole block down as content grows, moving the
excess below the box's boundary and directly behind the Login button.

## Suggested Fix

Change `height: 45px` to `min-height: 45px` (or remove the fixed height
and let the flex container size to its content). This would allow the
box to grow for longer messages while keeping the current fixed height
as the minimum for short ones.