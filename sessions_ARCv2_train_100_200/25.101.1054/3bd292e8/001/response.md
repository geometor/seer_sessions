```python
import numpy as np

"""
This program transforms an input grid based on the color of its pixels.
The input grid primarily contains Red (2) and Orange (7) pixels.
The transformation rules are:
1. Red (2) pixels remain unchanged in the output grid.
2. Orange (7) pixels are transformed based on their adjacency to Red (2) pixels in the input grid:
   - If an Orange (7) pixel is adjacent (horizontally, vertically, or diagonally) to at least one Red (2) pixel, it becomes Gray (5) in the output grid.
   - If an Orange (7) pixel is not adjacent to any Red (2) pixel, it becomes Green (3) in the output grid.
The output grid has the same dimensions as the input grid.
"""

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Transforms the input grid according to the rules described above.

    Args:
        input_grid: A list of lists representing the input grid.

    Returns:
        A list of lists representing the transformed output grid.
    """
    # Convert input list of lists to a numpy array for easier processing
    input_np = np.array(input_grid, dtype=int)
    height, width = input_np.shape

    # Initialize the output grid as a copy of the input grid.
    # This handles rule 1 automatically (Red pixels remain Red).
    # We will only modify the cells that were originally Orange.
    output_np = np.copy(input_np)

    # Define the relative coordinates for the 8 neighbors (including diagonals)
    neighbor_deltas = [
        (-1, -1), (-1, 0), (-1, 1),
        (0, -1),          (0, 1),
        (1, -1), (1, 0), (1, 1)
    ]

    # Iterate through each cell of the input grid
    for r in range(height):
        for c in range(width):
            # Check if the current pixel in the input grid is Orange (7)
            if input_np[r, c] == 7:
                is_adjacent_to_red = False
                # Examine the 8 neighbors of the current pixel in the *input* grid
                for dr, dc in neighbor_deltas:
                    nr, nc = r + dr, c + dc
                    # Check if the neighbor coordinates are within the grid bounds
                    if 0 <= nr < height and 0 <= nc < width:
                        # Check if the neighbor pixel is Red (2)
                        if input_np[nr, nc] == 2:
                            is_adjacent_to_red = True
                            break  # Found a red neighbor, no need to check further

                # Apply transformation based on adjacency
                if is_adjacent_to_red:
                    # Rule 2a: If adjacent to Red, change to Gray (5)
                    output_np[r, c] = 5
                else:
                    # Rule 2b: If not adjacent to Red, change to Green (3)
                    output_np[r, c] = 3

    # Convert the numpy array back to a list of lists for the final output
    output_grid = output_np.tolist()
    return output_grid

```