# State Transition Table — ParaBank Loan Request

Legend for the "Testable" column:
- **Direct** — can be triggered by a real user action (click/submit) and verified with Playwright.
- **Structural** — there is no UI affordance to trigger this event at all (for example, there is no “deny after approve” button). These rows document that the transition is impossible by design, not something a test can directly force. Verifying these means proving the absence of a control or path, which is a weaker and different kind of test than “click X, assert Y”. See the notes in the state transition test file.

| Current State | Event / Input | Next State | Valid? | Testable | Notes / Expected Behaviour |
|---|---|---|---|---|---|
| Loan application form | User submits loan request | Loan Request Processed | ✔ | Direct | System receives loan amount + downpayment |
| Loan application form | System approves | Loan application form | ❌ | Structural | Cannot approve before evaluation |
| Loan application form | System denies | Loan application form | ❌ | Structural | Cannot deny before evaluation |
| Loan application form | System creates loan account | Loan application form | ❌ | Structural | Account creation only happens after approval |
|  |  |  |  |  |  |
| Loan Request Processed | System evaluates (valid request) | Approved | ✔ | Direct | Status: Approved displayed |
| Loan Request Processed | System evaluates (invalid request) | Denied | ✔ | Direct | Status: Denied displayed |
| Loan Request Processed | User submits again | Loan Request Processed | ❌ | Structural | Reclassified from Direct. Approved/Denied renders on its own results page rather than back on the form. There is no session state or disabled control preventing a second submission; the user simply navigates back to a fresh form and applies again. That is a new independent loan request, not a duplicate-submission scenario. No real UI path exists to test a “duplicate rejected” case. |
| Loan Request Processed | System creates loan account | Loan Request Processed | ❌ | Structural | Account creation only happens after approval |
|  |  |  |  |  |  |
| Approved | System creates loan account | Loan Account Created | ✔ | Direct | New loan account appears in Accounts Overview |
| Approved | System denies | Approved | ❌ | Structural | Cannot deny after approval |
| Approved | System evaluates again | Approved | ❌ | Structural | No re-evaluation after approval |
|  |  |  |  |  |  |
| Denied | Workflow ends | Terminal State | ✔ | Direct | Added: the diagram implies Denied -> Terminal State directly; no loan account is created on this path |
| Denied | System approves | Denied | ❌ | Structural | Cannot approve after denial |
| Denied | System creates loan account | Denied | ❌ | Structural | No account created after denial |
| Denied | System evaluates again | Denied | ❌ | Structural | No re-evaluation after denial |
|  |  |  |  |  |  |
| Loan Account Created | Workflow ends | Terminal State | ✔ | Direct | Final state |
| Loan Account Created | System denies | Loan Account Created | ❌ | Structural | Cannot deny after account creation |
| Loan Account Created | System evaluates again | Loan Account Created | ❌ | Structural | No re-evaluation after account creation |
|  |  |  |  |  |  |
| Terminal State | Any event | Terminal State | ❌ | Structural | Terminal states have no outgoing transitions |

## Known deviation from the diagram (observed during testing)

The system sometimes crashes with an “Error!” page instead of reaching the “Denied” state after an invalid request is submitted. This is not represented anywhere in the diagram or the table above, because the diagram models intended behaviour only. It is tracked as its own test rather than folded into another test’s assertions so the finding remains visible as its own result rather than being hidden inside a different failure message.