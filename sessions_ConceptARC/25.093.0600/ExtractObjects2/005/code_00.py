"""
Identifies the unique integer value (including 0) in the input grid whose
occurrences have the highest density within their minimal bounding box.
Density is calculated as (number of occurrences) / (bounding box area).
Tie-breaking rules: highest density, then highest count, then smallest
bounding box area, then smallest integer value.
Extracts the subgrid corresponding to the bounding box of the selected value.
Filters the extracted subgrid, keeping only the cells that contained the
selected value in the original input and setting others to 0.
"""

import numpy as np
import collections # Although not strictly needed with numpy, kept for potential future use if logic changes

def _get_bounding_box(coords_indices):
    """
    Calculates the min/max row/col for a list/array of coordinates.

    Args:
        coords_indices (tuple of np.array): Output from np.where, containing arrays
                                          for row indices and column indices.

    Returns:
        tuple: (min_r, max_r, min_c, max_c) or None if coords_indices is empty.
    """
    if not coords_indices or len(coords_indices[0]) == 0:
        return None

    rows = coords_indices[0]
    cols = coords_indices[1]

    min_r = np.min(rows)
    max_r = np.max(rows)
    min_c = np.min(cols)
    max_c = np.max(cols)
    return min_r, max_r, min_c, max_c

def transform(input_grid_arg):
    """
    Finds the integer value with the highest density of occurrences within its
    bounding box, extracts that bounding box, and filters it to keep only
    the selected integer value.

    Args:
        input_grid_arg: The input 2D grid (list of lists or numpy array).

    Returns:
        list of list of int: The filtered subgrid based on the highest density value.
                             Returns an empty list if the input is empty or no suitable
                             value is found (e.g., only zeros and 0 isn't highest density).
    """
    # Ensure input is a NumPy array
    input_grid = np.array(input_grid_arg, dtype=int)

    # Handle empty input grid
    if input_grid.size == 0:
        return []

    rows, cols = input_grid.shape

    # Find unique values in the grid
    unique_values = np.unique(input_grid)

    # Initialize variables to track the best candidate
    best_value = None
    max_density = -1.0
    max_count = -1
    min_bbox_area = float('inf')
    best_bbox = None

    # Iterate through each unique value to find the one with the highest density
    for candidate_value in unique_values:
        # Find coordinates of all occurrences of the candidate value
        indices = np.where(input_grid == candidate_value)

        # Skip if the value doesn't exist (shouldn't happen with np.unique unless grid is empty)
        if len(indices[0]) == 0:
            continue

        # Calculate count
        current_count = len(indices[0])

        # Determine bounding box
        bbox = _get_bounding_box(indices)
        if bbox is None: # Should not happen if count > 0
             continue
        min_r, max_r, min_c, max_c = bbox

        # Calculate bounding box area
        current_bbox_area = (max_r - min_r + 1) * (max_c - min_c + 1)
        if current_bbox_area <= 0: # Avoid division by zero for single point/line cases
            current_density = float('inf') if current_count > 0 else 0 # Assign high density if area is minimal
        else:
            current_density = current_count / current_bbox_area

        # --- Apply selection criteria and tie-breaking ---
        is_better = False
        if current_density > max_density:
            is_better = True
        elif current_density == max_density:
            if current_count > max_count:
                is_better = True
            elif current_count == max_count:
                if current_bbox_area < min_bbox_area:
                    is_better = True
                elif current_bbox_area == min_bbox_area:
                    # Final tie-breaker: smaller integer value wins
                    if best_value is None or candidate_value < best_value:
                        is_better = True

        # Update best candidate if current one is better
        if is_better:
            max_density = current_density
            max_count = current_count
            min_bbox_area = current_bbox_area
            best_value = candidate_value
            best_bbox = bbox

    # If no suitable candidate was found (e.g., empty grid processed), return empty list
    if best_bbox is None:
        return []

    # Extract the subgrid corresponding to the best bounding box
    min_r, max_r, min_c, max_c = best_bbox
    extracted_subgrid = input_grid[min_r : max_r + 1, min_c : max_c + 1]

    # Filter the extracted subgrid: keep only the 'best_value', replace others with 0
    output_grid_np = np.where(extracted_subgrid == best_value, best_value, 0)

    # Convert the resulting NumPy array to a standard Python list of lists
    output_grid = output_grid_np.tolist()

    return output_grid