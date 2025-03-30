import numpy as np

"""
Identifies a red '+' shape in the input grid.
Preserves the original red cross in the output grid.
Draws 8 lines radiating outwards from the pixels adjacent to the cross center towards the grid boundaries.
- Diagonal lines starting from the pixels diagonally adjacent to the cross center are drawn in blue (1).
- Orthogonal lines starting from the pixels orthogonally adjacent to the cross center are drawn with a repeating pattern of Azure (8), Azure (8), Yellow (4).
Lines only overwrite white (0) background pixels. The starting pixel of the line is colored first, then the line continues outwards.
"""

def find_cross_center(grid):
    """
    Finds the center pixel (row, col) of the red '+' cross.
    The center is defined as the red pixel with 4 adjacent red neighbors.
    Returns None if no such center is found.
    """
    red_pixels = np.argwhere(grid == 2)
    if len(red_pixels) < 5: # A '+' shape needs at least 5 red pixels
        return None

    height, width = grid.shape

    for r, c in red_pixels:
        # Check for 4 red neighbours within bounds
        neighbor_count = 0
        # Check North
        if r > 0 and grid[r-1, c] == 2: neighbor_count += 1
        # Check South
        if r < height - 1 and grid[r+1, c] == 2: neighbor_count += 1
        # Check West
        if c > 0 and grid[r, c-1] == 2: neighbor_count += 1
        # Check East
        if c < width - 1 and grid[r, c+1] == 2: neighbor_count += 1

        if neighbor_count == 4:
             # Check if the center itself is red (already guaranteed by loop, but good practice)
             if grid[r,c] == 2:
                 return (r, c)

    return None # Indicate failure to find a suitable center


def draw_line(grid, start_r, start_c, dr, dc, color=None, pattern=None):
    """
    Draws a line on the grid starting *at* (start_r, start_c) and moving 
    in direction (dr, dc).
    Can draw a single color line or a patterned line.
    Only overwrites white (0) pixels.
    Modifies the grid in place.
    """
    height, width = grid.shape
    
    # Check if the starting point is valid and is white
    k = 0 # Pattern counter
    if 0 <= start_r < height and 0 <= start_c < width and grid[start_r, start_c] == 0:
        if pattern:
            current_color = pattern[k % len(pattern)]
            grid[start_r, start_c] = current_color
            k += 1
        elif color is not None:
            grid[start_r, start_c] = color
        # If neither color nor pattern provided, or start isn't white, nothing happens to start pixel

    # Continue drawing from the next pixel
    r, c = start_r + dr, start_c + dc

    while 0 <= r < height and 0 <= c < width:
        if grid[r, c] == 0: # Only draw on white background
            if pattern:
                current_color = pattern[k % len(pattern)]
                grid[r, c] = current_color
                k += 1 # Increment pattern counter only when drawing
            elif color is not None:
                grid[r, c] = color
            else:
                 # Should not happen if called correctly
                 break 
        
        # Always move to the next pixel regardless of whether we drew
        r += dr
        c += dc


def transform(input_grid):
    """
    Applies the transformation rule: find red cross, draw radiating lines.
    """
    # Convert input to numpy array for easier manipulation
    grid = np.array(input_grid, dtype=int)
    output_grid = grid.copy() # Initialize output_grid as a copy of the input
    height, width = grid.shape

    # Find the center of the red cross
    center = find_cross_center(output_grid) # Use output_grid as it will be modified
    if center is None:
        # If no center found, return the original grid 
        # (as per ARC behavior, avoid crashing)
        return input_grid 

    center_r, center_c = center

    # Define colors and patterns
    blue_color = 1
    orthogonal_pattern = [8, 8, 4] # Azure, Azure, Yellow

    # Define starting points *and* directions relative to the center.
    # The start point is the pixel immediately adjacent to the center.
    # The direction is the vector pointing away from the center.
    # Format: ((start_r, start_c), (dr, dc), color, pattern)
    lines_to_draw = [
        # Diagonals (Blue) - Start points are diagonal neighbors of the center
        ((center_r - 1, center_c - 1), (-1, -1), blue_color, None), # Up-Left
        ((center_r - 1, center_c + 1), (-1, +1), blue_color, None), # Up-Right
        ((center_r + 1, center_c - 1), (+1, -1), blue_color, None), # Down-Left
        ((center_r + 1, center_c + 1), (+1, +1), blue_color, None), # Down-Right
        # Orthogonals (Pattern) - Start points are orthogonal neighbors of the center
        ((center_r - 1, center_c), (-1, 0), None, orthogonal_pattern), # Up
        ((center_r + 1, center_c), (+1, 0), None, orthogonal_pattern), # Down
        ((center_r, center_c - 1), (0, -1), None, orthogonal_pattern), # Left
        ((center_r, center_c + 1), (0, +1), None, orthogonal_pattern), # Right
    ]

    # Draw all the lines
    for (start_r, start_c), (dr, dc), color, pattern in lines_to_draw:
         # draw_line handles boundary checks for the start point internally
         draw_line(output_grid, start_r, start_c, dr, dc, color=color, pattern=pattern)

    # Convert back to list of lists for standard ARC output format
    return output_grid.tolist()