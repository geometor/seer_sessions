```python
import collections

"""
Take the input sequence of 12 space-separated digits. Select the last 3 digits and the first 9 digits. Construct the output sequence by placing the selected last 3 digits at the beginning, followed by the selected first 9 digits, ensuring they are space-separated.
"""

def transform(input_str: str) -> str:
    """
    Performs a right rotation of a sequence of 12 space-separated digits by 3 positions.

    Args:
        input_str: A string containing 12 space-separated single digits.

    Returns:
        A string representing the rotated sequence, with digits separated by spaces.
    """
    # Split the input string into a list of individual digit strings
    digits = input_str.split(' ')

    # Check if the input has the expected length (12 digits)
    if len(digits) != 12:
        # Handle unexpected input length if necessary, e.g., raise an error or return input
        # For this specific task based on examples, we assume 12 digits
        print(f"Warning: Input string '{input_str}' does not contain exactly 12 digits.")
        # Decide on behavior: return input, raise error, or attempt processing?
        # Let's proceed assuming the core logic applies, but this might need refinement.
        # If strict length is required:
        # raise ValueError("Input must contain exactly 12 space-separated digits.")

    # Identify the last 3 digits (segment A)
    # Slicing works even if the list length is less than 12, but the logic assumes 12.
    segment_a = digits[-3:]

    # Identify the first 9 digits (segment B)
    segment_b = digits[:-3] # Equivalent to digits[0:9] for a list of length 12

    # Concatenate segment A followed by segment B to form the new sequence
    output_digits = segment_a + segment_b

    # Join the digits in the new sequence back into a space-separated string
    output_str = ' '.join(output_digits)

    return output_str

```