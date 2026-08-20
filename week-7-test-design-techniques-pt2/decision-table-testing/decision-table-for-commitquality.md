# Creating a Decision Table for the "Add Product" page on the CommitQuality demo site

## 1. Conditions

These are the input conditions extracted from the CommitQuality “Add Product” page.

### Name
- `< 2 characters`
- `≥ 2 characters`

### Price
- `Empty`
- `> 10 digits`
- `Valid (≤ 10 digits, not empty)`

### Date
- `Empty`
- `Future` *(includes Today — based on actual system behaviour)*
- `Over 100 years ago`
- `Past 100 years`

---

## 2. Full Decision Table (All 24 Combinations)

This table shows every possible combination of Name × Price × Date before collapsing.

| Rule | Name | Price | Date | Outcome |
|------|-------|--------|--------|----------|
| R1 | < 2 chars | Empty | Empty | Invalid |
| R2 | < 2 chars | Empty | Future | Invalid |
| R3 | < 2 chars | Empty | Over 100 years ago | Invalid |
| R4 | < 2 chars | Empty | Past 100 years | Invalid |
| R5 | < 2 chars | > 10 digits | Empty | Invalid |
| R6 | < 2 chars | > 10 digits | Future | Invalid |
| R7 | < 2 chars | > 10 digits | Over 100 years ago | Invalid |
| R8 | < 2 chars | > 10 digits | Past 100 years | Invalid |
| R9 | < 2 chars | Valid | Empty | Invalid |
| R10 | < 2 chars | Valid | Future | Invalid |
| R11 | < 2 chars | Valid | Over 100 years ago | Invalid |
| R12 | < 2 chars | Valid | Past 100 years | Invalid |
| R13 | ≥ 2 chars | Empty | Empty | Invalid |
| R14 | ≥ 2 chars | Empty | Future | Invalid |
| R15 | ≥ 2 chars | Empty | Over 100 years ago | Invalid |
| R16 | ≥ 2 chars | Empty | Past 100 years | Invalid |
| R17 | ≥ 2 chars | > 10 digits | Empty | Invalid |
| R18 | ≥ 2 chars | > 10 digits | Future | Invalid |
| R19 | ≥ 2 chars | > 10 digits | Over 100 years ago | Invalid |
| R20 | ≥ 2 chars | > 10 digits | Past 100 years | Invalid |
| R21 | ≥ 2 chars | Valid | Empty | Invalid |
| R22 | ≥ 2 chars | Valid | Future | Invalid |
| R23 | ≥ 2 chars | Valid | Over 100 years ago | Invalid |
| R24 | ≥ 2 chars | Valid | Past 100 years | Valid |

---

## **3. Collapsed Decision Table (Final Rules)**

This is the simplified version used for test design.  
“Don’t care” means the value does not affect the outcome.

| Rule | Name | Price | Date | Outcome |
|------|-------|--------|--------|----------|
| R1 | < 2 characters | don’t care | don’t care | Invalid |
| R2 | ≥ 2 characters | Empty | don’t care | Invalid |
| R3 | ≥ 2 characters | > 10 digits | don’t care | Invalid |
| R4 | ≥ 2 characters | Valid (≤ 10 digits) | Empty | Invalid |
| R5 | ≥ 2 characters | Valid (≤ 10 digits) | Future *(includes Today)* | Invalid |
| R6 | ≥ 2 characters | Valid (≤ 10 digits) | Over 100 years ago | Invalid |
| R7 | ≥ 2 characters | Valid (≤ 10 digits) | Past 100 years | Valid |

This table represents all meaningful behaviours of the form.

---

## 4. Converting Decision Table Rules Into Test Cases

See add-product-tests.py
