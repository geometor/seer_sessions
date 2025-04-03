"""
Transformation Rule:
Identify all contiguous blocks of maroon (9) pixels in the input 2D grid using 4-neighbor connectivity. 
Calculate the area (number of pixels) of each block.
Find the maximum area among all identified maroon blocks.
Change the color of all pixels belonging to any block whose area equals this maximum area to azure (8).
All other pixels (white pixels and pixels in maroon blocks smaller than the maximum area) remain unchanged.
"""

import numpy as np
from typing import List, Dict, Tuple, Set

def find_contiguous_blocks_2d(grid: np.ndarray, target_color: int) -> List[Dict]:
    """
    Finds contiguous blocks (4-connectivity) of a target color in a 2D grid.

    Args:
        grid: The input 2D numpy array representing the grid.
        target_color: The integer value of the color to find blocks of.

    Returns:
        A list of dictionaries, where each dictionary represents a block
        and contains 'pixels' (a list of (row, col) tuples) and 'size' (int).
    """
    rows, cols = grid.shape
    visited: Set[Tuple[int, int]] = set() # Use a set for faster lookups
    blocks: List[Dict] = []

    for r in range(rows):
        for c in range(cols):
            # If the cell has the target color and hasn't been visited yet
            if grid[r, c] == target_color and (r, c) not in visited:
                # Start a Breadth-First Search (BFS) to find the connected block
                current_block_pixels: List[Tuple[int, int]] = []
                q: List[Tuple[int, int]] = [(r, c)]
                visited.add((r, c))

                while q:
                    row, col = q.pop(0) # Get the next pixel from the queue
                    current_block_pixels.append((row, col)) # Add it to the current block

                    # Check neighbors (4-connectivity: up, down, left, right)
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = row + dr, col + dc
                        # Check bounds and if the neighbor is the target color and not visited
                        if 0 <= nr < rows and 0 <= nc < cols and \
                           grid[nr, nc] == target_color and (nr, nc) not in visited:
                            visited.add((nr, nc)) # Mark neighbor as visited
                            q.append((nr, nc)) # Add neighbor to the queue

                # Finished finding all pixels for this block
                if current_block_pixels:
                    blocks.append({'pixels': current_block_pixels, 'size': len(current_block_pixels)})
    return blocks

def transform(input_grid: np.ndarray) -> np.ndarray:
    """
    Applies the transformation rule to the input grid.

    Args:
        input_grid: A 2D numpy array representing the input grid.

    Returns:
        A 2D numpy array representing the transformed output grid.
    """
    maroon_color = 9
    azure_color = 8

    # 1. Find all contiguous blocks of maroon
    maroon_blocks = find_contiguous_blocks_2d(input_grid, maroon_color)

    # 2. Handle the case where no maroon blocks are found
    if not maroon_blocks:
        return np.copy(input_grid) # Return an unchanged copy

    # 3. Determine the maximum block size
    max_size = 0
    for block in maroon_blocks:
        if block['size'] > max_size:
            max_size = block['size']
    
    # Alternatively using max()
    # if maroon_blocks: # ensure list is not empty
    #     max_size = max(block['size'] for block in maroon_blocks)
    # else:
    #     return np.copy(input_grid) # Should be covered by earlier check, but safe

    # 4. Initialize the output grid as a copy of the input
    output_grid = np.copy(input_grid)

    # 5. Iterate through the blocks and transform the largest ones
    for block in maroon_blocks:
        # 6. Check if the current block's size is the maximum size
        if block['size'] == max_size:
            # 7. Change the color of all pixels in this block to azure
            for r, c in block['pixels']:
                output_grid[r, c] = azure_color

    # 8. Return the modified grid
    return output_grid