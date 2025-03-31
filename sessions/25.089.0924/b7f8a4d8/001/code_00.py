import numpy as np

"""
Identifies specific framed objects within the input grid based on their border color and size.
For each object found, it extracts the color of the inner content.
If the inner color matches a predefined 'trigger' color associated with that object type, 
new shapes are drawn in the empty (white) space adjacent to the original object.
The color, shape, and position of the new shapes depend on the specific trigger color and object type identified.
The original objects remain unchanged in the output grid.

Pattern 1 (Derived from train_1):
- Object: 5x5 Green (3) border, 2x2 inner block.
- Triggers: Azure (8), Yellow (4).
- Action: Draw a 2x2 block of the trigger color immediately to the right of the 5x5 frame, 
          vertically aligned with the inner 2x2 block.

Pattern 2 (Derived from train_2):
- Object: 3x3 Red (2) border, 1x1 inner pixel at the center.
- Triggers: Green (3), Blue (1).
- Action: Draw two separate 1x2 vertical lines of the trigger color.
          - Line 1: Two columns right of the center pixel, aligned vertically with the center pixel and the row below it.
          - Line 2: Four columns right of the center pixel, aligned vertically with the center pixel and the row below it.

Pattern 3 (Derived from train_3):
- Object: 3x3 Blue (1) border, 1x1 inner pixel at the center.
- Triggers: Green (3).
- Action: 
          - Draw a 3x3 block of Green (3) immediately to the right of the 3x3 frame, vertically aligned.
          - Draw a 1x3 vertical line of Green (3) immediately below the 3x3 frame, horizontally aligned with its center column.
"""

def is_valid(r, c, height, width):
    """Check if coordinates are within grid bounds."""
    return 0 <= r < height and 0 <= c < width

def check_pattern_1(grid, r, c, height, width):
    """Checks for the 5x5 Green frame pattern."""
    if r + 4 >= height or c + 4 >= width:
        return False, -1 # Not enough space

    # Check border
    for i in range(5):
        if grid[r, c+i] != 3 or grid[r+4, c+i] != 3: return False, -1 # Top/Bottom border
        if grid[r+i, c] != 3 or grid[r+i, c+4] != 3: return False, -1 # Left/Right border
    
    # Check inner content (assuming it's uniform 2x2 for trigger check)
    inner_color = grid[r+1, c+1] 
    # Verify the 2x2 inner block consistency (optional but good practice)
    if grid[r+1, c+2] != inner_color or \
       grid[r+2, c+1] != inner_color or \
       grid[r+2, c+2] != inner_color:
        # This case might indicate an invalid object or a variation not seen in training
        # For now, we base trigger on top-left inner pixel
        pass 

    return True, inner_color

def check_pattern_2_3(grid, r, c, height, width, border_color):
    """Checks for the 3x3 frame patterns (Red or Blue border)."""
    if r + 2 >= height or c + 2 >= width:
        return False, -1 # Not enough space

    # Check border
    for i in range(3):
        if grid[r, c+i] != border_color or grid[r+2, c+i] != border_color: return False, -1 # Top/Bottom border
        if grid[r+i, c] != border_color or grid[r+i, c+2] != border_color: return False, -1 # Left/Right border

    # Get inner content color
    inner_color = grid[r+1, c+1]
    return True, inner_color

def draw_block(output_grid, r, c, h, w, color, height, width):
    """Draws a solid block of color."""
    for i in range(h):
        for j in range(w):
            nr, nc = r + i, c + j
            # Draw only on white background
            if is_valid(nr, nc, height, width) and output_grid[nr, nc] == 0:
                output_grid[nr, nc] = color

def draw_vline(output_grid, r, c, h, color, height, width):
    """Draws a vertical line."""
    draw_block(output_grid, r, c, h, 1, color, height, width)

def transform(input_grid):
    """
    Applies the transformation rules based on identified patterns.
    """
    input_grid_np = np.array(input_grid, dtype=int)
    output_grid_np = np.copy(input_grid_np)
    height, width = input_grid_np.shape

    # Iterate through each cell as a potential top-left corner
    for r in range(height):
        for c in range(width):
            
            # Check for Pattern 1 (5x5 Green frame)
            is_p1, inner_color_p1 = check_pattern_1(input_grid_np, r, c, height, width)
            if is_p1:
                # Check triggers for Pattern 1
                if inner_color_p1 == 8 or inner_color_p1 == 4: # Azure or Yellow
                    # Calculate draw position: right of frame, aligned with inner block
                    draw_r, draw_c = r + 1, c + 5
                    # Draw 2x2 block
                    draw_block(output_grid_np, draw_r, draw_c, 2, 2, inner_color_p1, height, width)
                # Continue to next potential corner after finding a 5x5 block
                # This basic loop might re-check parts of found blocks, but is simple.
                # A more optimized approach would skip columns/rows known to be part of this block.
                continue # Skip other checks if pattern 1 found

            # Check for Pattern 2 (3x3 Red frame)
            is_p2, inner_color_p2 = check_pattern_2_3(input_grid_np, r, c, height, width, border_color=2)
            if is_p2:
                 # Check triggers for Pattern 2
                if inner_color_p2 == 3 or inner_color_p2 == 1: # Green or Blue
                    # Calculate draw positions relative to center (r+1, c+1)
                    center_r, center_c = r + 1, c + 1
                    # Position 1: 2 columns right
                    draw_c1 = center_c + 2
                    draw_vline(output_grid_np, center_r, draw_c1, 2, inner_color_p2, height, width)
                    # Position 2: 4 columns right
                    draw_c2 = center_c + 4
                    draw_vline(output_grid_np, center_r, draw_c2, 2, inner_color_p2, height, width)
                continue # Skip pattern 3 check if pattern 2 found

            # Check for Pattern 3 (3x3 Blue frame)
            is_p3, inner_color_p3 = check_pattern_2_3(input_grid_np, r, c, height, width, border_color=1)
            if is_p3:
                 # Check triggers for Pattern 3
                if inner_color_p3 == 3: # Green
                    # Action 1: Draw 3x3 block to the right
                    draw_r1, draw_c1 = r, c + 3
                    draw_block(output_grid_np, draw_r1, draw_c1, 3, 3, inner_color_p3, height, width)
                    # Action 2: Draw 1x3 vertical line below center
                    draw_r2, draw_c2 = r + 3, c + 1
                    draw_vline(output_grid_np, draw_r2, draw_c2, 3, inner_color_p3, height, width)
                # No continue needed as this is the last check in the loop

    return output_grid_np.tolist()