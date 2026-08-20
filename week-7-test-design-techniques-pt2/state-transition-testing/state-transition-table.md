| **Current State** | **Event / Input** | **Next State** | **Valid?** |
| --- | --- | --- | --- |
| **Loan Application Form (Start)** | User submits loan amount + down payment | **Submitted (Pending Evaluation)** | ✔️ |
| **Loan Application Form (Start)** | System attempts to approve | Loan Application Form (Start) | ❌ |
| **Loan Application Form (Start)** | System attempts to deny | Loan Application Form (Start) | ❌ |
| **Loan Application Form (Start)** | System attempts to create loan account | Loan Application Form (Start) | ❌ |
| **Submitted (Pending Evaluation)** | System evaluates loan request (valid) | **Approved** | ✔️ |
| **Submitted (Pending Evaluation)** | System evaluates loan request (invalid) | **Denied** | ✔️ |
| **Submitted (Pending Evaluation)** | System attempts to create loan account | Submitted (Pending Evaluation) | ❌ |
| **Submitted (Pending Evaluation)** | System produces conflicting evaluation (approve + deny) | Submitted (Pending Evaluation) | ❌ |
| **Submitted (Pending Evaluation)** | System re-evaluates loan request | Submitted (Pending Evaluation) | ❌ |
| **Approved** | System creates loan account | **Loan Account Created** | ✔️ |
| **Approved** | System attempts to deny | Approved | ❌ |
| **Approved** | System re-evaluates loan request | Approved | ❌ |
| **Approved** | System attempts to return to Submitted | Approved | ❌ |
| **Denied** | Workflow ends | **Terminal State** | ✔️ |
| **Denied** | System attempts to approve | Denied | ❌ |
| **Denied** | System attempts to create loan account | Denied | ❌ |
| **Loan Account Created** | Workflow ends | **Terminal State** | ✔️ |
| **Loan Account Created** | System attempts to deny | Loan Account Created | ❌ |
| **Loan Account Created** | System re-evaluates loan request | Loan Account Created | ❌ |
| **Terminal State** | Any event | Terminal State | ❌ |