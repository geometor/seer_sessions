```python
"""
1. **Identify Border Pixels:** Scan the input grid row by row, from left to right and top to bottom. A "border pixel" is a pixel that has at least one orthogonally adjacent neighbor (up, down, left, or right) with a different color. Diagonal neighbors are *not* considered.

2. **Extract Ordered Border Colors:** Create an *ordered* sequence, `border_colors`, of the *unique* colors of the border pixels, preserving the order in which they first appear during the scan.

3. **Determine Output Dimensions:**
   - The number of columns in the output grid is always 5.
   - The number of rows in the output grid is determined as follows:
       1. Let 'n' be the number of unique colors found in the `border_colors` sequence.
       2.  output_rows =  int(0.85*n + 0.5) if n > 4 else n-1 if n >=2 else n

4. **Construct Output Grid:**
    1. Create an output grid of the determined dimensions, filled initially with a placeholder value (e.g., -1).
    2. Fill the output grid with colors from the `border_colors` sequence. The precise placement logic is still under investigation, but it is based on `border_colors`.
"""

import numpy as np

def get_orthogonal_neighbors(grid, row, col):
    """Get the orthogonally adjacent neighbors of a cell."""
    rows, cols = grid.shape
    neighbors = []
    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
        new_row, new_col = row + dr, col + dc
        if 0 <= new_row < rows and 0 <= new_col < cols:
            neighbors.append(grid[new_row, new_col])
    return neighbors

def find_border_pixels(grid):
    """Find pixels that have at least one orthogonally adjacent neighbor of a different color."""
    rows, cols = grid.shape
    border_pixels = []
    for i in range(rows):
        for j in range(cols):
            neighbors = get_orthogonal_neighbors(grid, i, j)
            if any(neighbor != grid[i, j] for neighbor in neighbors):
                border_pixels.append((i, j, grid[i,j]))  # Store row, col, and color
    return border_pixels

def get_ordered_border_colors(grid):
    """Extract unique border colors in order of first appearance."""
    border_pixels = find_border_pixels(grid)
    ordered_colors = []
    for r, c, color in border_pixels:
        if color not in ordered_colors:
            ordered_colors.append(color)
    return ordered_colors

def transform(input_grid):
    """Transforms the input grid into a smaller output grid based on ordered border colors."""

    input_grid = np.array(input_grid)
    border_colors = get_ordered_border_colors(input_grid)

    # Determine output grid dimensions.
    num_colors = len(border_colors)
    output_cols = 5
    output_rows = int(0.85 * num_colors + 0.5) if num_colors > 4 else num_colors - 1 if num_colors>=2 else num_colors

    # Construct the output grid.
    output_grid = np.full((output_rows, output_cols), -1)

    # Fill the output grid (placeholder logic - needs refinement).
    num_to_fill = output_rows * output_cols
    repeated_colors = (border_colors * (num_to_fill // len(border_colors) + 1))[:num_to_fill]
    output_grid = np.array(repeated_colors).reshape(output_rows, output_cols)

    return output_grid.tolist()
```