
Previous Code:
```python
import numpy as np

"""
Identifies 3x3 objects with a single-color frame and a different center color. 
If the center color is not red (2) or yellow (4), it draws lines extending 
horizontally to the right and vertically downwards from the object's center row/column.
The lines are drawn with the center color and stop when they hit a non-white pixel 
or the grid boundary.

1. Iterate through the input grid to find potential top-left corners (r, c) of 3x3 objects.
2. For each potential corner, check if it forms a 3x3 square with a solid, 
   single-color frame (frame_color != 0) and a center pixel (center_color) 
   that is different from the frame_color.
3. If such a 3x3 object is found:
   a. Check if the center_color is one of the "active" colors (NOT red=2 and NOT yellow=4).
   b. If center_color is an "active" color:
      i. Get the coordinates of the center pixel: r_center = r + 1, c_center = c + 1.
      ii. Draw Horizontal Line: Starting from the column immediately right of the 
          object (c_center + 2), move rightwards. Fill white (0) cells in the 
          center row (r_center) with the center_color until a non-white pixel 
          or the grid edge is encountered.
      iii. Draw Vertical Line: Starting from the row immediately below the object 
           (r_center + 2), move downwards. Fill white (0) cells in the center 
           column (c_center) with the center_color until a non-white pixel or 
           the grid edge is encountered.
4. The output grid is the initial grid modified with all the drawn lines.
"""

def is_valid(r, c, height, width):
    """Checks if coordinates are within grid bounds."""
    return 0 <= r < height and 0 <= c < width

def find_framed_squares(grid):
    """
    Finds all 3x3 squares with a solid frame of one color 
    and a different center color.
    Returns a list of tuples: (top_left_row, top_left_col, frame_color, center_color).
    """
    squares = []
    height, width = grid.shape
    
    # Iterate through possible top-left corners (r, c)
    for r in range(height - 2):
        for c in range(width - 2):
            # Potential frame color from top-left
            frame_color = grid[r, c]
            
            # Frame must be non-white
            if frame_color == 0:
                continue

            # Check if all frame pixels match frame_color
            is_frame = True
            frame_coords = [
                (r, c), (r, c + 1), (r, c + 2),
                (r + 1, c),           (r + 1, c + 2),
                (r + 2, c), (r + 2, c + 1), (r + 2, c + 2)
            ]
            for fr, fc in frame_coords:
                if not is_valid(fr, fc, height, width) or grid[fr, fc] != frame_color:
                    is_frame = False
                    break
            
            if not is_frame:
                continue

            # Check center pixel
            center_r, center_c = r + 1, c + 1
            center_color = grid[center_r, center_c]

            # Center color must be different from frame color
            if center_color != frame_color:
                squares.append((r, c, frame_color, center_color))
                
    return squares

def transform(input_grid):
    """
    Applies the transformation rule to the input grid.
    """
    output_grid = np.copy(input_grid)
    height, width = output_grid.shape
    
    # Find all the relevant 3x3 squares
    squares = find_framed_squares(input_grid)
    
    # Process each found square
    for r, c, frame_color, center_color in squares:
        
        # Check if the center color triggers the drawing action (not red or yellow)
        if center_color != 2 and center_color != 4:
            
            r_center, c_center = r + 1, c + 1
            draw_color = center_color # Use the center color for drawing
            
            # Draw horizontal line to the right
            # Start column is immediately right of the square frame
            start_c_h = c + 3 
            for c_draw in range(start_c_h, width):
                if is_valid(r_center, c_draw, height, width) and output_grid[r_center, c_draw] == 0:
                    output_grid[r_center, c_draw] = draw_color
                else:
                    # Stop if out of bounds or non-white pixel encountered
                    break 
            
            # Draw vertical line downwards
            # Start row is immediately below the square frame
            start_r_v = r + 3 
            for r_draw in range(start_r_v, height):
                if is_valid(r_draw, c_center, height, width) and output_grid[r_draw, c_center] == 0:
                    output_grid[r_draw, c_center] = draw_color
                else:
                    # Stop if out of bounds or non-white pixel encountered
                    break

    return output_grid.tolist() # Return as list of lists as per ARC standard

```
Results for code_00.py:

Train Set Results:

## Example 1:
Input:
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 3 3 3 3 0 3 3 3 3 0 3 3 3 3 0 3 3 3 3 0 3 3 3 3 0 3 3 3
0 3 2 2 3 0 3 2 2 3 0 3 2 2 3 0 3 8 8 3 0 3 2 2 3 0 3 8 8
0 3 2 2 3 0 3 2 2 3 0 3 2 2 3 0 3 8 8 3 0 3 2 2 3 0 3 8 8
0 3 3 3 3 0 3 3 3 3 0 3 3 3 3 0 3 3 3 3 0 3 3 3 3 0 3 3 3
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 3 3 3 3 0 3 3 3 3 0 3 3 3 3 0 3 3 3 3 0 3 3 3 3 0 3 3 3
0 3 2 2 3 0 3 2 2 3 0 3 2 2 3 0 3 2 2 3 0 3 2 2 3 0 3 2 2
0 3 2 2 3 0 3 2 2 3 0 3 2 2 3 0 3 2 2 3 0 3 2 2 3 0 3 2 2
0 3 3 3 3 0 3 3 3 3 0 3 3 3 3 0 3 3 3 3 0 3 3 3 3 0 3 3 3
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 3 3 3 3 0 3 3 3 3 0 3 3 3 3 0 3 3 3 3 0 3 3 3 3 0 3 3 3
0 3 2 2 3 0 3 4 4 3 0 3 2 2 3 0 3 2 2 3 0 3 4 4 3 0 3 2 2
0 3 2 2 3 0 3 4 4 3 0 3 2 2 3 0 3 2 2 3 0 3 4 4 3 0 3 2 2
0 3 3 3 3 0 3 3 3 3 0 3 3 3 3 0 3 3 3 3 0 3 3 3 3 0 3 3 3
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 3 3 3 3 0 3 3 3 3 0 3 3 3 3 0 3 3 3 3 0 3 3 3 3 0 3 3 3
0 3 2 2 3 0 3 2 2 3 0 3 2 2 3 0 3 8 8 3 0 3 2 2 3 0 3 8 8
0 3 2 2 3 0 3 2 2 3 0 3 2 2 3 0 3 8 8 3 0 3 2 2 3 0 3 8 8
0 3 3 3 3 0 3 3 3 3 0 3 3 3 3 0 3 3 3 3 0 3 3 3 3 0 3 3 3
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 3 3 3 3 0 3 3 3 3 0 3 3 3 3 0 3 3 3 3 0 3 3 3 3 0 3 3 3
0 3 2 2 3 0 3 4 4 3 0 3 2 2 3 0 3 2 2 3 0 3 4 4 3 0 3 2 2
0 3 2 2 3 0 3 4 4 3 0 3 2 2 3 0 3 2 2 3 0 3 4 4 3 0 3 2 2
```
Expected Output:
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 3 3 3 3 0 3 3 3 3 0 3 3 3 3 0 3 3 3 3 0 3 3 3 3 0 3 3 3
0 3 2 2 3 0 3 2 2 3 0 3 2 2 3 0 3 8 8 3 8 3 2 2 3 8 3 8 8
0 3 2 2 3 0 3 2 2 3 0 3 2 2 3 0 3 8 8 3 8 3 2 2 3 8 3 8 8
0 3 3 3 3 0 3 3 3 3 0 3 3 3 3 0 3 3 3 3 0 3 3 3 3 0 3 3 3
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 8 8 0 0 0 0 0 0 0 0 8 8
0 3 3 3 3 0 3 3 3 3 0 3 3 3 3 0 3 3 3 3 0 3 3 3 3 0 3 3 3
0 3 2 2 3 0 3 2 2 3 0 3 2 2 3 0 3 2 2 3 0 3 2 2 3 0 3 2 2
0 3 2 2 3 0 3 2 2 3 0 3 2 2 3 0 3 2 2 3 0 3 2 2 3 0 3 2 2
0 3 3 3 3 0 3 3 3 3 0 3 3 3 3 0 3 3 3 3 0 3 3 3 3 0 3 3 3
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 8 8 0 0 0 0 0 0 0 0 8 8
0 3 3 3 3 0 3 3 3 3 0 3 3 3 3 0 3 3 3 3 0 3 3 3 3 0 3 3 3
0 3 2 2 3 0 3 4 4 3 4 3 2 2 3 4 3 2 2 3 4 3 4 4 3 0 3 2 2
0 3 2 2 3 0 3 4 4 3 4 3 2 2 3 4 3 2 2 3 4 3 4 4 3 0 3 2 2
0 3 3 3 3 0 3 3 3 3 0 3 3 3 3 0 3 3 3 3 0 3 3 3 3 0 3 3 3
0 0 0 0 0 0 0 4 4 0 0 0 0 0 0 0 0 8 8 0 0 0 4 4 0 0 0 8 8
0 3 3 3 3 0 3 3 3 3 0 3 3 3 3 0 3 3 3 3 0 3 3 3 3 0 3 3 3
0 3 2 2 3 0 3 2 2 3 0 3 2 2 3 0 3 8 8 3 8 3 2 2 3 8 3 8 8
0 3 2 2 3 0 3 2 2 3 0 3 2 2 3 0 3 8 8 3 8 3 2 2 3 8 3 8 8
0 3 3 3 3 0 3 3 3 3 0 3 3 3 3 0 3 3 3 3 0 3 3 3 3 0 3 3 3
0 0 0 0 0 0 0 4 4 0 0 0 0 0 0 0 0 0 0 0 0 0 4 4 0 0 0 0 0
0 3 3 3 3 0 3 3 3 3 0 3 3 3 3 0 3 3 3 3 0 3 3 3 3 0 3 3 3
0 3 2 2 3 0 3 4 4 3 4 3 2 2 3 4 3 2 2 3 4 3 4 4 3 0 3 2 2
0 3 2 2 3 0 3 4 4 3 4 3 2 2 3 4 3 2 2 3 4 3 4 4 3 0 3 2 2
```
Transformed Output:
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 3 3 3 3 0 3 3 3 3 0 3 3 3 3 0 3 3 3 3 0 3 3 3 3 0 3 3 3
0 3 2 2 3 0 3 2 2 3 0 3 2 2 3 0 3 8 8 3 0 3 2 2 3 0 3 8 8
0 3 2 2 3 0 3 2 2 3 0 3 2 2 3 0 3 8 8 3 0 3 2 2 3 0 3 8 8
0 3 3 3 3 0 3 3 3 3 0 3 3 3 3 0 3 3 3 3 0 3 3 3 3 0 3 3 3
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 3 3 3 3 0 3 3 3 3 0 3 3 3 3 0 3 3 3 3 0 3 3 3 3 0 3 3 3
0 3 2 2 3 0 3 2 2 3 0 3 2 2 3 0 3 2 2 3 0 3 2 2 3 0 3 2 2
0 3 2 2 3 0 3 2 2 3 0 3 2 2 3 0 3 2 2 3 0 3 2 2 3 0 3 2 2
0 3 3 3 3 0 3 3 3 3 0 3 3 3 3 0 3 3 3 3 0 3 3 3 3 0 3 3 3
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 3 3 3 3 0 3 3 3 3 0 3 3 3 3 0 3 3 3 3 0 3 3 3 3 0 3 3 3
0 3 2 2 3 0 3 4 4 3 0 3 2 2 3 0 3 2 2 3 0 3 4 4 3 0 3 2 2
0 3 2 2 3 0 3 4 4 3 0 3 2 2 3 0 3 2 2 3 0 3 4 4 3 0 3 2 2
0 3 3 3 3 0 3 3 3 3 0 3 3 3 3 0 3 3 3 3 0 3 3 3 3 0 3 3 3
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 3 3 3 3 0 3 3 3 3 0 3 3 3 3 0 3 3 3 3 0 3 3 3 3 0 3 3 3
0 3 2 2 3 0 3 2 2 3 0 3 2 2 3 0 3 8 8 3 0 3 2 2 3 0 3 8 8
0 3 2 2 3 0 3 2 2 3 0 3 2 2 3 0 3 8 8 3 0 3 2 2 3 0 3 8 8
0 3 3 3 3 0 3 3 3 3 0 3 3 3 3 0 3 3 3 3 0 3 3 3 3 0 3 3 3
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 3 3 3 3 0 3 3 3 3 0 3 3 3 3 0 3 3 3 3 0 3 3 3 3 0 3 3 3
0 3 2 2 3 0 3 4 4 3 0 3 2 2 3 0 3 2 2 3 0 3 4 4 3 0 3 2 2
0 3 2 2 3 0 3 4 4 3 0 3 2 2 3 0 3 2 2 3 0 3 4 4 3 0 3 2 2
```
Match: False
Pixels Off: 40
Size Correct: True
Color Palette Correct: True
Color Count Correct: False
Score: 11.494252873563227

## Example 2:
Input:
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 2 2 2 0 0 2 2 2 0 0 2 2 2 0 0 2 2 2 0 0 2 2 2 0 0 2 2
0 2 4 2 0 0 2 4 2 0 0 2 3 2 0 0 2 3 2 0 0 2 4 2 0 0 2 4
0 2 2 2 0 0 2 2 2 0 0 2 2 2 0 0 2 2 2 0 0 2 2 2 0 0 2 2
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 2 2 2 0 0 2 2 2 0 0 2 2 2 0 0 2 2 2 0 0 2 2 2 0 0 2 2
0 2 4 2 0 0 2 1 2 0 0 2 4 2 0 0 2 4 2 0 0 2 1 2 0 0 2 4
0 2 2 2 0 0 2 2 2 0 0 2 2 2 0 0 2 2 2 0 0 2 2 2 0 0 2 2
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 2 2 2 0 0 2 2 2 0 0 2 2 2 0 0 2 2 2 0 0 2 2 2 0 0 2 2
0 2 4 2 0 0 2 4 2 0 0 2 3 2 0 0 2 3 2 0 0 2 4 2 0 0 2 4
0 2 2 2 0 0 2 2 2 0 0 2 2 2 0 0 2 2 2 0 0 2 2 2 0 0 2 2
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 2 2 2 0 0 2 2 2 0 0 2 2 2 0 0 2 2 2 0 0 2 2 2 0 0 2 2
0 2 4 2 0 0 2 1 2 0 0 2 4 2 0 0 2 4 2 0 0 2 1 2 0 0 2 4
0 2 2 2 0 0 2 2 2 0 0 2 2 2 0 0 2 2 2 0 0 2 2 2 0 0 2 2
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 2 2 2 0 0 2 2 2 0 0 2 2 2 0 0 2 2 2 0 0 2 2 2 0 0 2 2
0 2 4 2 0 0 2 4 2 0 0 2 4 2 0 0 2 4 2 0 0 2 4 2 0 0 2 4
```
Expected Output:
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 2 2 2 0 0 2 2 2 0 0 2 2 2 0 0 2 2 2 0 0 2 2 2 0 0 2 2
0 2 4 2 0 0 2 4 2 0 0 2 3 2 3 3 2 3 2 0 0 2 4 2 0 0 2 4
0 2 2 2 0 0 2 2 2 0 0 2 2 2 0 0 2 2 2 0 0 2 2 2 0 0 2 2
0 0 0 0 0 0 0 0 0 0 0 0 3 0 0 0 0 3 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 3 0 0 0 0 3 0 0 0 0 0 0 0 0 0 0
0 2 2 2 0 0 2 2 2 0 0 2 2 2 0 0 2 2 2 0 0 2 2 2 0 0 2 2
0 2 4 2 0 0 2 1 2 1 1 2 4 2 1 1 2 4 2 1 1 2 1 2 0 0 2 4
0 2 2 2 0 0 2 2 2 0 0 2 2 2 0 0 2 2 2 0 0 2 2 2 0 0 2 2
0 0 0 0 0 0 0 1 0 0 0 0 3 0 0 0 0 3 0 0 0 0 1 0 0 0 0 0
0 0 0 0 0 0 0 1 0 0 0 0 3 0 0 0 0 3 0 0 0 0 1 0 0 0 0 0
0 2 2 2 0 0 2 2 2 0 0 2 2 2 0 0 2 2 2 0 0 2 2 2 0 0 2 2
0 2 4 2 0 0 2 4 2 0 0 2 3 2 3 3 2 3 2 0 0 2 4 2 0 0 2 4
0 2 2 2 0 0 2 2 2 0 0 2 2 2 0 0 2 2 2 0 0 2 2 2 0 0 2 2
0 0 0 0 0 0 0 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0 0 0
0 0 0 0 0 0 0 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0 0 0
0 2 2 2 0 0 2 2 2 0 0 2 2 2 0 0 2 2 2 0 0 2 2 2 0 0 2 2
0 2 4 2 0 0 2 1 2 1 1 2 4 2 1 1 2 4 2 1 1 2 1 2 0 0 2 4
0 2 2 2 0 0 2 2 2 0 0 2 2 2 0 0 2 2 2 0 0 2 2 2 0 0 2 2
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 2 2 2 0 0 2 2 2 0 0 2 2 2 0 0 2 2 2 0 0 2 2 2 0 0 2 2
0 2 4 2 0 0 2 4 2 0 0 2 4 2 0 0 2 4 2 0 0 2 4 2 0 0 2 4
```
Transformed Output:
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 2 2 2 0 0 2 2 2 0 0 2 2 2 0 0 2 2 2 0 0 2 2 2 0 0 2 2
0 2 4 2 0 0 2 4 2 0 0 2 3 2 3 3 2 3 2 3 3 2 4 2 0 0 2 4
0 2 2 2 0 0 2 2 2 0 0 2 2 2 0 0 2 2 2 0 0 2 2 2 0 0 2 2
0 0 0 0 0 0 0 0 0 0 0 0 3 0 0 0 0 3 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 3 0 0 0 0 3 0 0 0 0 0 0 0 0 0 0
0 2 2 2 0 0 2 2 2 0 0 2 2 2 0 0 2 2 2 0 0 2 2 2 0 0 2 2
0 2 4 2 0 0 2 1 2 1 1 2 4 2 0 0 2 4 2 0 0 2 1 2 1 1 2 4
0 2 2 2 0 0 2 2 2 0 0 2 2 2 0 0 2 2 2 0 0 2 2 2 0 0 2 2
0 0 0 0 0 0 0 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0 0 0
0 0 0 0 0 0 0 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0 0 0
0 2 2 2 0 0 2 2 2 0 0 2 2 2 0 0 2 2 2 0 0 2 2 2 0 0 2 2
0 2 4 2 0 0 2 4 2 0 0 2 3 2 3 3 2 3 2 3 3 2 4 2 0 0 2 4
0 2 2 2 0 0 2 2 2 0 0 2 2 2 0 0 2 2 2 0 0 2 2 2 0 0 2 2
0 0 0 0 0 0 0 0 0 0 0 0 3 0 0 0 0 3 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 3 0 0 0 0 3 0 0 0 0 0 0 0 0 0 0
0 2 2 2 0 0 2 2 2 0 0 2 2 2 0 0 2 2 2 0 0 2 2 2 0 0 2 2
0 2 4 2 0 0 2 1 2 1 1 2 4 2 0 0 2 4 2 0 0 2 1 2 1 1 2 4
0 2 2 2 0 0 2 2 2 0 0 2 2 2 0 0 2 2 2 0 0 2 2 2 0 0 2 2
0 0 0 0 0 0 0 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0 0 0
0 0 0 0 0 0 0 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0 0 0
0 2 2 2 0 0 2 2 2 0 0 2 2 2 0 0 2 2 2 0 0 2 2 2 0 0 2 2
0 2 4 2 0 0 2 4 2 0 0 2 4 2 0 0 2 4 2 0 0 2 4 2 0 0 2 4
```
Match: False
Pixels Off: 32
Size Correct: True
Color Palette Correct: True
Color Count Correct: False
Score: 9.937888198757747

## Example 3:
Input:
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 1 1 1 0 0 0 1 1 1 0 0 0 1 1 1 0 0 0 1 1 1 0 0 0 1 1 1 0
0 1 2 1 0 0 0 1 2 1 0 0 0 1 2 1 0 0 0 1 2 1 0 0 0 1 2 1 0
0 1 1 1 0 0 0 1 1 1 0 0 0 1 1 1 0 0 0 1 1 1 0 0 0 1 1 1 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 1 1 1 0 0 0 1 1 1 0 0 0 1 1 1 0 0 0 1 1 1 0 0 0 1 1 1 0
0 1 3 1 0 0 0 1 2 1 0 0 0 1 2 1 0 0 0 1 3 1 0 0 0 1 2 1 0
0 1 1 1 0 0 0 1 1 1 0 0 0 1 1 1 0 0 0 1 1 1 0 0 0 1 1 1 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 1 1 1 0 0 0 1 1 1 0 0 0 1 1 1 0 0 0 1 1 1 0 0 0 1 1 1 0
0 1 2 1 0 0 0 1 2 1 0 0 0 1 2 1 0 0 0 1 2 1 0 0 0 1 2 1 0
0 1 1 1 0 0 0 1 1 1 0 0 0 1 1 1 0 0 0 1 1 1 0 0 0 1 1 1 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 1 1 1 0 0 0 1 1 1 0 0 0 1 1 1 0 0 0 1 1 1 0 0 0 1 1 1 0
0 1 3 1 0 0 0 1 2 1 0 0 0 1 2 1 0 0 0 1 3 1 0 0 0 1 2 1 0
0 1 1 1 0 0 0 1 1 1 0 0 0 1 1 1 0 0 0 1 1 1 0 0 0 1 1 1 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 1 1 1 0 0 0 1 1 1 0 0 0 1 1 1 0 0 0 1 1 1 0 0 0 1 1 1 0
```
Expected Output:
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 1 1 1 0 0 0 1 1 1 0 0 0 1 1 1 0 0 0 1 1 1 0 0 0 1 1 1 0
0 1 2 1 0 0 0 1 2 1 0 0 0 1 2 1 0 0 0 1 2 1 0 0 0 1 2 1 0
0 1 1 1 0 0 0 1 1 1 0 0 0 1 1 1 0 0 0 1 1 1 0 0 0 1 1 1 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 1 1 1 0 0 0 1 1 1 0 0 0 1 1 1 0 0 0 1 1 1 0 0 0 1 1 1 0
0 1 3 1 3 3 3 1 2 1 3 3 3 1 2 1 3 3 3 1 3 1 0 0 0 1 2 1 0
0 1 1 1 0 0 0 1 1 1 0 0 0 1 1 1 0 0 0 1 1 1 0 0 0 1 1 1 0
0 0 3 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 3 0 0 0 0 0 0 0 0
0 0 3 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 3 0 0 0 0 0 0 0 0
0 0 3 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 3 0 0 0 0 0 0 0 0
0 1 1 1 0 0 0 1 1 1 0 0 0 1 1 1 0 0 0 1 1 1 0 0 0 1 1 1 0
0 1 2 1 0 0 0 1 2 1 0 0 0 1 2 1 0 0 0 1 2 1 0 0 0 1 2 1 0
0 1 1 1 0 0 0 1 1 1 0 0 0 1 1 1 0 0 0 1 1 1 0 0 0 1 1 1 0
0 0 3 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 3 0 0 0 0 0 0 0 0
0 0 3 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 3 0 0 0 0 0 0 0 0
0 0 3 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 3 0 0 0 0 0 0 0 0
0 1 1 1 0 0 0 1 1 1 0 0 0 1 1 1 0 0 0 1 1 1 0 0 0 1 1 1 0
0 1 3 1 3 3 3 1 2 1 3 3 3 1 2 1 3 3 3 1 3 1 0 0 0 1 2 1 0
0 1 1 1 0 0 0 1 1 1 0 0 0 1 1 1 0 0 0 1 1 1 0 0 0 1 1 1 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 1 1 1 0 0 0 1 1 1 0 0 0 1 1 1 0 0 0 1 1 1 0 0 0 1 1 1 0
```
Transformed Output:
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 1 1 1 0 0 0 1 1 1 0 0 0 1 1 1 0 0 0 1 1 1 0 0 0 1 1 1 0
0 1 2 1 0 0 0 1 2 1 0 0 0 1 2 1 0 0 0 1 2 1 0 0 0 1 2 1 0
0 1 1 1 0 0 0 1 1 1 0 0 0 1 1 1 0 0 0 1 1 1 0 0 0 1 1 1 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 1 1 1 0 0 0 1 1 1 0 0 0 1 1 1 0 0 0 1 1 1 0 0 0 1 1 1 0
0 1 3 1 3 3 3 1 2 1 0 0 0 1 2 1 0 0 0 1 3 1 3 3 3 1 2 1 0
0 1 1 1 0 0 0 1 1 1 0 0 0 1 1 1 0 0 0 1 1 1 0 0 0 1 1 1 0
0 0 3 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 3 0 0 0 0 0 0 0 0
0 0 3 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 3 0 0 0 0 0 0 0 0
0 0 3 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 3 0 0 0 0 0 0 0 0
0 1 1 1 0 0 0 1 1 1 0 0 0 1 1 1 0 0 0 1 1 1 0 0 0 1 1 1 0
0 1 2 1 0 0 0 1 2 1 0 0 0 1 2 1 0 0 0 1 2 1 0 0 0 1 2 1 0
0 1 1 1 0 0 0 1 1 1 0 0 0 1 1 1 0 0 0 1 1 1 0 0 0 1 1 1 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 1 1 1 0 0 0 1 1 1 0 0 0 1 1 1 0 0 0 1 1 1 0 0 0 1 1 1 0
0 1 3 1 3 3 3 1 2 1 0 0 0 1 2 1 0 0 0 1 3 1 3 3 3 1 2 1 0
0 1 1 1 0 0 0 1 1 1 0 0 0 1 1 1 0 0 0 1 1 1 0 0 0 1 1 1 0
0 0 3 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 3 0 0 0 0 0 0 0 0
0 0 3 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 3 0 0 0 0 0 0 0 0
0 0 3 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 3 0 0 0 0 0 0 0 0
0 1 1 1 0 0 0 1 1 1 0 0 0 1 1 1 0 0 0 1 1 1 0 0 0 1 1 1 0
```
Match: False
Pixels Off: 30
Size Correct: True
Color Palette Correct: True
Color Count Correct: False
Score: 7.9575596816976315
