```python
import math
# No other specific libraries like numpy seem necessary for this string/list manipulation task.

"""
Transforms an input string of space-separated single-digit integers by moving all 
zero digits to the beginning of the sequence while preserving the relative order 
of the non-zero digits. The output is also a space-separated string.
"""

def parse_input_string(input_str: str) -> list[int]:
    """Converts a space-separated string of digits into a list of integers."""
    # Handle potential empty input string gracefully, though examples don't show this.
    if not input_str:
        return []
    return [int(digit) for digit in input_str.split()]

def format_output_list(output_list: list[int]) -> str:
    """Converts a list of integers back into a space-separated string."""
    return ' '.join(map(str, output_list))

def partition_digits(sequence: list[int]) -> tuple[list[int], list[int]]:
    """
    Separates a sequence into zero and non-zero elements, preserving
    the relative order of non-zero elements.

    Args:
        sequence: A list of integers.

    Returns:
        A tuple containing two lists: (list_of_zeros, list_of_non_zeros).
    """
    zeros_list = []
    non_zeros_list = []
    # Iterate through the input sequence
    for digit in sequence:
        # Check if the element is zero
        if digit == 0:
            zeros_list.append(digit)
        else:
            # If not zero, add to the non_zeros list
            non_zeros_list.append(digit)
    return zeros_list, non_zeros_list

def transform(input_str: str) -> str:
    """
    Applies the transformation rule to the input string.

    Args:
        input_str: A string containing space-separated single-digit integers.

    Returns:
        A string containing the transformed sequence of space-separated digits.
    """

    # 1. & 2. Parse Input: Convert the input string into a list of integers.
    input_sequence = parse_input_string(input_str)

    # 3. Partition Digits: Separate the sequence into zeros and non-zeros.
    zeros_list, non_zeros_list = partition_digits(input_sequence)

    # 4. Construct Output Sequence: Concatenate the lists (zeros first).
    output_sequence = zeros_list + non_zeros_list

    # 5. Format Output: Convert the resulting list back to a space-separated string.
    output_str = format_output_list(output_sequence)

    # 6. Return Output
    return output_str
```