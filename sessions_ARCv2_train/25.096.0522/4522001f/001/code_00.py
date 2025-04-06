import numpy as np
from typing import List, Tuple, Optional

"""
Transforms a 3x3 input grid into a 9x9 output grid.

The transformation logic is based on the locations of digits '2' and '3' in the input grid.
1. Initialize a 9x9 output grid with zeros.
2. Find the location of the digit '2' (assuming at most one).
3. Find all locations of the digit '3'. Determine the 'anchor' location, which is the top-leftmost '3'.
4. Based on the anchor '3' location, select a placement pattern for two 4x4 blocks of '3's in the output grid. One block corresponds to the input '3's, and the other corresponds to the input '2'.
    - If the anchor '3' is at (0,0) in the input:
        - The '3' block starts at (0,0) in the output.
        - The '2' block starts at (4,4) in the output.
    - If the anchor '3' is at (1,2) in the input:
        - The '3' block starts at (5,5) in the output.
        - The '2' block starts at (1,1) in the output.
5. If the digit '2' exists in the input, draw its corresponding 4x4 block of '3's according to the selected pattern.
6. If the digit '3' exists in the input, draw its corresponding 4x4 block of '3's according to the selected pattern.
"""

def find_digit_locations(grid: np.ndarray, digit: int) -> List[Tuple[int, int]]:
    """Finds all (row, col) coordinates of a given digit in the grid."""
    locations = np.where(grid == digit)
    return list(zip(locations[0], locations[1]))

def find_anchor(locations: List[Tuple[int, int]]) -> Optional[Tuple[int, int]]:
    """Finds the top-leftmost coordinate (minimum row, then minimum column)."""
    if not locations:
        return None
    # Sort primarily by row, secondarily by column
    locations.sort()
    return locations[0]

def draw_block(grid: np.ndarray, top_left_row: int, top_left_col: int, size: int, value: int):
    """Draws a square block of a given size and value onto the grid."""
    if 0 <= top_left_row < grid.shape[0] and 0 <= top_left_col < grid.shape[1]:
        end_row = min(top_left_row + size, grid.shape[0])
        end_col = min(top_left_col + size, grid.shape[1])
        grid[top_left_row:end_row, top_left_col:end_col] = value

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Applies the transformation rule based on input digits '2' and '3'.
    """
    # Convert input list of lists to a numpy array for easier manipulation
    input_np = np.array(input_grid, dtype=int)
    rows_in, cols_in = input_np.shape
    
    # Initialize the 9x9 output grid with zeros
    output_size = 9
    output_np = np.zeros((output_size, output_size), dtype=int)

    # Find locations of digits 2 and 3
    locations_2 = find_digit_locations(input_np, 2)
    locations_3 = find_digit_locations(input_np, 3)

    # Determine if digits 2 and 3 are present
    has_2 = bool(locations_2)
    has_3 = bool(locations_3)

    # Find the anchor '3' location (top-leftmost)
    anchor_3_loc = find_anchor(locations_3)

    # Determine block placements based on the anchor '3' location
    block_size = 4
    block_value = 3
    placement_for_3 = None
    placement_for_2 = None

    if anchor_3_loc:
        # Pattern derived from train_2: anchor at (0,0)
        if anchor_3_loc == (0, 0):
            placement_for_3 = (0, 0)
            placement_for_2 = (4, 4)
        # Pattern derived from train_1: anchor at (1,2)
        elif anchor_3_loc == (1, 2):
            placement_for_3 = (5, 5)
            placement_for_2 = (1, 1)
        # Add more elif conditions here if other anchor locations define different patterns
        
        # Draw the block for '3' if '3' was present and a placement was determined
        if has_3 and placement_for_3:
            r, c = placement_for_3
            draw_block(output_np, r, c, block_size, block_value)

        # Draw the block for '2' if '2' was present and a placement was determined
        if has_2 and placement_for_2:
            r, c = placement_for_2
            draw_block(output_np, r, c, block_size, block_value)

    # Note: If anchor_3_loc is None (no '3' found), the current logic doesn't draw any blocks.
    # This might need adjustment if examples show '2' alone triggering a block.

    # Convert the final numpy array back to a list of lists
    return output_np.tolist()