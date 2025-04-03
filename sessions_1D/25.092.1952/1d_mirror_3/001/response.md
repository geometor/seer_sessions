```python
import numpy as np
from typing import List, Tuple

"""
Identifies three key components in a 1D input array: a single pivot pixel (maroon, 9), a contiguous block of a single color other than white (0) or maroon (9) (the 'colored object'), and a contiguous block of white (0) pixels separating the pivot and the colored object (the 'separator'). The transformation rearranges these components while preserving the original position of the pivot pixel. In the output array, the pivot pixel retains its original index. The separator block is placed immediately to the right of the pivot pixel, and the colored object block is placed immediately to the right of the separator block. All other positions in the output array are filled with white (0) pixels, maintaining the original total length of the array.
"""

def find_pivot(grid: np.ndarray) -> int:
    """Finds the index of the pivot pixel (9)."""
    pivot_indices = np.where(grid == 9)[0]
    if len(pivot_indices) == 1:
        return pivot_indices[0]
    else:
        raise ValueError("Input grid must contain exactly one pivot pixel (9).")

def find_colored_object(grid: np.ndarray) -> Tuple[List[int], int, int]:
    """Finds the contiguous block of non-0, non-9 color."""
    obj_indices = np.where((grid != 0) & (grid != 9))[0]
    if len(obj_indices) == 0:
        raise ValueError("Input grid must contain a colored object (non-0, non-9).")

    start_index = obj_indices[0]
    end_index = obj_indices[-1] # Inclusive end index for the object block

    # Verify contiguity
    if not np.all(np.diff(obj_indices) == 1):
         raise ValueError("Colored object is not contiguous.")
         
    # Verify single color
    obj_color = grid[start_index]
    if not np.all(grid[start_index:end_index+1] == obj_color):
        raise ValueError("Colored object block contains multiple colors.")

    colored_object = grid[start_index : end_index + 1].tolist()
    return colored_object, start_index, end_index

def find_separator(grid: np.ndarray, pivot_idx: int, obj_start_idx: int, obj_end_idx: int) -> List[int]:
    """Finds the separator block (0s) between the pivot and the object."""
    if pivot_idx < obj_start_idx:
        # Pivot is to the left of the object
        separator_slice = grid[pivot_idx + 1 : obj_start_idx]
        separator_start = pivot_idx + 1
        separator_end = obj_start_idx -1 # inclusive
    elif pivot_idx > obj_end_idx:
        # Pivot is to the right of the object
        separator_slice = grid[obj_end_idx + 1 : pivot_idx]
        separator_start = obj_end_idx + 1
        separator_end = pivot_idx -1 # inclusive
    else:
        raise ValueError("Pivot index is within the object bounds.")

    # Verify separator contains only zeros
    if not np.all(separator_slice == 0):
        raise ValueError(f"Separator between pivot ({pivot_idx}) and object ({obj_start_idx}-{obj_end_idx}) contains non-zero values.")

    return separator_slice.tolist()


def transform(input_grid: List[int]) -> List[int]:
    """
    Rearranges elements in a 1D array based on a pivot color (9).
    The pivot retains its original position, followed by the separator, 
    then the colored object. Remaining positions are filled with 0s.
    """
    # Convert input list to numpy array for easier manipulation
    input_array = np.array(input_grid)
    n = len(input_array)

    # --- Identify components ---
    # 1. Find the pivot (9)
    pivot_idx = find_pivot(input_array)
    pivot_value = 9

    # 2. Find the colored object (non-0, non-9 block)
    colored_object, obj_start_idx, obj_end_idx = find_colored_object(input_array)

    # 3. Find the separator (0s between pivot and object)
    separator = find_separator(input_array, pivot_idx, obj_start_idx, obj_end_idx)

    # --- Construct the output array ---
    # Initialize output grid with zeros (white)
    output_array = np.zeros(n, dtype=int)

    # Place the pivot at its original index
    output_array[pivot_idx] = pivot_value

    # Place the separator immediately after the pivot
    separator_start_out = pivot_idx + 1
    separator_end_out = separator_start_out + len(separator)
    if separator_end_out <= n: # Check bounds
        output_array[separator_start_out:separator_end_out] = separator
    else:
        # Handle cases where separator might wrap or go out of bounds (though unlikely based on examples)
        print("Warning: Separator placement extends beyond array bounds.") 
        place_len = n - separator_start_out
        if place_len > 0:
            output_array[separator_start_out:] = separator[:place_len]


    # Place the colored object immediately after the separator
    object_start_out = separator_end_out
    object_end_out = object_start_out + len(colored_object)
    if object_end_out <= n: # Check bounds
        output_array[object_start_out:object_end_out] = colored_object
    else:
        # Handle cases where object might wrap or go out of bounds
        print("Warning: Object placement extends beyond array bounds.")
        place_len = n - object_start_out
        if place_len > 0:
             output_array[object_start_out:] = colored_object[:place_len]


    # The rest of the array remains 0 (initialized state)

    # Convert numpy array back to list for the required output format
    output_grid = output_array.tolist()

    return output_grid
```