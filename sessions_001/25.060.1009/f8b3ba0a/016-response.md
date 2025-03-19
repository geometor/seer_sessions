# f8b3ba0a • 016 • example_3 • investigate_coder

---
```python
"""
1. **Identify Blocks:** Scan the input grid to find all 2x2 square regions where all four pixels have the same non-zero color.
2. **Ignore Background:** Disregard any rows that consist entirely of '0' (white) pixels.
3. **Extract Color:** For each identified 2x2 block, record the color value (the number) of the pixels within that block.
4. **Order Colors:** Sort the extracted color in ascending order by the row that they appear. The first one appears on row 4, the second on row 8, and the third on row 10.
5. **Build Output:** Create an output sequence which contains the sorted colors, where each is a separate entry presented as single stacked values.
"""

import numpy as np

def find_2x2_blocks(grid):
    """Finds all 2x2 blocks of the same non-zero color."""
    blocks = []
    rows, cols = grid.shape
    for i in range(rows - 1):
        for j in range(cols - 1):
            block = grid[i:i+2, j:j+2]
            if np.all(block == block[0, 0]) and block[0, 0] != 0:
                blocks.append((i, j, block[0, 0]))  # (row, col, color)
    return blocks

def transform(input_grid):
    # Convert input grid to a NumPy array
    grid = np.array(input_grid)

    # Find all 2x2 blocks
    blocks = find_2x2_blocks(grid)

    # Extract the color and row number of each block
    color_row_pairs = [(color, row) for row, _, color in blocks]

    # Sort by row number to ensure the correct output
    color_row_pairs.sort(key=lambda x: x[1])

    # Extract only the colors after sorting
    output_colors = [color for color, _ in color_row_pairs]
    
    # ensure numpy array
    output_colors = np.array(output_colors)

    return output_colors
```
