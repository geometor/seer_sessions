```python
"""
Transforms an input string of space-separated digits ('0', '1', '2') by sorting the digits numerically (lexicographically works here) in non-decreasing order and returning the sorted digits as a space-separated string.
"""

import typing

def transform(input_str: str) -> str:
    """
    Sorts the digits in a space-separated input string.

    Args:
        input_str: A string containing digits ('0', '1', '2') separated by spaces.

    Returns:
        A string containing the same digits as the input, sorted numerically
        (which is equivalent to lexicographically for '0','1','2') in
        non-decreasing order and separated by spaces.
    """
    # 1. Split the input string into a list of individual digit strings
    #    using the space character as the delimiter.
    #    Example: "0 1 0 0 2 0 0 0 2 2 0 0" -> ['0', '1', '0', '0', '2', '0', '0', '0', '2', '2', '0', '0']
    #    Filter out any empty strings that might result from multiple spaces.
    digit_strings = [s for s in input_str.split(' ') if s]

    # 2. Sort this list of digit strings. Standard lexicographical sort works
    #    correctly for '0', '1', '2' to achieve non-decreasing numerical order.
    #    Example: ['0', '1', '0', '0', '2', '0', '0', '0', '2', '2', '0', '0'] -> ['0', '0', '0', '0', '0', '0', '0', '0', '1', '2', '2', '2']
    digit_strings.sort()

    # 3. Join the elements of the sorted list back into a single string,
    #    using a single space character as the separator between each digit string.
    #    Example: ['0', '0', '0', '0', '0', '0', '0', '0', '1', '2', '2', '2'] -> "0 0 0 0 0 0 0 0 1 2 2 2"
    output_str = ' '.join(digit_strings)

    # 4. Return the resulting string.
    return output_str

```