import numpy as np
import copy

"""
The transformation rule operates on a 2D grid of digits. It identifies horizontal
separator rows (all 4s) and vertical separator columns (containing 4s in horizontal
separator rows). These separators define horizontal segments and vertical regions
within the grid.

The core logic involves replacing placeholder digits '1' with 'key' digits
(non-zero, non-1, non-4, i.e., 2, 3, 5, 6, 7, 8). The replacement rule depends
on the number of unique key digits found within each horizontal segment:

1.  **One Unique Key:** If a segment contains exactly one unique key digit, all
    '1's within that segment are replaced by that single key digit.
2.  **Zero Unique Keys:** If a segment contains no key digits (only 0s, 1s, and 4s),
    each '1' within that segment is replaced by the key digit associated with its
    corresponding vertical region in the *most recently processed segment that
    contained keys*.
3.  **Multiple Unique Keys:** If a segment contains more than one unique key digit,
    the '1's within that segment remain unchanged.

Key digits within a segment are associated with the vertical region they reside in.
The first key digit encountered when scanning a region (top-to-bottom,
left-to-right within rows) is typically used to define the region's key for
that segment. This region-to-key mapping is stored (in key_memory) and potentially
used by subsequent segments that lack their own keys. Horizontal separator rows
remain unchanged in the output.
"""

# --- Helper Functions ---

def _find_horizontal_separators(grid: np.ndarray) -> list[int]:
    """Finds the indices of rows that consist entirely of the separator digit (4)."""
    separator_rows = []
    separator_value = 4
    # Iterate through rows and check if all elements are the separator value
    for r_idx, row in enumerate(grid):
        if np.all(row == separator_value):
            separator_rows.append(r_idx)
    return separator_rows

def _find_vertical_separators(grid: np.ndarray, horizontal_separator_rows: list[int]) -> list[int]:
    """Finds the indices of columns that contain the separator digit (4) in at least one horizontal separator row."""
    separator_cols = set() # Use a set to automatically handle duplicates
    separator_value = 4
    # If there are no horizontal separators, there can be no vertical separators defined by them
    if not horizontal_separator_rows: 
        return []

    num_cols = grid.shape[1]
    # Check each column
    for c_idx in range(num_cols):
        # Check if this column contains a separator value in any of the horizontal separator rows
        for r_idx in horizontal_separator_rows:
             # Ensure row index is valid before accessing grid element
            if 0 <= r_idx < grid.shape[0] and grid[r_idx, c_idx] == separator_value:
                separator_cols.add(c_idx)
                break # Found a separator in this column, no need to check other rows
    return sorted(list(separator_cols)) # Return a sorted list of unique column indices

def _get_vertical_region_index(col: int, vertical_separator_cols: list[int]) -> int:
    """Determines the 0-based vertical region index for a given column index."""
    region_index = 0
    # Iterate through the separator column indices
    for sep_col in vertical_separator_cols:
        # If the column is to the left of the current separator, it belongs to the current region index
        if col < sep_col:
            return region_index
        # Otherwise, it's in a region further to the right
        region_index += 1
    # If the column is not less than any separator column, it's in the last region
    return region_index

# --- Main Transformation Function ---

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Applies the transformation rule to the input grid.
    """
    # Convert input list-of-lists to numpy array for efficient operations
    grid_np = np.array(input_grid, dtype=int)
    # Initialize the output grid as a copy of the input
    # Modifications will be made directly to this copy
    output_grid_np = grid_np.copy()
    num_rows, num_cols = grid_np.shape

    # Identify horizontal and vertical separators using helper functions
    horizontal_separator_rows = _find_horizontal_separators(grid_np)
    vertical_separator_cols = _find_vertical_separators(grid_np, horizontal_separator_rows)

    # Initialize memory to store region-to-key mapping from the last segment containing keys
    key_memory = {}

    # Define segment boundaries based on horizontal separators
    # Start indices include 0 and the row after each separator
    segment_starts = [0] + [r + 1 for r in horizontal_separator_rows]
    # End indices include the separator rows themselves and the total number of rows
    segment_ends = [r for r in horizontal_separator_rows] + [num_rows]

    # Define the set of digits that act as keys
    key_digits = {2, 3, 5, 6, 7, 8} 

    # Iterate through each horizontal segment
    for i in range(len(segment_starts)):
        r_start = segment_starts[i]
        r_end = segment_ends[i]

        # Skip processing for empty segments or rows that are themselves separators
        if r_start >= r_end or r_start in horizontal_separator_rows:
            continue 

        # Analyze the current segment using the *original* input grid
        unique_keys_in_segment = set()
        current_segment_region_keys = {}

        # Scan cells within the segment to find keys and map them to regions
        for r in range(r_start, r_end):
            for c in range(num_cols):
                val = grid_np[r, c]
                # Check if the cell value is a key digit
                if val in key_digits:
                    # Record the unique key
                    unique_keys_in_segment.add(val)
                    # Determine the vertical region index for this key
                    v_idx = _get_vertical_region_index(c, vertical_separator_cols)
                    # Store the first key found for each region within this segment
                    if v_idx not in current_segment_region_keys:
                        current_segment_region_keys[v_idx] = val

        # Determine the number of unique keys found in this segment
        num_unique_keys = len(unique_keys_in_segment)

        # Apply replacement rules based on the number of unique keys (modify output_grid_np)
        if num_unique_keys == 1:
            # Rule 1: Single unique key -> replace all '1's in this segment with this key
            segment_key = list(unique_keys_in_segment)[0]
            for r in range(r_start, r_end):
                for c in range(num_cols):
                    # Check the original grid for placeholder '1'
                    if grid_np[r, c] == 1:
                        # Modify the output grid
                        output_grid_np[r, c] = segment_key
        elif num_unique_keys == 0:
            # Rule 2: No unique keys -> replace '1's using key_memory based on region
            # Only attempt replacement if key_memory is not empty
            if key_memory: 
                for r in range(r_start, r_end):
                    for c in range(num_cols):
                        # Check the original grid for placeholder '1'
                        if grid_np[r, c] == 1:
                            v_idx = _get_vertical_region_index(c, vertical_separator_cols)
                            # If this region had a key in the last relevant segment, replace '1'
                            if v_idx in key_memory:
                                # Modify the output grid
                                output_grid_np[r, c] = key_memory[v_idx]
        # else num_unique_keys > 1:
            # Rule 3: Multiple unique keys -> do nothing. 
            # '1's remain unchanged as they were copied initially.
            pass

        # Update the key memory *if* keys were found in the current segment
        # This memory will be used by subsequent segments that have zero keys.
        if current_segment_region_keys: # Check if the map is non-empty (i.e., keys were found)
            key_memory = current_segment_region_keys.copy() # Use copy to store the state for the next iteration

    # Convert the final numpy array back to a standard list of lists for the return value
    return output_grid_np.tolist()