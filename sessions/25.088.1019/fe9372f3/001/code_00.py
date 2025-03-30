import numpy as np

"""
Identifies a red '+' shape in the input grid.
Preserves the original red cross in the output grid.
Draws lines radiating outwards from the cross towards the grid boundaries.
- Diagonal lines starting from the corners adjacent to the cross are drawn in blue (1).
- Orthogonal lines starting from the pixels adjacent to the central arms of the cross are drawn with a repeating pattern of Azure (8), Azure (8), Yellow (4).
Lines only overwrite white (0) background pixels.
"""

def find_cross_center(grid):
    """Finds the center pixel of the red '+' cross."""
    red_pixels = np.where(grid == 2)
    if not red_pixels or len(red_pixels[0]) == 0:
        # Handle cases where no red pixels are found (optional, based on task constraints)
        return None 

    # Iterate through potential centers (red pixels)
    for r, c in zip(red_pixels[0], red_pixels[1]):
        # Check for 4 red neighbours within bounds
        is_center = True
        height, width = grid.shape
        # Check North
        if r == 0 or grid[r-1, c] != 2: is_center = False
        # Check South
        if r == height - 1 or grid[r+1, c] != 2: is_center = False
        # Check West
        if c == 0 or grid[r, c-1] != 2: is_center = False
        # Check East
        if c == width - 1 or grid[r, c+1] != 2: is_center = False
        
        if is_center:
            return (r, c)
            
    # Fallback or error if no center is found (might indicate malformed input)
    # For ARC, we can often assume valid input structure based on examples.
    # Let's try a simpler approach if the strict center check fails: find the mean coordinate.
    if len(red_pixels[0]) > 0:
        center_r = int(np.round(np.mean(red_pixels[0])))
        center_c = int(np.round(np.mean(red_pixels[1])))
        # Verify if this calculated center is indeed red
        if grid[center_r, center_c] == 2:
             return (center_r, center_c)

    return None # Indicate failure to find a suitable center

def draw_line(grid, start_r, start_c, dr, dc, color=None, pattern=None):
    """
    Draws a line on the grid starting from (start_r, start_c) moving in direction (dr, dc).
    Can draw a single color line or a patterned line.
    Only overwrites white (0) pixels.
    """
    height, width = grid.shape
    r, c = start_r + dr, start_c + dc  # Start drawing from the next pixel
    k = 0 # Pattern counter

    while 0 <= r < height and 0 <= c < width:
        if grid[r, c] == 0: # Only draw on white background
            k += 1
            if pattern:
                current_color = pattern[(k - 1) % len(pattern)]
                grid[r, c] = current_color
            elif color is not None:
                grid[r, c] = color
            else:
                 # Should not happen if called correctly
                 break 
        
        # Stop if we hit a non-background pixel along the path? 
        # The examples suggest lines extend fully to boundary regardless of intermediate colors.
        # So, continue moving even if we don't draw.
        
        r += dr
        c += dc


def transform(input_grid):
    """
    Applies the transformation rule: find red cross, draw radiating lines.
    """
    # Convert input to numpy array for easier manipulation
    grid = np.array(input_grid, dtype=int)
    output_grid = grid.copy() # Start with a copy of the input
    height, width = grid.shape

    # Find the center of the red cross
    center = find_cross_center(grid)
    if center is None:
        # If no center found, return the original grid (or handle as error)
        return input_grid 

    center_r, center_c = center

    # Define colors and patterns
    blue_color = 1
    orthogonal_pattern = [8, 8, 4] # Azure, Azure, Yellow

    # Define starting points relative to the center for the pixel *adjacent* to the 3x3 box
    # These are the points *from* which the drawing starts in the given direction
    start_points_directions = [
        # Diagonals (Blue)
        ((center_r - 1, center_c - 1), (-1, -1), blue_color, None), # Up-Left
        ((center_r - 1, center_c + 1), (-1, +1), blue_color, None), # Up-Right
        ((center_r + 1, center_c - 1), (+1, -1), blue_color, None), # Down-Left
        ((center_r + 1, center_c + 1), (+1, +1), blue_color, None), # Down-Right
        # Orthogonals (Pattern)
        ((center_r - 1, center_c), (-1, 0), None, orthogonal_pattern), # Up
        ((center_r + 1, center_c), (+1, 0), None, orthogonal_pattern), # Down
        ((center_r, center_c - 1), (0, -1), None, orthogonal_pattern), # Left
        ((center_r, center_c + 1), (0, +1), None, orthogonal_pattern), # Right
    ]

    # Draw all the lines
    for (start_r, start_c), (dr, dc), color, pattern in start_points_directions:
         # Check if start point itself is valid before calling draw_line
         if 0 <= start_r < height and 0 <= start_c < width:
             draw_line(output_grid, start_r, start_c, dr, dc, color=color, pattern=pattern)


    # Convert back to list of lists for standard ARC output format
    return output_grid.tolist()
