import numpy as np
import math
from typing import List

"""
The transformation rule extracts all non-white pixels within their minimal bounding box from the input grid, collects these pixel values in row-major order, and reshapes them into a square output grid. The side length of the output grid is the square root of the total number of non-white pixels.

1. Find all non-white pixels (value != 0) in the input grid.
2. Calculate the total count (N) of these non-white pixels.
3. Determine the side length (S) of the output square grid, where S = sqrt(N). (Implicitly assumes N is a perfect square).
4. Determine the minimal bounding box (min_row, max_row, min_col, max_col) containing all non-white pixels.
5. Iterate through the rows of the input grid within the bounding box (from min_row to max_row).
6. Within each row, iterate through the columns within the bounding box (from min_col to max_col).
7. If a pixel at (row, col) is non-white, add its value to a 1D list.
8. Reshape this 1D list of N pixel values into an S x S grid.
9. Return the S x S grid.
"""

def _find_bounding_box(grid: np.ndarray) -> tuple[int, int, int, int] | None:
    """Finds the minimal bounding box containing all non-zero elements."""
    non_zero_coords = np.argwhere(grid != 0)
    if non_zero_coords.size == 0:
        return None  # No non-background pixels found
    min_row = non_zero_coords[:, 0].min()
    max_row = non_zero_coords[:, 0].max()
    min_col = non_zero_coords[:, 1].min()
    max_col = non_zero_coords[:, 1].max()
    return min_row, max_row, min_col, max_col

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Extracts non-background pixels within their bounding box and reshapes them into a square grid.
    """
    input_array = np.array(input_grid, dtype=int)

    # 1. Find coordinates and count of non-white pixels
    non_zero_coords = np.argwhere(input_array != 0)
    num_non_zero = non_zero_coords.shape[0]

    # Handle case where input grid is all background or empty
    if num_non_zero == 0:
        return []

    # 2. Calculate the side length of the output square grid
    side_length = int(math.sqrt(num_non_zero))
    # Basic check if N is a perfect square (might need more robust error handling if not guaranteed)
    if side_length * side_length != num_non_zero:
         # This case indicates the hypothesis might be wrong for some inputs
         # For now, proceed assuming it's always a square based on examples
         # or return an empty/error state? Returning empty for now.
        print(f"Warning: Number of non-zero pixels ({num_non_zero}) is not a perfect square.")
        return [] # Or raise an error

    # 3. Find the bounding box
    bbox = _find_bounding_box(input_array)
    # This check should be redundant if num_non_zero > 0, but good practice
    if bbox is None:
        return [] 
        
    min_row, max_row, min_col, max_col = bbox

    # 4. Extract non-white pixels within the bounding box in row-major order
    non_zero_pixels_list = []
    for r in range(min_row, max_row + 1):
        for c in range(min_col, max_col + 1):
            pixel = input_array[r, c]
            if pixel != 0:
                non_zero_pixels_list.append(pixel)

    # 5. Reshape the list into the S x S output grid
    # Check if the number of extracted pixels matches expected count N
    if len(non_zero_pixels_list) != num_non_zero:
         print(f"Error: Extracted pixel count ({len(non_zero_pixels_list)}) doesn't match expected ({num_non_zero}).")
         return [] # Error state

    output_array = np.array(non_zero_pixels_list).reshape((side_length, side_length))

    # 6. Convert final numpy array back to list of lists
    output_grid = output_array.tolist()

    return output_grid