# State Transition Table — ParaBank Loan Request

Legend for the new "Testable" column:
- **Direct** — can be triggered by a real user action (click/submit) and verified with Playwright.
- **Structural** — there is no UI affordance to trigger this event at all (e.g. no "deny after approve" button exists). These rows document that the transition is impossible by design, not something a test can directly force. Verifying these means proving the *absence* of a control/path, which is a weaker and different kind of test than "click X, assert Y" — see notes in test_loan_state_transitions.py.

| Current State             | Event / Input                         | Next State              | Valid? | Testable   | Notes / Expected Behaviour                          |
|---------------------------|----------------------------------------|--------------------------|--------|------------|------------------------------------------------------|
| Loan application form     | User submits loan request              | Loan Request Processed   | ✔      | Direct     | System receives loan amount + downpayment            |
| Loan application form     | System approves                        | Loan application form    | ❌     | Structural | Cannot approve before evaluation                     |
| Loan application form     | System denies                          | Loan application form    | ❌     | Structural | Cannot deny before evaluation                        |
| Loan application form     | System creates loan account            | Loan application form    | ❌     | Structural | Account creation only happens after approval         |
|                           |                                        |                          |        |            |                                                      |
| Loan Request Processed    | System evaluates (valid request)       | Approved                 | ✔      | Direct     | Status: Approved displayed                           |
| Loan Request Processed    | System evaluates (invalid request)     | Denied                   | ✔      | Direct     | Status: Denied displayed                             |
| Loan Request Processed    | User submits again                     | Loan Request Processed   | ❌     | Direct     | Duplicate submission not allowed — this is the one invalid-transition row that's straightforward to automate directly |
| Loan Request Processed    | System creates loan account            | Loan Request Processed   | ❌     | Structural | Account creation only happens after approval         |
|                           |                                        |                          |        |            |                                                      |
| Approved                  | System creates loan account            | Loan Account Created     | ✔      | Direct     | New loan account appears in Accounts Overview        |
| Approved                  | System denies                          | Approved                 | ❌     | Structural | Cannot deny after approval                           |
| Approved                  | System evaluates again                 | Approved                 | ❌     | Structural | No re-evaluation after approval                      |
|                           |                                        |                          |        |            |                                                      |
| Denied                    | Workflow ends                          | Terminal State            | ✔      | Direct     | ADDED — diagram draws Denied → Terminal State directly; no loan account is created on this path |
| Denied                    | System approves                        | Denied                    | ❌     | Structural | Cannot approve after denial                          |
| Denied                    | System creates loan account            | Denied                    | ❌     | Structural | No account created after denial                      |
| Denied                    | System evaluates again                 | Denied                    | ❌     | Structural | No re-evaluation after denial                        |
|                           |                                        |                          |        |            |                                                      |
| Loan Account Created      | Workflow ends                          | Terminal State            | ✔      | Direct     | Final state                                          |
| Loan Account Created      | System denies                          | Loan Account Created      | ❌     | Structural | Cannot deny after account creation                   |
| Loan Account Created      | System evaluates again                 | Loan Account Created      | ❌     | Structural | No re-evaluation after account creation              |
|                           |                                        |                          |        |            |                                                      |
| Terminal State            | Any event                              | Terminal State            | ❌     | Structural | Terminal states have no outgoing transitions         |

## Known deviation from the diagram (observed via testing)

The system sometimes crashes with an "Error!" page instead of reaching the
"Denied" state after an invalid request is submitted. This is not represented
anywhere in the diagram or the table above, since the diagram only models
intended behaviour. Tracked as its own test
(`test_denial_path_does_not_crash`) rather than folded into another test's
assertions, so this finding is visible as its own result rather than hidden
inside a different test's failure message.