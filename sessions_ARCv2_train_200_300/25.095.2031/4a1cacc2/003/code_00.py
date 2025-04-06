import math

"""
Identify the unique non-background pixel (not '8') in the input grid. 
Determine its location (r, c) and color (C). 
Calculate the grid's midpoint (mid_r, mid_c).
Based on whether the pixel is in the top-left, top-right, bottom-left, or bottom-right quadrant relative to the midpoint, 
fill a corresponding rectangular area in the output grid with the color C.
The boundaries of this rectangle are defined by the pixel's coordinates (r, c) and the grid edges. 
All other cells in the output grid are filled with the background color '8'.
"""

def find_foreground_pixel(grid: list[list[int]], background_color: int) -> tuple[int, int, int]:
    """Finds the row, column, and color of the first pixel not matching the background color."""
    height = len(grid)
    width = len(grid[0]) if height > 0 else 0
    for r in range(height):
        for c in range(width):
            if grid[r][c] != background_color:
                return r, c, grid[r][c]
    # Should not happen based on task description, but return invalid values if no foreground pixel is found
    return -1, -1, -1 

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Transforms the input grid based on the quadrant location of the foreground pixel.
    """
    
    # Define background color
    background_color = 8
    
    # Get grid dimensions
    height = len(input_grid)
    if height == 0:
        return []
    width = len(input_grid[0])
    if width == 0:
        return [[] for _ in range(height)]

    # Find the single foreground pixel's location (r, c) and color (C)
    fg_r, fg_c, fg_color = find_foreground_pixel(input_grid, background_color)

    # Handle edge case where no foreground pixel is found (unlikely given examples)
    if fg_r == -1:
        # Return a grid filled only with background color
        return [[background_color for _ in range(width)] for _ in range(height)]
        
    # Calculate the grid's midpoint coordinates
    mid_r = height // 2
    mid_c = width // 2

    # Initialize the output grid with the background color
    output_grid = [[background_color for _ in range(width)] for _ in range(height)]

    # Determine the quadrant and define the fill ranges based on foreground pixel location (fg_r, fg_c)
    row_start, row_end, col_start, col_end = 0, 0, 0, 0

    if fg_r < mid_r and fg_c < mid_c: # Top-Left (TL) quadrant
        row_start, row_end = 0, fg_r + 1
        col_start, col_end = 0, fg_c + 1
    elif fg_r < mid_r and fg_c >= mid_c: # Top-Right (TR) quadrant
        row_start, row_end = 0, fg_r + 1
        col_start, col_end = fg_c, width
    elif fg_r >= mid_r and fg_c < mid_c: # Bottom-Left (BL) quadrant
        row_start, row_end = fg_r, height
        col_start, col_end = 0, fg_c + 1
    else: # Bottom-Right (BR) quadrant (fg_r >= mid_r and fg_c >= mid_c)
        row_start, row_end = fg_r, height
        col_start, col_end = fg_c, width

    # Fill the determined rectangular area in the output grid with the foreground color
    for r in range(row_start, row_end):
        for c in range(col_start, col_end):
            # Ensure we don't write outside grid bounds (though logic should prevent this if fg pixel is valid)
            if 0 <= r < height and 0 <= c < width:
                 output_grid[r][c] = fg_color
            
    return output_grid