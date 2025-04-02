import numpy as np
from collections import namedtuple

# Define a structure to hold block information
Block = namedtuple('Block', ['color', 'height', 'width', 'top_row'])

"""
Identifies distinct horizontal rectangular blocks of non-background color starting at column 0 in the input grid.
Sorts these blocks based on their width in ascending order.
Reconstructs the output grid by placing the sorted blocks vertically, starting from the minimum top row occupied by any block in the original input, preserving their original height, width, and color. Blocks are placed starting at column 0.
"""

def _find_blocks(grid: np.ndarray) -> tuple[list[Block], int]:
    """
    Finds all distinct horizontal rectangular blocks starting at column 0.

    Args:
        grid (np.ndarray): The input grid.

    Returns:
        tuple[list[Block], int]: A tuple containing:
            - A list of Block namedtuples found.
            - The minimum top_row index among all found blocks (or grid height if none found).
    """
    height, width = grid.shape
    visited = np.zeros_like(grid, dtype=bool)
    blocks = []
    min_original_top_row = height # Initialize high

    # Iterate through rows, checking the first column for potential block starts
    for r in range(height):
        # Check column 0 for a non-background color that hasn't been visited
        if grid[r, 0] != 0 and not visited[r, 0]:
            color = grid[r, 0]
            
            # Determine width by scanning right from (r, 0)
            current_width = 0
            for c in range(width):
                if grid[r, c] == color:
                    current_width += 1
                else:
                    break # Width ends here

            if current_width == 0: # Should not happen with grid[r,0] != 0 check, but safe
                continue

            # Determine height by scanning down
            current_height = 0
            for h_idx in range(r, height):
                row_matches = True
                # Check if the segment matches the color
                for w_idx in range(current_width):
                    if h_idx >= height or grid[h_idx, w_idx] != color:
                        row_matches = False
                        break
                if not row_matches:
                    break # Height ends here
                
                # Check if the block incorrectly extends further right in this row
                if current_width < width and grid[h_idx, current_width] == color:
                    row_matches = False
                    break # This isn't a clean rectangle of current_width

                # If row matches and doesn't extend, increment height
                if row_matches:
                    current_height += 1
                else: # Should be caught by breaks above, but double-check
                    break

            # If a valid block is found (height > 0)
            if current_height > 0:
                # Store block info
                block = Block(color=color, height=current_height, width=current_width, top_row=r)
                blocks.append(block)
                
                # Update minimum starting row
                if r < min_original_top_row:
                    min_original_top_row = r

                # Mark visited cells for this block
                for r_visit in range(r, r + current_height):
                    for c_visit in range(current_width):
                         # Check bounds before marking visited
                        if r_visit < height and c_visit < width:
                            visited[r_visit, c_visit] = True
            
            # Skip rows already part of the detected block
            # Note: The outer loop continues, but visited check prevents reprocessing
            
    # If no blocks found, set min_top_row to 0 for default behavior if needed,
    # though the main function handles the empty block list.
    if not blocks:
        min_original_top_row = 0
        
    return blocks, min_original_top_row


def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Transforms the input grid by rearranging horizontal blocks based on width.

    Args:
        input_grid (list[list[int]]): The input grid represented as a list of lists.

    Returns:
        list[list[int]]: The transformed grid.
    """
    # Convert input to numpy array for easier manipulation
    input_grid_np = np.array(input_grid, dtype=int)
    height, width = input_grid_np.shape
    background_color = 0 # Assuming white background

    # 1. Find all distinct horizontal rectangular blocks starting at col 0
    #    and the minimum original top row they occupy.
    blocks, min_original_top_row = _find_blocks(input_grid_np)

    # 2. Handle edge case: No blocks found, return the original grid.
    if not blocks:
        return input_grid # Return original list of lists

    # 3. Sort the blocks based on their width in ascending order.
    sorted_blocks = sorted(blocks, key=lambda b: b.width)

    # 4. Create a new output grid filled with the background color.
    output_grid = np.full_like(input_grid_np, background_color)

    # 5. Initialize the starting row for placing blocks in the output grid.
    current_row = min_original_top_row

    # 6. Iterate through sorted blocks and place them onto the output grid.
    for block in sorted_blocks:
        # Get block properties
        color = block.color
        block_height = block.height
        block_width = block.width
        start_col = 0 # Blocks always start at column 0

        # Calculate end row and column, ensuring they don't exceed grid bounds
        end_row = min(current_row + block_height, height)
        end_col = min(start_col + block_width, width)

        # Place the block onto the output grid
        output_grid[current_row:end_row, start_col:end_col] = color

        # Update the current row for the next block
        current_row += block_height # Next block starts immediately below

    # 7. Convert the output numpy array back to a list of lists and return.
    return output_grid.tolist()