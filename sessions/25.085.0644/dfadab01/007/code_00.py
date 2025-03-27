import numpy as np

"""
The transformation identifies isolated pixels of specific 'trigger' colors (Red=2, Green=3, Gray=5) in the input grid. 
It then creates a copy of the input grid and draws a 4x4 hollow square onto this copy, centered at the location of each identified isolated trigger pixel. 
The color of the square's perimeter is determined by a mapping from the trigger color (Red->Yellow(4), Green->Blue(1), Gray->Magenta(6)). 
The 2x2 interior of the square is set to the background color (White=0). 
The drawing process overwrites any existing pixels in the copied grid within the 4x4 area.

1. Define trigger colors, background color, and color mapping:
   - Trigger colors: Red (2), Green (3), Gray (5)
   - Background color: White (0)
   - Color mapping: Red(2) -> Yellow(4), Green(3) -> Blue(1), Gray(5) -> Magenta(6)

2. Initialize output grid: Create a copy of the input grid.

3. Identify isolated trigger pixels: Iterate through the *original* input grid. For each pixel:
   - Check if its color is one of the trigger colors (2, 3, 5).
   - Check if all its 8 neighbors (orthogonal and diagonal) are the background color (0). Pixels on edges/corners are considered isolated if all their existing neighbors are background.
   - Store the location (row, col) and original color of each isolated trigger pixel found.

4. Draw hollow squares onto the output grid: For each isolated trigger pixel identified in step 3:
   - Get the center coordinates (r, c) and the trigger color.
   - Determine the corresponding output color using the mapping (2->4, 3->1, 5->6).
   - Calculate the top-left corner coordinates for a 4x4 square centered at (r, c). This would be (r-1, c-1).
   - Iterate through the 4x4 area defined by the top-left corner (from row r-1 to r+2, and col c-1 to c+2).
   - For each cell (nr, nc) within this 4x4 area:
     - Check if the cell coordinates (nr, nc) are within the grid boundaries.
     - If within bounds:
       - Determine if the cell is on the perimeter of the 4x4 square (nr is r-1 or r+2, OR nc is c-1 or c+2).
       - If it is on the perimeter, set the color of the cell in the output grid (`output_grid[nr, nc]`) to the determined output color.
       - If it is in the inner 2x2 area (not on the perimeter), set the color of the cell in the output grid (`output_grid[nr, nc]`) to the background color (0).

5. Return the final modified output grid.
"""

def is_isolated(grid, r, c, trigger_colors, background_color=0):
    """
    Checks if the pixel at (r, c) is one of the trigger_colors and 
    if all its 8 neighbors are the background_color.
    Handles grid boundaries implicitly.

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
    for r_offset in range(4):
        for c_offset in range(4):
            # Calculate current cell coordinates
            nr, nc = start_r + r_offset, start_c + c_offset
            
            # Ensure the drawing coordinates are within the grid bounds
            if 0 <= nr < height and 0 <= nc < width:
                # Determine if the current cell (nr, nc) is on the perimeter
                # A cell is on the perimeter if its row or column offset is 0 or 3
                is_perimeter = (r_offset == 0 or r_offset == 3 or
                                c_offset == 0 or c_offset == 3)
                                
                if is_perimeter:
                    # Set perimeter cells to the specified color
                    grid[nr, nc] = color
                else:
                    # Set inner (non-perimeter) cells to the background color
                    grid[nr, nc] = background_color


def transform(input_grid):
    """
    Transforms the input grid by drawing 4x4 hollow squares centered on 
    isolated trigger pixels (Red, Green, Gray), overwriting existing content.
    """
    height, width = input_grid.shape
    
    # 1. Define colors and mapping
    trigger_colors = {2, 3, 5} # Red, Green, Gray
    background_color = 0
    color_map = {
        2: 4, # Red -> Yellow
        3: 1, # Green -> Blue
        5: 6  # Gray -> Magenta
    }

    # 2. Initialize output grid (make a copy of the input)
    output_grid = np.copy(input_grid)

    # 3. Identify isolated trigger pixels in the *original* input grid
    isolated_pixels = []
    for r in range(height):
        for c in range(width):
            if is_isolated(input_grid, r, c, trigger_colors, background_color):
                isolated_pixels.append({
                    'r': r, 
                    'c': c, 
                    'color': input_grid[r,c]
                })

    # 4. Draw hollow squares onto the output grid for each isolated pixel
    #    This step modifies the output_grid directly, overwriting previous values.
    for pixel_info in isolated_pixels:
        center_r = pixel_info['r']
        center_c = pixel_info['c']
        trigger_color = pixel_info['color']
        output_color = color_map[trigger_color]
        
        draw_hollow_square(output_grid, center_r, center_c, output_color, background_color)
                
    # 5. Return the final modified grid
    return output_grid