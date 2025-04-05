```python
"""
Sorts a space-separated string of integers (0, 1, 2) in descending order.
"""

import collections

def transform(input_str: str) -> str:
    """
    Transforms the input string by sorting its integer elements in descending order.

    Args:
        input_str: A string containing space-separated integers (0, 1, or 2).

    Returns:
        A string containing the sorted integers, space-separated.
    """
    # Convert the input string into a list of integers
    input_list = [int(x) for x in input_str.split()]

    # Sort the list of integers in descending order
    # Python's sort/sorted uses ascending by default, so use reverse=True
    sorted_list = sorted(input_list, reverse=True)

    # Convert the sorted list back into a space-separated string
    output_str = " ".join(map(str, sorted_list))

    return output_str

```