"""
1.  **Identify Regions:** Divide the input grid into distinct regions. A region is a group of connected pixels of the same color.  Pixels are considered connected if they are adjacent horizontally, vertically, or diagonally.
2.  **Identify Boundary Pixels:** A boundary pixel is a pixel that belongs to a region and is directly adjacent (horizontally, vertically, or diagonally) to a pixel of a *different* color.
3. **Determine Colors at Boundary**: For each pair of different colored adjacent pixels at the shared boundary, determine the lower and higher values
4.  **Apply Color Change:** At the boundary, if the two adjacent pixels have different color values, change the pixel with the *lower* color value to azure (8).
5. Do not change the color of any white (0) pixel.
"""

import numpy as np

def get_neighbors(grid, r, c):
    """Gets the valid neighbors of a pixel, including diagonals."""
    rows, cols = grid.shape
    neighbors = []
    for dr in [-1, 0, 1]:
        for dc in [-1, 0, 1]:
            if dr == 0 and dc == 0:
                continue  # Skip the pixel itself
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols:
                neighbors.append((nr, nc))
    return neighbors

def transform(input_grid):
    """
    Transforms the input grid by changing the color of boundary pixels.
    """
    rows, cols = input_grid.shape
    output_grid = np.copy(input_grid)

    # Iterate through each pixel to find boundary pixels
    for r in range(rows):
        for c in range(cols):
            current_color = input_grid[r, c]

            # Skip white pixels
            if current_color == 0:
                continue

            neighbors = get_neighbors(input_grid, r, c)
            for nr, nc in neighbors:
                neighbor_color = input_grid[nr, nc]
                
                # Check for boundary and color difference
                if neighbor_color != current_color and neighbor_color !=0:
                    # Apply color change rule: lower color becomes azure
                    if current_color < neighbor_color :
                        output_grid[r, c] = 8


    return output_grid