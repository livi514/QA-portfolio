# State Transition Testing

## What is State Transition Testing?

State transition testing is a black-box test design technique that checks how a system behaves as it moves between the states it can occupy. The tester identifies every state the system can be in, every event that can trigger a transition, every valid transition between states, and every action the system performs as the transition occurs. Test cases are derived from this model to cover both transitions that should be accepted and transitions that should be rejected.

This technique is suitable for systems where behaviour depends on previous conditions or state, not just on the current input alone. A system that always returns the same result for the same input does not need state transition testing. A system where the same input produces different results depending on the system's current state does.

Typical examples include:
- Loan approval workflows
- Shopping cart or checkout flows
- Login and account access journeys
- Form validation with multi-step logic
- Systems with approve/deny, success/failure, or locked/unlocked states

## The four components of a state transition model

Every state transition model is built from the same core components. Naming them clearly matters because they map directly to the structure of test cases.

### 1. State
A state is the condition the system is currently in.

Examples from the ParaBank loan flow:
- Loan application form
- Loan request processed
- Approved
- Denied
- Loan account created
- Terminal state

### 2. Event
An event is an input or trigger that can cause a move from one state to another.

Examples:
- User submits a loan request
- System evaluates the request
- User selects an account to fund the loan

### 3. Transition
A transition is a move from one state to another, triggered by an event.

Examples:
- Loan application form -> Loan Request Processed when the user submits valid data
- Loan Request Processed -> Approved when the system evaluates the request and approves it
- Loan Request Processed -> Denied when the system evaluates the request and rejects it

### 4. Action
An action is something the system does during a transition.

Examples:
- When the loan is approved, the system creates a new loan account
- When the request is denied, the system does not create an account and the journey ends in a terminal state

Each system includes a start state and one or more end states. The start state is where the journey begins, and the end states are where journeys legitimately stop.

## State Transition Diagrams

A state transition diagram is a visual map of the system's states and the paths between them. States are usually represented as labelled shapes, and transitions are shown as arrows labelled with the event that triggers the move and any action that happens along the way.

For the ParaBank loan request flow, the diagram shows the journey from the application form through processing, outcome, and final state. The key point is that the system behaves differently depending on whether the request is approved or denied.

This diagram is useful when the team needs shared understanding of the lifecycle and wants a quick way to review the overall flow without reading a lot of test code.

### Strengths of diagrams
- Good for communicating the journey visually
- Useful for stakeholder review
- Helps highlight decisions and state boundaries

### Limitations of diagrams
- They can become overcrowded as the system grows
- They are harder to use for exhaustive transition checking than tables

## State Transition Tables

A state transition table is the more formal test design representation. In the classic format:
- Rows = states
- Columns = events
- Cells = next state or expected result

This makes it easy to see which transitions are valid, invalid, or undefined.

For the ParaBank example, the table in [state-transition-table.md](state-transition-table.md) is fairly close to this idea, but it also includes extra notes such as whether a transition is direct or structural. That is useful in practice because some transitions are not directly testable via a UI action.

### Important point about table format
My earlier table had multiple rows per state, which is not the strictest traditional format. That is still valid if the table is being used as a working design artifact, but the more textbook structure is:
- One row per state
- One column per event
- One cell per state-event combination

The reason this matters is that a state transition table should make all possible transitions visible. If a transition is impossible or not directly testable, the table should flag that clearly rather than pretending it exists.

### Why invalid cells matter
The invalid or undefined cells are just as important as the valid ones. Many defects appear when a system allows a transition that should be blocked or when it crashes instead of moving to the correct outcome.

In the ParaBank flow, a good example is the known issue where an invalid request can lead to an "Error!" page instead of a clean denial path. That is exactly the kind of behaviour a state transition table makes visible and testable.

## Practical example from the ParaBank flow

The table in [state-transition-table.md](state-transition-table.md) includes examples such as:

| Current State | Event | Next State | Valid? | Testable |
|---|---|---|---|---|
| Loan application form | User submits loan request | Loan Request Processed | Yes | Direct |
| Loan Request Processed | System evaluates valid request | Approved | Yes | Direct |
| Loan Request Processed | System evaluates invalid request | Denied | Yes | Direct |
| Approved | System creates loan account | Loan Account Created | Yes | Direct |
| Denied | Workflow ends | Terminal State | Yes | Direct |
| Approved | System denies | Approved (no change) | No | Structural — no UI control exists to deny an already-approved request; the absence of this control is itself the thing being verified, not a UI action to script |

This is useful because it separates:
- Direct transitions that can be triggered through the page
- Structural transitions that the UI does not allow and therefore should not be treated as normal manual test actions

This distinction is reflected in the Playwright tests in [test_state_transitions.py](state-transition-testing/test_state_transitions.py):
- Direct transitions are exercised through real UI steps
- Structural transitions are not forced via fake UI actions because they are not available in the product

## Practical example from the automated tests

The automated tests in [test_state_transitions.py](state-transition-testing/test_state_transitions.py) are a practical example of how state transition testing works in real life.

### Example 1: Loan form to processed state
This test covers the transition:
- Loan application form -> Loan Request Processed

The test calls the shared helper that fills in the form and submits the request. It then asserts that the user reaches the processed state rather than crashing or staying on the form.

This maps directly to the state transition table row:
- Current state: Loan application form
- Event: user submits loan request
- Next state: Loan Request Processed

### Example 2: Outcome branch
The test called `test_loan_outcome_matches_account_state` checks the branch after processing:
- If the loan is approved, exactly one new account should be created
- If the loan is denied, no new account should be created

This is a strong state transition example because the same "processed" state can lead to different valid outcomes depending on the underlying rules or system response.

### Example 3: Defect discovery through state transitions
The test `test_denial_path_does_not_crash` is valuable because it captures a real defect discovered during testing. Instead of moving to a clean denial path, the system sometimes shows an "Error!" page. This is a state transition problem because the system does not reach the expected state.

This shows that state transition testing is not only about happy paths; it is also about detecting unexpected transitions and invalid states.

## When to build both a diagram and a table

The best approach is usually to build both.

### Use a diagram when:
- You need a quick visual explanation of the lifecycle
- You want to communicate the flow to non-technical people
- You need to review the journey before turning it into test cases

### Use a table when:
- You need exhaustive transition coverage
- You want to check valid and invalid state-event combinations
- You need to convert transitions directly into automated tests

A good workflow is:
1. Draw the state transition diagram
2. Derive the state transition table
3. Convert the valid rows into test cases
4. Include invalid and undefined transitions as negative tests

## State Transition Testing Checklist

When creating a state model, ask:
- What states can the system be in?
- What events move it between states?
- What action happens during each transition?
- Which transitions are valid and invalid?
- Which states are terminal?
- Which transitions are directly testable in the UI?
- Which transitions are only structural and should be documented rather than forced manually?

## Summary

State transition testing is a strong technique for systems whose behaviour depends on the current state of the system, not just on the input being used. It is especially useful where the same action can lead to different outcomes depending on the state the system is in.

In my practical work, the ParaBank loan application flow is a clear example of this. The state model shows how the process moves from form input to processed request, then to either approval or denial, and finally to a terminal state or account creation. The table in [state-transition-table.md](state-transition-table.md) and the tests in [test_state_transitions.py](state-transition-testing/test_state_transitions.py) show how those transitions can be used to design, review, and automate coverage.

The key takeaway is this: state transition testing is not only about happy paths. It is about proving that the system behaves correctly as it moves through every meaningful state while also identifying transitions that should not exist, should be blocked, or currently fail unexpectedly.