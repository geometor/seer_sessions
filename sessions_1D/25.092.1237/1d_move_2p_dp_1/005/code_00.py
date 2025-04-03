"""
Transformation Rule:
Given a 1xN grid (represented as a 2D NumPy array), identify the single red pixel (2). 
Identify the contiguous block of non-white (0), non-red (2) pixels located immediately to the left of two white (0) separator pixels, which are themselves immediately to the left of the red pixel. 
Swap the positions of this colored block segment and the two white separator pixels segment within the row. 
All other pixels (leading background, red pixel, trailing background) remain in their relative positions.
The output grid has the same shape as the input grid.
"""

import numpy as np
from typing import Tuple, Optional

# --- Helper Functions ---

def find_single_pixel_coords(grid_row: np.ndarray, color: int) -> Optional[int]:
    """Finds the column index of the single pixel with the specified color in a 1D array (row)."""
    indices = np.where(grid_row == color)[0]
    if len(indices) == 1:
        return indices[0]
    # Return None if not found or multiple found, indicating an unexpected state
    elif len(indices) == 0:
        print(f"Warning: Pixel with color {color} not found.")
        return None
    else:
        print(f"Warning: Multiple pixels with color {color} found.")
        return None # Or potentially indices[0] if we assume the first one matters

def find_colored_block_indices_in_row(grid_row: np.ndarray, search_end_col: int) -> Optional[Tuple[int, int]]:
    """
    Finds the start and end column indices of a contiguous block of non-white, non-red pixels
    ending immediately before search_end_col in a 1D NumPy array (row).
    Returns (start_col, end_col) or None if not found or invalid structure.
    """
    if search_end_col <= 0:
        # Cannot have a block ending before column 0
        return None

    block_end_col = search_end_col - 1
    if block_end_col < 0:
         # Should not happen if search_end_col > 0, but safe check
         return None

    block_color = grid_row[block_end_col]

    # Check if the color is valid for a 'colored block' (not white, not red)
    if block_color == 0 or block_color == 2:
         # The pixel immediately left of the separators is not a colored block start
         return None

    block_start_col = block_end_col
    # Iterate leftwards to find where the block starts
    while block_start_col > 0 and grid_row[block_start_col - 1] == block_color:
        block_start_col -= 1

    # Optional: Check if the pixel before the block start is white or if it's the beginning of the array
    # if block_start_col > 0 and grid_row[block_start_col - 1] != 0:
    #     print(f"Warning: Pixel before block start (col {block_start_col - 1}) is not white (0).")
        # pass # Relaxing this constraint as per previous analysis

    return block_start_col, block_end_col

# --- Main Transformation Function ---

def transform(input_grid: np.ndarray) -> np.ndarray:
    """
    Applies the transformation rule to the input 2D NumPy array.
    """
    # Ensure input is a 2D NumPy array
    if not isinstance(input_grid, np.ndarray) or input_grid.ndim != 2:
         raise ValueError("Input grid must be a 2-dimensional NumPy array.")

    # Assume transformation operates on the first row if multiple rows exist,
    # or the only row if shape is (1, N).
    if input_grid.shape[0] == 0 or input_grid.shape[1] == 0:
         print("Warning: Input grid is empty.")
         return input_grid # Return empty grid

    # Work on a copy to avoid modifying the original input array
    output_grid = np.copy(input_grid)
    grid_row = output_grid[0] # Operate on the first row

    # 1. Find the column index of the red pixel (marker)
    red_col = find_single_pixel_coords(grid_row, 2)
    if red_col is None:
        print("Error: Red pixel (2) marker not found or ambiguous. Returning original grid.")
        return input_grid # Cannot proceed without the marker

    # 2. Verify the two white separator pixels exist immediately to the left
    if red_col < 2:
        print(f"Error: Red pixel at column {red_col} is too close to the start for separators. Returning original grid.")
        return input_grid
    if not (grid_row[red_col - 1] == 0 and grid_row[red_col - 2] == 0):
        print(f"Error: Expected white separator pixels (0, 0) at columns {red_col - 2}, {red_col - 1}. Returning original grid.")
        return input_grid # Structure mismatch

    white_sep_start_col = red_col - 2

    # 3. Find the indices (start_col, end_col) of the colored block immediately left of separators
    block_indices = find_colored_block_indices_in_row(grid_row, white_sep_start_col)
    if block_indices is None:
        print(f"Error: Could not find valid colored block ending at column {white_sep_start_col - 1}. Returning original grid.")
        return input_grid # Structure mismatch

    block_start_col, block_end_col = block_indices

    # 4. Extract the segments of the row using NumPy slicing
    leading_segment = grid_row[:block_start_col]
    colored_block_segment = grid_row[block_start_col : block_end_col + 1]
    white_separator_segment = grid_row[white_sep_start_col : red_col] # Cols white_sep_start_col, white_sep_start_col + 1
    red_pixel_segment = grid_row[red_col : red_col + 1] # Just the red pixel at red_col
    trailing_segment = grid_row[red_col + 1 :]

    # 5. Construct the new row by concatenating segments in the swapped order
    new_row = np.concatenate([
        leading_segment,
        white_separator_segment, # Separators move left
        colored_block_segment,   # Block moves right
        red_pixel_segment,       # Red pixel stays
        trailing_segment         # Trailing part stays
    ])

    # 6. Place the modified row back into the output grid
    output_grid[0] = new_row

    return output_grid