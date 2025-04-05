import math

"""
Transforms an input sequence of space-separated integers based on a repeating pattern. 
The input sequence consists of an initial non-zero sequence (prefix) followed by one 
or more zeros. The non-zero prefix is assumed to be formed by repeating a smaller, 
non-empty block of integers (B) twice (B B). The transformation identifies block B 
and repeats it to fill the entire length of the original input sequence, replacing 
the zeros and truncating if necessary.
"""

# Helper function to parse the input string into a list of integers
def parse_input_sequence(input_str: str) -> list[int]:
    """Converts a space-separated string of digits into a list of integers."""
    if not input_str:
        return []
    # Handle potential multiple spaces between numbers and filter empty strings
    return [int(x) for x in input_str.split() if x]

# Helper function to format the output list into a space-separated string
def format_output_sequence(output_list: list[int]) -> str:
    """Converts a list of integers into a space-separated string."""
    return " ".join(map(str, output_list))

# Helper function to find the index of the first zero
def find_first_zero_index(int_list: list[int]) -> int:
    """Finds the index of the first zero in the list. Returns list length if no zero is found."""
    try:
        return int_list.index(0)
    except ValueError:
        # No zeros found, the 'prefix' effectively spans the entire list length
        return len(int_list)

def transform(input_str: str) -> str:
    """
    Applies the transformation rule: identify the repeating block (B) from the
    non-zero prefix (BB) and repeat B to fill the sequence length.
    """
    # 1. Parse Input: Convert the input string to a list of integers.
    input_list = parse_input_sequence(input_str)
    
    # 2. Get Total Length: Determine the total number of elements (N).
    total_length = len(input_list)

    # Handle edge case: empty input
    if total_length == 0:
        return ""

    # 3. Locate Prefix Boundary: Find the index (Z) of the first zero.
    first_zero_index = find_first_zero_index(input_list)

    # 4. Extract Prefix: Isolate the sub-list before the first zero.
    non_zero_prefix = input_list[:first_zero_index]
    prefix_length = len(non_zero_prefix)

    # Handle edge case: Input starts with zero or is all zeros.
    # In this case, no BB pattern exists to replicate. Return original.
    if prefix_length == 0:
        return input_str

    # 5. Validate Prefix: Check assumed structure (length >= 2 and even).
    # If the structure doesn't match the examples, the rule is ambiguous.
    # Return original input as a safe default for unexpected formats.
    if prefix_length < 2 or prefix_length % 2 != 0:
        # This case deviates from the observed pattern in all examples.
        return input_str 

    # 6. Identify Block B: Extract the first half of the non-zero prefix.
    block_length = prefix_length // 2
    repeating_block = non_zero_prefix[:block_length]
    
    # Defensive check: ensure the block is not empty (shouldn't happen if prefix_length>=2)
    if not repeating_block:
        # Fallback if block extraction fails unexpectedly
        return input_str

    # 7. Generate Output: Create the output list by repeating block B.
    output_list = []
    while len(output_list) < total_length:
        output_list.extend(repeating_block)

    # 8. Truncate Output: Ensure the output list has the exact original length N.
    output_list = output_list[:total_length]

    # 9. Format Output: Convert the final list back to a space-separated string.
    output_str = format_output_sequence(output_list)

    return output_str