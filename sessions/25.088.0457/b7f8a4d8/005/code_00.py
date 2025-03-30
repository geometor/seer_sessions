import numpy as np

"""
Identifies 4x4 objects with a single-color non-white frame and a 2x2 single-color non-white center 
where the center color is different from the frame color. 
If the (frame_color, center_color) pair matches specific triggering conditions, 
it draws lines extending horizontally to the right and vertically downwards 
from the object's center rows/columns.
The lines are drawn with the center_color and stop when they hit a non-white pixel 
or the grid boundary.

Triggering Conditions (frame_color, center_color):
- Green(3), Yellow(4)
- Green(3), Azure(8)
- Red(2), Green(3)
- Red(2), Blue(1)
- Blue(1), Green(3)

1. Initialize the output grid as a copy of the input grid.
2. Scan the input grid to find all instances of "Framed Square" objects. A "Framed Square" is a 4x4 area where:
   - The 12 pixels forming the 1-pixel thick border are all of the same non-white color (frame_color).
   - The 4 pixels forming the 2x2 center are all of the same non-white color (center_color).
   - The frame_color is different from the center_color.
3. For each "Framed Square" found at top-left position (r, c) with frame_color and center_color:
   - Check if the pair (frame_color, center_color) is one of the triggering pairs.
   - If it is a triggering pair:
     - Set the draw_color to be the center_color.
     - Define the center rows: r1 = r + 1, r2 = r + 2.
     - Define the center columns: c1 = c + 1, c2 = c + 2.
     - Draw Horizontal Lines:
       - For row r1, starting from column c + 4, iterate rightwards. Change white(0) pixels to draw_color until a non-white pixel or the grid edge is hit.
       - Repeat for row r2.
     - Draw Vertical Lines:
       - For column c1, starting from row r + 4, iterate downwards. Change white(0) pixels to draw_color until a non-white pixel or the grid edge is hit.
       - Repeat for column c2.
4. Return the modified output grid.
"""

def find_framed_4x4_squares(grid):
    """
    Finds all 4x4 squares with a solid non-white frame of one color 
    and a solid non-white 2x2 center of a different color.
    Returns a list of tuples: (top_left_row, top_left_col, frame_color, center_color).
    """
    squares = []
    height, width = grid.shape
    
    # Iterate through possible top-left corners (r, c)
    for r in range(height - 3): # Need space for 4 rows
        for c in range(width - 3): # Need space for 4 cols
            
            # Potential frame color from top-left
            frame_color = grid[r, c]
            
            # Frame must be non-white
            if frame_color == 0:
                continue

            # Check if all 12 frame pixels match frame_color
            is_frame_valid = True
            # Top row (r, c to c+3)
            if not np.all(grid[r, c:c+4] == frame_color): is_frame_valid = False
            # Bottom row (r+3, c to c+3)
            if is_frame_valid and not np.all(grid[r+3, c:c+4] == frame_color): is_frame_valid = False
            # Left col (r+1 to r+2, c)
            if is_frame_valid and not np.all(grid[r+1:r+3, c] == frame_color): is_frame_valid = False
            # Right col (r+1 to r+2, c+3)
            if is_frame_valid and not np.all(grid[r+1:r+3, c+3] == frame_color): is_frame_valid = False
            
            if not is_frame_valid:
                continue

            # Check 2x2 center block
            center_color = grid[r + 1, c + 1]
            # Center must be non-white
            if center_color == 0:
                continue
                
            is_center_valid = True
            if not np.all(grid[r+1:r+3, c+1:c+3] == center_color):
                is_center_valid = False
            
            if not is_center_valid:
                continue

            # Center color must be different from frame color 
            if center_color != frame_color: 
                squares.append((r, c, frame_color, center_color))
                
    return squares

def transform(input_grid_list):
    """
    Applies the transformation rule to the input grid.
    """
    input_grid = np.array(input_grid_list, dtype=int)
    output_grid = np.copy(input_grid)
    height, width = output_grid.shape
    
    # Define the pairs that trigger the drawing action
    TRIGGER_PAIRS = {
        (3, 4), # Green Frame, Yellow Center
        (3, 8), # Green Frame, Azure Center
        (2, 3), # Red Frame, Green Center
        (2, 1), # Red Frame, Blue Center
        (1, 3)  # Blue Frame, Green Center
    }
    
    # Find all the relevant 4x4 squares
    squares = find_framed_4x4_squares(input_grid)
    
    # Process each found square
    for r, c, frame_color, center_color in squares:
        
        # Check if the (frame_color, center_color) pair is a trigger
        if (frame_color, center_color) in TRIGGER_PAIRS:
            
            # Define drawing parameters
            r_center1, r_center2 = r + 1, r + 2
            c_center1, c_center2 = c + 1, c + 2
            draw_color = center_color # Use the center color for drawing
            
            # --- Draw horizontal lines to the right ---
            start_c_h = c + 4 # Start column is immediately right of the square frame
            
            # Row r_center1
            if start_c_h < width: # Check if drawing start is within bounds
                for c_draw in range(start_c_h, width):
                    if output_grid[r_center1, c_draw] == 0: # Only draw on white
                        output_grid[r_center1, c_draw] = draw_color
                    else:
                        break # Stop if non-white pixel encountered
            
            # Row r_center2
            if start_c_h < width: # Check if drawing start is within bounds
                for c_draw in range(start_c_h, width):
                    if output_grid[r_center2, c_draw] == 0: # Only draw on white
                        output_grid[r_center2, c_draw] = draw_color
                    else:
                        break # Stop if non-white pixel encountered
            
            # --- Draw vertical lines downwards ---
            start_r_v = r + 4 # Start row is immediately below the square frame

            # Column c_center1
            if start_r_v < height: # Check if drawing start is within bounds
                for r_draw in range(start_r_v, height):
                    if output_grid[r_draw, c_center1] == 0: # Only draw on white
                        output_grid[r_draw, c_center1] = draw_color
                    else:
                        break # Stop if non-white pixel encountered

            # Column c_center2
            if start_r_v < height: # Check if drawing start is within bounds
                 for r_draw in range(start_r_v, height):
                     if output_grid[r_draw, c_center2] == 0: # Only draw on white
                        output_grid[r_draw, c_center2] = draw_color
                     else:
                        break # Stop if non-white pixel encountered

    return output_grid.tolist() # Return as list of lists