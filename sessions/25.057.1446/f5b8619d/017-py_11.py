"""
1.  **Input:**  A 2x2 grid containing colors represented by integers (0, 4, 5, or 6).
2.  **Quadrant Creation:** Create a 2x2 "quadrant" as follows:
    *   Each non-zero color in the *original* input is duplicated with a second color
    *   Yellow (4) is paired with Azure (8)
    *   Gray (5) is paired with Magenta (6)
    *   Magenta (6) is paired with Blue (1)
    *   The original color is top-left and bottom-right, the paired color is top-right and bottom-left.
3. **Expansion:** Create a 4x4 output grid.
4. **Placement:**
    *   Top-Left Quadrant: Place the quadrant created from the top-left pixel of input.
    *   Top-Right Quadrant: Place the quadrant created from the top-right pixel of input.
    *   Bottom-Left Quadrant: Place the quadrant created from the bottom-left pixel of input.
    *   Bottom-Right Quadrant: Place the quadrant created from the bottom-right pixel of input.
5. **Output:** The resulting 4x4 grid.
"""

import numpy as np

def create_quadrant(color):
    """Creates a 2x2 quadrant based on the input color."""
    if color == 0:
        return np.array([[0, 0], [0, 0]])
    elif color == 4:
        return np.array([[4, 8], [8, 4]])
    elif color == 5:
        return np.array([[5, 6], [6, 5]])
    elif color == 6:
        return np.array([[6, 1], [1, 6]])
    else:
        return np.array([[0, 0], [0, 0]])  # Should not happen based on problem constraints, but good practice


def transform(input_grid):
    # Initialize output_grid as 4x4 zero array
    output_grid = np.zeros((4, 4), dtype=int)

    # Create and place quadrants
    output_grid[0:2, 0:2] = create_quadrant(input_grid[0, 0])  # Top-Left
    output_grid[0:2, 2:4] = create_quadrant(input_grid[0, 1])  # Top-Right
    output_grid[2:4, 0:2] = create_quadrant(input_grid[1, 0])  # Bottom-Left
    output_grid[2:4, 2:4] = create_quadrant(input_grid[1, 1])  # Bottom-Right

    return output_grid