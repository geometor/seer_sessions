```python
import numpy as np

"""
Transforms an input grid based on the adjacency of yellow pixels to blue pixels.

1.  Initialize the output grid as a copy of the input grid.
2.  Iterate through each pixel of the input grid.
3.  If a pixel is yellow (4):
    a.  Count its orthogonal blue (1) neighbors.
    b.  Count its diagonal blue (1) neighbors.
    c.  Apply color changes to the corresponding pixel in the output grid based on these counts:
        - If orthogonally adjacent to 2 or more blue pixels, change to magenta (6).
        - Else if orthogonally adjacent to exactly 1 blue pixel, change to red (2).
        - Else if diagonally adjacent to 1 or more blue pixels (and not orthogonally adjacent to any blue pixel), change to azure (8).
4.  Leave all other pixels (including the original blue pixels) unchanged.
5.  Return the modified output grid.
"""

def transform(input_grid: np.ndarray) -> np.ndarray:
    """
    Applies adjacency-based coloring rules to an input grid.

    Args:
        input_grid: A 2D numpy array representing the input grid.

    Returns:
        A 2D numpy array representing the transformed output grid.
    """
    # Initialize output_grid as a copy of the input
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # Define neighbor offsets
    # Orthogonal: [(dr, dc)] -> Up, Down, Left, Right
    orthogonal_neighbors = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    # Diagonal: [(dr, dc)] -> Top-Left, Top-Right, Bottom-Left, Bottom-Right
    diagonal_neighbors = [(-1, -1), (-1, 1), (1, -1), (1, 1)]

    # Iterate through each pixel in the grid
    for r in range(rows):
        for c in range(cols):
            # Only process pixels that are yellow (4) in the input
            if input_grid[r, c] == 4:
                ortho_blue_count = 0
                diag_blue_count = 0

                # Check orthogonal neighbors
                for dr, dc in orthogonal_neighbors:
                    nr, nc = r + dr, c + dc
                    # Check if neighbor is within bounds
                    if 0 <= nr < rows and 0 <= nc < cols:
                        # Check if neighbor is blue (1)
                        if input_grid[nr, nc] == 1:
                            ortho_blue_count += 1

                # Check diagonal neighbors only if no orthogonal blue neighbors were found
                # (as per rule priorities: magenta > red > azure)
                if ortho_blue_count == 0:
                    for dr, dc in diagonal_neighbors:
                        nr, nc = r + dr, c + dc
                        # Check if neighbor is within bounds
                        if 0 <= nr < rows and 0 <= nc < cols:
                             # Check if neighbor is blue (1)
                            if input_grid[nr, nc] == 1:
                                diag_blue_count += 1

                # Apply coloring rules based on neighbor counts
                if ortho_blue_count >= 2:
                    output_grid[r, c] = 6  # Magenta
                elif ortho_blue_count == 1:
                    output_grid[r, c] = 2  # Red
                elif diag_blue_count >= 1: # Implicitly ortho_blue_count == 0 here
                    output_grid[r, c] = 8  # Azure
                # Else: pixel remains yellow (4) as initialized

    return output_grid
```