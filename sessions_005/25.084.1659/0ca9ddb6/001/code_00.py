import numpy as np

"""
Transformation Rule:
1. Initialize the output grid as a copy of the input grid.
2. Identify all red (2) pixels in the input grid. For each red pixel, find its diagonal neighbors (top-left, top-right, bottom-left, bottom-right). If a diagonal neighbor is within the grid bounds and is currently white (0) in the *input* grid, change the color of that corresponding cell in the *output* grid to yellow (4).
3. Identify all blue (1) pixels in the input grid. For each blue pixel, find its orthogonal neighbors (up, down, left, right). If an orthogonal neighbor is within the grid bounds and is currently white (0) in the *input* grid, change the color of that corresponding cell in the *output* grid to orange (7).
4. Preserve all other original pixels from the input grid in the output grid.
"""

def transform(input_grid: np.ndarray) -> np.ndarray:
    """
    Applies the transformation rule to the input grid.

    Args:
        input_grid: A numpy array representing the input grid.

    Returns:
        A numpy array representing the output grid.
    """
    # Get grid dimensions
    height, width = input_grid.shape

    # Initialize output_grid as a copy of the input grid
    output_grid = np.copy(input_grid)

    # Define relative coordinates for neighbors
    diagonal_neighbors = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
    orthogonal_neighbors = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    # Create a list to store modifications to avoid race conditions or order dependency
    modifications = []

    # Iterate through each cell of the input grid
    for r in range(height):
        for c in range(width):
            pixel_color = input_grid[r, c]

            # Check for red pixels (2)
            if pixel_color == 2:
                # Check diagonal neighbors
                for dr, dc in diagonal_neighbors:
                    nr, nc = r + dr, c + dc
                    # Check if neighbor is within bounds
                    if 0 <= nr < height and 0 <= nc < width:
                        # Check if neighbor is white (0) in the original input grid
                        if input_grid[nr, nc] == 0:
                            # Schedule modification to yellow (4)
                            modifications.append(((nr, nc), 4))

            # Check for blue pixels (1)
            elif pixel_color == 1:
                # Check orthogonal neighbors
                for dr, dc in orthogonal_neighbors:
                    nr, nc = r + dr, c + dc
                    # Check if neighbor is within bounds
                    if 0 <= nr < height and 0 <= nc < width:
                        # Check if neighbor is white (0) in the original input grid
                        if input_grid[nr, nc] == 0:
                            # Schedule modification to orange (7)
                            modifications.append(((nr, nc), 7))

    # Apply the collected modifications to the output grid
    # Using a dictionary ensures that if multiple rules target the same cell,
    # the last one applied wins (though in this specific problem, overlaps
    # between blue-orthogonal and red-diagonal affecting the same white cell don't occur).
    # A simple list iteration also works fine here.
    changes_dict = {}
    for (coords, color) in modifications:
        changes_dict[coords] = color # Overwrite if multiple modifications target the same cell

    for (r, c), color in changes_dict.items():
        output_grid[r, c] = color

    return output_grid