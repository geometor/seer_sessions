```python
import re

"""
Transforms an input sequence of space-separated digits by performing a left 
shift by one position. The digit at the first position (index 0) is discarded, 
and a digit '0' is appended to the end of the sequence to maintain the 
original length.
"""

def transform(input_str: str) -> str:
    """
    Applies a left shift transformation to a sequence of digits.

    Args:
        input_str: A string containing space-separated digits.

    Returns:
        A string containing the transformed sequence of space-separated digits.
    """
    # Split the input string into a list of digit strings
    input_sequence = input_str.split(' ')

    # Perform the left shift by slicing the list from the second element
    # This effectively discards the element at index 0
    shifted_sequence = input_sequence[1:]

    # Append '0' to the end of the shifted sequence
    shifted_sequence.append('0')

    # Join the elements back into a space-separated string
    output_str = ' '.join(shifted_sequence)

    return output_str

```