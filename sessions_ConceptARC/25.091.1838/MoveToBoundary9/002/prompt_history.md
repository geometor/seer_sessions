
## train_1

**input:**
```
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 2 2 2 0 1 1 1 0 0
0 0 2 2 2 0 1 1 1 0 0
0 0 2 2 2 0 1 1 1 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
2 2 2 0 0 0 0 0 1 1 1
2 2 2 0 0 0 0 0 1 1 1
2 2 2 0 0 0 0 0 1 1 1
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
```


## train_2

**input:**
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 3 0 3 0 3 0 0 0 4 0 4 0 4 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 3 0 0 0 3 0 0 0 4 0 0 0 4 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 3 0 3 0 3 0 0 0 4 0 4 0 4 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
3 0 3 0 3 0 0 0 0 0 0 0 0 0 4 0 4 0 4
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
3 0 0 0 3 0 0 0 0 0 0 0 0 0 4 0 0 0 4
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
3 0 3 0 3 0 0 0 0 0 0 0 0 0 4 0 4 0 4
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

Okay, let's analyze the provided examples (`train_1` and `train_2`).

**Perception of Elements:**

*   **Grids:** Both examples involve rectangular grids of varying sizes containing pixels of different colors. The background is predominantly white (0).
*   **Objects:** In both inputs, there are distinct groups of non-white pixels.
    *   `train_1`: A 3x3 red (2) square and a 3x3 blue (1) square.
    *   `train_2`: Several green (3) pixels forming disconnected shapes and several yellow (4) pixels forming disconnected shapes. These can be conceptually grouped by color.
*   **Transformation:** The core transformation appears to be a horizontal movement of the non-white objects or pixel groups.
    *   In `train_1`, the red square moves to the leftmost edge, and the blue square moves to the rightmost edge.
    *   In `train_2`, all green pixels collectively shift to the leftmost edge, and all yellow pixels collectively shift to the rightmost edge.
*   **Movement Logic:** The direction of movement seems related to the initial horizontal position of the object/group relative to the grid's center. Objects starting on the left side move left, and objects starting on the right side move right. The movement continues until the object hits the respective grid boundary (left or right edge). The objects maintain their original shape and color during the move.

**YAML Fact Documentation:**


```yaml
task_context:
  grid_properties:
    - background_color: white (0)
    - variable_size: true
  objects:
    - type: contiguous_pixels_same_color
    - exclude_color: white (0)
    - properties:
        - color
        - shape
        - position (row, column)
        - bounding_box (min_row, min_col, max_row, max_col)
        - horizontal_center
  actions:
    - action: identify_objects
      description: Find all contiguous blocks of non-white pixels.
    - action: determine_movement_direction
      description: Based on the object's horizontal position relative to the grid's horizontal center.
      details: Objects centered to the left of the grid's midpoint move left; objects centered at or to the right of the midpoint move right.
    - action: calculate_horizontal_shift
      description: Determine the column offset needed to move the object to the corresponding edge.
      details:
        - For leftward movement, shift = 0 - object's leftmost column.
        - For rightward movement, shift = (grid_width - 1) - object's rightmost column.
    - action: apply_shift
      description: Move all pixels of an object by the calculated horizontal shift.
    - action: render_output
      description: Create a new grid of the same size, initially white, and draw the shifted objects onto it.
  relationships:
    - relationship: object_position_vs_grid_center
      description: An object's horizontal center determines its movement direction (left or right).
    - relationship: object_extent_vs_grid_boundary
      description: An object's leftmost or rightmost column determines the magnitude of the shift required to reach the edge.
```


**Natural Language Program:**

1.  Initialize an output grid with the same dimensions as the input grid, filled entirely with the background color (white, 0).
2.  Identify all distinct, contiguous objects composed of non-white pixels in the input grid. Treat each connected component of the same non-white color as a single object.
3.  Calculate the horizontal midpoint column index of the grid: `mid_col = (grid_width - 1) / 2`.
4.  For each identified object:
    a.  Determine its bounding box, specifically its minimum column (`obj_min_col`) and maximum column (`obj_max_col`).
    b.  Calculate the object's horizontal center: `obj_center = (obj_min_col + obj_max_col) / 2`.
    c.  Determine the movement direction and calculate the horizontal shift (`delta_col`):
        i.  If `obj_center < mid_col`, the object moves left. Set `delta_col = 0 - obj_min_col`.
        ii. If `obj_center >= mid_col`, the object moves right. Set `delta_col = (grid_width - 1) - obj_max_col`.
    d.  Iterate through all the pixels `(r, c)` that constitute the current object in the input grid.
    e.  For each pixel `(r, c)` with color `k`, place the same color `k` at the new position `(r, c + delta_col)` in the output grid.
5.  Return the completed output grid.
```python
import numpy as np
from collections import deque

"""
Identify all distinct contiguous objects of non-white pixels in the input grid.
For each object, determine its horizontal center based on its leftmost and rightmost columns.
Compare the object's horizontal center to the grid's horizontal midpoint.
If the object's center is to the left of the grid's midpoint, calculate the horizontal shift needed to move the object's leftmost column to column 0.
If the object's center is at or to the right of the grid's midpoint, calculate the horizontal shift needed to move the object's rightmost column to the last column of the grid.
Create an output grid initialized with the background color (white, 0).
For each object, copy its pixels to the output grid at their original row and shifted column.
"""

def find_objects(grid, background_color=0):
    """
    Finds all contiguous objects of the same non-background color in the grid.

    Args:
        grid (np.array): The input grid.
        background_color (int): The color to ignore (usually 0 for white).

    Returns:
        list: A list of objects. Each object is represented as a tuple:
              (color, list_of_coordinates, min_col, max_col).
    """
    height, width = grid.shape
    visited = np.zeros_like(grid, dtype=bool)
    objects = []

    for r in range(height):
        for c in range(width):
            if grid[r, c] != background_color and not visited[r, c]:
                # Start finding a new object
                color = grid[r, c]
                coords = []
                q = deque([(r, c)])
                visited[r, c] = True
                min_c, max_c = c, c

                while q:
                    curr_r, curr_c = q.popleft()
                    coords.append((curr_r, curr_c))
                    min_c = min(min_c, curr_c)
                    max_c = max(max_c, curr_c)

                    # Check 8 neighbors (including diagonals)
                    for dr in [-1, 0, 1]:
                        for dc in [-1, 0, 1]:
                            if dr == 0 and dc == 0:
                                continue
                            nr, nc = curr_r + dr, curr_c + dc

                            # Check bounds, color match, and visited status
                            if 0 <= nr < height and 0 <= nc < width and \
                               grid[nr, nc] == color and not visited[nr, nc]:
                                visited[nr, nc] = True
                                q.append((nr, nc))
                
                if coords: # Ensure we found at least one pixel
                    objects.append((color, coords, min_c, max_c))
    return objects

def transform(input_grid):
    """
    Moves non-white objects horizontally to the grid edges based on their position relative to the center.

    Args:
        input_grid (list of lists): The input grid represented as a 2D list.

    Returns:
        list of lists: The transformed grid.
    """
    # Convert input to numpy array for easier manipulation
    input_np = np.array(input_grid, dtype=int)
    height, width = input_np.shape
    
    # Initialize output grid with background color (0)
    output_np = np.zeros_like(input_np)
    
    # Define background color
    background_color = 0
    
    # Find all non-background objects
    objects = find_objects(input_np, background_color)
    
    # Calculate grid horizontal midpoint
    # Use floating point for accurate comparison, even for odd widths
    grid_mid_col = (width - 1) / 2.0 
    
    # Process each object
    for color, coords, min_col, max_col in objects:
        # Calculate object's horizontal center
        obj_center_col = (min_col + max_col) / 2.0
        
        # Determine movement direction and calculate horizontal shift (delta_col)
        delta_col = 0
        if obj_center_col < grid_mid_col:
            # Move left
            delta_col = 0 - min_col
        else:
            # Move right (or stay if already at right edge)
            delta_col = (width - 1) - max_col
            
        # Apply the shift to each pixel of the object
        for r, c in coords:
            new_c = c + delta_col
            # Ensure the new column is within bounds (should be by calculation, but safety check)
            if 0 <= new_c < width:
                output_np[r, new_c] = color

    # Convert output numpy array back to list of lists
    output_grid = output_np.tolist()
    
    return output_grid
```
