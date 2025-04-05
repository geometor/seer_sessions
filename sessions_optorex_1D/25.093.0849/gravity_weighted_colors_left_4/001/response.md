```python
"""
Transforms an input string of space-separated digits (0, 1, 2) by sorting the digits numerically in non-decreasing (ascending) order and returning the sorted digits as a space-separated string.
"""

import collections

def transform(input_str: str) -> str:
    """
    Sorts the digits in a space-separated string.

    Args:
        input_str: A string containing digits (0, 1, 2) separated by spaces.

    Returns:
        A string containing the same digits as the input, sorted numerically
        in non-decreasing order and separated by spaces.
    """
    # 1. Split the input string by spaces to get a list of digit characters.
    # Example: "0 1 0 0 2 0 0 0 2 2 0 0" -> ['0', '1', '0', '0', '2', '0', '0', '0', '2', '2', '0', '0']
    digits_str = input_str.split(' ')

    # 2. Convert the list of string digits to integers for numerical sorting (optional but cleaner).
    # Example: ['0', '1', '0', '0', '2', '0', '0', '0', '2', '2', '0', '0'] -> [0, 1, 0, 0, 2, 0, 0, 0, 2, 2, 0, 0]
    # digits_int = [int(d) for d in digits_str] # Alternative if conversion is desired

    # 3. Sort the list of digit characters numerically (Python's sort works directly on strings here).
    # Example: ['0', '1', '0', '0', '2', '0', '0', '0', '2', '2', '0', '0'] -> ['0', '0', '0', '0', '0', '0', '0', '0', '1', '2', '2', '2']
    digits_str.sort() # Sorting strings '0', '1', '2' works numerically

    # 4. Join the sorted list of digit characters back into a single string, using a space as the separator.
    # Example: ['0', '0', '0', '0', '0', '0', '0', '0', '1', '2', '2', '2'] -> "0 0 0 0 0 0 0 0 1 2 2 2"
    output_str = ' '.join(digits_str)

    # 5. Return the resulting string.
    return output_str

```