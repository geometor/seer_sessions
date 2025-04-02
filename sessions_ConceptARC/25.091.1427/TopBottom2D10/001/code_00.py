"""
Identifies distinct horizontal rectangular blocks of non-background color in the input grid.
Determines the vertical order of these blocks based on their top row.
Swaps the first (top-most) and the last (bottom-most) blocks in this vertical sequence.
Reconstructs the stack of blocks in the output grid, starting from the original top row of the stack, 
maintaining the blocks' original horizontal positions, widths, and heights, but using the modified vertical order.
The background color fills the rest of the grid.
"""

import numpy as np
from typing import List, Dict, Tuple, Any

def find_blocks(grid: np.ndarray) -> List[Dict[str, Any]]:
    """
    Finds all distinct, maximal, horizontal rectangular blocks of non-background color.

    Args:
        grid: The input grid as a numpy array.

    Returns:
        A list of dictionaries, where each dictionary represents a block
        and contains 'color', 'top_row', 'left_col', 'height', 'width'.
        Returns an empty list if no non-background blocks are found.
    """
    height, width = grid.shape
    visited = np.zeros_like(grid, dtype=bool)
    blocks = []
    background_color = 0

    for r in range(height):
        for c in range(width):
            color = grid[r, c]
            if color != background_color and not visited[r, c]:
                # Found the start of a potential block
                
                # Find horizontal extent
                start_c = c
                end_c = c
                while end_c + 1 < width and grid[r, end_c + 1] == color and not visited[r, end_c + 1]:
                    end_c += 1
                
                block_width = end_c - start_c + 1

                # Find vertical extent (check if rows below match exactly)
                start_r = r
                end_r = r
                while end_r + 1 < height:
                    match = True
                    for current_c in range(start_c, end_c + 1):
                        if grid[end_r + 1, current_c] != color or visited[end_r + 1, current_c]:
                            match = False
                            break
                    if match:
                        end_r += 1
                    else:
                        break
                
                block_height = end_r - start_r + 1

                # Store block info
                blocks.append({
                    'color': color,
                    'top_row': start_r,
                    'left_col': start_c,
                    'height': block_height,
                    'width': block_width
                })

                # Mark cells as visited
                for row_idx in range(start_r, end_r + 1):
                    for col_idx in range(start_c, end_c + 1):
                        visited[row_idx, col_idx] = True
                        
                # Optimization: continue search after the found block in the current row
                # We already scanned up to end_c for this row 'r'
                # No need to re-check columns start_c to end_c for row 'r'
                # The outer loop's `c` will advance. Correcting this:
                # Actually, the outer loop `c` advancing handles this implicitly
                # because `visited` prevents reprocessing. No explicit `c` jump needed.


    return blocks

def draw_block(output_grid: np.ndarray, block: Dict[str, Any], start_row: int):
    """Draws a block onto the output grid at the specified start row."""
    top = start_row
    bottom = start_row + block['height']
    left = block['left_col']
    right = block['left_col'] + block['width']
    output_grid[top:bottom, left:right] = block['color']


def transform(input_grid: List[List[int]]) -> List[List[int]]:
    """
    Applies the transformation rule: find colored blocks, sort vertically,
    swap top and bottom, reconstruct the stack.

    Args:
        input_grid: A list of lists representing the input grid.

    Returns:
        A list of lists representing the transformed output grid.
    """
    input_arr = np.array(input_grid, dtype=int)
    height, width = input_arr.shape
    background_color = 0

    # Find all colored rectangular blocks
    blocks = find_blocks(input_arr)

    # If no blocks or only one block, return the input as is
    if len(blocks) < 2:
        return input_grid

    # Sort blocks by their top row index to determine vertical order
    blocks.sort(key=lambda b: b['top_row'])

    # Record the original top row of the entire stack
    original_stack_top_row = blocks[0]['top_row']

    # Swap the first (top-most) and last (bottom-most) blocks in the sequence
    blocks[0], blocks[-1] = blocks[-1], blocks[0]

    # Initialize the output grid with the background color
    output_arr = np.full((height, width), background_color, dtype=int)

    # Reconstruct the stack in the output grid
    current_row = original_stack_top_row
    for block in blocks:
        # Draw the block at the current vertical position, using its original horizontal position and dimensions
        draw_block(output_arr, block, current_row)
        # Update the starting row for the next block
        current_row += block['height']

    # Convert the numpy array back to a list of lists
    output_grid = output_arr.tolist()

    return output_grid