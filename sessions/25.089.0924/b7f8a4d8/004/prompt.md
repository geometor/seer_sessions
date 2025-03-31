
Previous Code:
```python
import numpy as np

"""
The transformation identifies specific framed objects within the input grid based on their border color and size. 
There are three distinct patterns recognized:

1. A 5x5 Green (3) border surrounding a 2x2 inner block.
2. A 3x3 Red (2) border surrounding a 1x1 center pixel.
3. A 3x3 Blue (1) border surrounding a 1x1 center pixel.

For each identified object, the color of its inner content is examined. If this inner color matches a specific 'trigger' color associated with that pattern, new shapes are drawn onto the output grid in the adjacent white (0) space. The original objects are preserved.

- Pattern 1 Trigger/Action:
  - If the inner 2x2 block is Azure (8) or Yellow (4):
    - Draw a 2x2 block of the trigger color immediately to the right of the 5x5 frame (starting at column c+5), vertically aligned with the inner 2x2 block (starting at row r+1).

- Pattern 2 Trigger/Action:
  - If the inner center pixel is Green (3) or Blue (1):
    - Draw two separate 1x2 vertical lines of the trigger color.
    - Line 1: Located 2 columns to the right of the center pixel (at column c+3), starting at the center pixel's row (row r+1).
    - Line 2: Located 4 columns to the right of the center pixel (at column c+5), starting at the center pixel's row (row r+1).

- Pattern 3 Trigger/Action:
  - If the inner center pixel is Green (3):
    - Draw a 3x3 block of Green (3) immediately to the right of the 3x3 frame (starting at column c+3), vertically aligned with the frame (starting at row r).
    - Draw a 1x3 vertical line (3 pixels high) of Green (3) immediately below the 3x3 frame (starting at row r+3), horizontally aligned with the frame's center column (column c+1).

The output grid is initialized as a copy of the input, and modifications (drawing new shapes) are applied directly to this copy. Drawing only occurs on cells that were originally white (0).
"""

def is_valid(r, c, height, width):
    """Check if coordinates (r, c) are within the grid bounds (height, width)."""
    return 0 <= r < height and 0 <= c < width

def check_pattern_1(grid, r, c, height, width):
    """
    Checks for the 5x5 Green frame pattern at (r, c).
    Returns (True, inner_color) if pattern matches, else (False, -1).
    Inner color is taken from the top-left of the 2x2 center block.
    """
    if r + 4 >= height or c + 4 >= width:
        return False, -1 # Not enough space for a 5x5 block

    # Check border color (Green = 3)
    for i in range(5):
        # Top and Bottom rows
        if not is_valid(r, c+i, height, width) or grid[r, c+i] != 3: return False, -1
        if not is_valid(r+4, c+i, height, width) or grid[r+4, c+i] != 3: return False, -1
        # Left and Right columns (excluding corners checked above)
        if i > 0 and i < 4:
            if not is_valid(r+i, c, height, width) or grid[r+i, c] != 3: return False, -1
            if not is_valid(r+i, c+4, height, width) or grid[r+i, c+4] != 3: return False, -1

    # Check if inner area is accessible (basic check)
    if not is_valid(r+1, c+1, height, width):
         return False, -1 # Should not happen if border check passed, but safe check

    # Get inner content color from top-left of the 2x2 center
    inner_color = grid[r+1, c+1]
    
    # Optional: Verify the entire 2x2 inner block is the same color (as seen in example)
    # This wasn't strictly necessary based on the description but matches example 1
    # if not is_valid(r+1, c+2, height, width) or grid[r+1, c+2] != inner_color: return False, -1
    # if not is_valid(r+2, c+1, height, width) or grid[r+2, c+1] != inner_color: return False, -1
    # if not is_valid(r+2, c+2, height, width) or grid[r+2, c+2] != inner_color: return False, -1
    
    return True, inner_color

def check_pattern_2_3(grid, r, c, height, width, border_color):
    """
    Checks for the 3x3 frame patterns (Red=2 or Blue=1 border) at (r, c).
    Returns (True, inner_color) if pattern matches, else (False, -1).
    Inner color is the center pixel.
    """
    if r + 2 >= height or c + 2 >= width:
        return False, -1 # Not enough space for a 3x3 block

    # Check border color
    for i in range(3):
        # Top and Bottom rows
        if not is_valid(r, c+i, height, width) or grid[r, c+i] != border_color: return False, -1
        if not is_valid(r+2, c+i, height, width) or grid[r+2, c+i] != border_color: return False, -1
        # Left and Right columns (excluding corners)
        if i == 1:
            if not is_valid(r+i, c, height, width) or grid[r+i, c] != border_color: return False, -1
            if not is_valid(r+i, c+2, height, width) or grid[r+i, c+2] != border_color: return False, -1

    # Check center pixel is accessible and get inner color
    if not is_valid(r+1, c+1, height, width):
        return False, -1 # Should be valid if border check passed
    inner_color = grid[r+1, c+1]
    
    return True, inner_color

def draw_block(output_grid, r, c, h, w, color, height, width):
    """Draws a solid block of color onto output_grid, checking bounds and background."""
    for i in range(h):
        for j in range(w):
            nr, nc = r + i, c + j
            # Draw only if within bounds AND on a white (0) background pixel
            if is_valid(nr, nc, height, width) and output_grid[nr, nc] == 0:
                output_grid[nr, nc] = color

def draw_vline(output_grid, r, c, h, color, height, width):
    """Draws a vertical line (width 1) using draw_block."""
    draw_block(output_grid, r, c, h, 1, color, height, width)

# --- Specific Drawing Functions for Each Pattern's Output ---

def draw_pattern_1_output(output_grid, r, c, color, height, width):
    """Draws the 2x2 block for pattern 1."""
    # Draw position: starts row r+1, col c+5
    draw_r, draw_c = r + 1, c + 5
    draw_block(output_grid, draw_r, draw_c, 2, 2, color, height, width)

def draw_pattern_2_output(output_grid, r, c, color, height, width):
    """Draws the two 1x2 vertical lines for pattern 2."""
    # Line 1: starts row r+1, col c+3, height 2
    draw_vline(output_grid, r + 1, c + 3, 2, color, height, width)
    # Line 2: starts row r+1, col c+5, height 2
    draw_vline(output_grid, r + 1, c + 5, 2, color, height, width)

def draw_pattern_3_output(output_grid, r, c, color, height, width):
    """Draws the 3x3 block and 1x3 vertical line for pattern 3."""
    # Action 1: Draw 3x3 block to the right (starts r, c+3)
    draw_block(output_grid, r, c + 3, 3, 3, color, height, width)
    # Action 2: Draw 1x3 vertical line below center (starts r+3, c+1)
    draw_vline(output_grid, r + 3, c + 1, 3, color, height, width)

# --- Main Transformation Function ---

def transform(input_grid):
    """
    Applies the transformation rules by finding patterns and drawing corresponding outputs.
    """
    # Convert input to numpy array for easier manipulation
    input_grid_np = np.array(input_grid, dtype=int)
    # Initialize output grid as a copy of the input
    output_grid_np = np.copy(input_grid_np)
    height, width = input_grid_np.shape

    # Keep track of processed areas to avoid redundant checks/drawing within found objects
    # This helps if objects could potentially overlap in checks, though not seen in examples.
    processed = np.zeros((height, width), dtype=bool)

    # Iterate through each cell as a potential top-left corner
    for r in range(height):
        for c in range(width):
            # Skip if this cell was part of an already processed object
            if processed[r, c]:
                continue

            # Check for Pattern 1 (5x5 Green frame) - Highest priority check
            is_p1, inner_color_p1 = check_pattern_1(input_grid_np, r, c, height, width)
            if is_p1:
                # Mark the area of this 5x5 object as processed
                processed[r:r+5, c:c+5] = True 
                # Check triggers for Pattern 1
                if inner_color_p1 == 8 or inner_color_p1 == 4: # Azure or Yellow
                    draw_pattern_1_output(output_grid_np, r, c, inner_color_p1, height, width)
                continue # Move to the next potential top-left corner outside this object

            # Check for Pattern 2 (3x3 Red frame)
            is_p2, inner_color_p2 = check_pattern_2_3(input_grid_np, r, c, height, width, border_color=2)
            if is_p2:
                # Mark the area of this 3x3 object as processed
                processed[r:r+3, c:c+3] = True
                # Check triggers for Pattern 2
                if inner_color_p2 == 3 or inner_color_p2 == 1: # Green or Blue
                    draw_pattern_2_output(output_grid_np, r, c, inner_color_p2, height, width)
                continue # Move to the next potential top-left corner

            # Check for Pattern 3 (3x3 Blue frame)
            is_p3, inner_color_p3 = check_pattern_2_3(input_grid_np, r, c, height, width, border_color=1)
            if is_p3:
                 # Mark the area of this 3x3 object as processed
                processed[r:r+3, c:c+3] = True
                # Check triggers for Pattern 3
                if inner_color_p3 == 3: # Green
                    draw_pattern_3_output(output_grid_np, r, c, inner_color_p3, height, width)
                # No continue needed as it's the last check in this loop iteration

    # Convert the final numpy array back to a list of lists
    return output_grid_np.tolist()
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
0 2 4 2 0 0 2 4 2 0 0 2 3 2 3 0 2 3 2 3 0 2 4 2 0 0 2 4
0 2 2 2 0 0 2 2 2 0 0 2 2 2 3 0 2 2 2 3 0 2 2 2 0 0 2 2
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 2 2 2 0 0 2 2 2 0 0 2 2 2 0 0 2 2 2 0 0 2 2 2 0 0 2 2
0 2 4 2 0 0 2 1 2 1 0 2 4 2 0 0 2 4 2 0 0 2 1 2 1 0 2 4
0 2 2 2 0 0 2 2 2 1 0 2 2 2 0 0 2 2 2 0 0 2 2 2 1 0 2 2
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 2 2 2 0 0 2 2 2 0 0 2 2 2 0 0 2 2 2 0 0 2 2 2 0 0 2 2
0 2 4 2 0 0 2 4 2 0 0 2 3 2 3 0 2 3 2 3 0 2 4 2 0 0 2 4
0 2 2 2 0 0 2 2 2 0 0 2 2 2 3 0 2 2 2 3 0 2 2 2 0 0 2 2
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 2 2 2 0 0 2 2 2 0 0 2 2 2 0 0 2 2 2 0 0 2 2 2 0 0 2 2
0 2 4 2 0 0 2 1 2 1 0 2 4 2 0 0 2 4 2 0 0 2 1 2 1 0 2 4
0 2 2 2 0 0 2 2 2 1 0 2 2 2 0 0 2 2 2 0 0 2 2 2 1 0 2 2
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 2 2 2 0 0 2 2 2 0 0 2 2 2 0 0 2 2 2 0 0 2 2 2 0 0 2 2
0 2 4 2 0 0 2 4 2 0 0 2 4 2 0 0 2 4 2 0 0 2 4 2 0 0 2 4
```
Match: False
Pixels Off: 40
Size Correct: True
Color Palette Correct: True
Color Count Correct: False
Score: 12.422360248447205

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
0 1 1 1 3 3 3 1 1 1 0 0 0 1 1 1 0 0 0 1 1 1 3 3 3 1 1 1 0
0 1 3 1 3 3 3 1 2 1 0 0 0 1 2 1 0 0 0 1 3 1 3 3 3 1 2 1 0
0 1 1 1 3 3 3 1 1 1 0 0 0 1 1 1 0 0 0 1 1 1 3 3 3 1 1 1 0
0 0 3 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 3 0 0 0 0 0 0 0 0
0 0 3 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 3 0 0 0 0 0 0 0 0
0 0 3 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 3 0 0 0 0 0 0 0 0
0 1 1 1 0 0 0 1 1 1 0 0 0 1 1 1 0 0 0 1 1 1 0 0 0 1 1 1 0
0 1 2 1 0 0 0 1 2 1 0 0 0 1 2 1 0 0 0 1 2 1 0 0 0 1 2 1 0
0 1 1 1 0 0 0 1 1 1 0 0 0 1 1 1 0 0 0 1 1 1 0 0 0 1 1 1 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 1 1 1 3 3 3 1 1 1 0 0 0 1 1 1 0 0 0 1 1 1 3 3 3 1 1 1 0
0 1 3 1 3 3 3 1 2 1 0 0 0 1 2 1 0 0 0 1 3 1 3 3 3 1 2 1 0
0 1 1 1 3 3 3 1 1 1 0 0 0 1 1 1 0 0 0 1 1 1 3 3 3 1 1 1 0
0 0 3 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 3 0 0 0 0 0 0 0 0
0 0 3 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 3 0 0 0 0 0 0 0 0
0 0 3 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 3 0 0 0 0 0 0 0 0
0 1 1 1 0 0 0 1 1 1 0 0 0 1 1 1 0 0 0 1 1 1 0 0 0 1 1 1 0
```
Match: False
Pixels Off: 54
Size Correct: True
Color Palette Correct: True
Color Count Correct: False
Score: 14.323607427055691
