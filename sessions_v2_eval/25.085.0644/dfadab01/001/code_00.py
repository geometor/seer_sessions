import numpy as np

"""
Identifies isolated pixels of specific colors (red (2), green (3), gray (5)) and replaces the area around them with a 4x4 hollow square of a corresponding mapped color (yellow (4), blue (1), magenta (6), respectively). 

An isolated pixel is defined as a pixel whose 8 neighbors (orthogonal and diagonal) are all the background color (white, 0). Pixels on the border or corner of the grid are considered isolated if all their existing neighbors are background color.

When an isolated pixel of a trigger color is found at position (r, c), a 4x4 hollow square is drawn on the output grid. This square is centered at (r, c), meaning its top-left corner is at (r-1, c-1). The perimeter of the 4x4 square is set to the mapped color, and the inner 2x2 area is set to the background color (white, 0). Drawing respects grid boundaries.

All other pixels from the input grid that are not part of these transformations (i.e., not isolated trigger pixels and not part of the area where a hollow square is drawn) remain unchanged in the output grid.
"""


def is_isolated(grid, r, c, trigger_colors, background_color=0):
    """
    Checks if the pixel at (r, c) is one of the trigger_colors and 
    if all its 8 neighbors are the background_color.
    Handles grid boundaries implicitly (out-of-bounds is treated as isolated).

    Args:
        grid (np.array): The input grid.
        r (int): Row index of the pixel to check.
        c (int): Column index of the pixel to check.
        trigger_colors (set): Set of colors that trigger the transformation if isolated.
        background_color (int): The color value considered as background.

    Returns:
        bool: True if the pixel is isolated and has a trigger color, False otherwise.
    """
    height, width = grid.shape
    
    # Check if the center pixel itself has a trigger color
    if grid[r, c] not in trigger_colors:
        return False
        
    # Check all 8 neighbors
    for dr in [-1, 0, 1]:
        for dc in [-1, 0, 1]:
            # Skip the center cell itself
            if dr == 0 and dc == 0:
                continue
            
            nr, nc = r + dr, c + dc
            
            # Check if the neighbor coordinate is within grid bounds
            if 0 <= nr < height and 0 <= nc < width:
                # If the neighbor is within bounds, it MUST be the background color
                if grid[nr, nc] != background_color:
                    return False
            # If the neighbor is out of bounds, it doesn't violate the isolation condition.
            
    # If all existing neighbors were background, the pixel is isolated
    return True

def draw_hollow_square(grid, center_r, center_c, color, background_color=0):
    """
    Draws a 4x4 hollow square of the specified 'color' onto the 'grid',
    centered at (center_r, center_c). The inner 2x2 area is set to 
    'background_color'. Modifies the grid in place. Handles grid boundaries.

    Args:
        grid (np.array): The grid to draw on (modified in place).
        center_r (int): Row index of the center of the square.
        center_c (int): Column index of the center of the square.
        color (int): The color to use for the square's perimeter.
        background_color (int): The color to use for the square's interior.
    """
    height, width = grid.shape
    # Calculate the top-left corner of the 4x4 bounding box
    start_r, start_c = center_r - 1, center_c - 1
    
    # Iterate over the 4x4 area where the square should be drawn
    for r in range(start_r, start_r + 4):
        for c in range(start_c, start_c + 4):
            # Ensure the drawing coordinates are within the grid bounds
            if 0 <= r < height and 0 <= c < width:
                # Determine if the current cell (r, c) is on the perimeter
                # A cell is on the perimeter if its row is the start/end row
                # OR its column is the start/end column of the 4x4 box.
                is_perimeter = (r == start_r or r == start_r + 3 or
                                c == start_c or c == start_c + 3)
                                
                if is_perimeter:
                    # Set perimeter cells to the specified color
                    grid[r, c] = color
                else:
                    # Set inner (non-perimeter) cells to the background color
                    grid[r, c] = background_color

def transform(input_grid):
    """
    Transforms the input grid by finding isolated red (2), green (3), or gray (5) 
    pixels and replacing the area around them with a centered 4x4 hollow square 
    of yellow (4), blue (1), or magenta (6) respectively.

    Args:
        input_grid (np.array): The 2D numpy array representing the input grid.

    Returns:
        np.array: The 2D numpy array representing the transformed output grid.
    """
    # Create a copy of the input grid to avoid modifying the original
    output_grid = np.copy(input_grid)
    height, width = input_grid.shape
    
    # Define the colors that trigger the transformation when isolated
    trigger_colors = {2, 3, 5} # Red, Green, Gray
    
    # Define the mapping from trigger color to the output square color
    color_map = {
        2: 4, # Red -> Yellow
        3: 1, # Green -> Blue
        5: 6  # Gray -> Magenta
    }
    
    # Define the background color
    background_color = 0

    # Iterate through each cell of the input grid
    for r in range(height):
        for c in range(width):
            # Check if the current cell contains an isolated trigger pixel
            # Use the input_grid for checking conditions
            if is_isolated(input_grid, r, c, trigger_colors, background_color):
                # Get the corresponding color for the output square
                output_color = color_map[input_grid[r, c]]
                
                # Draw the hollow square onto the output grid
                # The draw function modifies the output_grid in place
                draw_hollow_square(output_grid, r, c, output_color, background_color)
                
    # Return the modified grid
    return output_grid