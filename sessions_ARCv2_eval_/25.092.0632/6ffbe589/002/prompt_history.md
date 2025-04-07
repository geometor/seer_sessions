
## train_1

**input:**
```
0 0 0 0 0 0 0 0 3 0 3 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 3 3 3 3 3 3 3 3 3 3 3 0 0
0 0 0 0 0 0 3 3 8 8 0 8 8 8 0 8 0 3 0 0
0 0 0 0 0 0 0 3 8 0 8 8 0 8 8 8 8 3 0 0
0 0 0 0 0 0 0 3 0 8 0 0 6 0 0 8 0 3 0 0
0 0 0 0 0 0 0 3 8 8 6 6 6 6 0 8 8 3 3 0
0 0 0 0 0 0 0 3 8 0 0 6 0 6 0 0 8 3 0 0
0 0 0 0 0 0 0 3 8 8 0 6 6 6 6 8 8 3 3 0
0 0 0 0 0 0 0 3 0 8 0 0 6 0 0 8 0 3 0 0
0 0 0 0 0 0 3 3 8 8 8 8 0 8 8 8 8 3 0 0
0 0 0 0 0 0 0 3 0 8 0 8 8 8 0 8 0 3 0 0
0 0 0 0 0 0 0 3 3 3 3 3 3 3 3 3 3 3 0 0
0 0 0 0 0 0 0 0 0 0 0 3 3 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 8 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 8 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 3 0 0 0 6 6 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 3 0 0 0 0 0 0 3 0 0
0 3 3 3 3 3 3 3 3 3 3 3 0
0 3 0 8 0 8 8 8 0 8 0 3 3
0 3 8 8 8 8 0 8 8 8 8 3 0
0 3 0 8 0 0 6 0 0 8 0 3 3
3 3 8 8 6 6 6 6 0 8 8 3 0
3 3 8 0 0 6 0 6 0 0 8 3 0
0 3 8 8 0 6 6 6 6 8 8 3 0
0 3 0 8 0 0 6 0 0 8 0 3 0
0 3 8 8 8 8 0 8 8 0 8 3 0
0 3 0 8 0 8 8 8 0 8 8 3 0
0 3 3 3 3 3 3 3 3 3 3 3 0
0 0 0 0 0 3 0 3 0 0 0 0 0
```


## train_2

**input:**
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 5 0 5 0 5 5 5 5 0 5 0 0 0 0
0 0 0 0 0 0 0 0 0 3 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 5 0 0 3 3 3 3 0 0 5 0 0 0 0
0 0 0 0 0 0 0 3 3 0 4 0 0 3 0 5 0 0 0 0
0 0 0 0 0 0 5 0 3 0 4 4 0 3 3 0 0 0 0 0
0 0 0 0 0 0 5 0 3 0 4 4 4 3 0 5 0 0 0 0
0 0 0 0 0 0 5 0 3 0 0 0 0 3 0 5 0 0 0 0
0 0 0 0 0 0 5 0 0 3 3 3 3 0 0 5 0 0 0 0
0 0 0 0 0 0 0 0 0 0 3 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 5 0 5 5 0 5 5 5 0 5 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 3 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 4 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```


**output:**
```
5 0 5 0 5 5 5 5 0 5
0 0 0 0 0 0 3 0 0 0
5 0 0 3 3 3 3 0 0 5
0 0 3 0 0 0 0 3 3 5
5 3 3 0 4 4 4 3 0 0
5 0 3 0 4 4 0 3 0 5
5 0 3 0 4 0 0 3 0 5
5 0 0 3 3 3 3 0 0 5
0 0 0 0 0 3 0 0 0 0
5 0 5 5 0 5 5 5 0 5
```


## train_3

**input:**
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 1 1 1 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 4 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 4 0 4 0 4 0 4 0 4 0 0 0 0 0 0 0 0 0 0
0 0 4 0 4 0 4 0 4 0 4 0 0 0 0 0 0 0 0 0
0 4 0 0 0 0 1 0 0 4 0 0 0 0 0 0 0 0 0 0
0 0 4 0 1 0 0 1 1 0 4 0 0 0 0 0 0 0 0 0
0 4 0 0 1 2 2 0 1 4 0 0 0 0 0 0 0 0 0 0
0 0 4 1 0 2 2 1 0 0 4 0 0 0 0 0 0 0 0 0
0 4 0 0 1 1 0 0 0 4 0 0 0 0 0 0 0 0 0 0
0 0 4 0 0 1 1 0 0 0 4 0 0 0 0 0 0 0 0 0
0 4 0 4 0 4 0 4 0 4 0 0 0 0 0 0 0 0 0 0
0 0 4 0 4 0 4 0 4 0 4 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 4 0 4 0 4 0 4 0 4
4 0 4 0 4 0 4 0 4 0
0 4 0 1 1 0 0 0 0 4
4 0 0 1 0 1 0 0 4 0
0 4 1 0 2 2 0 1 0 4
4 0 0 0 2 2 1 1 4 0
0 4 0 1 1 0 1 0 0 4
4 0 0 0 0 1 0 0 4 0
0 4 0 4 0 4 0 4 0 4
4 0 4 0 4 0 4 0 4 0
```

*   **Perception:**
    *   Each input grid contains multiple non-white elements (pixels or groups of pixels).
    *   One prominent, larger, connected structure or pattern exists in each input, typically surrounded by white space but sometimes near the grid edges.
    *   Other smaller, isolated non-white pixels or small groups may exist elsewhere in the input grid.
    *   The output grid is consistently smaller than the input grid.
    *   The output grid contains the prominent structure from the input, seemingly extracted or cropped.
    *   The smaller, isolated elements from the input are absent in the output.
    *   The colors within the extracted structure remain unchanged between input and output.
    *   The shape and relative positions of pixels within the extracted structure are preserved.

*   **YAML Facts:**
    
```yaml
    task_description: Extract the largest contiguous non-white object from the input grid.
    
    elements:
      - role: background
        color: white (0)
      - role: object
        description: Contiguous area of non-white pixels. Multiple objects can exist.
    
    relationships:
      - type: size_comparison
        description: Objects can be compared based on the number of pixels they contain.
      - type: spatial_enclosure
        description: A bounding box can be defined for any object, representing the smallest rectangle containing all its pixels.
    
    actions:
      - name: identify_objects
        description: Find all distinct contiguous groups of non-white pixels in the input grid.
      - name: find_largest_object
        description: Determine which identified object has the greatest number of pixels.
      - name: calculate_bounding_box
        description: Find the minimum row, maximum row, minimum column, and maximum column coordinates for the largest object.
      - name: extract_subgrid
        description: Create the output grid by copying the portion of the input grid defined by the calculated bounding box of the largest object.
    
    constraints:
      - If multiple objects share the maximum size, the specific choice might need further clarification, but examples suggest there's usually one clearly largest object.
      - The output grid's dimensions are determined solely by the bounding box of the largest object.
    ```


*   **Natural Language Program:**
    1.  Scan the input grid to identify all separate contiguous blocks of non-white pixels. Consider pixels connected horizontally or vertically (not diagonally) as part of the same block.
    2.  For each identified block (object), count the total number of pixels it contains.
    3.  Select the object that has the largest pixel count.
    4.  Determine the minimum bounding box for this largest object. This means finding the top-most row, bottom-most row, left-most column, and right-most column occupied by any pixel of this object.
    5.  Create a new grid (the output grid) whose dimensions match the height and width of the calculated bounding box.
    6.  Copy the pixels from the input grid within the calculated bounding box region into the corresponding positions in the new output grid.
```python
import numpy as np
from collections import deque

"""
Identifies all contiguous non-white objects in the input grid, selects the object 
with the largest number of pixels, calculates its bounding box, and returns a 
new grid containing only the portion of the input grid within that bounding box.
"""

def _find_connected_component(grid, start_row, start_col, visited):
    """
    Finds a single connected component of non-white pixels using BFS.
    
    Args:
        grid (np.array): The input grid.
        start_row (int): The starting row for the search.
        start_col (int): The starting column for the search.
        visited (np.array): A boolean grid tracking visited pixels.

    Returns:
        list: A list of (row, col) tuples representing the coordinates of the
              pixels in the found component, or None if the start pixel is
              invalid (white or already visited).
    """
    rows, cols = grid.shape
    # Check if the starting point is valid
    if not (0 <= start_row < rows and 0 <= start_col < cols) or \
       visited[start_row, start_col] or \
       grid[start_row, start_col] == 0: # 0 is white/background
        return None

    component_coords = []
    q = deque([(start_row, start_col)])
    visited[start_row, start_col] = True

    while q:
        r, c = q.popleft()
        component_coords.append((r, c))

        # Check neighbors (up, down, left, right)
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nr, nc = r + dr, c + dc
            # Check bounds, visited status, and if the neighbor is non-white
            if 0 <= nr < rows and 0 <= nc < cols and \
               not visited[nr, nc] and \
               grid[nr, nc] != 0:
                visited[nr, nc] = True
                q.append((nr, nc))

    return component_coords

def _find_all_objects(grid):
    """
    Finds all distinct contiguous non-white objects in the grid.
    
    Args:
        grid (np.array): The input grid.

    Returns:
        list: A list where each element is a list of (row, col) tuples
              representing an object.
    """
    rows, cols = grid.shape
    visited = np.zeros((rows, cols), dtype=bool)
    all_objects = []

    # Iterate through each pixel
    for r in range(rows):
        for c in range(cols):
            # If pixel is non-white and not visited, start a search
            if grid[r, c] != 0 and not visited[r, c]:
                component = _find_connected_component(grid, r, c, visited)
                if component: # Should always be true if conditions met
                    all_objects.append(component)
    return all_objects

def _get_bounding_box(coords):
    """
    Calculates the bounding box for a set of coordinates.
    
    Args:
        coords (list): A list of (row, col) tuples.

    Returns:
        tuple: (min_row, max_row, min_col, max_col) or None if coords is empty.
    """
    if not coords:
        return None
        
    min_r = min(r for r, c in coords)
    max_r = max(r for r, c in coords)
    min_c = min(c for r, c in coords)
    max_c = max(c for r, c in coords)
    return min_r, max_r, min_c, max_c

def transform(input_grid):
    """
    Extracts the largest contiguous non-white object from the input grid.

    Args:
        input_grid (list of lists): The input grid represented as a list of lists.

    Returns:
        list of lists: The extracted subgrid containing the largest object.
                       Returns a 1x1 white grid if no non-white objects are found.
    """
    # Convert input to numpy array for easier processing
    grid_np = np.array(input_grid, dtype=int)
    
    # 1. Scan the input grid to identify all separate contiguous blocks (objects)
    all_objects = _find_all_objects(grid_np)

    # Handle case where no non-white objects are found
    if not all_objects:
        return [[0]] # Return a 1x1 white grid as specified in thought process

    # 2. & 3. Count pixels for each object and select the largest one
    largest_object = max(all_objects, key=len)

    # 4. Determine the minimum bounding box for the largest object
    min_r, max_r, min_c, max_c = _get_bounding_box(largest_object)

    # 5. & 6. Create the output grid by copying the relevant subgrid
    output_grid_np = grid_np[min_r : max_r + 1, min_c : max_c + 1]
    
    # Convert back to list of lists for the required output format
    output_grid = output_grid_np.tolist()

    return output_grid
```
