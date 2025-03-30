import numpy as np

"""
Identifies 4x4 objects with a single-color frame and a 2x2 single-color center 
where the center color is different from the frame color. 
If the center color is not red (2) or yellow (4), it draws lines extending 
horizontally to the right and vertically downwards from the object's center rows/columns.
The lines are drawn with the center color and stop when they hit a non-white pixel 
or the grid boundary.

1. Iterate through the input grid to find potential top-left corners (r, c) of 4x4 objects.
2. For each potential corner (r, c):
   a. Check if a 4x4 square exists starting at (r, c).
   b. Identify the frame color (must be non-white) from grid[r, c].
   c. Verify that all 12 pixels forming the 1-pixel thick border of the 4x4 square match the frame_color.
   d. Identify the potential center color from grid[r+1, c+1].
   e. Verify that the 2x2 center block (grid[r+1:r+3, c+1:c+3]) consists entirely of the center_color.
   f. Verify that the frame_color and center_color are different.
3. If such a 4x4 object is found:
   a. Check if the center_color is one of the "active" colors (NOT red=2 and NOT yellow=4).
   b. If center_color is an "active" color:
      i. Get the coordinates of the center rows/columns: 
         r_center1 = r + 1, r_center2 = r + 2
         c_center1 = c + 1, c_center2 = c + 2
         draw_color = center_color
      ii. Draw Horizontal Lines: 
          - Starting from the column immediately right of the object (c + 4), move rightwards. 
          - Fill white (0) cells in rows r_center1 and r_center2 with draw_color 
            until a non-white pixel or the grid edge is encountered for each row independently.
      iii. Draw Vertical Lines: 
           - Starting from the row immediately below the object (r + 4), move downwards.
           - Fill white (0) cells in columns c_center1 and c_center2 with draw_color 
             until a non-white pixel or the grid edge is encountered for each column independently.
4. The output grid is the initial grid modified with all the drawn lines.
"""

def is_valid(r, c, height, width):
    """Checks if coordinates are within grid bounds."""
    return 0 <= r < height and 0 <= c < width

def find_framed_4x4_squares(grid):
    """
    Finds all 4x4 squares with a solid frame of one color 
    and a solid 2x2 center of a different color.
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

            # Check if all frame pixels match frame_color
            is_frame_valid = True
            # Top row
            for fc in range(c, c + 4):
                if grid[r, fc] != frame_color:
                    is_frame_valid = False; break
            if not is_frame_valid: continue
            # Bottom row
            for fc in range(c, c + 4):
                 if grid[r + 3, fc] != frame_color:
                    is_frame_valid = False; break
            if not is_frame_valid: continue
            # Left col (middle rows)
            for fr in range(r + 1, r + 3):
                 if grid[fr, c] != frame_color:
                    is_frame_valid = False; break
            if not is_frame_valid: continue
            # Right col (middle rows)
            for fr in range(r + 1, r + 3):
                 if grid[fr, c + 3] != frame_color:
                    is_frame_valid = False; break
            
            if not is_frame_valid:
                continue

            # Check 2x2 center block
            center_color = grid[r + 1, c + 1]
            is_center_valid = True
            for cr in range(r + 1, r + 3):
                for cc in range(c + 1, c + 3):
                    if grid[cr, cc] != center_color:
                        is_center_valid = False; break
                if not is_center_valid: break
            
            if not is_center_valid:
                continue

            # Center color must be different from frame color and non-white
            # Although center being white isn't explicitly forbidden by text, 
            # examples don't show it, and it likely wouldn't trigger drawing.
            # We keep the check simple: different from frame.
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
    
    # Find all the relevant 4x4 squares
    squares = find_framed_4x4_squares(input_grid)
    
    # Process each found square
    for r, c, frame_color, center_color in squares:
        
        # Check if the center color triggers the drawing action (not red=2 and not yellow=4)
        if center_color != 2 and center_color != 4:
            
            r_center1, r_center2 = r + 1, r + 2
            c_center1, c_center2 = c + 1, c + 2
            draw_color = center_color # Use the center color for drawing
            
            # --- Draw horizontal lines to the right ---
            start_c_h = c + 4 # Start column is immediately right of the square frame
            
            # Row r_center1
            for c_draw in range(start_c_h, width):
                if output_grid[r_center1, c_draw] == 0: # Only draw on white
                    output_grid[r_center1, c_draw] = draw_color
                else:
                    break # Stop if non-white pixel encountered
            
            # Row r_center2
            for c_draw in range(start_c_h, width):
                if output_grid[r_center2, c_draw] == 0: # Only draw on white
                    output_grid[r_center2, c_draw] = draw_color
                else:
                    break # Stop if non-white pixel encountered
            
            # --- Draw vertical lines downwards ---
            start_r_v = r + 4 # Start row is immediately below the square frame

            # Column c_center1
            for r_draw in range(start_r_v, height):
                if output_grid[r_draw, c_center1] == 0: # Only draw on white
                    output_grid[r_draw, c_center1] = draw_color
                else:
                    break # Stop if non-white pixel encountered

            # Column c_center2
            for r_draw in range(start_r_v, height):
                 if output_grid[r_draw, c_center2] == 0: # Only draw on white
                    output_grid[r_draw, c_center2] = draw_color
                 else:
                    break # Stop if non-white pixel encountered

    return output_grid.tolist() # Return as list of lists