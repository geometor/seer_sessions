import numpy as np

"""
Transforms an input grid into an output grid of double the dimensions.
Each pixel in the input grid maps to a 2x2 block in the output grid.

1. If the input pixel color is non-white (not 0), the corresponding 2x2 output block is filled entirely with that color.
2. If the input pixel color is white (0):
   a. Check if the input pixel has any non-white diagonal neighbors in the input grid.
   b. If it does, the corresponding 2x2 output block is filled with the pattern [[1, 0], [0, 1]] (blue anti-diagonal).
   c. If it does not, the corresponding 2x2 output block is filled entirely with white (0).
"""

def _has_non_white_diagonal_neighbor(input_grid_np, r, c):
    """
    Checks if a pixel at (r, c) in the input grid has any non-white diagonal neighbors.

    Args:
        input_grid_np (np.ndarray): The input grid as a numpy array.
        r (int): The row index of the pixel to check.
        c (int): The column index of the pixel to check.

    Returns:
        bool: True if a non-white diagonal neighbor exists, False otherwise.
    """
    height, width = input_grid_np.shape
    diagonal_offsets = [
        (-1, -1), (-1, 1),
        (1, -1), (1, 1)
    ]

    for dr, dc in diagonal_offsets:
        nr, nc = r + dr, c + dc
        # Check if neighbor coordinates are within grid bounds
        if 0 <= nr < height and 0 <= nc < width:
            # Check if the neighbor color is non-white (not 0)
            if input_grid_np[nr, nc] != 0:
                return True
    return False


def transform(input_grid):
    """
    Applies the transformation rule to the input grid.

    Args:
        input_grid (list[list[int]]): A 2D list representing the input grid.

    Returns:
        list[list[int]]: A 2D list representing the transformed output grid.
    """
    # Convert input to numpy array for easier manipulation
    input_np = np.array(input_grid, dtype=int)
    input_height, input_width = input_np.shape

    # Calculate output dimensions (double the input dimensions)
    output_height = input_height * 2
    output_width = input_width * 2

    # Initialize output grid with zeros (white)
    output_grid_np = np.zeros((output_height, output_width), dtype=int)

    # Iterate through each pixel of the input grid
    for r in range(input_height):
        for c in range(input_width):
            input_color = input_np[r, c]

            # Determine the top-left corner of the 2x2 block in the output grid
            out_r = r * 2
            out_c = c * 2

            # Apply transformation based on the input pixel color
            if input_color != 0:
                # If the input color is non-white, fill the 2x2 block with that color
                output_grid_np[out_r:out_r+2, out_c:out_c+2] = input_color
            else:
                # If the input color is white (0), check for non-white diagonal neighbors
                if _has_non_white_diagonal_neighbor(input_np, r, c):
                    # Apply the blue anti-diagonal pattern [[1, 0], [0, 1]]
                    output_grid_np[out_r, out_c] = 1      # Top-left: blue
                    output_grid_np[out_r, out_c + 1] = 0  # Top-right: white
                    output_grid_np[out_r + 1, out_c] = 0  # Bottom-left: white
                    output_grid_np[out_r + 1, out_c + 1] = 1  # Bottom-right: blue
                else:
                    # Otherwise, fill the 2x2 block with white (0)
                    # This is already the default, but can be explicitly set:
                    output_grid_np[out_r:out_r+2, out_c:out_c+2] = 0

    # Convert the final numpy array back to a list of lists
    output_grid = output_grid_np.tolist()

    return output_grid