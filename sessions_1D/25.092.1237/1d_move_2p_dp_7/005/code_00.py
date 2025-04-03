import numpy as np
from typing import List, Tuple, Optional

"""
Transformation Rule Natural Language Description:

1.  **Find Boundary:** Scan the input array from left to right to find the index of the first maroon pixel (9). This is the `boundary_index`.
2.  **Define Segments:**
    *   If a maroon pixel (9) is found at `boundary_index`:
        *   `segment_before`: Contains all pixels from the start of the array up to (but not including) `boundary_index`.
        *   `boundary_pixel`: The maroon pixel (9) itself.
        *   `segment_after`: Contains all pixels from `boundary_index + 1` to the end of the array.
    *   If no maroon pixel (9) is found:
        *   `segment_before`: Contains all pixels of the input array.
        *   `boundary_pixel`: Does not exist.
        *   `segment_after`: Is empty.
3.  **Process `segment_before`:**
    *   Identify all white pixels (0) within this segment (`background_pixels`).
    *   Identify all non-white pixels within this segment (`content_pixels`), preserving their relative order.
    *   Create `reconstructed_segment_before` by concatenating `background_pixels` followed by `content_pixels`.
4.  **Assemble Output:**
    *   If a `boundary_pixel` exists: The final output array is formed by concatenating `reconstructed_segment_before`, the `boundary_pixel`, and `segment_after`.
    *   If no `boundary_pixel` exists: The final output array is simply `reconstructed_segment_before`.
"""

def find_first_occurrence(arr: np.ndarray, value: int) -> int:
    """Finds the index of the first occurrence of a value in a NumPy array.
       Returns -1 if the value is not found."""
    indices = np.where(arr == value)[0]
    return indices[0] if len(indices) > 0 else -1

def transform(input_grid: List[List[int]]) -> List[List[int]]:
    """
    Applies the transformation rule to the input grid.
    Rearranges elements before the first '9' pixel, moving '0's to the start
    of that segment, followed by the other non-'9' elements. Elements from
    the first '9' onwards remain fixed.
    """
    # --- Input Validation and Initialization ---
    if not input_grid or not input_grid[0]:
        return input_grid # Return empty or invalid input as is
    
    # Convert the inner list (representing the 1D grid) to a NumPy array
    input_array = np.array(input_grid[0], dtype=int) # Explicit dtype

    # --- Core Logic ---

    # 1. Find Boundary (index of the first maroon pixel '9')
    boundary_index = find_first_occurrence(input_array, 9)

    # 2. Define Segments based on the boundary index
    segment_before: np.ndarray
    boundary_pixel: Optional[np.ndarray] = None # Use None or an empty array
    segment_after: np.ndarray

    if boundary_index != -1:
        # Boundary found: Partition the array
        segment_before = input_array[:boundary_index]
        boundary_pixel = np.array([input_array[boundary_index]], dtype=int) # Store as array for concat
        segment_after = input_array[boundary_index + 1:]
    else:
        # No boundary found: The entire array is the 'before' segment
        segment_before = input_array
        boundary_pixel = np.array([], dtype=int) # Use empty array for concat consistency
        segment_after = np.array([], dtype=int) # Use empty array

    # 3. Process `segment_before`
    reconstructed_segment_before: np.ndarray
    if segment_before.size > 0:
        # Separate background (0) and content (non-0) pixels
        background_pixels = segment_before[segment_before == 0]
        content_pixels = segment_before[segment_before != 0]
        
        # Reconstruct the segment: background followed by content
        reconstructed_segment_before = np.concatenate((background_pixels, content_pixels))
    else:
        # If segment_before is empty, the reconstructed part is also empty
        reconstructed_segment_before = np.array([], dtype=int)

    # 4. Assemble Output by concatenating the parts
    # Note: np.concatenate works correctly with empty arrays
    output_array = np.concatenate((reconstructed_segment_before, boundary_pixel, segment_after))

    # --- Output Formatting ---
    # Convert the final NumPy array back to the required list of lists format
    output_grid = [output_array.tolist()]

    return output_grid