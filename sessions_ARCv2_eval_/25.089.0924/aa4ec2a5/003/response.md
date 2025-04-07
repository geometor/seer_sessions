```python
import numpy as np

"""
Transforms an input grid based on the adjacency of yellow pixels to blue pixels, 
applying a two-stage process:

1.  **Stage 1 (Coloring Yellow Pixels):**
    a.  Initialize an output grid as a copy of the input grid.
    b.  Create a temporary grid (`stage1_colors`) to store the calculated colors 
        for pixels that were initially yellow (4).
    c.  Iterate through each yellow pixel in the input grid.
    d.  Count its orthogonal and diagonal blue (1) neighbors in the *input* grid.
    e.  Determine the color for this yellow pixel based on the counts:
        - Magenta (6) if orthogonally adjacent to 2 or more blue pixels.
        - Red (2) if orthogonally adjacent to exactly 1 blue pixel.
        - Azure (8) if diagonally adjacent to 1 or more blue pixels AND 
          NOT orthogonally adjacent to any blue pixels.
        - Yellow (4) otherwise.
    f.  Store this calculated color in the `stage1_colors` grid.
    g.  Update the main output grid with the colors calculated in `stage1_colors`.

2.  **Stage 2 (Coloring Blue Pixels):**
    a.  Iterate through each pixel that was originally blue (1) in the input grid.
    b.  Check its 8 neighbors (orthogonal and diagonal).
    c.  If any neighbor `(nr, nc)` was originally yellow (4) in the input grid 
        AND its calculated color in `stage1_colors` is azure (8), then change 
        the current blue pixel in the output grid to azure (8).
    d.  Otherwise, the blue pixel remains blue (1).

3.  Return the final output grid.
"""

def transform(input_grid: np.ndarray) -> np.ndarray:
    """
    Applies a two-stage adjacency-based coloring rule to the input grid.

    Args:
        input_grid: A 2D numpy array representing the input grid.

    Returns:
        A 2D numpy array representing the transformed output grid.
    """
    rows, cols = input_grid.shape
    # Initialize output_grid as a copy of the input
    output_grid = np.copy(input_grid)
    # Temporary grid to store colors calculated for initially yellow pixels
    # Initialize with -1 to distinguish from valid colors (0-9)
    stage1_colors = np.full_like(input_grid, -1, dtype=int) 

    # Define neighbor offsets
    orthogonal_neighbors = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    diagonal_neighbors = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
    all_neighbors = orthogonal_neighbors + diagonal_neighbors

    # --- Stage 1: Calculate colors for initially yellow pixels ---
    for r in range(rows):
        for c in range(cols):
            # Only process pixels that are yellow (4) in the input
            if input_grid[r, c] == 4:
                ortho_blue_count = 0
                diag_blue_count = 0

                # Check orthogonal neighbors in the original input grid
                for dr, dc in orthogonal_neighbors:
                    nr, nc = r + dr, c + dc
                    if 0 <= nr < rows and 0 <= nc < cols and input_grid[nr, nc] == 1:
                        ortho_blue_count += 1

                # Check diagonal neighbors in the original input grid
                for dr, dc in diagonal_neighbors:
                    nr, nc = r + dr, c + dc
                    if 0 <= nr < rows and 0 <= nc < cols and input_grid[nr, nc] == 1:
                        diag_blue_count += 1

                # Determine color based on rules and store in stage1_colors
                if ortho_blue_count >= 2:
                    stage1_colors[r, c] = 6  # Magenta
                elif ortho_blue_count == 1:
                    stage1_colors[r, c] = 2  # Red
                elif diag_blue_count >= 1: # Only if ortho_blue_count is 0
                    stage1_colors[r, c] = 8  # Azure
                else:
                    stage1_colors[r, c] = 4 # Remains Yellow

    # Apply Stage 1 colors to the output grid
    for r in range(rows):
        for c in range(cols):
            if stage1_colors[r, c] != -1: # If a color was calculated (i.e., was originally yellow)
                output_grid[r, c] = stage1_colors[r, c]

    # --- Stage 2: Check if original blue pixels should turn azure ---
    # Create a list of blue pixels to update to avoid modifying the grid while iterating
    blue_to_azure_updates = []
    for r in range(rows):
        for c in range(cols):
            # Only process pixels that were blue (1) in the input
            if input_grid[r, c] == 1:
                should_turn_azure = False
                # Check all 8 neighbors
                for dr, dc in all_neighbors:
                    nr, nc = r + dr, c + dc
                    # Check if neighbor is within bounds
                    if 0 <= nr < rows and 0 <= nc < cols:
                        # Check if the neighbor was originally yellow AND its calculated color is azure
                        if input_grid[nr, nc] == 4 and stage1_colors[nr, nc] == 8:
                            should_turn_azure = True
                            break # Found one azure-inducing neighbor, no need to check further
                
                if should_turn_azure:
                    blue_to_azure_updates.append((r, c))

    # Apply the blue-to-azure updates
    for r, c in blue_to_azure_updates:
        output_grid[r, c] = 8 # Azure

    return output_grid
```