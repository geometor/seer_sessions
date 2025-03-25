"""
1.  **Identify Largest Contiguous Block:** In the input grid, find the largest contiguous block of non-zero pixels. Contiguous means that the pixels are connected horizontally, vertically.

2. **Determine Bounding Box:** Draw an imaginary bounding box that encloses the entire contiguos block. The bounding box should have sides parallel with the input grid and be as small as it can and still include all pixels of the contiguos block.

3. **Sample pixels** Sample pixels from the bounding box corners.

    *   output[0,0] = top-left corner
    *   output[0,1] = top-right corner
    *    output[1,0] = bottom-left corner
    *    output[1,1] = bottom-right corner

4. **Construct output grid**: Construct 2x2 output array

5.  **Populate Output:** Populate the output grid using values from the input array.

"""

import numpy as np

def find_largest_contiguous_block(grid):
    """Finds the largest contiguous block of non-zero pixels and returns its bounding box."""
    rows, cols = grid.shape
    visited = np.zeros((rows, cols), dtype=bool)
    max_size = 0
    bounding_box = None

    def dfs(row, col, current_block):
        """Depth-first search to explore contiguous non-zero pixels."""
        if row < 0 or row >= rows or col < 0 or col >= cols or visited[row, col] or grid[row, col] == 0:
            return
        visited[row, col] = True
        current_block.append((row, col))
        dfs(row + 1, col, current_block)
        dfs(row - 1, col, current_block)
        dfs(row, col + 1, current_block)
        dfs(row, col - 1, current_block)

    for i in range(rows):
        for j in range(cols):
            if grid[i, j] != 0 and not visited[i, j]:
                current_block = []
                dfs(i, j, current_block)
                if len(current_block) > max_size:
                    max_size = len(current_block)
                    min_row = min(current_block, key=lambda x: x[0])[0]
                    max_row = max(current_block, key=lambda x: x[0])[0]
                    min_col = min(current_block, key=lambda x: x[1])[1]
                    max_col = max(current_block, key=lambda x: x[1])[1]
                    bounding_box = (min_row, min_col, max_row, max_col)

    return bounding_box

def transform(input_grid):
     # Convert input to numpy array
    input_grid = np.array(input_grid)

     # find the largest contiguos block
    bounding_box = find_largest_contiguous_block(input_grid)

    if bounding_box is None:
          return [[]]

    min_row, min_col, max_row, max_col = bounding_box

    # Construct 2x2 output array
    output_grid = np.zeros((2,2), dtype=int)

    # Sample from the corners
    output_grid[0,0] = input_grid[min_row, min_col]
    output_grid[0,1] = input_grid[min_row,max_col]
    output_grid[1,0] = input_grid[max_row, min_col]
    output_grid[1,1] = input_grid[max_row, max_col]

    return output_grid.tolist()