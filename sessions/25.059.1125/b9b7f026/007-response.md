# b9b7f026 • 007 • refine_coder

---
```python
"""
1.  **Identify Blocks:** Examine the input grid to find all rectangular, contiguous blocks of pixels that share the same color.  A block can be a single pixel or a larger rectangle. Ignore blocks of color 0 (white, or blank).
2.  **Find Top-Leftmost:** Among the identified blocks, determine the "top-leftmost" block. This is the block whose top-left corner pixel has the smallest row index. If multiple blocks share the same smallest row index, select the one with the smallest column index among those.
3.  **Output Color:** Create a 1x1 output grid.  Fill this grid with the color of the top-leftmost block identified in step 2.
"""

import numpy as np

def find_blocks(grid):
    """
    Identifies rectangular blocks of the same color in a grid.
    Returns a list of tuples: (color, (top_row, left_col), (bottom_row, right_col)).
    """
    blocks = []
    visited = set()
    rows, cols = grid.shape

    def is_valid(r, c):
        return 0 <= r < rows and 0 <= c < cols

    def dfs(r, c, color, top_row, left_col, bottom_row, right_col):
        if (r, c) in visited or not is_valid(r, c) or grid[r, c] != color:
            return top_row, left_col, bottom_row, right_col
        visited.add((r, c))
        top_row = min(top_row, r)
        left_col = min(left_col, c)
        bottom_row = max(bottom_row, r)
        right_col = max(right_col, c)

        # Explore adjacent cells
        top_row, left_col, bottom_row, right_col = dfs(r + 1, c, color, top_row, left_col, bottom_row, right_col)
        top_row, left_col, bottom_row, right_col = dfs(r - 1, c, color, top_row, left_col, bottom_row, right_col)
        top_row, left_col, bottom_row, right_col = dfs(r, c + 1, color, top_row, left_col, bottom_row, right_col)
        top_row, left_col, bottom_row, right_col = dfs(r, c - 1, color, top_row, left_col, bottom_row, right_col)
        return top_row, left_col, bottom_row, right_col

    for r in range(rows):
        for c in range(cols):
            if (r, c) not in visited and grid[r,c] != 0:
                color = grid[r, c]
                top_row, left_col, bottom_row, right_col = dfs(r, c, color, r, c, r, c)
                blocks.append((color, (top_row, left_col), (bottom_row, right_col)))

    return blocks

def transform(input_grid):
    """
    Transforms the input grid according to the rules described above.
    """
    # Convert input_grid to numpy array for easier manipulation
    grid = np.array(input_grid)

    # Find all blocks in the grid.
    blocks = find_blocks(grid)

    # Find the top-leftmost block.
    if blocks:
        top_left_block = min(blocks, key=lambda x: (x[1][0], x[1][1])) # Sort by top row, then left column
        output_color = top_left_block[0]
    else:
        output_color = 0  # Default to 0 if no blocks are found


    # Return a 1x1 grid with the selected output color
    output_grid = np.array([[output_color]])
    return output_grid.tolist()
```

