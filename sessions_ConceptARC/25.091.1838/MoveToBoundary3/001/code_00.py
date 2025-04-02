"""
Identifies the single non-background object (color red, 2) in the input grid.
Calculates the horizontal distance needed to shift the object so its rightmost edge aligns with the rightmost column of the grid.
Creates a new grid of the same dimensions, initialized with the background color (white, 0).
Copies the object pixels to the new grid, shifted horizontally by the calculated distance.
The object's shape, color, and vertical position remain unchanged.
"""

import numpy as np

def find_object_pixels(grid, background_color=0):
    """
    Finds the coordinates of all pixels that are not the background color.

    Args:
        grid (np.array): The input grid.
        background_color (int): The color representing the background.

    Returns:
        list: A list of tuples, where each tuple is (row, col) of an object pixel.
        int: The color of the object found. Returns None if no object is found.
    """
    pixels = []
    object_color = None
    height, width = grid.shape
    for r in range(height):
        for c in range(width):
            if grid[r, c] != background_color:
                pixels.append((r, c))
                if object_color is None:
                    object_color = grid[r, c]
                elif grid[r, c] != object_color:
                    # This assumes a single object color, raise error or handle if needed
                    print(f"Warning: Multiple non-background colors found. Using first found: {object_color}")
    return pixels, object_color

def transform(input_grid):
    """
    Transforms the input grid by shifting the single object horizontally
    so its rightmost edge aligns with the grid's rightmost column.

    Args:
        input_grid (list of lists): The input grid represented as a list of lists.

    Returns:
        list of lists: The transformed grid.
    """
    # Convert input to numpy array for easier manipulation
    input_np = np.array(input_grid, dtype=int)
    height, width = input_np.shape
    background_color = 0

    # Find all pixels belonging to the object and the object's color
    object_pixels, object_color = find_object_pixels(input_np, background_color)

    # If no object is found, return the original grid
    if not object_pixels:
        return input_grid # Or return np.zeros_like(input_np).tolist() if preferred

    # Find the maximum column index occupied by the object
    max_col = -1
    for r, c in object_pixels:
        if c > max_col:
            max_col = c

    # Calculate the horizontal shift needed
    # shift = (grid_width - 1) - max_col_index
    shift = (width - 1) - max_col

    # Initialize the output grid with the background color
    output_grid = np.full((height, width), background_color, dtype=int)

    # Place the object in the output grid at the shifted position
    for r, c in object_pixels:
        new_col = c + shift
        # Check bounds just in case, though logic should prevent out of bounds
        if 0 <= new_col < width:
            output_grid[r, new_col] = object_color

    # Convert the output numpy array back to a list of lists
    return output_grid.tolist()