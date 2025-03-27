import numpy as np

"""
The transformation identifies two 3x3 patterns of gray pixels within the central 7x3 area (rows 1-3, cols 1-7) of the input grid, separated by a column of white pixels.
The left 3x3 pattern (cols 1-3) determines the single output color:
- Pattern 1 (like train_1, train_3) results in blue (1).
- Pattern 2 (like train_4, train_5, train_6) results in red (2).
- Pattern 3 (like train_2) results in green (3).
The right 3x3 pattern (cols 5-7) determines the shape of the 3x3 output grid.
Where the right pattern has a gray pixel (5), the output grid has a pixel of the determined color.
Where the right pattern has a white pixel (0), the output grid has a white pixel (0).
"""

# Define reference patterns for color determination based on the left 3x3 subgrid
# These patterns represent the configuration of gray (5) and white (0) pixels.
pattern_blue = np.array([
    [5, 5, 5],
    [0, 5, 0],
    [0, 5, 0]
], dtype=int)

pattern_red = np.array([
    [5, 5, 0],
    [0, 5, 0],
    [0, 5, 5]
], dtype=int)

pattern_green = np.array([
    [0, 5, 5],
    [0, 5, 0],
    [5, 5, 0]
], dtype=int)

def determine_color(left_subgrid):
    """
    Determines the output color based on the pattern of the left 3x3 subgrid.

    Args:
        left_subgrid (np.ndarray): A 3x3 numpy array representing the subgrid from input rows 1-3, cols 1-3.

    Returns:
        int: The color code (1 for blue, 2 for red, 3 for green).

    Raises:
        ValueError: If the left_subgrid pattern does not match any known trigger pattern.
    """
    if np.array_equal(left_subgrid, pattern_blue):
        return 1  # Blue
    elif np.array_equal(left_subgrid, pattern_red):
        return 2  # Red
    elif np.array_equal(left_subgrid, pattern_green):
        return 3  # Green
    else:
        # This case should not happen based on the provided examples,
        # but it's good practice to handle unexpected inputs.
        raise ValueError("Unknown pattern encountered in the left subgrid.")

def transform(input_grid):
    """
    Transforms the input grid based on two 3x3 subpatterns.

    The left subpattern determines the output color, and the right subpattern
    determines the output shape.

    Args:
        input_grid (list[list[int]]): A 2D list representing the input grid.

    Returns:
        list[list[int]]: A 3x3 2D list representing the transformed output grid.
    """
    # Convert input to numpy array for easier slicing
    input_np = np.array(input_grid, dtype=int)

    # --- Extract Subgrids ---
    # Extract the left 3x3 subgrid (rows 1-3, cols 1-3)
    # Note: Python slicing is exclusive of the end index.
    left_subgrid = input_np[1:4, 1:4]

    # Extract the right 3x3 subgrid (rows 1-3, cols 5-7)
    right_subgrid = input_np[1:4, 5:8]

    # --- Determine Output Color ---
    # Use the left subgrid to find the corresponding output color
    output_color = determine_color(left_subgrid)

    # --- Create Output Grid ---
    # Initialize a 3x3 output grid filled with white (0)
    output_grid = np.zeros((3, 3), dtype=int)

    # Iterate through the right subgrid to determine the output shape
    for r in range(3):
        for c in range(3):
            # If the pixel in the right subgrid pattern is gray (5)
            if right_subgrid[r, c] == 5:
                # Set the corresponding pixel in the output grid to the determined color
                output_grid[r, c] = output_color

    # Convert the numpy array back to a list of lists for the final output
    return output_grid.tolist()