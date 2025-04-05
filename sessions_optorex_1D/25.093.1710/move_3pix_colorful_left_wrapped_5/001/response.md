```python
import re

def transform(input_str: str) -> str:
    """
    Moves the first three elements of a space-separated sequence of 12 digits to the end of the sequence, preserving the relative order of both the moved elements and the remaining elements.

    Args:
        input_str: A string containing 12 space-separated digits.

    Returns:
        A string containing the transformed sequence of 12 space-separated digits.
    """

    # Parse the input string into a list of digits (as strings)
    # Using regex to handle potential multiple spaces
    digits = re.findall(r'\d', input_str)

    # Ensure the input has exactly 12 digits
    if len(digits) != 12:
        raise ValueError("Input string must contain exactly 12 digits.")

    # Extract the first three elements
    first_three = digits[:3]

    # Extract the remaining elements (from index 3 to the end)
    remaining = digits[3:]

    # Concatenate the remaining elements followed by the first three
    output_digits = remaining + first_three

    # Format the output list back into a space-separated string
    output_str = " ".join(output_digits)

    return output_str

```