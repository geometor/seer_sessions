"""
The transformation rule operates on a sequence of single-digit integers, represented as a space-separated string.

1.  **Identify Pivot:** Find the index of the first occurrence of the digit '2'. If '2' is not present, the sequence remains unchanged.
2.  **Partition:** Split the sequence into three parts: the elements *before* the first '2' (`before_2`), the '2' itself (`pivot`), and the elements *after* the first '2' (`after_2`).
3.  **Process `after_2`:** Rearrange this section by moving all '0's to the end, while preserving the relative order of the non-zero digits. The non-zero digits come first, followed by the '0's.
4.  **Process `before_2`:**
    *   Identify the '0's and non-zero digits in this section.
    *   **Special Case Check:** Determine if *all* non-zero digits in `before_2` are '3's AND if there is at least one '0' present in `before_2`.
    *   **Special Case Execution:** If the special case conditions are met, rearrange `before_2` by placing all '0's except one at the very beginning, followed by all the '3's, and finally placing the single remaining '0' at the end of this section (just before the pivot '2').
    *   **General Case Execution:** If the special case conditions are *not* met, rearrange `before_2` by moving all '0's to the beginning, followed by the non-zero digits, preserving the relative order of the non-zero digits.
5.  **Combine:** Concatenate the processed `before_2` section, the `pivot` ('2'), and the processed `after_2` section.
6.  **Format:** Convert the resulting list of integers back into a space-separated string for the final output.
"""

import math

# Helper functions
def parse_input(input_str: str) -> list[int]:
    """Converts the space-separated string of digits into a list of integers."""
    # Handles potential empty strings or extra spaces gracefully
    return [int(digit) for digit in input_str.split() if digit.isdigit()]

def format_output(output_list: list[int]) -> str:
    """Converts the list of integers back into a space-separated string."""
    return " ".join(map(str, output_list))

def process_before_section(section: list[int]) -> list[int]:
    """
    Rearranges the section before the pivot '2' according to the rules.

    Args:
        section: The list of integers before the pivot '2'.

    Returns:
        The rearranged list section.
    """
    if not section:
        return []

    # Separate zeros and non-zeros
    zeros = [digit for digit in section if digit == 0]
    non_zeros = [digit for digit in section if digit != 0]
    num_zeros = len(zeros)
    num_non_zeros = len(non_zeros)

    # Check for special case: all non-zeros are '3' and there are both zeros and non-zeros present
    all_are_threes = all(digit == 3 for digit in non_zeros)
    special_case = all_are_threes and num_non_zeros > 0 and num_zeros > 0

    if special_case:
        # Special case: Place all but one zero at the start, then non-zeros (all 3s), then the last zero
        # Example: [3, 3, 0, 0, 0] -> [0, 0, 3, 3, 0]
        return zeros[:-1] + non_zeros + [0]
    else:
        # General case: All zeros first, then non-zeros preserving relative order
        # Example: [0, 9, 0, 9] -> [0, 0, 9, 9]
        return zeros + non_zeros

def process_after_section(section: list[int]) -> list[int]:
    """
    Rearranges the section after the pivot '2'. Moves zeros to the end.

    Args:
        section: The list of integers after the pivot '2'.

    Returns:
        The rearranged list section.
    """
    if not section:
        return []

    # Separate zeros and non-zeros
    zeros = [digit for digit in section if digit == 0]
    non_zeros = [digit for digit in section if digit != 0]

    # Non-zeros first (preserving relative order), then zeros
    # Example: [0, 5, 0, 5] -> [5, 5, 0, 0]
    return non_zeros + zeros

# Main transform function
def transform(input_str: str) -> str:
    """
    Applies the transformation rule to the input string sequence.
    """
    # 1. Parse input string to list of integers
    input_list = parse_input(input_str)
    if not input_list: # Handle empty input
        return ""

    # 2. Find the index of the first '2' (pivot)
    pivot_index = -1
    try:
        pivot_index = input_list.index(2)
    except ValueError:
        # If '2' is not found, return the original string
        return input_str

    # 3. Partition the list based on the pivot
    before_2 = input_list[:pivot_index]
    pivot = [2]  # Keep the pivot as a list for easy concatenation
    after_2 = input_list[pivot_index + 1:]

    # 4. Process the section *after* the '2'
    processed_after_2 = process_after_section(after_2)

    # 5. Process the section *before* the '2'
    processed_before_2 = process_before_section(before_2)

    # 6. Combine the processed sections with the pivot
    output_list = processed_before_2 + pivot + processed_after_2

    # 7. Format the result list back into a string
    output_str = format_output(output_list)

    return output_str