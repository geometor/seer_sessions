```python
"""
Transforms an input list of 12 elements by moving the first three elements to the end of the list, preserving the relative order of both the moved elements and the remaining elements.
"""

from typing import List, Any # Use Any to be flexible about element types, though they appear to be numbers

def transform(input_list: List[Any]) -> List[Any]:
    """
    Moves the first three elements of a list of 12 elements to the end.

    Args:
        input_list: A list containing exactly 12 elements.

    Returns:
        A new list with the first three elements moved to the end.

    Raises:
        ValueError: If the input is not a list or does not contain exactly 12 elements.
    """

    # Validate input type
    if not isinstance(input_list, list):
        raise ValueError(f"Input must be a list. Got type: {type(input_list)}")

    # Validate input length
    expected_length = 12
    if len(input_list) != expected_length:
        raise ValueError(f"Input list must contain exactly {expected_length} elements. Found {len(input_list)}.")

    # Extract the first three elements (indices 0, 1, 2)
    first_three_elements = input_list[:3]

    # Extract the remaining elements (from index 3 to the end)
    remaining_elements = input_list[3:]

    # Concatenate the remaining elements followed by the first three
    output_list = remaining_elements + first_three_elements

    # Return the transformed list
    return output_list
```