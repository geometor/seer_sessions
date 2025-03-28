import numpy as np

"""
Transforms an input grid based on the number and type of unique non-white colors present.

1.  Analyzes the input grid to find unique non-white colors and counts them (N).
2.  Determines an output color (C_out) based on N:
    - If N = 3, C_out is the maximum value among the unique non-white colors.
    - If N = 2, C_out is always Azure (8).
    - Otherwise, C_out is White (0).
3.  Determines a 3x3 output pattern based on N and input features:
    - If N = 3, the pattern is 'Shape A': [[C,0,0],[0,C,C],[C,0,0]].
    - If N = 2:
        - Checks if a 'Strict Plus Shape' for Azure (8) exists in the input (center+cardinal=8, corners=0).
        - If yes, the pattern is 'Shape +': [[0,C,0],[C,C,C],[0,C,0]].
        - If no, the pattern is 'Shape X': [[C,0,C],[0,C,0],[C,0,C]].
    - Otherwise, the pattern is all White (0).
4.  Constructs a 3x3 output grid using the determined pattern and color.
"""

def _find_non_white_colors(grid):
    """
    Finds all unique non-white colors in the grid.

    Args:
        grid (np.ndarray): The input grid.

    Returns:
        set: A set of unique non-white color integers.
    """
    unique_colors = np.unique(grid)
    return set(color for color in unique_colors if color != 0)

def _check_strict_plus_shape(grid, color):
    """
    Checks if a 3x3 'strict' plus shape of the specified color exists anywhere in the grid.
    A 'strict' plus shape has the given color at the center and its 4 cardinal neighbors,
    and white (0) at the 4 corner positions relative to the center.

    Args:
        grid (np.ndarray): The input grid.
        color (int): The non-white color to check for.

    Returns:
        bool: True if at least one strict plus shape of the given color is found, False otherwise.
    """
    rows, cols = grid.shape
    # Iterate through possible center points (r, c) of a 3x3 shape
    # We need to leave a 1-pixel border around the grid
    for r in range(1, rows - 1):
        for c in range(1, cols - 1):
            # Check center pixel
            if grid[r, c] == color:
                # Check cardinal neighbors
                if (grid[r-1, c] == color and
                    grid[r+1, c] == color and
                    grid[r, c-1] == color and
                    grid[r, c+1] == color):
                    # Check corner neighbors (must be white)
                    if (grid[r-1, c-1] == 0 and
                        grid[r-1, c+1] == 0 and
                        grid[r+1, c-1] == 0 and
                        grid[r+1, c+1] == 0):
                        return True  # Found a strict plus shape
    return False # No strict plus shape found for this color

def transform(input_grid):
    """
    Transforms the input grid based on the rules described in the module docstring.

    Args:
        input_grid (list of lists): The input grid.

    Returns:
        list of lists: The 3x3 transformed output grid.
    """
    # Convert input to numpy array for easier handling
    grid = np.array(input_grid, dtype=int)

    # Step 1: Analyze Input - Find unique non-white colors and count (N)
    non_white_colors = _find_non_white_colors(grid)
    num_non_white_colors = len(non_white_colors)

    # Initialize output grid (3x3) and output color
    output_grid = np.zeros((3, 3), dtype=int)
    output_color = 0
    shape_pattern = None # To hold the pattern coordinates

    # Step 2 & 3: Determine Output Color (C_out) and Shape Pattern based on N
    if num_non_white_colors == 3:
        # Rule for N=3: Max color, Shape A
        output_color = max(non_white_colors)
        # Define coordinates for Shape A: [[C,0,0],[0,C,C],[C,0,0]]
        shape_pattern = [(0, 0), (1, 1), (1, 2), (2, 0)]

    elif num_non_white_colors == 2:
        # Rule for N=2: Color is Azure(8)
        output_color = 8
        # Check for strict plus shape of Azure(8) in input
        has_strict_plus = _check_strict_plus_shape(grid, 8)
        if has_strict_plus:
            # Shape +: [[0,C,0],[C,C,C],[0,C,0]]
            shape_pattern = [(0, 1), (1, 0), (1, 1), (1, 2), (2, 1)]
        else:
            # Shape X: [[C,0,C],[0,C,0],[C,0,C]]
            shape_pattern = [(0, 0), (0, 2), (1, 1), (2, 0), (2, 2)]

    # Else (N is not 2 or 3), output_color remains 0 and shape_pattern remains None
    # The output_grid will remain all zeros (White)

    # Step 4: Construct Output Grid
    if output_color != 0 and shape_pattern is not None:
        for r, c in shape_pattern:
            output_grid[r, c] = output_color

    # Return as list of lists per ARC standard
    return output_grid.tolist()