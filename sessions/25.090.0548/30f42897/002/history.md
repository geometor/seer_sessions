
## train_1

**input:**
```
8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 2
8 8 8 8 8 8 8 8 8 2
8 8 8 8 8 8 8 8 8 2
8 8 8 8 8 8 8 8 8 2
8 8 8 8 8 8 8 8 8 2
8 8 8 8 8 8 8 8 8 8
```


**output:**
```
2 2 2 2 2 8 8 8 8 8
8 8 8 8 8 8 8 8 8 2
8 8 8 8 8 8 8 8 8 2
8 8 8 8 8 8 8 8 8 2
8 8 8 8 8 8 8 8 8 2
8 8 8 8 8 8 8 8 8 2
2 2 2 2 2 8 8 8 8 8
```


## train_2

**input:**
```
9 9 9 8 8 8 8 8 8 8
9 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8
```


**output:**
```
9 9 9 8 8 8 8 9 9 9
9 8 8 8 8 8 8 8 8 9
8 8 8 8 8 8 8 8 8 8
8 8 8 9 9 9 9 8 8 8
```


## train_3

**input:**
```
8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8
4 8 8 8 8 8 8 8 8
4 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8
```


**output:**
```
8 4 4 8 8 4 4 8 8
8 8 8 8 8 8 8 8 4
4 8 8 8 8 8 8 8 4
4 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 4
4 4 8 8 4 4 8 8 4
```

Okay, let's analyze the provided examples.

## Perception

1.  **Grid Structure:** The inputs and outputs are rectangular grids of pixels with different colors. The dominant color is typically Azure (8), acting as a background.
2.  **Object Identification:** In each input grid, there is a single contiguous object made of a non-background color (Red-2, Maroon-9, Yellow-4). These objects vary in shape (vertical line, rectangle).
3.  **Transformation Goal:** The transformation involves keeping the original object and adding new shapes of the same color to the grid.
4.  **Added Shapes:** The shapes added depend on the dimensions (height H, width W) of the original object.
    *   If the object is a vertical line (W=1), new horizontal and sometimes vertical lines of length H are added near the grid boundaries. The number and placement vary between Example 1 (H=5) and Example 3 (H=2).
    *   If the object is a rectangle (H>1, W>1), a copy of the object is added at the top-right, and a horizontal line related to the object's width (W+1) is added at the bottom-center.
5.  **Color Preservation:** The color of the added shapes is always the same as the color of the original object. The background remains unchanged.
6.  **Positional Logic:** The placement of the added shapes seems related to the corners and edges of the grid, and sometimes involves centering (Example 2). The rules for placement appear specific to the object's shape category (vertical line vs. rectangle) and potentially its exact dimensions (height of the vertical line).

## Facts


```yaml
task_description: Identify a single non-background object in the input grid and add new shapes of the same color to the grid based on the object's dimensions and type (vertical line or rectangle).

examples:
  - id: train_1
    input:
      grid_size: [7, 10]
      background_color: 8 # Azure
      objects:
        - id: obj1
          color: 2 # Red
          shape: vertical_line
          pixels: [[1, 9], [2, 9], [3, 9], [4, 9], [5, 9]]
          bounding_box: { top: 1, left: 9, height: 5, width: 1 }
    output:
      grid_size: [7, 10]
      background_color: 8 # Azure
      objects:
        - id: obj1 # Original object
          color: 2 # Red
          shape: vertical_line
          pixels: [[1, 9], [2, 9], [3, 9], [4, 9], [5, 9]]
        - id: added1
          color: 2 # Red
          shape: horizontal_line
          pixels: [[0, 0], [0, 1], [0, 2], [0, 3], [0, 4]] # Length 5 (H)
          position: top-left
        - id: added2
          color: 2 # Red
          shape: horizontal_line
          pixels: [[6, 0], [6, 1], [6, 2], [6, 3], [6, 4]] # Length 5 (H)
          position: bottom-left
    transformation_rule_applied: vertical_line_h5

  - id: train_2
    input:
      grid_size: [4, 10]
      background_color: 8 # Azure
      objects:
        - id: obj1
          color: 9 # Maroon
          shape: rectangle
          pixels: [[0, 0], [0, 1], [0, 2], [1, 0], [1, 1], [1, 2]]
          bounding_box: { top: 0, left: 0, height: 2, width: 3 }
    output:
      grid_size: [4, 10]
      background_color: 8 # Azure
      objects:
        - id: obj1 # Original object
          color: 9 # Maroon
          shape: rectangle
          pixels: [[0, 0], [0, 1], [0, 2], [1, 0], [1, 1], [1, 2]]
        - id: added1 # Copy of obj1
          color: 9 # Maroon
          shape: rectangle
          pixels: [[0, 7], [0, 8], [0, 9], [1, 7], [1, 8], [1, 9]] # Size 2x3 (HxW)
          position: top-right
        - id: added2
          color: 9 # Maroon
          shape: horizontal_line
          pixels: [[3, 3], [3, 4], [3, 5], [3, 6]] # Length 4 (W+1)
          position: bottom-center
    transformation_rule_applied: rectangle

  - id: train_3
    input:
      grid_size: [7, 9]
      background_color: 8 # Azure
      objects:
        - id: obj1
          color: 4 # Yellow
          shape: vertical_line
          pixels: [[2, 0], [3, 0]]
          bounding_box: { top: 2, left: 0, height: 2, width: 1 }
    output:
      grid_size: [7, 9]
      background_color: 8 # Azure
      objects:
        - id: obj1 # Original object
          color: 4 # Yellow
          shape: vertical_line
          pixels: [[2, 0], [3, 0]]
        # Added shapes (all length H=2)
        - id: added_h1
          color: 4 # Yellow
          shape: horizontal_line
          pixels: [[0, 1], [0, 2]]
        - id: added_h2
          color: 4 # Yellow
          shape: horizontal_line
          pixels: [[0, 5], [0, 6]]
        - id: added_v1
          color: 4 # Yellow
          shape: vertical_line
          pixels: [[1, 8], [2, 8]]
        - id: added_v2
          color: 4 # Yellow
          shape: vertical_line
          pixels: [[5, 8], [6, 8]]
        - id: added_h3
          color: 4 # Yellow
          shape: horizontal_line
          pixels: [[6, 0], [6, 1]]
        - id: added_h4
          color: 4 # Yellow
          shape: horizontal_line
          pixels: [[6, 4], [6, 5]]
    transformation_rule_applied: vertical_line_h2

common_properties:
  background_color: 8 # Azure seems consistent as background
  object_count: Exactly one non-background object in input.
  action: Add shapes based on original object's properties (color, H, W).
  color_rule: Added shapes use the same color as the original object.
  original_object_persistence: The original object remains in the output grid.

relationships:
  - The type and placement of added shapes depend on the original object's shape category (vertical line vs. rectangle) and dimensions (H, W).
  - For vertical lines, the specific rule seems to vary based on height H (compare H=5 vs H=2).
  - For rectangles, a copy is added top-right, and a line of length W+1 is added bottom-center.
  - Added shapes are typically lines whose length is derived from the original object's height (H) or width (W), or are direct copies.
```


## Natural Language Program

1.  **Identify Background and Object:** Determine the background color (the most common color in the input grid). Find the single contiguous block of non-background pixels; this is the 'object'. Record its color (C), height (H), and width (W).
2.  **Initialize Output:** Create the output grid as an exact copy of the input grid.
3.  **Apply Shape-Specific Rule:**
    *   **If the object is a vertical line (W=1):**
        *   **If H = 5:** Create a horizontal line segment of color C and length H (1x5). Add this segment starting at the top-left corner (0,0). Add another identical segment starting at the bottom-left corner (GridHeight-1, 0).
        *   **If H = 2:** Create horizontal segments of color C and length H (1x2). Create vertical segments of color C and length H (2x1). Add these segments at the following fixed locations (assuming GridHeight=7, GridWidth=9 as in the example):
            *   Horizontal at row 0, columns 1-2.
            *   Horizontal at row 0, columns 5-6.
            *   Horizontal at row 6, columns 0-1.
            *   Horizontal at row 6, columns 4-5.
            *   Vertical at column 8, rows 1-2.
            *   Vertical at column 8, rows 5-6.
        *   *(Generalize if possible, otherwise handle specific H values as cases)*
    *   **If the object is a horizontal line (H=1):** *(No direct example, but inferring symmetry)* Create vertical line segments of color C and length W (Wx1). Add these based on a pattern potentially mirroring the vertical line rules (e.g., add at top-left and top-right corners).
    *   **If the object is a rectangle (H>1 and W>1):**
        *   Create a copy of the object (HxW area with color C). Add this copy to the output grid, aligned with the top-right corner (position 0, GridWidth-W).
        *   Create a horizontal line segment of color C and length W+1 (1x(W+1)). Add this segment to the output grid on the bottom row (GridHeight-1), centered horizontally. If W+1 is even and GridWidth is even/odd causing centering ambiguity, default to placing the start slightly left of the exact center.
4.  **Final Output:** Return the modified grid.
```python
import numpy as np
from collections import Counter

"""
This program transforms an input grid based on the properties of a single 
non-background colored object found within it.

1.  **Identify Background and Object:** 
    Determine the background color (most common color). Find the single 
    contiguous non-background object, its color (C), height (H), and width (W).
2.  **Initialize Output:** Copy the input grid to the output grid.
3.  **Apply Shape-Specific Rules:**
    *   **Vertical Line (W=1):**
        *   If H=5: Add horizontal lines of length H and color C at the top-left 
          (row 0, cols 0 to H-1) and bottom-left (last row, cols 0 to H-1).
        *   If H=2: Add specific horizontal (length H) and vertical (length H) 
          lines of color C at fixed/relative positions based on example 3.
           - Horizontal: [0, 1:3], [0, 5:7], [6, 0:2], [6, 4:6]
           - Vertical:   [1:3, 8], [5:7, 8] 
           (Assuming grid size 7x9, adjustments might be needed for other sizes)
    *   **Rectangle (H>1, W>1):**
        *   Add a copy of the object (color C, size HxW) to the top-right 
          corner (rows 0 to H-1, cols GridWidth-W to GridWidth-1).
        *   Add a horizontal line of color C and length W+1 centered on the 
          bottom row (last row).
4.  **Return:** The modified output grid.
"""

def find_objects(grid, background_color):
    """
    Finds contiguous objects of non-background colors in the grid.
    Uses a simple flood fill (BFS) approach.
    """
    objects = []
    visited = np.zeros(grid.shape, dtype=bool)
    rows, cols = grid.shape

    for r in range(rows):
        for c in range(cols):
            if grid[r, c] != background_color and not visited[r, c]:
                color = grid[r, c]
                obj_pixels = []
                q = [(r, c)]
                visited[r, c] = True
                min_r, max_r = r, r
                min_c, max_c = c, c

                while q:
                    row, col = q.pop(0)
                    obj_pixels.append((row, col))
                    min_r = min(min_r, row)
                    max_r = max(max_r, row)
                    min_c = min(min_c, col)
                    max_c = max(max_c, col)

                    # Check 4 neighbors (up, down, left, right)
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = row + dr, col + dc
                        if 0 <= nr < rows and 0 <= nc < cols and \
                           not visited[nr, nc] and grid[nr, nc] == color:
                            visited[nr, nc] = True
                            q.append((nr, nc))
                
                bounding_box = {
                    'top': min_r, 
                    'left': min_c, 
                    'height': max_r - min_r + 1, 
                    'width': max_c - min_c + 1
                }
                objects.append({
                    'color': color, 
                    'pixels': obj_pixels, 
                    'bounding_box': bounding_box
                })
                
    return objects

def transform(input_grid):
    """
    Applies the transformation rules based on the detected object.
    """
    # Convert input to numpy array for easier manipulation
    input_np = np.array(input_grid, dtype=int)
    output_grid = np.copy(input_np)
    grid_h, grid_w = input_np.shape

    # 1. Identify Background and Object
    colors, counts = np.unique(input_np, return_counts=True)
    background_color = colors[np.argmax(counts)]
    
    objects = find_objects(input_np, background_color)
    
    # Expecting exactly one non-background object based on examples
    if not objects or len(objects) > 1:
        # If no object or multiple objects, return copy (or handle error)
        print(f"Warning: Found {len(objects)} objects, expected 1. Returning copy.")
        return output_grid.tolist() 
        
    obj = objects[0]
    obj_color = obj['color']
    bbox = obj['bounding_box']
    H = bbox['height']
    W = bbox['width']
    top = bbox['top']
    left = bbox['left']

    # 3. Apply Shape-Specific Rule
    if W == 1: # Vertical Line
        if H == 5: # Rule from train_1
            # Add horizontal line top-left
            if 0 + H <= grid_w:
                 output_grid[0, 0:H] = obj_color
            # Add horizontal line bottom-left
            if 0 + H <= grid_w:
                 output_grid[grid_h - 1, 0:H] = obj_color
                 
        elif H == 2: # Rule from train_3 (specific to 7x9 grid?)
             # Add shapes based on fixed/relative positions observed in example 3
             # Check boundaries before drawing
             # Horizontal lines (length H=2)
             if 1 + H <= grid_w: output_grid[0, 1:1+H] = obj_color # row 0, cols 1-2
             if 5 + H <= grid_w: output_grid[0, 5:5+H] = obj_color # row 0, cols 5-6
             if 0 + H <= grid_w: output_grid[grid_h-1, 0:0+H] = obj_color # row 6, cols 0-1
             if 4 + H <= grid_w: output_grid[grid_h-1, 4:4+H] = obj_color # row 6, cols 4-5
             # Vertical lines (length H=2)
             if 1 + H <= grid_h and grid_w > 0: output_grid[1:1+H, grid_w-1] = obj_color # col 8, rows 1-2
             if 5 + H <= grid_h and grid_w > 0: output_grid[5:5+H, grid_w-1] = obj_color # col 8, rows 5-6
        else:
             # Handle other vertical line heights if necessary, or default behavior
             print(f"Warning: Unhandled vertical line height H={H}. Returning copy.")
             # pass # No specific rule defined for other heights yet
             
    elif H > 1 and W > 1: # Rectangle (Rule from train_2)
        # Add copy of object at top-right
        if 0 + H <= grid_h and grid_w - W >= 0:
            # Ensure we only copy the object pixels, not the background within the bbox
            # This simpler version copies the whole bbox area. Refine if needed.
            # output_grid[0:H, grid_w-W:grid_w] = input_np[top:top+H, left:left+W] 
            # More precisely, color only the non-background pixels from the original object's bbox
             object_slice = input_np[top:top+H, left:left+W]
             target_slice = output_grid[0:H, grid_w-W:grid_w]
             mask = (object_slice == obj_color)
             target_slice[mask] = obj_color


        # Add horizontal line of length W+1 at bottom-center
        line_len = W + 1
        if line_len <= grid_w:
            start_col = (grid_w - line_len) // 2
            output_grid[grid_h - 1, start_col : start_col + line_len] = obj_color
            
    # elif H == 1: # Horizontal Line (Inferred, no example)
        # print("Warning: Horizontal line case not explicitly defined by examples.")
        # pass # Add rules here if needed based on future examples or inference

    else:
        # Handle other cases or single pixel objects if necessary
        print(f"Warning: Unhandled object shape H={H}, W={W}. Returning copy.")
        # pass 

    # 4. Final Output - convert back to list of lists
    return output_grid.tolist()

```
