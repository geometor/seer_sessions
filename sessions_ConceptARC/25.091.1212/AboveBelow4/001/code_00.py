import numpy as np
from typing import List, Tuple, Dict, Any

"""
Identify the unique horizontal line that spans the full width of the input grid.
Record its color (line_color) and row index (line_row).
Identify all distinct horizontal, contiguous blocks of pixels whose color is 
neither white (0) nor line_color.
Create a copy of the input grid to serve as the output grid.
For each identified block:
  Determine its row index (block_row), leftmost column index (col_start), 
  and rightmost column index (col_end).
  Compare block_row to line_row:
    If block_row < line_row (block is above the line), update the pixel at 
      (block_row, col_start) in the output grid to line_color.
    If block_row > line_row (block is below the line), update the pixel at 
      (block_row, col_end) in the output grid to line_color.
Return the modified output grid.
"""

def find_reference_line(grid: np.ndarray) -> Tuple[int, int]:
    """
    Finds the horizontal line spanning the grid width.

    Args:
        grid: The input grid as a numpy array.

    Returns:
        A tuple (line_color, line_row) if found, otherwise raises ValueError.
    """
    height, width = grid.shape
    for r in range(height):
        row = grid[r, :]
        first_pixel_color = row[0]
        if first_pixel_color != 0 and np.all(row == first_pixel_color):
            # Check if it truly spans the whole width (might be redundant if np.all passed)
             if len(np.unique(row)) == 1:
                 return int(first_pixel_color), r
    raise ValueError("No reference line found in the grid.")

def find_target_blocks(grid: np.ndarray, line_color: int, line_row: int) -> List[Dict[str, Any]]:
    """
    Finds all horizontal blocks that are not the background or the reference line.

    Args:
        grid: The input grid as a numpy array.
        line_color: The color of the reference line.
        line_row: The row index of the reference line.

    Returns:
        A list of dictionaries, each representing a block with keys:
        'row', 'col_start', 'col_end', 'color'.
    """
    blocks = []
    height, width = grid.shape
    processed = np.zeros_like(grid, dtype=bool) # Keep track of visited block pixels

    for r in range(height):
        if r == line_row: # Skip the reference line itself
            continue
        for c in range(width):
            if processed[r, c]:
                continue

            pixel_color = grid[r, c]
            # Check if the pixel is part of a potential target block
            if pixel_color != 0 and pixel_color != line_color:
                # Found the start of a potential block
                col_start = c
                col_end = c
                # Find the end of the horizontal contiguous block of the same color
                while col_end + 1 < width and grid[r, col_end + 1] == pixel_color:
                    col_end += 1
                    # Ensure we don't process parts of the same block multiple times
                    if col_end < width:
                         processed[r, col_end] = True

                # Store block information
                blocks.append({
                    'row': r,
                    'col_start': col_start,
                    'col_end': col_end,
                    'color': int(pixel_color)
                })

                # Mark the starting pixel as processed
                processed[r, c] = True
                # Important: The outer loop continues, but inner checks `processed`
            else:
                 # Mark non-target pixels as processed so we don't re-check them
                 processed[r, c] = True

    return blocks

def transform(input_grid: List[List[int]]) -> List[List[int]]:
    """
    Applies the transformation rule to the input grid.
    Identifies a horizontal reference line and modifies specific pixels
    in other horizontal blocks based on their position relative to the line.

    Args:
        input_grid: A list of lists representing the input grid.

    Returns:
        A list of lists representing the transformed output grid.
    """
    # Convert input to numpy array for easier manipulation
    grid_np = np.array(input_grid, dtype=int)
    output_grid_np = grid_np.copy()
    height, width = grid_np.shape

    # 1. Identify the unique horizontal reference line
    try:
        line_color, line_row = find_reference_line(grid_np)
    except ValueError as e:
        print(f"Error: {e}")
        # Handle error case: maybe return input grid or raise further
        return input_grid # Return original if line not found as per examples

    # 2. Identify all target horizontal blocks
    target_blocks = find_target_blocks(grid_np, line_color, line_row)

    # 3. Apply modifications to the output grid based on block position
    for block in target_blocks:
        block_row = block['row']
        col_start = block['col_start']
        col_end = block['col_end']

        # Determine which pixel to change based on position relative to the line
        if block_row < line_row:
            # Block is above the line: change leftmost pixel
            output_grid_np[block_row, col_start] = line_color
        elif block_row > line_row:
            # Block is below the line: change rightmost pixel
            output_grid_np[block_row, col_end] = line_color
        # Blocks on the same row as the line are ignored (and shouldn't be found by find_target_blocks)

    # Convert back to list of lists for the required output format
    output_grid = output_grid_np.tolist()
    return output_grid
