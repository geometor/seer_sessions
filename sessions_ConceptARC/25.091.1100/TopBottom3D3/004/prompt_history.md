
## train_1

**input:**
```
0 0 0 0 0 0 0 0
0 0 2 2 2 0 0 0
0 1 2 2 2 1 1 0
0 1 2 2 2 1 1 0
0 1 2 2 2 1 1 0
0 1 2 2 2 1 1 0
0 1 2 2 2 1 1 0
0 0 2 2 2 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 1 1 1 1 1 1 0
0 1 1 1 1 1 1 0
0 1 1 1 1 1 1 0
0 1 1 1 1 1 1 0
0 1 1 1 1 1 1 0
0 0 0 0 0 0 0 0
```


## train_2

**input:**
```
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 4 4 4 4 0 0
0 3 4 4 4 4 3 0
0 3 4 4 4 4 3 0
0 0 4 4 4 4 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 3 3 3 3 3 3 0
0 3 3 3 3 3 3 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
```


## train_3

**input:**
```
0 0 0 6 0 0 0 0
7 7 7 6 7 0 0 0
7 7 7 6 7 0 0 0
7 7 7 6 7 0 0 0
7 7 7 6 7 0 0 0
0 0 0 6 0 0 0 0
0 0 0 6 0 0 0 0
0 0 0 6 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0
7 7 7 7 7 0 0 0
7 7 7 7 7 0 0 0
7 7 7 7 7 0 0 0
7 7 7 7 7 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
```

*   **Perception of the Elements:**
    *   Each input grid contains a background of white pixels (0).
    *   There are two distinct non-white colored objects in each input grid.
    *   One object appears to be an "inner" shape (cross, rectangle, line).
    *   The second object acts as a "frame" or border around parts of the inner shape. The frame color is different from the inner shape color.
    *   In the output grid, the inner shape's pixels are replaced by the color of the frame object.
    *   The frame object itself remains unchanged in the output.
    *   The background pixels remain unchanged.

*   **YAML Facts:**
    
```yaml
    task_description: Identify two distinct non-background colored objects. One object (frame) partially encloses the other (inner). Replace the pixels of the inner object with the color of the frame object.
    
    elements:
      - object: background
        color_property: white (0)
        role: static background
      - object: inner_shape
        color_property: varies (red, yellow, magenta in examples)
        topology: contiguous block of a single color, does not touch the grid edge directly in examples, enclosed by frame_shape and background.
        role: target for color replacement
      - object: frame_shape
        color_property: varies (blue, green, orange in examples), distinct from inner_shape color.
        topology: contiguous block of a single color, partially surrounds inner_shape, touches background (0).
        role: source color for replacement, remains unchanged in output.
    
    relationships:
      - type: spatial
        description: frame_shape partially encloses or borders inner_shape.
      - type: spatial
        description: frame_shape touches the background (0).
      - type: spatial
        description: inner_shape is surrounded by frame_shape and/or background (0), does not directly touch the grid boundary in examples (or touches less than frame_shape).
    
    actions:
      - action: identify_colors
        inputs: input_grid
        outputs: background_color (0), color1, color2
      - action: identify_frame_color
        inputs: input_grid, color1, color2
        outputs: frame_color
        logic: The color that has pixels adjacent to the background color (0) is the frame_color. (Alternative logic: Find bounding box of non-background colors; the color present at the edge of the bounding box is the frame_color).
      - action: identify_inner_color
        inputs: color1, color2, frame_color
        outputs: inner_color
        logic: The non-background color that is not the frame_color.
      - action: replace_color
        inputs: input_grid, inner_color, frame_color
        outputs: output_grid
        logic: Create a new grid where pixels matching inner_color in the input are changed to frame_color. All other pixels retain their original color.
    
    derived_properties:
      bounding_box: The minimum rectangle enclosing all non-background pixels. The frame_color pixels typically lie on the boundary of this box, while inner_color pixels are inside.
    ```


*   **Natural Language Program:**
    1.  Identify all distinct colors present in the input grid besides the background color (white, 0). There will be exactly two such colors: `color_A` and `color_B`.
    2.  Determine which of these two colors, `color_A` or `color_B`, forms the "frame". The frame color is the one whose pixels are adjacent (horizontally or vertically) to background (white, 0) pixels. Assign this color to `frame_color`.
    3.  The other non-background color is the "inner" color. Assign this color to `inner_color`.
    4.  Create the output grid based on the input grid:
        *   For each pixel in the input grid:
            *   If the pixel's color is `inner_color`, set the corresponding output pixel's color to `frame_color`.
            *   Otherwise, keep the pixel's original color in the output grid.
```python
import numpy as np

def get_neighbors(grid, r, c):
    """Gets the adjacent neighbors (up, down, left, right) of a cell."""
    neighbors = []
    rows, cols = grid.shape
    if r > 0:
        neighbors.append(grid[r-1, c])
    if r < rows - 1:
        neighbors.append(grid[r+1, c])
    if c > 0:
        neighbors.append(grid[r, c-1])
    if c < cols - 1:
        neighbors.append(grid[r, c+1])
    return neighbors

def transform(input_grid):
    """
    Identifies two distinct non-background colored objects (frame and inner).
    The frame object has pixels adjacent to the background (0).
    Replaces the pixels of the inner object with the color of the frame object.
    """
    
    # Convert input list of lists to numpy array for easier manipulation
    grid = np.array(input_grid)
    rows, cols = grid.shape
    
    # Initialize output_grid as a copy of the input_grid
    output_grid = np.copy(grid)

    # Find unique non-background colors
    unique_colors = np.unique(grid)
    non_background_colors = [color for color in unique_colors if color != 0]

    # Check if there are exactly two non-background colors as expected
    if len(non_background_colors) != 2:
        # Handle unexpected cases, perhaps return input or raise error
        # For this specific problem structure, we assume 2 colors.
        # If not, the logic might fail or produce incorrect results.
        # Let's proceed assuming the structure holds for valid inputs.
        # In a more robust solution, we'd add error handling here.
        # If only one color, what should happen? If more than two?
        # Based on examples, we only expect two.
        if len(non_background_colors) == 1: # Edge case: Only one non-bg color - treat it as both frame and inner? Assume no change.
             return output_grid
        elif len(non_background_colors) == 0: # Edge case: Only background
             return output_grid
        else: # More than 2 non-bg colors - problem definition unclear
             # Let's just pick the first two found based on iteration? This is risky.
             # The core logic below relies on exactly two colors.
             # We'll stick to the assumption based on examples. A more general solution would need clarification.
             pass # Proceed, might fail later if colors aren't found as expected

    color_A = non_background_colors[0]
    color_B = non_background_colors[1]
    
    frame_color = -1 # Initialize with invalid value
    inner_color = -1 # Initialize with invalid value

    # Iterate through the grid to find the frame color
    # The frame color is the non-background color adjacent to the background (0)
    found_frame = False
    for r in range(rows):
        for c in range(cols):
            pixel_color = grid[r, c]
            if pixel_color in non_background_colors:
                neighbors = get_neighbors(grid, r, c)
                if 0 in neighbors: # Check if adjacent to background
                    frame_color = pixel_color
                    found_frame = True
                    break # Found the frame color
        if found_frame:
            break
            
    # Determine the inner color
    if frame_color == color_A:
        inner_color = color_B
    elif frame_color == color_B:
        inner_color = color_A
    else:
        # This shouldn't happen if the input structure is as expected (two non-bg colors, one adjacent to bg)
        # If it does, return the original grid or handle error
        return output_grid 

    # Create the output grid by replacing the inner color with the frame color
    for r in range(rows):
        for c in range(cols):
            if grid[r, c] == inner_color:
                output_grid[r, c] = frame_color
                
    # Convert back to list of lists if required by the testing framework
    return output_grid.tolist()
```
```python
import numpy as np

"""
The transformation identifies two distinct non-background colors in the input grid.
One color acts as a 'frame' and the other as an 'inner' color.
The 'inner' color is defined as the non-background color where NONE of its pixels are adjacent (N, S, E, W) to the background color (0).
The 'frame' color is the other non-background color (which will have at least one pixel adjacent to the background).
The transformation replaces all pixels of the 'inner' color with the 'frame' color.
Pixels of the 'frame' color and background pixels remain unchanged.
"""

def get_neighbors(grid, r, c):
    """Gets the adjacent neighbors (up, down, left, right) values of a cell."""
    neighbors = []
    rows, cols = grid.shape
    # Check Up
    if r > 0:
        neighbors.append(grid[r-1, c])
    # Check Down
    if r < rows - 1:
        neighbors.append(grid[r+1, c])
    # Check Left
    if c > 0:
        neighbors.append(grid[r, c-1])
    # Check Right
    if c < cols - 1:
        neighbors.append(grid[r, c+1])
    return neighbors

def transform(input_grid):
    """
    Transforms the input grid by identifying frame and inner colors and replacing
    the inner color with the frame color.
    """
    # Convert input list of lists to numpy array for easier manipulation
    grid = np.array(input_grid, dtype=np.int8)
    rows, cols = grid.shape

    # Find unique non-background colors
    unique_colors = np.unique(grid)
    non_background_colors = [color for color in unique_colors if color != 0]

    # Expect exactly two non-background colors based on examples
    if len(non_background_colors) != 2:
        # If not two colors, return the original grid as transformation is undefined
        return input_grid

    color_A = non_background_colors[0]
    color_B = non_background_colors[1]

    # Determine which color is the 'inner' color (does not touch background 0)
    A_touches_background = False
    for r in range(rows):
        for c in range(cols):
            if grid[r, c] == color_A:
                neighbors = get_neighbors(grid, r, c)
                if 0 in neighbors:
                    A_touches_background = True
                    break # Found a touch, no need to check further for color A
        if A_touches_background:
            break

    B_touches_background = False
    # Only need to check B if A didn't touch background
    if A_touches_background: # Optimization: if A touches, B must be inner (or structure is unexpected)
         for r in range(rows):
            for c in range(cols):
                if grid[r, c] == color_B:
                    neighbors = get_neighbors(grid, r, c)
                    if 0 in neighbors:
                        B_touches_background = True
                        break
            if B_touches_background:
                 break
    else: # If A didn't touch background, B must be the one touching (frame)
        B_touches_background = True # Assume B must touch if A does not

    inner_color = -1
    frame_color = -1

    # Assign roles based on background adjacency
    if not A_touches_background and B_touches_background:
        inner_color = color_A
        frame_color = color_B
    elif A_touches_background and not B_touches_background:
        inner_color = color_B
        frame_color = color_A
    else:
        # This case (both touch or neither touch) indicates the hypothesis might be wrong
        # or the input doesn't fit the pattern. Return original grid.
        # Based on re-analysis, this case *should* cover the examples correctly.
        # The previous analysis showing both touch was flawed because it didn't check *all* pixels.
        # If the logic holds, one color will have *no* pixels touching background.
        # If both touch (e.g. two separate shapes touching background), return original.
        return input_grid

    # Create the output grid by replacing the inner color with the frame color
    output_grid = np.copy(grid)
    for r in range(rows):
        for c in range(cols):
            if grid[r, c] == inner_color:
                output_grid[r, c] = frame_color

    # Convert back to list of lists
    return output_grid.tolist()
```
