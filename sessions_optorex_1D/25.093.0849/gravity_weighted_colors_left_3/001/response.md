```python
import numpy as np

"""
Takes an input string containing space-separated integers, parses these integers,
sorts them in ascending order, and returns the sorted integers as a space-separated string.
"""

def transform(input_str: str) -> str:
    """
    Sorts a sequence of numbers given as a space-separated string.

    Args:
        input_str: A string containing space-separated integers (e.g., "2 2 0 1 0").

    Returns:
        A string containing the sorted integers, space-separated (e.g., "0 0 1 2 2").
    """
    # Parse the input string into a list of integers
    # Example: "2 2 0 1 0" -> [2, 2, 0, 1, 0]
    numbers = [int(x) for x in input_str.split()]

    # Sort the list of integers in ascending order
    # Example: [2, 2, 0, 1, 0] -> [0, 0, 1, 2, 2]
    sorted_numbers = sorted(numbers)

    # Convert the sorted list of integers back into a space-separated string
    # Example: [0, 0, 1, 2, 2] -> "0 0 1 2 2"
    output_str = " ".join(map(str, sorted_numbers))

    # Return the sorted string
    return output_str

```