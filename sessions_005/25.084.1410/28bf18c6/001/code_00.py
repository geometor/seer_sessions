"""
Identifies the single contiguous non-white object in the input grid, determines its minimal bounding box, extracts the subgrid corresponding to this box, and creates the output grid by horizontally concatenating this extracted subgrid with itself.
"""

import numpy as np

def find_bounding_box(grid):
    """Finds the minimal bounding box of non-white pixels."""
    non_white_pixels = np.argwhere(grid != 0)
    if non_white_pixels.size == 0:
        return None # No non-white pixels found
    min_row = np.min(non_white_pixels[:, 0])
    max_row = np.max(non_white_pixels[:, 0])
    min_col = np.min(non_white_pixels[:, 1])
    max_col = np.max(non_white_pixels[:, 1])
    return (min_row, min_col, max_row, max_col)

def transform(input_grid):
    """
    Transforms the input grid by extracting the bounding box of the non-white object
    and duplicating it horizontally.
    """
    # Convert input list of lists to numpy array for easier processing
    input_array = np.array(input_grid, dtype=int)

    # 1 & 2: Identify the non-white object and determine its minimal bounding box.
    # Note: We don't strictly need to find the *connected* object first,
    # as finding the bounding box of *all* non-white pixels achieves the same result
    # based on the examples provided (single object).
    bbox = find_bounding_box(input_array)

    if bbox is None:
        # Handle case with no non-white pixels (e.g., return empty or original grid)
        # Based on task description, this shouldn't happen, but good practice.
        return np.array([[]], dtype=int) # Return an empty grid

    min_row, min_col, max_row, max_col = bbox

    # 3: Extract the subgrid defined by the bounding box.
    extracted_subgrid = input_array[min_row : max_row + 1, min_col : max_col + 1]

    # 4: Construct the output grid by concatenating the extracted subgrid horizontally with itself.
    output_grid = np.hstack((extracted_subgrid, extracted_subgrid))

    # Convert back to list of lists if required by the environment, though numpy array is often preferred.
    # return output_grid.tolist()
    return output_grid