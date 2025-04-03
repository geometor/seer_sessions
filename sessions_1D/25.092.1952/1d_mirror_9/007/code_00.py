"""
Transforms an input grid by relocating a contiguous colored block based on a marker pixel.
1. Assume the input is a flat list representing a 4x6 grid. Reshape the input list into a 4x6 NumPy array.
2. Create a new 4x6 output grid (NumPy array) and initialize it with the background color (white, 0).
3. Find the coordinates (row R_marker, column C_marker) of the marker pixel (maroon, 9) in the input grid.
4. Find the source row (R_source) in the input grid that contains any color other than white (0) or maroon (9).
5. Within row R_source, identify the contiguous horizontal block of this non-white, non-maroon color. Record its color (C_object), start column (ignored for placement), and length (L_object).
6. Calculate the destination row index R_dest = R_marker + 1.
7. Place the identified object block into the output grid at row R_dest, starting at column 0 and extending for L_object columns, using the color C_object. Ensure placement stays within grid boundaries.
8. Place the marker pixel (maroon, 9) back into the output grid at its original coordinates (R_marker, C_marker).
9. Return the output grid converted back to a list of lists.
"""

import numpy as np

def find_marker(grid, marker_color=9):
    """Finds the coordinates (row, col) of the first occurrence of the marker color."""
    coords = np.argwhere(grid == marker_color)
    if len(coords) > 0:
        return tuple(coords[0]) # Return (row, col)
    else:
        return None # Marker not found

def find_object_block(grid, background_color=0, marker_color=9):
    """
    Finds the properties of the contiguous object block.
    Returns: (source_row_index, object_color, object_start_col, object_length) or None if not found.
    """
    num_rows, num_cols = grid.shape
    for r_idx in range(num_rows):
        row = grid[r_idx, :]
        object_color = -1
        obj_start_col = -1
        obj_length = 0
        in_block = False

        # Find potential object colors in the row
        unique_colors = np.unique(row)
        potential_object_colors = [c for c in unique_colors if c != background_color and c != marker_color]

        if len(potential_object_colors) > 0:
             # Assume the first such color found defines the block for this task
             object_color = potential_object_colors[0]
             for c_idx, pixel in enumerate(row):
                 if pixel == object_color:
                     if not in_block:
                         obj_start_col = c_idx
                         in_block = True
                     obj_length += 1
                 elif in_block:
                      # End of the contiguous block
                      break
             # If a block was found (even if it ends at the edge), return its properties
             if in_block:
                 return r_idx, object_color, obj_start_col, obj_length

    return None # Object block not found

def transform(input_grid):
    """
    Transforms the input grid according to the specified rules.
    """
    # --- Convert input to NumPy array and determine shape ---
    input_arr_flat = np.array(input_grid, dtype=int)
    rows, cols = -1, -1
    assumed_shape = (4, 6) # Based on example analysis

    if input_arr_flat.ndim == 1:
        size = input_arr_flat.shape[0]
        if size == assumed_shape[0] * assumed_shape[1]: # Check if size matches assumption
            try:
                input_arr = input_arr_flat.reshape(assumed_shape)
                rows, cols = assumed_shape
            except ValueError:
                 print(f"Error: Cannot reshape {size}-element flat array to {assumed_shape}.")
                 # Fallback or error handling - return original? empty?
                 # For this task, returning original seems safest if shape is wrong.
                 return input_grid
        else:
            # Cannot determine shape for other sizes from a flat list alone
            print(f"Error: Input is 1D with unexpected size ({size} elements). Cannot process.")
            return input_grid
    elif input_arr_flat.ndim == 2:
         # Input was already likely a list of lists
         input_arr = input_arr_flat # Use it directly
         rows, cols = input_arr.shape
         # Optional: Check if shape matches expected 4x6 if needed?
         # if (rows, cols) != assumed_shape:
         #     print(f"Warning: Input grid is 2D but shape is {input_arr.shape}, not {assumed_shape}.")
    else:
        print(f"Error: Input grid has unexpected dimensions: {input_arr_flat.ndim}")
        return input_grid

    if rows == -1 or cols == -1: # Check if shape determination failed
        # This case should be caught above, but as a safeguard:
        return input_grid

    # --- Initialize output grid ---
    output_grid = np.zeros_like(input_arr)

    # --- Find Marker ---
    marker_coords = find_marker(input_arr, 9)
    if marker_coords is None:
        print("Warning: Marker (9) not found. Returning background grid.")
        return output_grid.tolist()
    marker_row, marker_col = marker_coords

    # --- Find Object Block ---
    object_info = find_object_block(input_arr, 0, 9)

    # --- Perform Transformation ---
    if object_info is not None:
        source_row, obj_color, obj_start_col, obj_length = object_info

        # Calculate destination row and column range
        dest_row = marker_row + 1
        dest_start_col = 0
        dest_end_col = dest_start_col + obj_length # Exclusive index for slicing

        # Place the object block if destination is valid
        if 0 <= dest_row < rows:
            # Ensure the block doesn't go past the right edge
            actual_end_col = min(dest_end_col, cols)
            actual_length = actual_end_col - dest_start_col
            if actual_length > 0: # Check if there's anything to place
                output_grid[dest_row, dest_start_col:actual_end_col] = obj_color
                if actual_length < obj_length:
                    print(f"Warning: Object block truncated during placement. Original length: {obj_length}, Placed length: {actual_length}")
            else:
                 print(f"Warning: Object block destination starts outside grid width. Block not placed.")

        else:
            print(f"Warning: Object destination row {dest_row} is out of bounds ({rows} rows). Object block not placed.")

    else:
        # Object block not found, proceed to place marker only
        print("Warning: Object block not found. Placing only marker.")


    # --- Place Marker ---
    # Always place the marker at its original coordinates, potentially overwriting background
    # or even part of the moved object if coordinates overlap (though not expected in this task)
    output_grid[marker_row, marker_col] = 9


    # --- Return result ---
    # Convert back to list of lists format
    return output_grid.tolist()