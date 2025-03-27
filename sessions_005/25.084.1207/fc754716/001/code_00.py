import numpy as np

"""
Create a border around the grid using the color of the single non-white pixel found in the input.
The output grid has the same dimensions as the input grid.
The border is 1 pixel thick and located at the perimeter (top row, bottom row, left column, right column).
The interior of the grid (pixels not part of the border) is filled with white (0).
"""

def find_unique_non_white_color(grid):
    """
    Scans the grid to find the color of the single non-white pixel.

    Args:
        grid (np.array): The input grid.

    Returns:
        int: The color value (1-9) of the unique non-white pixel.
             Returns 0 if no non-white pixel is found (though the task implies one always exists).
    """
    for r in range(grid.shape[0]):
        for c in range(grid.shape[1]):
            if grid[r, c] != 0:
                return grid[r, c]
    # Should not happen based on task description, but return 0 as a fallback
    return 0

def transform(input_grid):
    """
    Applies the border transformation to the input grid.

    Args:
        input_grid (list of lists): The input grid represented as a list of lists.

    Returns:
        list of lists: The transformed grid with a border.
    """
    # Convert input list of lists to a numpy array for easier manipulation
    input_np = np.array(input_grid, dtype=int)

    # Step 1: Determine the height (H) and width (W) of the input grid.
    H, W = input_np.shape

    # Step 2: Scan the input grid to find the unique non-white color, C.
    border_color = find_unique_non_white_color(input_np)

    # Step 3 & 4: Create a new output grid initialized with white (0).
    output_grid = np.zeros((H, W), dtype=int)

    # Step 5: Color the top row (row index 0) with color C.
    if H > 0:
        output_grid[0, :] = border_color

    # Step 6: Color the bottom row (row index H-1) with color C.
    if H > 1: # Ensure there is a distinct bottom row
        output_grid[H - 1, :] = border_color

    # Step 7: Color the leftmost column (column index 0) with color C.
    if W > 0:
        output_grid[:, 0] = border_color

    # Step 8: Color the rightmost column (column index W-1) with color C.
    if W > 1: # Ensure there is a distinct rightmost column
        output_grid[:, W - 1] = border_color

    # Step 9: Return the resulting grid, converted back to list of lists.
    return output_grid.tolist()
