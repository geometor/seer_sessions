```python
import math
# No other specific libraries like numpy are needed for this list manipulation task.

"""
Transforms an input string of space-separated single-digit integers by moving all 
zero digits to the beginning of the sequence while preserving the relative order 
of the non-zero digits. The output is also a space-separated string.
"""

def parse_input_string(input_str: str) -> list[int]:
    """Converts a space-separated string of digits into a list of integers."""
    # Handle potential empty input string gracefully.
    if not input_str.strip():
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
    # Iterate through the input sequence element by element
    for digit in sequence:
        # Check if the element is the integer 0
        if digit == 0:
            zeros_list.append(digit)
        else:
            # If not 0, add it to the non_zeros list, maintaining order
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
    # 1. Parse Input: Convert the input string into a list of integers.
    #    Example: "9 0 7" -> [9, 0, 7]
    input_sequence = parse_input_string(input_str)

    # 2. Partition Digits: Separate the list into zeros and non-zeros,
    #    preserving the relative order of non-zeros.
    #    Example: [9, 0, 7] -> ([0], [9, 7])
    zeros_list, non_zeros_list = partition_digits(input_sequence)

    # 3. Construct Output Sequence: Concatenate the lists (zeros first).
    #    Example: [0] + [9, 7] -> [0, 9, 7]
    output_sequence = zeros_list + non_zeros_list

    # 4. Format Output: Convert the resulting list back to a space-separated string.
    #    Example: [0, 9, 7] -> "0 9 7"
    output_str = format_output_list(output_sequence)

    # 5. Return the result.
    return output_str
```