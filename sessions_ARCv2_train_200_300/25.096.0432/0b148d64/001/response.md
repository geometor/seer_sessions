Warning: Response generation stopped. Finish Reason: MAX_TOKENS (2)
Partial text available:
---
```python
import numpy as np

"""
Transforms an input grid by identifying four quadrants separated by the largest
contiguous horizontal and vertical bands of zeros. It then selects one quadrant
based on the distribution of non-zero numbers.

Selection Rules:
1. Identify non-zero numbers unique to a single quadrant.
2. If unique numbers exist, select the quadrant containing the maximum unique number.
3. If no numbers are unique to one quadrant, find the overall maximum non-zero
   number (M) across all quadrants.
4. Select the quadrant containing M based on priority: Bottom-Right (BR) >
   Bottom-Left (BL) > Top-Right (TR) > Top-Left (TL).
"""

def find_largest_zero_band_rows(grid: np.ndarray):
    """
    Finds the start and end row indices of the largest contiguous block of
    all-zero rows.
    Returns tuple (start_index, end_index).
    Raises ValueError if no all-zero row is found.
    """
    num_rows, _ = grid.shape
    max_len = 0
    best_start, best_end = -1, -1
    current_start, current_len = -1, 0

    for r in range(num_rows):
        # Check if the entire row is zero
        if np.all(grid[r, :] == 0):
            if current_len == 0: # Start of a new potential band
                current_start = r
            current_len += 1
        else: # End of the current zero band (or not in one)
            if current_len > max_len: # Check if the ended band was the largest so far
                max_len = current_len
                best_start = current_start
                best_end = r - 1
            current_len = 0 # Reset length for the next potential band

    # After loop, check if the grid ended with the longest zero band
    if current_len > max_len:
        # max_len = current_len # Not strictly needed to update max_len here
        best_start = current_start
        best_end = num_rows - 1

    # If no zero row was ever found, best_start remains -1
    if best_start == -1:
         raise ValueError("No horizontal zero band found.")

    return best_start, best_end

def find_largest_zero_band_cols(grid: np.ndarray):
    """
    Finds the start and end column indices of the largest contiguous block of
    all-zero columns.
    Returns tuple (start_index, end_index).
    Raises ValueError if no all-zero column is found.
    """
    _, num_cols = grid.shape
    max_len = 0
    best_start, best_end = -1, -1
    current_start, current_len = -1, 0

    for c in range(num_cols):
         # Check if the entire column is zero
        if np.all(grid[:, c] == 0):
            if current_len == 0: # Start of a new potential band
                current_start = c
            current_len += 1
        else: # End of the current zero band (or not in one)
            if current_len > max_len: # Check if the ended band was the largest so far
                max_len = current_len
                best_start = current_start
                best_end = c - 1
            current_len = 0 # Reset length for the next potential band

    # After loop, check if the grid ended with the longest zero band
    if current_len > max_len:
        # max_len = current_len # Not strictly needed
        best_start = current_start
        best_end = num_cols - 1

    # If no zero column was ever found, best_start remains -1
    if best_start == -1:
         raise ValueError("No vertical zero band found.")

    return best_start, best_end

def get_unique_non_zeros(subgrid: np.ndarray) -> set:
    """
    Extracts the set of unique non-zero values from a subgrid (NumPy array).
    Returns an empty set if the subgrid is empty or contains only zeros.
    """
    # Return empty set immediately if subgrid has no elements
    if subgrid.size == 0:
        return set()
    # Find unique values in the flattened subgrid
    unique_vals = np.unique(subgrid)
    # Filter out zero and return the set of non-zero unique values
    return set(val for val in unique_vals if val != 0)

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    # Convert input list of lists to a NumPy array for efficient processing
    grid = np.array(input_grid, dtype=int)
    num_rows, num_cols = grid.shape

    # Handle empty input grid
    if num_rows == 0 or num_cols == 0:
        return []

    # Find the largest horizontal and vertical zero bands
    try:
        hr_start, hr_end = find_largest_zero_band_rows(grid)
        vc_start, vc_end = find_largest_zero_band_cols(grid)
    except ValueError as e:
        # If the expected zero bands are not found, the grid structure is invalid
        # for this transformation. Return empty list.
        print(f"Error: Could not find required zero bands - {e}")
        return []

    # Define the four quadrants using NumPy slicing based on band indices
    # Note: Slicing `[a:b]` includes `a` up to `b-1`.
    # Note: `vc_end + 1` and `hr_end + 1` give the start of the next section.
    tl_quad = grid[0:hr_start, 0:vc_start]
    tr_quad = grid[0:hr_start, vc_end + 1 : num_cols]
    bl_quad = grid[hr_end + 1 : num_rows, 0:vc_start]
    br_quad = grid[hr_end + 1 : num_rows, vc_end + 1 : num_cols]

    # Store quadrants and their names for easier access
    quadrants = {
        "TL": tl_quad, "TR": tr_quad,
        "BL": bl_quad, "BR": br_quad
    }

    # Get the set of unique non-zero numbers within each quadrant
    quadrant_non_zeros = {name: get_unique_non_zeros(q) for name, q in quadrants.items()}

    # Collect all unique non-zero values present across all quadrants
    all_non_zeros = set().union(*quadrant_non_zeros.values())

    # If no non-zero numbers exist in any quadrant, return an empty list.
    if not all_non_zeros:
        # This could happen if quadrants are empty or contain only zeros.
        return []

    # Determine which non-zero values are unique to a single quadrant
    value_locations = {} # Dictionary mapping value -> list of quadrant names
    for val in all_non_zeros:
        locations = []
        for name, non_zeros_set in quadrant_non_zeros.items():
            if val in non_zeros_set:
                locations.append(name)
        value_locations[val] = locations

    # Find values that appear in exactly one quadrant
    unique_values = {val: locs[0] for val, locs in value_locations.items() if len(locs) == 1}

    selected_quad_name = None

    # --- Selection Logic ---
    if unique_values:
        # Rule 1: If unique values exist, find the maximum among them
        max_unique_val = max(unique_values.keys())
        # The selected quadrant is the one containing this max unique value
        selected_quad_name = unique_values[max_unique_val]
    else:
        # Rule 2: If no unique values, find the overall maximum non-zero value (M)
        M = max(
---
