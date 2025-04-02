
## train_1

**input:**
```
0 0 0 0 0 0 8 0 0 0
0 2 2 2 0 8 8 8 0 0
0 2 2 2 0 0 8 8 0 0
0 2 2 2 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 1 1 1 0 5 5 5 0
0 0 1 1 1 0 0 5 5 0
0 0 1 1 1 0 5 5 5 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0
0 2 2 2 0 0 0 0 0 0
0 2 2 2 0 0 0 0 0 0
0 2 2 2 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 1 1 1 0 0 0 0 0
0 0 1 1 1 0 0 0 0 0
0 0 1 1 1 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```


## train_2

**input:**
```
6 6 0 0 0 0 4 4
0 0 0 0 0 0 4 4
0 0 4 0 0 0 4 4
0 4 4 4 0 0 0 0
0 0 4 0 0 2 0 0
0 0 0 0 2 2 2 0
7 7 0 0 0 2 0 0
7 7 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 4 0 0 0 0 0
0 4 4 4 0 0 0 0
0 0 4 0 0 2 0 0
0 0 0 0 2 2 2 0
0 0 0 0 0 2 0 0
0 0 0 0 0 0 0 0
```


## train_3

**input:**
```
0 0 0 0 0 0 0 0 0
0 7 7 7 0 3 3 3 0
0 0 7 0 0 0 3 0 0
0 7 7 7 0 3 3 3 0
0 0 0 0 0 7 7 7 0
0 3 3 3 0 7 7 7 0
0 0 3 0 0 7 7 7 0
0 3 3 3 0 0 0 0 0
0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0
0 7 7 7 0 3 3 3 0
0 0 7 0 0 0 3 0 0
0 7 7 7 0 3 3 3 0
0 0 0 0 0 0 0 0 0
0 3 3 3 0 0 0 0 0
0 0 3 0 0 0 0 0 0
0 3 3 3 0 0 0 0 0
0 0 0 0 0 0 0 0 0
```

Okay, let's analyze the task examples.

**Perception of the elements:**

1.  **Input/Output Structure:** Each example provides a pair of grids, an input and an output, of the same dimensions.
2.  **Content:** The grids contain colored pixels, forming distinct shapes (objects) against a white (0) background.
3.  **Transformation:** Comparing inputs and outputs reveals that some colored objects present in the input are entirely absent in the output (replaced by the white background color), while others remain unchanged.
4.  **Key Feature:** The determining factor for whether an object is kept or removed seems to be its position relative to the grid's borders. Objects touching any edge (top, bottom, left, or right) in the input grid are removed in the output grid. Objects entirely contained within the grid, not touching any edge, are preserved.

**YAML Facts:**


```yaml
Examples:
  - id: train_1
    input_grid_size: [10, 10]
    output_grid_size: [10, 10]
    input_objects:
      - color: red (2)
        location: B2:D4 # Using spreadsheet notation for rough area
        touches_border: false
      - color: azure (8)
        location: A7:C9
        touches_border: true # Touches top and right
      - color: blue (1)
        location: F3:H5
        touches_border: false
      - color: gray (5)
        location: F7:H9
        touches_border: true # Touches right
    output_objects_kept:
      - color: red (2)
      - color: blue (1)
    action: Remove objects touching the border.
  - id: train_2
    input_grid_size: [8, 8]
    output_grid_size: [8, 8]
    input_objects:
      - color: magenta (6)
        location: A1:A2
        touches_border: true # Touches top
      - color: yellow (4)
        location: A7:C8
        touches_border: true # Touches top and right
      - color: yellow (4)
        location: C3:E5 # Roughly
        touches_border: false
      - color: red (2)
        location: E6:G8 # Roughly
        touches_border: false
      - color: orange (7)
        location: G1:H2
        touches_border: true # Touches left
    output_objects_kept:
      - color: yellow (4)
      - color: red (2)
    action: Remove objects touching the border.
  - id: train_3
    input_grid_size: [9, 9]
    output_grid_size: [9, 9]
    input_objects:
      - color: orange (7)
        location: B2:D4 # Roughly
        touches_border: false
      - color: green (3)
        location: B6:D8 # Roughly
        touches_border: false
      - color: orange (7)
        location: E6:G8 # Roughly
        touches_border: true # Touches right
      - color: green (3)
        location: F2:H4 # Roughly
        touches_border: false
    output_objects_kept:
      - color: orange (7) # Top-left one
      - color: green (3) # Both
    action: Remove objects touching the border.

Grid_Properties:
  - border_rows: [0, max_row_index]
  - border_cols: [0, max_col_index]

Object_Properties:
  - is_contiguous_block: true
  - color: non-white (1-9)
  - location: set of (row, col) coordinates
  - touches_border: boolean (true if any coordinate has row=0, col=0, row=max_row, or col=max_col)

Transformation_Rule:
  - Identify all distinct, contiguous non-white objects.
  - Check if any pixel of an object lies on any of the four grid borders.
  - If an object touches a border, remove it (replace all its pixels with white).
  - If an object does not touch any border, keep it unchanged.
```


**Natural Language Program:**

1.  Initialize the output grid as a copy of the input grid.
2.  Identify all distinct connected components (objects) of non-white pixels in the input grid.
3.  For each identified object:
    a.  Check if any pixel belonging to this object is located in the first row, last row, first column, or last column of the grid.
    b.  If the object touches any border (i.e., the check in step 3a is true), then iterate through all the pixel coordinates belonging to this object and set the corresponding pixel values in the output grid to white (0).
4.  Return the modified output grid. Objects that did not touch any border remain unchanged from the initial copy.
```python
"""
Identify all distinct connected components (objects) of non-white pixels in the input grid.
For each object, check if any of its constituent pixels lie on the border (first/last row or first/last column) of the grid.
If an object touches any border, replace all pixels belonging to that object with the background color (white, 0) in the output grid.
Objects that do not touch any border remain unchanged.
The output grid has the same dimensions as the input grid.
"""

import numpy as np
from collections import deque

def find_object(grid, start_row, start_col, visited):
    """
    Finds a connected object of the same color starting from (start_row, start_col).
    Uses Breadth-First Search (BFS).

    Args:
        grid (np.array): The input grid.
        start_row (int): The starting row index.
        start_col (int): The starting column index.
        visited (np.array): A boolean grid indicating visited pixels.

    Returns:
        tuple: (list of pixel coordinates [(r, c), ...], boolean indicating if it touches border)
               Returns (None, False) if the starting pixel is invalid or already visited.
    """
    rows, cols = grid.shape
    if not (0 <= start_row < rows and 0 <= start_col < cols) or visited[start_row, start_col]:
        return None, False

    color = grid[start_row, start_col]
    if color == 0: # Background color is not an object
         visited[start_row, start_col] = True # Mark as visited to avoid re-checking
         return None, False

    q = deque([(start_row, start_col)])
    object_pixels = []
    touches_border = False
    visited[start_row, start_col] = True

    while q:
        r, c = q.popleft()
        object_pixels.append((r, c))

        # Check if this pixel touches the border
        if r == 0 or r == rows - 1 or c == 0 or c == cols - 1:
            touches_border = True

        # Explore neighbors (up, down, left, right)
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nr, nc = r + dr, c + dc

            # Check if neighbor is valid, has the same color, and hasn't been visited
            if 0 <= nr < rows and 0 <= nc < cols and \
               not visited[nr, nc] and grid[nr, nc] == color:
                visited[nr, nc] = True
                q.append((nr, nc))

    return object_pixels, touches_border


def transform(input_grid):
    """
    Transforms the input grid by removing non-background objects that touch the border.

    Args:
        input_grid (np.array): A 2D numpy array representing the input grid.

    Returns:
        np.array: A 2D numpy array representing the transformed output grid.
    """
    # Initialize output_grid as a copy of the input grid
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape
    
    # Keep track of visited pixels to avoid processing parts of the same object multiple times
    visited = np.zeros_like(input_grid, dtype=bool)

    # Iterate through each pixel of the input grid
    for r in range(rows):
        for c in range(cols):
            # If the pixel is part of an object (non-background) and hasn't been visited yet
            if input_grid[r, c] != 0 and not visited[r, c]:
                # Find the complete object connected to this pixel
                object_pixels, touches_border = find_object(input_grid, r, c, visited)
                
                # If the object was found and it touches the border
                if object_pixels is not None and touches_border:
                    # Erase the object from the output grid by setting its pixels to white (0)
                    for pr, pc in object_pixels:
                        output_grid[pr, pc] = 0
            elif input_grid[r, c] == 0:
                 # Make sure background pixels are marked visited so find_object doesn't start on them
                 visited[r,c] = True 

    return output_grid
```
```python
"""
Transforms the input grid by removing non-background objects that touch the border.
An object is defined as a contiguous group of pixels of the same non-zero color (non-white).
A pixel touches the border if its row index is 0 or the maximum row index, or its column 
index is 0 or the maximum column index. If any pixel of an object touches the border, the 
entire object is removed (replaced with the background color 0 - white). Objects that
do not touch any border remain unchanged.
"""

import numpy as np
from collections import deque

def find_object(grid, start_row, start_col, visited):
    """
    Finds a connected object of the same color starting from (start_row, start_col) 
    using Breadth-First Search (BFS). Marks visited pixels for the found object 
    within the provided visited array.

    Args:
        grid (np.array): The input grid.
        start_row (int): The starting row index.
        start_col (int): The starting column index.
        visited (np.array): A boolean grid indicating visited pixels (modified in place).

    Returns:
        tuple: (list of pixel coordinates [(r, c), ...], boolean indicating if it touches border)
               Returns (None, False) if the starting pixel is background (color 0) or 
               has already been visited as part of another object search.
    """
    rows, cols = grid.shape
    
    # Check if the starting point is out of bounds
    if not (0 <= start_row < rows and 0 <= start_col < cols):
        return None, False
        
    # Check if already visited or is background color
    if visited[start_row, start_col] or grid[start_row, start_col] == 0:
        # Mark as visited if not already (e.g., if it's background) 
        # to avoid redundant checks by the caller.
        visited[start_row, start_col] = True 
        return None, False

    # Start BFS
    color = grid[start_row, start_col]
    q = deque([(start_row, start_col)])
    object_pixels = []
    touches_border = False
    visited[start_row, start_col] = True # Mark the starting pixel as visited

    while q:
        r, c = q.popleft()
        object_pixels.append((r, c))

        # Check if this pixel touches the border (top, bottom, left, or right edge)
        if r == 0 or r == rows - 1 or c == 0 or c == cols - 1:
            touches_border = True # Set the flag; it stays true if any part touches

        # Explore neighbors (4-connectivity: up, down, left, right)
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nr, nc = r + dr, c + dc

            # Check if neighbor is within grid bounds
            if 0 <= nr < rows and 0 <= nc < cols:
                 # Check if neighbor has the same color and hasn't been visited yet
                if not visited[nr, nc] and grid[nr, nc] == color:
                    visited[nr, nc] = True # Mark visited when adding to queue
                    q.append((nr, nc))

    return object_pixels, touches_border


def transform(input_grid):
    """
    Transforms the input grid by removing non-background objects that touch the border.

    Args:
        input_grid (np.array): A 2D numpy array representing the input grid.

    Returns:
        np.array: A 2D numpy array representing the transformed output grid.
    """
    # Initialize output_grid as a copy of the input grid. Objects that are not
    # removed will implicitly remain.
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape
    
    # Keep track of visited pixels during object finding to ensure each pixel
    # is processed only once as part of an object.
    visited = np.zeros_like(input_grid, dtype=bool)

    # Iterate through each pixel of the input grid
    for r in range(rows):
        for c in range(cols):
            # If the pixel hasn't been visited yet (means it's either unvisited non-background
            # or unvisited background)
            if not visited[r, c]:
                # Attempt to find an object starting from this pixel.
                # find_object will handle checking if it's background (color 0)
                # or already visited, returning None in those cases.
                # It will also update the 'visited' array for all pixels it processes.
                object_pixels, touches_border = find_object(input_grid, r, c, visited)
                
                # If a valid object was found (object_pixels is not None) 
                # AND this object touches the border
                if object_pixels is not None and touches_border:
                    # Erase the object from the output grid by setting all its pixels
                    # to the background color (white, 0).
                    for pr, pc in object_pixels:
                        output_grid[pr, pc] = 0
                # No 'else' block is needed:
                # - If object_pixels is None, it was background or already visited; handled by 'visited'.
                # - If object_pixels is not None but touches_border is False, the object should
                #   remain, which it does because output_grid started as a copy.

    return output_grid
```
