"""
The transformation rule operates on a 1D NumPy array of single-digit integers.

1.  **Identify Pivot:** Find the index of the first occurrence of the integer '2'. If '2' is not present, the array remains unchanged.
2.  **Partition:** Split the array into three parts: the elements *before* the first '2' (`before_2`), the '2' itself (`pivot`), and the elements *after* the first '2' (`after_2`).
3.  **Process `after_2`:** Rearrange this section by moving all '0's to the end, while preserving the relative order of the non-zero digits. The non-zero digits come first, followed by the '0's.
4.  **Process `before_2`:**
    *   Identify the '0's and non-zero digits in this section.
    *   **Special Case Check:** Determine if *all* non-zero digits in `before_2` are '3's AND if there is at least one '0' present in `before_2`.
    *   **Special Case Execution:** If the special case conditions are met, rearrange `before_2` by placing all '0's except one at the very beginning, followed by all the '3's, and finally placing the single remaining '0' at the end of this section (just before the pivot '2').
    *   **General Case Execution:** If the special case conditions are *not* met, rearrange `before_2` by moving all '0's to the beginning, followed by the non-zero digits, preserving the relative order of the non-zero digits.
5.  **Combine:** Concatenate the processed `before_2` section, the `pivot` ('2'), and the processed `after_2` section into a new NumPy array.
6.  **Return:** Return the resulting NumPy array.
"""

import numpy as np

# Helper function to process the section *before* the pivot '2'
def _process_before_section(section: np.ndarray) -> np.ndarray:
    """
    Rearranges the section before the pivot '2' according to the rules,
    including the special case for '3's.

    Args:
        section: The 1D NumPy array of integers before the pivot '2'.

    Returns:
        The rearranged 1D NumPy array section.
    """
    if section.size == 0:
        return np.array([], dtype=int) # Return empty array if section is empty

    # Separate zeros and non-zeros
    zeros = section[section == 0]
    non_zeros = section[section != 0]
    num_zeros = zeros.size
    num_non_zeros = non_zeros.size

    # Check for special case: all non-zeros are '3' AND there are both zeros and non-zeros present
    all_are_threes = np.all(non_zeros == 3) if num_non_zeros > 0 else False # Check only if non-zeros exist
    special_case = all_are_threes and num_non_zeros > 0 and num_zeros > 0

    if special_case:
        # Special case: Place all but one zero at the start, then non-zeros (all 3s), then the last zero
        # Need at least one zero for this logic:
        if num_zeros > 0:
             return np.concatenate((zeros[:-1], non_zeros, zeros[-1:]))
        else: # Should not happen if special_case is True, but safe fallback
             return non_zeros # Only 3s, no zeros
    else:
        # General case: All zeros first, then non-zeros preserving relative order
        return np.concatenate((zeros, non_zeros))

# Helper function to process the section *after* the pivot '2'
def _process_after_section(section: np.ndarray) -> np.ndarray:
    """
    Rearranges the section after the pivot '2'. Moves zeros to the end,
    preserving the relative order of non-zeros.

    Args:
        section: The 1D NumPy array of integers after the pivot '2'.

    Returns:
        The rearranged 1D NumPy array section.
    """
    if section.size == 0:
        return np.array([], dtype=int) # Return empty array if section is empty

    # Separate zeros and non-zeros
    zeros = section[section == 0]
    non_zeros = section[section != 0]

    # Non-zeros first (preserving relative order), then zeros
    return np.concatenate((non_zeros, zeros))


def transform(input_array: np.ndarray) -> np.ndarray:
    # Ensure input is a NumPy array (might be redundant if guaranteed by caller)
    if not isinstance(input_array, np.ndarray):
        # Attempt conversion if possible, or raise error/return input
        try:
            input_array = np.array(input_array)
        except Exception as e:
             print(f"Error: Input could not be converted to NumPy array: {e}")
             return input_array # Or raise TypeError

    # 1. Find the index of the first '2' (pivot)
    pivot_indices = np.where(input_array == 2)[0]

    # If '2' is not found, return the original array
    if pivot_indices.size == 0:
        return input_array.copy() # Return a copy to avoid modifying original

    pivot_index = pivot_indices[0]

    # 2. Partition the array based on the pivot
    before_part = input_array[:pivot_index]
    pivot_part = np.array([2], dtype=int) # Keep the pivot as an array
    after_part = input_array[pivot_index + 1:]

    # 3. Process the section *after* the '2'
    processed_after_part = _process_after_section(after_part)

    # 4. Process the section *before* the '2' using its specific rules
    processed_before_part = _process_before_section(before_part)

    # 5. Combine the processed sections with the pivot
    output_array = np.concatenate((processed_before_part, pivot_part, processed_after_part))

    # 6. Return the final transformed array
    return output_array