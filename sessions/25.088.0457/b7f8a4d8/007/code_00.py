import numpy as np

"""
Identifies 3x3 objects with a single-color non-white frame (8 pixels) and a single non-white center pixel 
where the center color is different from the frame color. 
If the (frame_color, center_color) pair matches specific triggering conditions, 
it draws lines extending horizontally to the right and vertically downwards 
from the object's center pixel.
The lines are drawn with the center_color and stop when they hit a non-white pixel 
or the grid boundary.

Triggering Conditions (frame_color, center_color):
- Green(3), Yellow(4)
- Green(3), Azure(8)
- Red(2), Green(3)
- Red(2), Blue(1)
- Blue(1), Green(3)

1. Initialize the output grid as a copy of the input grid.
2. Scan the input grid to find all instances of "Framed 3x3 Square" objects. A "Framed 3x3 Square" is a 3x3 area where:
   - The 8 pixels forming the 1-pixel thick border are all of the same non-white color (frame_color).
   - The 1 pixel at the center (r+1, c+1) is a non-white color (center_color).
   - The frame_color is different from the center_color.
3. For each "Framed 3x3 Square" found at top-left position (r, c) with frame_color and center_color:
   - Check if the pair (frame_color, center_color) is one of the triggering pairs.
   - If it is a triggering pair:
     - Set the draw_color to be the center_color.
     - Define the center coordinates: r_center = r + 1, c_center = c + 1.
     - Draw Horizontal Line: Starting from column c_center + 1, iterate rightwards. Change white(0) pixels at row r_center to draw_color until a non-white pixel or the grid edge is hit.
     - Draw Vertical Line: Starting from row r_center + 1, iterate downwards. Change white(0) pixels at column c_center to draw_color until a non-white pixel or the grid edge is hit.
4. Return the modified output grid.
"""

def find_framed_3x3_squares(grid):
    """
    Finds all 3x3 squares with a solid non-white frame (8 pixels) of one color 
    and a single non-white center pixel of a different color.
    Returns a list of tuples: (top_left_row, top_left_col, frame_color, center_color).
    """
    squares = []
    height, width = grid.shape
    
    # Iterate through possible top-left corners (r, c)
    for r in range(height - 2): # Need space for 3 rows
        for c in range(width - 2): # Need space for 3 cols
            
            # Potential frame color from top-left
            frame_color = grid[r, c]
            
            # Frame must be non-white
            if frame_color == 0:
                continue

            # Check if all 8 frame pixels match frame_color
            is_frame_valid = True
            # Top row (r, c to c+2)
            if not np.all(grid[r, c:c+3] == frame_color): is_frame_valid = False
            # Bottom row (r+2, c to c+2)
            if is_frame_valid and not np.all(grid[r+2, c:c+3] == frame_color): is_frame_valid = False
            # Middle row sides (r+1, c) and (r+1, c+2)
            if is_frame_valid and not (grid[r+1, c] == frame_color and grid[r+1, c+2] == frame_color): is_frame_valid = False
            
            if not is_frame_valid:
                continue

            # Check center pixel
            center_color = grid[r + 1, c + 1]
            
            # Center must be non-white
            if center_color == 0:
                continue
                
            # Center color must be different from frame color 
            if center_color != frame_color: 
                squares.append((r, c, frame_color, center_color))
                
    return squares

def transform(input_grid_list):
    """
    Applies the transformation rule to the input grid.
    """
    # Convert list of lists to numpy array for easier processing
    input_grid = np.array(input_grid_list, dtype=int)
    # Initialize output grid as a copy of the input
    output_grid = np.copy(input_grid)
    height, width = output_grid.shape
    
    # Define the pairs that trigger the drawing action
    # (frame_color, center_color)
    TRIGGER_PAIRS = {
        (3, 4), # Green Frame, Yellow Center
        (3, 8), # Green Frame, Azure Center
        (2, 3), # Red Frame, Green Center
        (2, 1), # Red Frame, Blue Center
        (1, 3)  # Blue Frame, Green Center
    }
    
    # Find all the relevant 3x3 squares
    squares = find_framed_3x3_squares(input_grid)
    
    # Process each found square
    for r, c, frame_color, center_color in squares:
        
        # Check if the (frame_color, center_color) pair is a trigger
        if (frame_color, center_color) in TRIGGER_PAIRS:
            
            # Define drawing parameters
            r_center = r + 1
            c_center = c + 1
            draw_color = center_color # Use the center color for drawing
            
            # --- Draw horizontal line to the right ---
            # Start column is immediately right of the center pixel
            start_c_h = c_center + 1 
            if start_c_h < width: # Check if drawing start is within bounds
                for c_draw in range(start_c_h, width):
                    if output_grid[r_center, c_draw] == 0: # Only draw on white
                        output_grid[r_center, c_draw] = draw_color
                    else:
                        break # Stop if non-white pixel encountered
            
            # --- Draw vertical line downwards ---
            # Start row is immediately below the center pixel
            start_r_v = r_center + 1 
            if start_r_v < height: # Check if drawing start is within bounds
                for r_draw in range(start_r_v, height):
                    if output_grid[r_draw, c_center] == 0: # Only draw on white
                        output_grid[r_draw, c_center] = draw_color
                    else:
                        break # Stop if non-white pixel encountered

    # Return as list of lists, matching the expected format
    return output_grid.tolist()