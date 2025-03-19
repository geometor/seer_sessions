# 9f236235 • 012 • refine_coder

---
```python
"""
Transforms a large grid containing colored rectangular blocks into a smaller grid,
representing the presence and relative positions of the colored blocks. The
transformation identifies red (2), blue (1), and green (3) blocks, selects a
single pixel from each, and places them in the output grid, maintaining their
relative positions.
"""

import numpy as np

def find_colored_blocks(grid):
    """Finds distinct colored blocks (2, 1, 3) in the grid."""
    blocks = {}
    visited = set()
    block_id = 0

    def is_valid(r, c):
        return 0 <= r < grid.shape[0] and 0 <= c < grid.shape[1]

    def dfs(r, c, color, block):
        if (r, c) in visited or not is_valid(r, c) or grid[r, c] != color:
            return
        visited.add((r, c))
        block.append((r, c))
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            dfs(r + dr, c + dc, color, block)

    for r in range(grid.shape[0]):
        for c in range(grid.shape[1]):
            color = grid[r, c]
            if color in [2, 1, 3] and (r, c) not in visited:
                block = []
                dfs(r, c, color, block)
                blocks[block_id] = {"color": color, "pixels": block}
                block_id += 1
    return blocks

def calculate_centroids(blocks):
    """Calculates the centroid for each block."""
    centroids = {}
    for block_id, block_data in blocks.items():
        pixels = block_data["pixels"]
        centroid_row = sum(r for r, _ in pixels) / len(pixels)
        centroid_col = sum(c for _, c in pixels) / len(pixels)
        centroids[block_id] = (centroid_row, centroid_col)
    return centroids

def determine_output_grid_size(num_blocks):
    """Determine the output grid size"""
    rows = int(np.ceil(np.sqrt(num_blocks)))
    cols = int(np.ceil(num_blocks / rows))

    return rows, cols

def transform(input_grid):
    # Convert input_grid to a NumPy array
    input_grid = np.array(input_grid)

    # Find colored blocks (2, 1, 3)
    colored_blocks = find_colored_blocks(input_grid)

    # Calculate centroids
    centroids = calculate_centroids(colored_blocks)
    
    # Determine Output Grid Size
    num_blocks = len(colored_blocks)
    rows, cols = determine_output_grid_size(num_blocks)
    
    # Initialize output_grid 
    output_grid = np.zeros((rows, cols), dtype=int)
    

    # Normalize centroids to output grid dimensions
    normalized_centroids = {}
    for block_id, (centroid_row, centroid_col) in centroids.items():
        #Simple scaling, potential for improvement with relative comparisons
        norm_row = int((centroid_row / input_grid.shape[0]) * rows)
        norm_col = int((centroid_col / input_grid.shape[1]) * cols)
        normalized_centroids[block_id] = (norm_row, norm_col)

    # Place one representative pixel from each block into the output grid
    for block_id, block_data in colored_blocks.items():
        color = block_data["color"]
        row, col = normalized_centroids[block_id]
        
        #Handle potential collisions, ensure we stay in bounds
        while output_grid[row,col] != 0:
          col += 1
          if col >= output_grid.shape[1]:
            col = 0
            row = (row + 1) % output_grid.shape[0]
        
        output_grid[row, col] = color

    return output_grid
```
