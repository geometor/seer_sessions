import numpy as np
from typing import List, Tuple

"""
Rearranges elements in a 1D array relative to a fixed pivot point (maroon, 9). 
The pivot's index remains constant. A contiguous block of a single color 
(other than white 0 or maroon 9), called the 'colored object', and a 
contiguous block of white 0s separating the pivot and object in the input, 
called the 'separator', are identified. In the output, the pivot is placed 
at its original index, the separator block is placed immediately to the 
right of the pivot, and the colored object block is placed immediately 
to the right of the separator. All other positions in the output array 
are filled with white 0s. The array length is conserved. Placement respects
array boundaries, truncating if necessary.
"""

def find_pivot(grid: np.ndarray) -> int:
    """Finds the index of the single pivot pixel (9)."""
    pivot_indices = np.where(grid == 9)[0]
    if len(pivot_indices) != 1:
        # This condition should not be met based on task constraints/examples.
        raise ValueError("Input grid must contain exactly one pivot pixel (9).")
    return pivot_indices[0]

def find_colored_object(grid: np.ndarray) -> Tuple[List[int], int, int]:
    """
    Finds the contiguous block of non-0, non-9 color ('colored_object').
    Returns the block content (list of pixel values), its start index 
    in the input grid, and its end index (inclusive) in the input grid.
    """
    # Find all indices of pixels that are neither background (0) nor pivot (9).
    obj_indices = np.where((grid != 0) & (grid != 9))[0]
    if len(obj_indices) == 0:
        # This condition should not be met based on task constraints/examples.
        raise ValueError("Input grid must contain a colored object (non-0, non-9).")

    # Since the object is known to be contiguous, find its bounds.
    start_index = obj_indices[0]
    end_index = obj_indices[-1] # Inclusive end index 
    
    # Extract the content (pixel values) of the colored object block.
    colored_object_content = grid[start_index : end_index + 1].tolist()
    
    # Optional assertion/check: verify contiguity based on indices found.
    # This helps catch potential issues if assumptions are wrong.
    # assert len(obj_indices) == (end_index - start_index + 1), "Detected object indices are not contiguous."
    # Optional assertion/check: verify single color
    # assert len(set(colored_object_content)) <= 1, "Detected object block has multiple colors."


    return colored_object_content, start_index, end_index

def find_separator(grid: np.ndarray, pivot_idx: int, obj_start_idx: int, obj_end_idx: int) -> List[int]:
    """
    Finds the separator block (contiguous 0s) located spatially between 
    the pivot and the colored object in the input grid.
    Returns the block content (list of 0s). Can be an empty list if 
    pivot and object are adjacent.
    """
    separator_content = []
    if pivot_idx < obj_start_idx:
        # Pivot is to the left of the object. Separator is between them.
        # Slice from element after pivot up to element before object start.
        separator_slice = grid[pivot_idx + 1 : obj_start_idx]
    elif pivot_idx > obj_end_idx:
        # Pivot is to the right of the object. Separator is between them.
        # Slice from element after object end up to element before pivot.
        separator_slice = grid[obj_end_idx + 1 : pivot_idx]
    else:
        # Pivot index is within or adjacent to object bounds. No separator exists.
        # This case implies an empty separator, which is handled by returning [].
        # If they truly overlap (which would be invalid input), this still returns [],
        # but the overall logic might fail elsewhere or produce unexpected output.
        separator_slice = np.array([], dtype=int) # Ensure correct type for check below

    # Verify that the identified separator region contains only zeros.
    if len(separator_slice) > 0 and not np.all(separator_slice == 0):
         # This might indicate an issue with component identification or input format.
        raise ValueError(f"Region identified as separator between pivot ({pivot_idx}) and object ({obj_start_idx}-{obj_end_idx}) contains non-zero values.")

    separator_content = separator_slice.tolist()
    return separator_content

def transform(input_grid: List[int]) -> List[int]:
    """
    Applies the transformation rule to the input grid.
    
    Args:
        input_grid: A list of integers representing the 1D input grid.

    Returns:
        A list of integers representing the transformed 1D output grid.
    """
    # Convert input list to numpy array for efficient processing
    input_array = np.array(input_grid)
    n = len(input_array)

    # Initialize the output array with the background color (0)
    output_array = np.zeros(n, dtype=int)

    # --- Step 1: Identify components in the input array ---
    # Locate the pivot (9) and its index
    pivot_idx = find_pivot(input_array)
    pivot_value = 9 

    # Locate the colored_object block, get its content and original indices
    object_content, obj_start_in, obj_end_in = find_colored_object(input_array)

    # Locate the separator block between pivot and object in input, get its content
    separator_content = find_separator(input_array, pivot_idx, obj_start_in, obj_end_in)

    # --- Step 2: Construct the output array ---
    # Place the pivot at its original index in the output
    # Check if pivot index itself is valid (should always be true if input is valid)
    if 0 <= pivot_idx < n:
        output_array[pivot_idx] = pivot_value
    else:
        # Should not happen with valid inputs.
        raise IndexError("Pivot index is out of bounds.")

    # Calculate placement indices for the separator in the output
    # Separator starts immediately after the pivot
    sep_start_out = pivot_idx + 1
    sep_len = len(separator_content)
    sep_end_out = sep_start_out + sep_len # Exclusive end index

    # Place separator, handling boundary conditions (ensure indices are within array bounds)
    if sep_start_out < n: # Check if the start index is valid (i.e., pivot wasn't the last element)
        # Calculate how many elements of the separator can actually fit into the array
        placeable_len_sep = min(sep_len, n - sep_start_out)
        if placeable_len_sep > 0:
             # Slice the output array and assign the placeable part of the separator content
             output_array[sep_start_out : sep_start_out + placeable_len_sep] = separator_content[:placeable_len_sep]

    # Calculate placement indices for the colored object in the output
    # Object starts immediately after where the separator ended (or would have ended if truncated)
    obj_start_out = sep_end_out 
    obj_len = len(object_content)
    # obj_end_out = obj_start_out + obj_len # Exclusive end index

    # Place object, handling boundary conditions
    if obj_start_out < n: # Check if the start index is valid
        # Calculate how many elements of the object can actually fit
        placeable_len_obj = min(obj_len, n - obj_start_out)
        if placeable_len_obj > 0:
            # Slice the output array and assign the placeable part of the object content
            output_array[obj_start_out : obj_start_out + placeable_len_obj] = object_content[:placeable_len_obj]

    # The rest of the array remains 0 (background/padding) as initialized

    # Convert the final numpy array back to a list for the required output format
    output_grid = output_array.tolist()

    return output_grid