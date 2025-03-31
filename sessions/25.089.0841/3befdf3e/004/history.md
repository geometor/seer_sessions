
## train_1

**input:**
```
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 2 2 2 2 0 0 0
0 0 0 2 7 7 2 0 0 0
0 0 0 2 7 7 2 0 0 0
0 0 0 2 2 2 2 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0
0 0 0 2 2 2 2 0 0 0
0 0 0 2 2 2 2 0 0 0
0 2 2 7 7 7 7 2 2 0
0 2 2 7 2 2 7 2 2 0
0 2 2 7 2 2 7 2 2 0
0 2 2 7 7 7 7 2 2 0
0 0 0 2 2 2 2 0 0 0
0 0 0 2 2 2 2 0 0 0
0 0 0 0 0 0 0 0 0 0
```


## train_2

**input:**
```
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 4 4 4 0 0 0 0
0 0 0 4 6 4 0 0 0 0
0 0 0 4 4 4 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 4 4 4 0 0 0 0
0 0 4 6 6 6 4 0 0 0
0 0 4 6 4 6 4 0 0 0
0 0 4 6 6 6 4 0 0 0
0 0 0 4 4 4 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```


## train_3

**input:**
```
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 3 3 3 3 0 0 0 0
0 0 3 1 1 3 0 0 0 0
0 0 3 1 1 3 0 0 0 0
0 0 3 3 3 3 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0
0 0 3 3 3 3 0 0 0 0
0 0 3 3 3 3 0 0 0 0
3 3 1 1 1 1 3 3 0 0
3 3 1 3 3 1 3 3 0 0
3 3 1 3 3 1 3 3 0 0
3 3 1 1 1 1 3 3 0 0
0 0 3 3 3 3 0 0 0 0
0 0 3 3 3 3 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

Okay, let's analyze the provided examples to understand the transformation.

**Perception**

1.  **Input Structure:** Each input grid features a single, prominent, non-white object set against a uniform white background (color 0). This object consistently appears as a rectangular frame of one color (`outer_color`) surrounding a rectangular core region containing another color (`inner_color`).
2.  **Output Structure:** The output grid also contains a single, larger object against a white background. This output object incorporates the original input object at its center. The original object appears expanded outwards.
3.  **Transformation Pattern:** The transformation seems to involve projecting the original object's structure outwards by two "layers".
    *   The rows and columns occupied by the original object are extended outwards by two cells on each side (left, right, top, bottom).
    *   The cells immediately adjacent (1 cell away) to the original object along these extended rows/columns are filled with the original object's `inner_color`.
    *   The cells next further out (2 cells away) along these extended rows/columns are filled with the original object's `outer_color`.
    *   The original object remains unchanged in its initial position.
    *   Pixels outside these extended rows/columns remain white, creating a cross-like or plus-shaped expansion rather than a solid rectangular one.

**Facts**


```python
import numpy as np

"""
Find the single object in the input grid, composed of an outer frame color and an inner core color. 
Create an output grid by copying the input. 
Then, for every pixel in the original input object: 
- if it has the inner color, paint its direct orthogonal neighbors (up, down, left, right) with the inner color, provided they are currently white (0) and within grid bounds. 
- if it has the outer color, paint the cells two steps away orthogonally (up, down, left, right) with the outer color, provided they are currently white (0) and within grid bounds.
The painting happens on the output grid, using the original input grid as the reference for source pixel colors and locations.
"""

def find_colors(grid):
    """Finds the unique non-zero colors in the grid."""
    return sorted(list(np.unique(grid[grid != 0])))

def find_bounding_box(grid):
    """Finds the bounding box (min_row, min_col, max_row, max_col) of non-zero pixels."""
    non_white_coords = np.argwhere(grid != 0)
    if non_white_coords.size == 0:
        return None
    min_r, min_c = non_white_coords.min(axis=0)
    max_r, max_c = non_white_coords.max(axis=0)
    return (min_r, min_c, max_r, max_c)

def determine_inner_outer(grid, colors, bbox):
    """
    Determines the inner and outer colors.
    Assumes the color at the top-left corner of the bounding box is the outer color.
    """
    min_r, min_c, _, _ = bbox
    # The color at a corner of the bounding box is assumed to be the outer frame color.
    outer_c = grid[min_r, min_c]
    # The other non-white color must be the inner color.
    inner_c = colors[0] if colors[1] == outer_c else colors[1]
    return inner_c, outer_c

def transform(input_grid):
    """
    Applies the expansion transformation to the input grid.
    """
    input_np = np.array(input_grid, dtype=int)
    output_np = np.copy(input_np)
    rows, cols = input_np.shape

    # Find the non-white colors present
    non_white_colors = find_colors(input_np)

    # Expecting exactly two non-white colors for this pattern
    if len(non_white_colors) != 2:
        # If not two colors, or no colors, return the original grid
        # Or could raise an error depending on desired behavior for unexpected inputs
        return input_grid 

    # Find the bounding box of the object
    bbox = find_bounding_box(input_np)
    if bbox is None:
        # If no object found, return the original grid
        return input_grid

    # Determine which color is inner and which is outer
    inner_color, outer_color = determine_inner_outer(input_np, non_white_colors, bbox)

    # Define the relative coordinates for 1-step and 2-step orthogonal neighbors
    one_step_neighbors = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    two_step_neighbors = [(0, 2), (0, -2), (2, 0), (-2, 0)]

    # Iterate through each cell of the *original* input grid
    for r in range(rows):
        for c in range(cols):
            original_color = input_np[r, c]

            # If the cell has the inner color, paint 1 step away
            if original_color == inner_color:
                for dr, dc in one_step_neighbors:
                    nr, nc = r + dr, c + dc
                    # Check bounds and if the target cell in the output is currently white
                    if 0 <= nr < rows and 0 <= nc < cols and output_np[nr, nc] == 0:
                        output_np[nr, nc] = inner_color
            
            # If the cell has the outer color, paint 2 steps away
            elif original_color == outer_color:
                for dr, dc in two_step_neighbors:
                    nr, nc = r + dr, c + dc
                    # Check bounds and if the target cell in the output is currently white
                    if 0 <= nr < rows and 0 <= nc < cols and output_np[nr, nc] == 0:
                        output_np[nr, nc] = outer_color

    # Convert the result back to a list of lists
    return output_np.tolist()
```
```python
import numpy as np

"""
Expands a central rectangular object outwards by two layers, using the object's inner and outer colors.

The transformation identifies the single rectangular object in the input, which is composed of an outer frame color and an inner core color. It then creates an expanded version in the output grid. The expansion adds two layers around the original object: the layer immediately adjacent (orthogonal distance 1) is filled with the inner color, and the next layer (orthogonal distance 2) is filled with the outer color. The original object remains in place. The expansion only colors cells that were initially white (background color 0).
"""

def find_colors(grid):
    """Finds the unique non-zero colors in the grid."""
    return sorted(list(np.unique(grid[grid != 0])))

def find_bounding_box(grid):
    """Finds the bounding box (min_row, min_col, max_row, max_col) of non-zero pixels."""
    non_white_coords = np.argwhere(grid != 0)
    if non_white_coords.size == 0:
        return None
    min_r, min_c = non_white_coords.min(axis=0)
    max_r, max_c = non_white_coords.max(axis=0)
    return (min_r, min_c, max_r, max_c)

def determine_inner_outer(grid, colors, bbox):
    """
    Determines the inner and outer colors.
    Assumes the color at the top-left corner of the bounding box is the outer color.
    Handles cases where only one non-white color might be present (although the description implies two).
    """
    if len(colors) == 0:
        return None, None # No colors found
    
    min_r, min_c, _, _ = bbox
    outer_c = grid[min_r, min_c]
    
    if len(colors) == 1:
        # If only one color, it acts as both inner and outer for expansion
        # This might need adjustment based on specific task behavior for single-color objects
        inner_c = outer_c
    else:
        # If two colors, find the one that isn't the outer color
        inner_c = colors[0] if colors[1] == outer_c else colors[1]
        
    return inner_c, outer_c

def get_object_coords(grid):
    """Returns a list of (row, col) tuples for all non-zero pixels."""
    return [tuple(coord) for coord in np.argwhere(grid != 0)]

def min_manhattan_distance(point, coord_set):
    """Calculates the minimum Manhattan distance from a point to any coordinate in a set."""
    if not coord_set:
        return float('inf') # Or handle as appropriate if the set can be empty
    r1, c1 = point
    min_dist = float('inf')
    for r2, c2 in coord_set:
        dist = abs(r1 - r2) + abs(c1 - c2)
        min_dist = min(min_dist, dist)
    return min_dist

def transform(input_grid):
    """
    Applies the two-layer expansion transformation based on distance to the original object.
    """
    input_np = np.array(input_grid, dtype=int)
    rows, cols = input_np.shape
    
    # 1. Identify the object and its properties
    non_white_colors = find_colors(input_np)
    object_coords = get_object_coords(input_np)

    if not object_coords: # No object found
        return input_grid # Return original grid if no object

    bbox = find_bounding_box(input_np) 
    
    # Handle cases where finding colors/bbox might fail or be inconsistent
    if not non_white_colors or bbox is None:
         return input_grid # Should not happen if object_coords is not empty, but safe check

    # Expecting two colors based on examples, but handle single color case.
    # The description implies two colors, adjust if single-color behavior differs.
    if len(non_white_colors) > 2:
        # Unexpected number of colors, return original grid or raise error
        print(f"Warning: Expected 1 or 2 non-white colors, found {len(non_white_colors)}. Returning original grid.")
        return input_grid

    inner_color, outer_color = determine_inner_outer(input_np, non_white_colors, bbox)
    
    # 2. Initialize the output grid as a copy of the input
    output_np = np.copy(input_np)

    # 3. Iterate through all grid cells to potentially color them
    for r in range(rows):
        for c in range(cols):
            # Only consider coloring cells that are currently white (background)
            if output_np[r, c] == 0:
                # 4. Calculate the minimum orthogonal distance to the original object
                min_dist = min_manhattan_distance((r, c), object_coords)

                # 5. Apply coloring rules based on distance
                if min_dist == 1:
                    # Color with inner_color if distance is 1
                    output_np[r, c] = inner_color
                elif min_dist == 2:
                    # Color with outer_color if distance is 2
                    output_np[r, c] = outer_color
                    
    # 6. Return the modified grid as a list of lists
    return output_np.tolist()
```
