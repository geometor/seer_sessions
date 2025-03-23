"""
The transformation rule involves replacing all cells in the input grid with a color based on the position of gray(5) cells.

1.  **Identify Gray Pixels:** Find the coordinates (row, column) of all cells with the value 5 (gray) in the input grid.

2.  **Determine Replacement Color:**
    *   If all gray pixels are in the *same column*, the replacement color is 3 (green).
    *   If the gray pixels form a *main diagonal* line (where row index equals column index for all gray pixels), the replacement color is 2 (red).
    *   Otherwise, the replacement color is 4 (yellow).

3.  **Replace All Cells:** Create an output grid of the same dimensions as the input grid. Replace *all* cells in the output grid with the determined `replacement_color`.

4.  **Output:** Return the modified grid as the output.
"""

import numpy as np

def get_gray_pixel_positions(grid):
    """Finds the coordinates of all gray pixels (value 5)."""
    grid = np.array(grid)
    gray_indices = np.where(grid == 5)
    return list(zip(gray_indices[0], gray_indices[1]))

def determine_replacement_color(gray_positions):
    """Determines the replacement color based on gray pixel positions."""
    if not gray_positions:
        return 0  # Default color if no gray pixels (shouldn't happen based on problem, but safe)

    # Check if all gray pixels are in the same column
    first_col = gray_positions[0][1]
    if all(pos[1] == first_col for pos in gray_positions):
        return 3  # Green

    # Check if all gray pixels are on the main diagonal
    if all(pos[0] == pos[1] for pos in gray_positions):
        return 2  # Red

    return 4  # Yellow

def transform(input_grid):
    """Transforms the input grid according to the described rule."""
    input_grid = np.array(input_grid)
    output_grid = np.zeros_like(input_grid)

    # Find gray pixel positions
    gray_positions = get_gray_pixel_positions(input_grid)

    # Determine the replacement color
    replacement_color = determine_replacement_color(gray_positions)

    # Replace all cells in the output grid
    output_grid[:] = replacement_color

    return output_grid.tolist()