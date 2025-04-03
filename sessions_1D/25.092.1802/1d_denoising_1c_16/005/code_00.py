import numpy as np
from typing import List, Tuple, Optional

"""
Identify the largest contiguous vertical block of solid, identically colored, non-white rows in the input grid. 
A solid row consists entirely of a single color that is not white (0).
A block is a vertically contiguous sequence of solid rows that all share the same non-white color.
The largest block is defined as the one with the greatest height (number of rows). If there is a tie in height, 
the block appearing earliest in the grid (lowest starting row index) is chosen.
Preserve only this largest block in the output grid, setting all other pixels to white (0).
If no solid rows or blocks are found, the output grid is entirely white.
"""

# Define type aliases for clarity
Grid = List[List[int]]
SolidRowInfo = Tuple[int, int]  # (row_index, color)
BlockInfo = Tuple[int, int, int, int] # (start_row, end_row, color, height)

def _find_solid_rows(input_array: np.ndarray) -> List[SolidRowInfo]:
    """
    Identifies rows composed of a single non-white color.

    Args:
        input_array: The input grid as a NumPy array.

    Returns:
        A list of tuples, where each tuple contains the row index and the color 
        of a solid non-white row. Returns an empty list if none are found.
    """
    solid_rows: List[SolidRowInfo] = []
    height, _ = input_array.shape
    for r in range(height):
        row = input_array[r, :]
        unique_colors = np.unique(row)
        # Check if the row has exactly one unique color and it's not white (0)
        if len(unique_colors) == 1 and unique_colors[0] != 0:
            solid_rows.append((r, int(unique_colors[0]))) # Store row index and color
    return solid_rows

def _group_solid_rows_into_blocks(solid_rows: List[SolidRowInfo]) -> List[BlockInfo]:
    """
    Groups adjacent solid rows of the same color into blocks.

    Args:
        solid_rows: A list of tuples (row_index, color) representing solid rows,
                    assumed to be sorted by row_index implicitly by _find_solid_rows.

    Returns:
        A list of tuples, where each tuple represents a block:
        (start_row, end_row, color, height). Returns an empty list if no blocks
        can be formed.
    """
    if not solid_rows:
        return []

    blocks: List[BlockInfo] = []
    current_block_start_index = 0
    while current_block_start_index < len(solid_rows):
        start_row, color = solid_rows[current_block_start_index]
        current_height = 1
        
        # Look ahead to find contiguous rows of the same color
        next_row_in_block_idx = current_block_start_index + 1
        while (next_row_in_block_idx < len(solid_rows) and
               solid_rows[next_row_in_block_idx][0] == start_row + current_height and # Check vertical contiguity
               solid_rows[next_row_in_block_idx][1] == color): # Check for the same color
            current_height += 1
            next_row_in_block_idx += 1
            
        end_row = start_row + current_height - 1
        blocks.append((start_row, end_row, color, current_height))
        
        # Move to the start of the next potential block
        # next_row_in_block_idx now points to the first row *not* in the current block
        current_block_start_index = next_row_in_block_idx
        
    return blocks

def _find_largest_block(blocks: List[BlockInfo]) -> Optional[BlockInfo]:
    """
    Selects the largest block based on height from a list of blocks.
    Ties are broken by choosing the block that appears first (lowest start_row).

    Args:
        blocks: A list of block information tuples (start_row, end_row, color, height).

    Returns:
        The tuple representing the largest block, or None if the input list is empty.
    """
    if not blocks:
        return None
        
    # Find the block with the maximum height.
    # max() with a key naturally handles ties by returning the first element 
    # encountered that matches the maximum key value. Since blocks are generated
    # in top-to-bottom order by _group_solid_rows_into_blocks, 
    # this correctly selects the highest block (lowest start_row) in case of ties.
    largest_block = max(blocks, key=lambda item: item[3]) # item[3] is height
    
    return largest_block

def transform(input_grid: Grid) -> Grid:
    """
    Transforms the input grid by finding the largest contiguous block of solid, 
    non-white rows and preserving only that block, making everything else white.
    """
    # Convert input list of lists to a NumPy array for efficient processing.
    # Assumes input_grid is a valid 2D list representation of the grid.
    try:
        input_array = np.array(input_grid, dtype=int)
        if input_array.ndim != 2:
             # Handle potential malformed input (e.g., flat list) by returning an empty grid 
             # or a grid of expected shape filled with 0s, although the ARC standard implies correct shape.
             # Let's assume we should return an all-white grid matching input structure if possible,
             # or fail gracefully if the input structure is completely unusable.
             # For now, return an all-white grid of the same 'structure' if it looks like a list of lists.
             if isinstance(input_grid, list) and all(isinstance(row, list) for row in input_grid):
                 h = len(input_grid)
                 w = len(input_grid[0]) if h > 0 else 0
                 return np.zeros((h, w), dtype=int).tolist()
             else: # Unclear structure, return empty list
                 return [] 
    except ValueError: # Catches issues if lists within the list have different lengths
        # Return empty list or handle error appropriately
        return []
        
    height, width = input_array.shape
    
    # Initialize an output grid of the same dimensions, filled with white (0).
    output_grid = np.zeros_like(input_array)

    # Step 1: Find all rows that consist of a single non-white color.
    solid_rows = _find_solid_rows(input_array)

    # If no solid rows are found, the output is already correctly initialized as all white.
    if not solid_rows:
        return output_grid.tolist()

    # Step 2: Group these solid rows into contiguous vertical blocks of the same color.
    blocks = _group_solid_rows_into_blocks(solid_rows)

    # If no blocks could be formed (e.g., solid rows exist but none are contiguous),
    # the output remains all white.
    if not blocks:
         return output_grid.tolist()

    # Step 3: Identify the largest block based on height (number of rows).
    # Ties are broken by selecting the block that starts at the lowest row index.
    largest_block = _find_largest_block(blocks)

    # Step 4: If a largest block was successfully identified, copy it from the
    # input array to the corresponding location in the otherwise white output grid.
    if largest_block:
        start_r, end_r, _, _ = largest_block
        # Copy the slice corresponding to the largest block from input to output
        output_grid[start_r : end_r + 1, :] = input_array[start_r : end_r + 1, :]

    # Convert the final NumPy array back to a standard list of lists format and return.
    return output_grid.tolist()