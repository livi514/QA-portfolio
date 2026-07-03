# Parametrized tests

Parametrized tests aren't exclusive to Playwright - however, this is a concept I happened to stumble across during my journey of learning Playwright, hence why I wanted to make some notes about it.
In fact, this is a pure pytest feature. It works for any test, Playwright or not.

The core problem parametrize solves: you often want to run the exact same logic with different inputs. Without it, you'd copy-paste the test body multiple times and just change a few values. Parametrize avoids this repetition.

Simple, non-Playwright example:

import pytest

def add_one(n):
    return n + 1

@pytest.mark.parametrize("input_value, expected", [
    (1, 2),
    (5, 6),
    (10, 11),
])
def test_add_one(input_value, expected):
    assert add_one(input_value) == expected

The big advantage: if you needed to add another test case for the same feature, you add one line to the list, not a whole new function.
And if the logic itself has a bug, you fix it in one place instead of four.

The syntax breakdown:
- @pytest.mark.parametrize(...) is a decorator. It sits directly above the function and modifies how pytest runs it.
- The first argument is a string of parameter names, comma-separated: "input_value, expected".
- The second argument is a list of tuples, where each tuple supplies values for those parameter names, in order.
- Those parameter names then become arguments to your test function, alongside page if you need it.

If one of the three add_one cases failed, what would the output look like?
- Each case is reported separately, even though there's only one function.
- So, if (5,6) was wrong but the other two were fine, your output would show something like:
test_add_one[1-2] PASSED
test_add_one[5-6] FAILED
test_add_one[10-11] PASSED
- pytest tells you exactly which input broke, not just "something in this test failed".