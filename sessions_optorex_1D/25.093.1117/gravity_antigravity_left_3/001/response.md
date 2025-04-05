```python
"""
Transforms an input sequence of digits (0, 1, 2) by reordering them.
The output sequence contains all the '2's from the input, followed by all the '0's,
and finally all the '1's. The counts of each digit remain the same.
"""

import collections

def transform(input_str: str) -> str:
    """
    Reorders the digits in the input string according to the rule: 2s, then 0s, then 1s.

    Args:
        input_str: A string containing space-separated digits (0, 1, 2).

    Returns:
        A string containing the reordered space-separated digits.
    """
    # Parse the input string into a list of integers
    input_digits = [int(d) for d in input_str.split()]

    # Count the occurrences of each digit (0, 1, 2)
    counts = collections.Counter(input_digits)
    count_2 = counts.get(2, 0)
    count_0 = counts.get(0, 0)
    count_1 = counts.get(1, 0)

    # Construct the output list based on the counts and the desired order (2, 0, 1)
    output_digits = []
    output_digits.extend([2] * count_2) # Append '2's
    output_digits.extend([0] * count_0) # Append '0's
    output_digits.extend([1] * count_1) # Append '1's

    # Convert the output list back to a space-separated string
    output_str = " ".join(map(str, output_digits))

    return output_str

```