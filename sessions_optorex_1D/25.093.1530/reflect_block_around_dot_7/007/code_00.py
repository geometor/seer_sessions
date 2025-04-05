import math
from typing import List, Tuple, Union
import numpy as np

"""
Transforms an input numerical sequence (list or numpy array) by fixing the position
of the number '2' (pivot) and mirroring the positions of all other non-zero numbers 
across the pivot's position. The resulting sequence is returned as a space-separated string.
"""

def _find_pivot_index(data: Union[List[int], np.ndarray], pivot_value: int = 2) -> int:
    """Finds the index of the first occurrence of the pivot value."""
    # Convert numpy array to list for consistent index finding
    if isinstance(data, np.ndarray):
        data_list = data.tolist()
    else:
        data_list = list(data) # Ensure it's a list if not already

    try:
        return data_list.index(pivot_value)
    except ValueError:
        # This case should not happen based on problem constraints/examples
        raise ValueError(f"Pivot value {pivot_value} not found in the input sequence.")

def _find_other_non_zeros(data: Union[List[int], np.ndarray], pivot_index: int) -> List[Tuple[int, int]]:
    """Finds all non-zero values (excluding the pivot) and their original indices."""
    others = []
    # Iterate using enumerate for index and value
    for index, value in enumerate(data):
        # Convert value to standard Python int just in case it's a numpy type
        current_value = int(value)
        # Check if the value is not zero AND it's not the pivot element itself
        if current_value != 0 and index != pivot_index:
            others.append((current_value, index))
    return others

def _format_output_list(data: List[int]) -> str:
    """Converts the list of integers back into a space-separated string."""
    return " ".join(map(str, data))

def transform(input_sequence: Union[List[int], np.ndarray]) -> str:
    """
    Applies the mirroring transformation to the input numerical sequence.

    Args:
        input_sequence: A 1D list or numpy array of integers.

    Returns:
        A space-separated string representing the transformed sequence.
    """
    # Step 1: Determine the length of the sequence
    n = len(input_sequence)
    pivot_value = 2

    # Step 2: Find the index of the pivot element '2'
    pivot_index = _find_pivot_index(input_sequence, pivot_value)

    # Step 3: Identify the values and original indices of other non-zero elements
    other_non_zeros = _find_other_non_zeros(input_sequence, pivot_index)

    # Step 4: Initialize the output list with zeros
    output_list = [0] * n

    # Step 5: Place the pivot element '2' in the output list at its original position
    # Basic bounds check (although pivot_index should always be valid if found)
    if 0 <= pivot_index < n:
        output_list[pivot_index] = pivot_value
    else:
         # Should be unreachable if _find_pivot_index worked correctly
         raise IndexError("Pivot index determined to be out of bounds.")

    # Step 6: Iterate through the other non-zero elements and place them mirrored
    for value, original_index in other_non_zeros:
        # Calculate the new mirrored index using the reflection formula
        # new_index = pivot_index - (original_index - pivot_index)
        # new_index = pivot_index - original_index + pivot_index
        new_index = 2 * pivot_index - original_index

        # Ensure the calculated new index is within the bounds of the list
        if 0 <= new_index < n:
            # Place the value at the mirrored position.
            # Overwrites happen if multiple elements map to the same location.
            output_list[new_index] = value
        # else:
            # Optional: Log or handle cases where mirrored index falls outside bounds
            # print(f"Warning: Mirrored index {new_index} for value {value} is out of bounds.")


    # Step 7: Format the final output list into a space-separated string
    output_str = _format_output_list(output_list)

    # Step 8: Return the result string
    return output_str