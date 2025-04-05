import collections
from typing import List, Dict, Tuple, Optional

"""
Transforms an input list of integers based on the following rule:
1. Identify all unique non-zero digits and the indices where they appear.
2. Check if any non-zero digit appears exactly twice in the list.
3. If one or more digits appear exactly twice, select the digit whose *first* occurrence (smallest index) is earliest in the list. This is the "target digit".
4. If a target digit is found with indices idx1 and idx2 (idx1 < idx2), create a copy of the input list.
5. In the copied list, change the value of all elements at indices strictly between idx1 and idx2 (i.e., from index idx1 + 1 up to, but not including, index idx2) to the value of the target digit.
6. Return the modified list.
7. If no non-zero digit appears exactly twice, return the original input list unchanged (as a new list copy).
"""

def _find_non_zero_digit_indices(data_list: List[int]) -> Tuple[Dict[int, List[int]], Dict[int, int]]:
    """
    Finds all indices for each non-zero number and tracks the first index seen.

    Args:
        data_list: The input list of integers.

    Returns:
        A tuple containing:
        - dict: A dictionary mapping each non-zero digit to a list of its indices.
        - dict: A dictionary mapping each non-zero digit to its first encountered index.
    """
    # Use defaultdict to easily append indices for each digit
    indices_map = collections.defaultdict(list)
    # Keep track of the first time we see a digit
    first_occurrence = {}
    for index, value in enumerate(data_list):
        if value != 0:
            indices_map[value].append(index)
            # Record the first occurrence index if not already seen
            if value not in first_occurrence:
                first_occurrence[value] = index
    return indices_map, first_occurrence

def transform(input_list: List[int]) -> List[int]:
    """
    Applies the transformation rule to the input list.

    Args:
        input_list: A list of integers.

    Returns:
        A new list representing the transformed output, or a copy of the original list if no transformation applies.
    """

    # Step 1 & 2 (partially): Find indices and first occurrences of non-zero digits
    indices_map, first_occurrence = _find_non_zero_digit_indices(input_list)

    # Step 3 & 5a: Identify potential target digits (those appearing exactly twice)
    # and select the one with the earliest first occurrence.
    target_digit: Optional[int] = None
    min_first_index = float('inf')
    target_indices: Optional[List[int]] = None

    # Iterate through the non-zero digits found
    for digit, indices in indices_map.items():
        # Check if the digit occurs exactly twice
        if len(indices) == 2:
            # Get the first occurrence index for this digit
            current_first_index = first_occurrence[digit]
            # If this digit's first occurrence is earlier than the current best,
            # update the target digit and its details.
            if current_first_index < min_first_index:
                min_first_index = current_first_index
                target_digit = digit
                target_indices = indices # Store the two indices [idx1, idx2]

    # Step 4 & 7: If no target digit was found, return a copy of the original list.
    if target_digit is None or target_indices is None:
        return list(input_list) # Return a copy

    # Step 5b-e: A target digit was found, perform the fill operation.
    # Create a copy of the input list to modify.
    output_list = list(input_list)
    # Retrieve the start and end indices for the fill.
    idx1, idx2 = target_indices[0], target_indices[1] # Indices are already sorted as they were found sequentially

    # Fill the gap between the two indices (exclusive) with the target digit.
    # The range starts from the element *after* the first occurrence (idx1 + 1)
    # and goes up to (but does not include) the second occurrence (idx2).
    for i in range(idx1 + 1, idx2):
        # Only modify if the element is currently 0 (implied by examples, though could fill any)
        # The examples only show 0s being filled, so let's stick to that for now.
        # Revisit if examples show non-zeros being overwritten.
        # On second thought, the prompt says "fill the gap", which implies replacing whatever is there.
        # Let's assume replacement.
        output_list[i] = target_digit

    # Step 6: Return the modified list.
    return output_list