"""
1. **Identify Border Pixels:** Scan the input grid to identify "border pixels." A border pixel is any pixel with at least one orthogonally adjacent neighbor (up, down, left, or right, but *not* diagonal) of a different color.

2. **Extract Ordered Border Colors:** Create an ordered list, `border_colors`, of the *unique* colors of the border pixels. The order is determined by the first appearance of each border pixel during a top-to-bottom, left-to-right scan of the input grid.

3. **Determine Output Dimensions:**
    *   The number of columns in the output grid is always 5.
    *   The number of rows is determined by the number of unique colors in `border_colors` (denoted as 'n'):
        *   If n > 4, output rows = int(0.85*n + 0.5)
        *   If 2 <= n <= 4, output rows = n - 1.
        *   If n < 2, output rows = n.

4. **Construct Output Grid:**

    1.  Create an output grid with the calculated dimensions, initially filled with a placeholder (e.g., -1).
    2. The colors and structure of the expected output depends on the order and spatial relationships between border colors in the original image.
    3. Fill the output grid row by row.  The sequence of unique border colors is used to construct the output grid, repeating the sequence as needed.

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
    output_rows = int(0.85 * num_colors + 0.5) if num_colors > 4 else num_colors - 1 if 2 <= num_colors <= 4 else num_colors

    # Construct the output grid.
    output_grid = np.full((output_rows, output_cols), -1)

    # Fill the output grid by cycling through border_colors
    for r in range(output_rows):
        for c in range(output_cols):
            index = (r * output_cols + c) % num_colors
            output_grid[r,c] = border_colors[index]

    return output_grid.tolist()