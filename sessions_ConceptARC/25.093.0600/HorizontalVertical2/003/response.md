```python
import numpy as np
from collections import deque

"""
Transforms the input grid based on the properties of connected non-zero blocks.

Rule:
1. Identify all connected blocks of non-zero numbers. Calculate their sum, size (number of cells), and maximum row index (bottom extent).
2. **Special Case:** If exactly two blocks exist and they have the same size, return an all-zero grid.
3. Otherwise, find the maximum sum and maximum size among all blocks.
4. Identify candidate blocks: A block is a candidate if its sum equals the maximum sum OR its size equals the maximum size.
5. Find the maximum bottom extent (maximum row index) among all candidate blocks.
6. Select the final blocks: These are the candidate blocks whose bottom extent equals the maximum bottom extent found in step 5.
7. Create an output grid filled with zeros. Copy the cells from the finally selected blocks (from step 6) into the output grid at their original positions.
"""

def find_blocks_with_properties(grid):
    """
    Identifies connected blocks of non-zero cells and calculates their properties.

    Args:
        grid: A NumPy array representing the input grid.

    Returns:
        A list of dictionaries, where each dictionary represents a block
        and contains: 'coords' (list of (r, c) tuples), 'sum', 'size', 'max_r'.
        Returns an empty list if no non-zero cells are found.
    """
    rows, cols = grid.shape
    visited = np.zeros_like(grid, dtype=bool)
    blocks_data = []

    for r in range(rows):
        for c in range(cols):
            # Start BFS if a non-zero cell is found that hasn't been visited
            if grid[r, c] != 0 and not visited[r, c]:
                current_block_coords = []
                q = deque([(r, c)])
                visited[r, c] = True
                block_sum = 0
                max_r_in_block = -1

                while q:
                    curr_r, curr_c = q.popleft()
                    current_block_coords.append((curr_r, curr_c))
                    block_sum += grid[curr_r, curr_c]
                    max_r_in_block = max(max_r_in_block, curr_r)

                    # Explore neighbors (4-connectivity)
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = curr_r + dr, curr_c + dc

                        # Check bounds, non-zero value, and visited status
                        if 0 <= nr < rows and 0 <= nc < cols and \
                           grid[nr, nc] != 0 and not visited[nr, nc]:
                            visited[nr, nc] = True
                            q.append((nr, nc))
                
                # Store properties of the found block
                if current_block_coords:
                    blocks_data.append({
                        'coords': current_block_coords,
                        'sum': block_sum,
                        'size': len(current_block_coords),
                        'max_r': max_r_in_block
                    })
    return blocks_data

def transform(input_grid):
    """
    Applies the transformation rule to the input grid.

    Args:
        input_grid: A list of lists representing the input grid.

    Returns:
        A list of lists representing the transformed grid.
    """
    # Convert input to numpy array for efficient processing
    input_array = np.array(input_grid, dtype=int)
    rows, cols = input_array.shape
    
    # Initialize output grid with zeros
    output_grid = np.zeros_like(input_array)

    # Find all blocks and their properties
    blocks = find_blocks_with_properties(input_array)

    # Handle the case of no blocks
    if not blocks:
        return output_grid.tolist()

    # Special Case: Exactly two blocks of identical size
    if len(blocks) == 2 and blocks[0]['size'] == blocks[1]['size']:
        return output_grid.tolist() # Return the all-zero grid

    # Determine maximum sum and maximum size among all blocks
    max_sum = 0
    max_size = 0
    for block in blocks:
        max_sum = max(max_sum, block['sum'])
        max_size = max(max_size, block['size'])

    # Identify candidate blocks (max sum OR max size)
    candidate_blocks = []
    for block in blocks:
        if block['sum'] == max_sum or block['size'] == max_size:
            candidate_blocks.append(block)

    # Handle the case where no candidates are found (shouldn't happen if blocks exist)
    if not candidate_blocks:
         return output_grid.tolist()

    # Find the maximum bottom extent among candidate blocks
    max_bottom_extent = -1
    for block in candidate_blocks:
        max_bottom_extent = max(max_bottom_extent, block['max_r'])

    # Select final blocks (candidates with the maximum bottom extent)
    final_blocks = []
    for block in candidate_blocks:
        if block['max_r'] == max_bottom_extent:
            final_blocks.append(block)

    # Copy the cells of the final selected blocks to the output grid
    for block in final_blocks:
        for r, c in block['coords']:
            output_grid[r, c] = input_array[r, c]

    # Convert the output NumPy array back to a list of lists
    return output_grid.tolist()
```