"""
1. **Identify Border Pixels:** Scan the input grid to identify "border pixels." A border pixel is defined as a pixel that has at least one orthogonally adjacent neighbor (up, down, left, or right) of a *different* color. Diagonal neighbors are not considered for border definition.
2. **Extract Border Colors**: Create a sequence that includes the unique colors of the border pixels detected.
3. **Determine Output Dimensions**: The dimensions depend of the number of different colors in the border sequence. If there are *n* colors, the output will be min(n, 5) x 5.
4. **Construct the Output Grid.** Fill the grid with the colors from the border sequence obtained in step 2, repeating those colors as necessary to fill the grid.
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
                border_pixels.append((i, j))
    return border_pixels

def extract_border_colors(grid, border_pixels):
    """Extract unique colors from the border pixels."""
    border_colors = []
    for r, c in border_pixels:
        color = grid[r,c]
        if color not in border_colors:
           border_colors.append(color)

    return border_colors

def transform(input_grid):
    """Transforms the input grid into a smaller output grid based on border colors."""

    input_grid = np.array(input_grid)
    border_pixels_coords = find_border_pixels(input_grid)
    border_colors = extract_border_colors(input_grid, border_pixels_coords)

    # Determine output grid dimensions.
    output_rows = min(len(border_colors), 5)
    output_cols = 5

    # Construct the output grid.
    output_grid = np.full((output_rows, output_cols), -1)  # Fill with -1 as a placeholder

    # Fill with border colors, repeating as necessary.
    
    num_to_fill = output_rows*output_cols
    
    repeated_colors = (border_colors * (num_to_fill // len(border_colors) + 1))[:num_to_fill]
    
    output_grid = np.array(repeated_colors).reshape(output_rows, output_cols)

    return output_grid.tolist()