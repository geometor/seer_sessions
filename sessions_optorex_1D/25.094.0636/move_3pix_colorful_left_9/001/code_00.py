import math
import numpy as np
from collections import deque # deque is efficient for rotations/shifts

"""
Transforms a sequence of 12 space-separated digits by moving the first three digits to the end of the sequence, maintaining the relative order within both the moved part and the remaining part.
"""

def transform(input_str: str) -> str:
    """
    Applies a cyclic left shift of 3 positions to a sequence of 12 digits.

    Args:
        input_str: A string containing 12 space-separated digits.

    Returns:
        A string containing the transformed sequence with digits separated by spaces.
    """
    # 1. Read the input sequence and split it into a list of digit strings.
    # Example: "0 0 0 7 3 6 4 8 2 0 0 0" -> ['0', '0', '0', '7', '3', '6', '4', '8', '2', '0', '0', '0']
    digits = input_str.split(' ')

    # Validate input length (optional but good practice)
    if len(digits) != 12:
        print(f"Warning: Input length is {len(digits)}, expected 12. Proceeding anyway.")
        # Or raise ValueError("Input must contain exactly 12 space-separated digits.")

    # Use deque for efficient rotation (alternative to slicing)
    # dq = deque(digits)
    # dq.rotate(-3) # Negative value rotates left
    # output_digits = list(dq)

    # --- Alternatively, using list slicing as per the natural language program ---

    # 2. Separate the sequence into two parts:
    #    Part A: The first three digits.
    part_a = digits[:3] # First 3 elements
    #    Part B: The remaining nine digits (from the 4th to the 12th).
    part_b = digits[3:] # Elements from index 3 onwards

    # 3. Create the output sequence by appending Part A to the end of Part B.
    # Example: ['7', '3', '6', '4', '8', '2', '0', '0', '0'] + ['0', '0', '0']
    output_digits = part_b + part_a

    # 4. Format the output sequence by joining the digits with spaces.
    # Example: ['7', '3', '6', '4', '8', '2', '0', '0', '0', '0', '0', '0'] -> "7 3 6 4 8 2 0 0 0 0 0 0"
    output_str = ' '.join(output_digits)

    return output_str
