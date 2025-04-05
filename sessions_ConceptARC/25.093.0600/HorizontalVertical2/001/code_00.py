import numpy as np
from collections import deque

def find_blocks(grid):
    """
    Identifies connected blocks of non-zero cells in a grid.

    Args:
        grid: A NumPy array representing the input grid.

    Returns:
        A list of blocks, where each block is a list of (row, col) tuples.
    """
    rows, cols = grid.shape
    visited = np.zeros_like(grid, dtype=bool)
    blocks = []

    for r in range(rows):
        for c in range(cols):
            # If the cell is non-zero and not yet visited, start a search (BFS)
            if grid[r, c] != 0 and not visited[r, c]:
                current_block = []
                q = deque([(r, c)])
                visited[r, c] = True

                while q:
                    curr_r, curr_c = q.popleft()
                    current_block.append((curr_r, curr_c))

                    # Check 4 neighbors (up, down, left, right)
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = curr_r + dr, curr_c + dc

                        # Check bounds, non-zero value, and if not visited
                        if 0 <= nr < rows and 0 <= nc < cols and \
                           grid[nr, nc] != 0 and not visited[nr, nc]:
                            visited[nr, nc] = True
                            q.append((nr, nc))
                
                if current_block: # Ensure we found something
                    blocks.append(current_block)
    return blocks

def calculate_block_sum(grid, block_coords):
    """
    Calculates the sum of values for cells within a block.

    Args:
        grid: A NumPy array representing the input grid.
        block_coords: A list of (row, col) tuples representing the block.

    Returns:
        The sum of the values in the specified block coordinates.
    """
    total_sum = 0
    for r, c in block_coords:
        total_sum += grid[r, c]
    return total_sum

"""
Identifies all distinct connected blocks of non-zero numbers in the input grid.
Calculates the sum of the numerical values for each block.
Selects the block with the maximum sum.
Creates an output grid containing only the selected block, with all other cells set to zero.
"""
def transform(input_grid):
    """
    Transforms the input grid by keeping only the connected block of non-zero 
    numbers that has the largest sum of its elements.

    Args:
        input_grid: A list of lists representing the input grid.

    Returns:
        A list of lists representing the transformed grid.
    """
    # Convert input to numpy array for easier processing
    input_array = np.array(input_grid, dtype=int)
    rows, cols = input_array.shape
    
    # Initialize output_grid with zeros, same shape as input
    output_grid = np.zeros_like(input_array)

    # Find all distinct non-zero blocks
    blocks = find_blocks(input_array)

    # If no blocks are found, return the zero grid
    if not blocks:
        return output_grid.tolist()

    # Calculate the sum for each block and find the block with the maximum sum
    max_sum = -1
    best_block = None
    for block in blocks:
        current_sum = calculate_block_sum(input_array, block)
        if current_sum > max_sum:
            max_sum = current_sum
            best_block = block
        # Note: Implicit tie-breaking: the first block encountered with the max sum is chosen.

    # Copy the selected block (the one with the maximum sum) to the output grid
    if best_block:
        for r, c in best_block:
            output_grid[r, c] = input_array[r, c]

    # Convert the output NumPy array back to a list of lists
    return output_grid.tolist()