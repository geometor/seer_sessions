import numpy as np

"""
Transformation rule:
1. Identify the background color (the most frequent color in the grid).
2. Create a copy of the input grid.
3. Iterate through each pixel in the grid.
4. If a pixel has the background color, check if it is enclosed by a single non-background color in all four cardinal directions (up, down, left, right).
5. To check for enclosure:
   - Look upwards from the pixel: Find the first non-background pixel. Record its color. If the grid boundary is hit first, it's not enclosed.
   - Look downwards: Find the first non-background pixel. Record its color. If the grid boundary is hit first, it's not enclosed.
   - Look leftwards: Find the first non-background pixel. Record its color. If the grid boundary is hit first, it's not enclosed.
   - Look rightwards: Find the first non-background pixel. Record its color. If the grid boundary is hit first, it's not enclosed.
6. If all four directions hit a non-background pixel, and all four non-background pixels found have the *same* color, then the original background pixel is considered enclosed.
7. If a background pixel is enclosed by color 'C', change its color to 'C' in the copied grid.
8. Pixels that were not background pixels, or background pixels that were not enclosed, remain unchanged.
9. Return the modified copied grid.
"""

def get_background_color(grid):
    """Finds the most frequent color in the grid."""
    colors, counts = np.unique(grid, return_counts=True)
    return colors[np.argmax(counts)]

def check_enclosed(grid, r, c, bg_color, height, width):
    """
    Checks if the background pixel at (r, c) is enclosed by a single non-background color.
    Returns (True, frame_color) if enclosed, (False, None) otherwise.
    """
    frame_color = -1 # Use -1 to indicate no frame color found yet

    # Check Up
    found_up = False
    for i in range(r - 1, -1, -1):
        if grid[i, c] != bg_color:
            frame_color = grid[i, c]
            found_up = True
            break
    if not found_up:
        return False, None

    # Check Down
    found_down = False
    for i in range(r + 1, height):
        if grid[i, c] != bg_color:
            if grid[i, c] != frame_color: return False, None # Different color
            found_down = True
            break
    if not found_down:
        return False, None

    # Check Left
    found_left = False
    for j in range(c - 1, -1, -1):
        if grid[r, j] != bg_color:
            if grid[r, j] != frame_color: return False, None # Different color
            found_left = True
            break
    if not found_left:
        return False, None

    # Check Right
    found_right = False
    for j in range(c + 1, width):
        if grid[r, j] != bg_color:
            if grid[r, j] != frame_color: return False, None # Different color
            found_right = True
            break
    if not found_right:
        return False, None

    # If all checks passed and found the same frame color
    return True, frame_color


def transform(input_grid):
    """
    Fills the interior of hollow rectangular frames with the color of the frame.
    """
    # Convert list of lists to numpy array for easier manipulation
    input_grid_np = np.array(input_grid, dtype=int)
    
    # Initialize output_grid as a copy of the input
    output_grid = np.copy(input_grid_np)
    height, width = output_grid.shape

    # Identify the background color
    bg_color = get_background_color(input_grid_np)

    # Iterate through each pixel potentially inside a frame
    for r in range(height):
        for c in range(width):
            # Check only pixels that currently have the background color
            if input_grid_np[r, c] == bg_color:
                # Check if this background pixel is enclosed
                is_enclosed, frame_color = check_enclosed(input_grid_np, r, c, bg_color, height, width)
                
                # If enclosed, fill the pixel with the frame color
                if is_enclosed:
                    output_grid[r, c] = frame_color

    # Convert back to list of lists for the expected output format
    return output_grid.tolist()