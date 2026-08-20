| Current State             | Event / Input                         | Next State              | Valid? | Notes / Expected Behaviour                          |
|---------------------------|----------------------------------------|--------------------------|--------|------------------------------------------------------|
| Loan application form     | User submits loan request              | Loan Request Processed   | ✔      | System receives loan amount + downpayment            |
| Loan application form     | System approves                        | Loan application form    | ❌     | Cannot approve before evaluation                     |
| Loan application form     | System denies                          | Loan application form    | ❌     | Cannot deny before evaluation                        |
| Loan application form     | System creates loan account            | Loan application form    | ❌     | Account creation only happens after approval         |
|                           |                                        |                          |        |                                                      |
| Loan Request Processed    | System evaluates (valid request)       | Approved                 | ✔      | Status: Approved displayed                           |
| Loan Request Processed    | System evaluates (invalid request)     | Denied                   | ✔      | Status: Denied displayed                             |
| Loan Request Processed    | User submits again                     | Loan Request Processed   | ❌     | Duplicate submission not allowed                     |
| Loan Request Processed    | System creates loan account            | Loan Request Processed   | ❌     | Account creation only happens after approval         |
|                           |                                        |                          |        |                                                      |
| Approved                  | System creates loan account            | Loan Account Created     | ✔      | New loan account appears in Accounts Overview        |
| Approved                  | System denies                          | Approved                 | ❌     | Cannot deny after approval                           |
| Approved                  | System evaluates again                 | Approved                 | ❌     | No re-evaluation after approval                      |
|                           |                                        |                          |        |                                                      |
| Denied                    | System approves                        | Denied                   | ❌     | Cannot approve after denial                          |
| Denied                    | System creates loan account            | Denied                   | ❌     | No account created after denial                      |
| Denied                    | System evaluates again                 | Denied                   | ❌     | No re-evaluation after denial                        |
|                           |                                        |                          |        |                                                      |
| Loan Account Created      | Workflow ends                          | Terminal State           | ✔      | Final state                                          |
| Loan Account Created      | System denies                          | Loan Account Created     | ❌     | Cannot deny after account creation                   |
| Loan Account Created      | System evaluates again                 | Loan Account Created     | ❌     | No re-evaluation after account creation              |
|                           |                                        |                          |        |                                                      |
| Terminal State            | Any event                              | Terminal State           | ❌     | Terminal states have no outgoing transitions         |
