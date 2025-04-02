
## train_1

**input:**
```
0 0 0 0 0 0 0 0 0 0
0 0 0 2 2 2 0 0 0 0
0 0 0 2 0 2 0 0 0 0
0 0 0 2 2 2 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 3 3 0 0 1 1 1 1 0
0 3 3 0 0 1 0 0 1 0
0 3 3 0 0 1 1 1 1 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0
0 0
0 0
```


## train_2

**input:**
```
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 4 4 4 4 0
0 0 0 0 0 4 4 4 4 0
0 7 7 7 0 4 4 4 4 0
0 7 0 7 0 4 4 4 4 0
0 7 0 7 0 0 0 0 0 0
0 7 0 7 0 8 8 8 0 0
0 7 0 7 0 8 0 8 0 0
0 7 7 7 0 8 8 8 0 0
0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0
0 0 0 0
0 0 0 0
0 0 0 0
```


## train_3

**input:**
```
0 6 6 6 6 6 0 8 8 8
0 6 0 0 0 6 0 8 0 8
0 6 6 6 6 6 0 8 8 8
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 4 4 4 0
0 2 2 2 0 0 4 0 4 0
0 2 2 2 0 0 4 0 4 0
0 2 2 2 0 0 4 4 4 0
0 2 2 2 0 0 0 0 0 0
0 2 2 2 0 0 0 0 0 0
```


**output:**
```
0 0 0
0 0 0
0 0 0
0 0 0
0 0 0
```

**Perception**

1.  **Input Structure:** The input is a grid containing a white background (color 0) and several distinct "objects". Each object is a contiguous block of pixels of the same non-white color.
2.  **Output Structure:** The output is always a grid filled entirely with white pixels (color 0). The size (height and width) of the output grid varies between examples.
3.  **Transformation Goal:** The task is to determine the correct dimensions (height and width) for the output grid based on the properties of the objects found in the input grid.
4.  **Object Properties:** The key properties of the objects seem to be their bounding box dimensions (height and width). Color itself doesn't directly determine the output grid's content (which is always white) or necessarily its size, but it helps distinguish objects.
5.  **Identifying the Rule:**
    *   First, all distinct non-white objects need to be identified.
    *   For each object, its height and width (based on its bounding box) must be calculated.
    *   From the set of all object dimensions, four values are crucial: the overall maximum height (MaxH), the overall minimum width (MinW), the overall maximum width (MaxW), and potentially the overall minimum height (MinH), although MinH wasn't needed in the final rule.
    *   A comparison between MaxH and MaxW determines how the output dimensions are calculated.
    *   If the maximum height found among all objects is strictly greater than the maximum width found among all objects (MaxH > MaxW), then the output grid's dimensions are MaxW x MaxW.
    *   Otherwise (if MaxH <= MaxW), the output grid's dimensions are MaxH x MinW.
    *   The output grid is then created with these calculated dimensions and filled with white (0).

**Facts**


```python
import numpy as np

"""
Identifies all distinct non-white objects in the input grid.
Calculates the bounding box height and width for each object.
Determines the overall maximum height (MaxH), maximum width (MaxW), and minimum width (MinW) across all objects.
Compares MaxH and MaxW to determine the output grid dimensions:
- If MaxH is equal to MaxW, the output dimensions are MaxH x MinW.
- If MaxH is less than MaxW, the output dimensions are MaxH x MaxH.
- If MaxH is greater than MaxW, the output dimensions are MaxW x MaxW.
Creates an output grid of the calculated dimensions filled entirely with white pixels (color 0).
"""

def find_objects(grid):
    """
    Finds all contiguous objects of the same non-background color.

    Args:
        grid (np.array): The input grid.

    Returns:
        list: A list of tuples, where each tuple contains (color, set_of_coordinates).
              Returns an empty list if no objects are found.
    """
    rows, cols = grid.shape
    visited = np.zeros_like(grid, dtype=bool)
    objects = []
    background_color = 0 # Assuming 0 is always the background

    for r in range(rows):
        for c in range(cols):
            # If this pixel is not background and hasn't been visited yet
            if grid[r, c] != background_color and not visited[r, c]:
                color = grid[r, c]
                obj_coords = set()
                # Use Breadth-First Search (BFS) to find all connected pixels of the same color
                q = [(r, c)]
                visited[r, c] = True
                
                while q:
                    row, col = q.pop(0)
                    obj_coords.add((row, col))
                    
                    # Check 4 neighbors (up, down, left, right)
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = row + dr, col + dc
                        
                        # Check boundaries and if the neighbor is valid
                        if 0 <= nr < rows and 0 <= nc < cols and \
                           not visited[nr, nc] and grid[nr, nc] == color:
                            visited[nr, nc] = True
                            q.append((nr, nc))
                            
                # Add the found object (color and coordinates) to the list
                if obj_coords:
                    objects.append((color, obj_coords))
    return objects

def get_bounding_box_dims(obj_coords):
    """
    Calculates the height and width of the bounding box for a set of coordinates.

    Args:
        obj_coords (set): A set of (row, col) tuples representing the object's pixels.

    Returns:
        tuple: (height, width) of the bounding box. Returns (0, 0) if input is empty.
    """
    if not obj_coords:
        return 0, 0
        
    rows = [r for r, c in obj_coords]
    cols = [c for r, c in obj_coords]
    
    min_r, max_r = min(rows), max(rows)
    min_c, max_c = min(cols), max(cols)
    
    height = max_r - min_r + 1
    width = max_c - min_c + 1
    
    return height, width

def transform(input_grid):
    """
    Transforms the input grid based on the dimensions of the contained objects.

    Args:
        input_grid (list of lists): The input grid represented as a list of lists.

    Returns:
        np.array: The transformed output grid (filled with white).
    """
    # Convert input to numpy array for easier manipulation
    grid = np.array(input_grid, dtype=int)
    
    # Find all distinct objects in the grid
    objects = find_objects(grid)
    
    # If no objects are found, return a default 1x1 white grid
    if not objects:
        return np.zeros((1, 1), dtype=int)
        
    # Calculate dimensions (height, width) for each object's bounding box
    object_dims = [get_bounding_box_dims(coords) for color, coords in objects]
    
    # Extract all heights and widths
    heights = [h for h, w in object_dims]
    widths = [w for h, w in object_dims]
    
    # Find the maximum height, maximum width, and minimum width across all objects
    max_h = max(heights)
    max_w = max(widths)
    min_w = min(widths)
    
    # Determine the output grid dimensions based on the comparison of MaxH and MaxW
    out_h, out_w = 0, 0
    if max_h == max_w:
        out_h = max_h
        out_w = min_w
    elif max_h < max_w:
        out_h = max_h
        out_w = max_h
    else: # max_h > max_w
        out_h = max_w
        out_w = max_w
        
    # Create the output grid with the calculated dimensions, filled with white (0)
    output_grid = np.zeros((out_h, out_w), dtype=int)
    
    return output_grid
```
