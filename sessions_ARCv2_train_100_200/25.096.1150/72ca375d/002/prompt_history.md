
## train_1

**input:**
```
0 0 0 0 0 0 0 0 0 0
0 0 4 4 0 0 0 0 0 0
0 0 4 4 0 0 8 8 8 0
0 0 0 0 0 0 8 0 8 8
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 2 2 2 2 0 0 0 0
0 2 2 2 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```


**output:**
```
4 4
4 4
```


## train_2

**input:**
```
0 0 0 0 0 0 0 0 0 0
0 2 2 0 0 0 0 0 0 0
0 0 2 2 2 0 0 7 7 0
0 0 0 0 0 0 7 0 7 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 6 6 6 6 0 0 0
0 0 0 0 6 6 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```


**output:**
```
6 6 6 6
0 6 6 0
```


## train_3

**input:**
```
0 0 0 0 0 0 0 0 0 0
0 3 3 0 0 0 0 0 0 0
0 0 3 0 0 5 0 0 5 0
0 0 3 0 0 5 5 5 5 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 8 8 8 0 0 0 0
8 8 8 8 0 8 8 0 0 0
0 0 0 0 0 0 0 0 0 0
```


**output:**
```
5 0 0 5
5 5 5 5
```

Okay, let's break down the task based on the provided examples.

**Perception of Elements:**

1.  **Input:** A 10x10 grid containing numerical digits. The digit '0' represents the background. Non-zero digits represent different 'colors' or 'types' of objects.
2.  **Objects:** Within the input grid, there are distinct shapes formed by connected cells of the same non-zero digit. Connectivity appears to be orthogonal (up, down, left, right), not diagonal. Each example seems to contain exactly three distinct non-zero objects.
3.  **Output:** A smaller rectangular grid, also containing digits. The content of the output grid appears to be a direct copy of a specific portion of the input grid.
4.  **Transformation:** The core task is to identify which specific object from the input grid should be selected and then extract the rectangular region (bounding box) enclosing that object to form the output.

**Discerning the Logic:**

*   The selection of the object doesn't seem based solely on color value, size (number of cells), or bounding box area alone, as different examples prioritize objects differently based on these individual metrics.
*   Let's consider the "density" of each object within its bounding box (number of object cells / total cells in bounding box).
    *   **Train 1:**
        *   Object 4: 4 cells / (2x2 area) = density 1.0
        *   Object 8: 6 cells / (2x4 area) = density 0.75
        *   Object 2: 7 cells / (2x4 area) = density 0.875
        *   Highest density is 1.0 (Object 4). Output is the bounding box of Object 4.
    *   **Train 2:**
        *   Object 2: 5 cells / (2x4 area) = density 0.625
        *   Object 7: 4 cells / (2x3 area) = density ~0.667
        *   Object 6: 6 cells / (2x4 area) = density 0.75
        *   Highest density is 0.75 (Object 6). Output is the bounding box of Object 6.
    *   **Train 3:**
        *   Object 3: 4 cells / (3x3 area) = density ~0.444
        *   Object 5: 6 cells / (2x4 area) = density 0.75
        *   Object 8: 7 cells / (2x5 area) = density 0.70
        *   Highest density is 0.75 (Object 5). Output is the bounding box of Object 5.

*   The consistent rule appears to be: identify the object with the highest density within its own bounding box and output that bounding box.

**YAML Fact Document:**


```yaml
task_description: Extract the bounding box of a specific object from an input grid based on density.

input_elements:
  - type: grid
    rows: 10
    columns: 10
    cell_type: digit (0-9)
    properties:
      - background_value: 0
      - objects:
          description: Connected components of identical non-zero digits.
          connectivity: orthogonal (up, down, left, right)
          count_per_example: 3 (observed)

output_elements:
  - type: grid
    properties:
      - content: Subgrid extracted from the input grid.
      - source: Corresponds to the bounding box of a selected object from the input.

transformation:
  - action: identify_objects
    description: Find all distinct connected components of non-zero cells in the input grid.
    inputs: input_grid
    outputs: list_of_objects
      - object_properties:
          - color (digit)
          - cell_coordinates
  - action: calculate_object_properties
    description: For each identified object, calculate its properties.
    inputs: list_of_objects
    outputs: list_of_objects_with_properties
      - object_properties:
          - color
          - cell_coordinates
          - bounding_box: (min_row, max_row, min_col, max_col)
          - area: bounding_box_height * bounding_box_width
          - mass: count of cells in the object
          - density: mass / area
  - action: select_target_object
    description: Choose the object with the maximum calculated density.
    inputs: list_of_objects_with_properties
    outputs: target_object
    selection_criterion: maximum_density
  - action: extract_output
    description: Extract the subgrid from the input grid defined by the bounding box of the target_object.
    inputs:
      - input_grid
      - target_object.bounding_box
    outputs: output_grid
```


**Natural Language Program:**

1.  Examine the input grid and identify all distinct objects, where an object is a group of connected cells having the same non-zero digit. Consider cells connected horizontally or vertically as part of the same object.
2.  For each identified object:
    a.  Determine its bounding box (the smallest rectangle containing all its cells).
    b.  Count the number of cells belonging to the object (its "mass").
    c.  Calculate the area of its bounding box (height * width).
    d.  Calculate the object's density by dividing its mass by its bounding box area.
3.  Select the object that has the highest density value.
4.  Create the output grid by copying the portion of the input grid that falls within the bounding box of the selected highest-density object.
```python
"""
Identify all distinct objects (connected components of the same non-zero digit) in the input grid.
For each object, calculate its bounding box (smallest rectangle containing all its cells).
Calculate the object's "mass" (number of cells belonging to the object).
Calculate the area of the object's bounding box (height * width).
Calculate the object's density (mass / area).
Select the object with the highest density.
Return the subgrid from the input corresponding to the bounding box of the selected highest-density object.
"""

import collections

def get_bounding_box(coords):
    """Calculates the bounding box for a set of coordinates."""
    if not coords:
        return None
    min_r = min(r for r, c in coords)
    max_r = max(r for r, c in coords)
    min_c = min(c for r, c in coords)
    max_c = max(c for r, c in coords)
    # Returns (min_row, max_row, min_col, max_col)
    return min_r, max_r, min_c, max_c

def find_objects(grid: list[list[int]]) -> list[dict]:
    """Finds all connected components of non-zero cells in the grid."""
    rows = len(grid)
    if rows == 0:
        return []
    cols = len(grid[0])
    if cols == 0:
        return []
        
    visited = set()
    objects = [] # List to store dicts: {'color': color, 'coords': set_of_coords}

    # Iterate through each cell to find starting points of objects
    for r in range(rows):
        for c in range(cols):
            # If cell is non-zero and not yet visited, start a search (BFS)
            if grid[r][c] != 0 and (r, c) not in visited:
                color = grid[r][c]
                current_object_coords = set()
                # Use deque for efficient queue operations in BFS
                queue = collections.deque([(r, c)]) 
                visited.add((r, c))
                
                while queue:
                    row, col = queue.popleft() # Get next cell from queue
                    current_object_coords.add((row, col))
                    
                    # Check orthogonal neighbors (up, down, left, right)
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = row + dr, col + dc
                        # Check bounds, if neighbor has the same color, and not visited
                        if 0 <= nr < rows and 0 <= nc < cols and \
                           (nr, nc) not in visited and \
                           grid[nr][nc] == color:
                            visited.add((nr, nc))
                            queue.append((nr, nc))
                
                # Store the found object if it has coordinates
                if current_object_coords:
                     objects.append({'color': color, 'coords': current_object_coords})
    return objects


def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Transforms the input grid by finding the object with the highest density
    within its bounding box and returning that bounding box subgrid.
    """
    
    # 1. Find all distinct objects in the input grid
    found_objects = find_objects(input_grid)
    
    # Handle edge case where no objects are found
    if not found_objects:
        return [] 

    object_details = []
    # 2. For each object, calculate its properties (bounding box, mass, area, density)
    for obj in found_objects:
        coords = obj['coords']
        # Calculate bounding box
        bbox = get_bounding_box(coords)
        if bbox is None: # Skip if object somehow has no coordinates
            continue

        min_r, max_r, min_c, max_c = bbox
        # Calculate mass (number of cells)
        mass = len(coords)
        # Calculate bounding box dimensions
        height = max_r - min_r + 1
        width = max_c - min_c + 1
        # Calculate bounding box area
        area = height * width
        # Calculate density, handle division by zero just in case (though area should be > 0)
        density = mass / area if area > 0 else 0
        
        # Store calculated properties
        object_details.append({
            'color': obj['color'],
            'coords': coords,
            'bbox': bbox,
            'mass': mass,
            'area': area,
            'density': density
        })

    # Handle edge case where no valid object details were generated
    if not object_details:
         return [] 

    # 3. Select the object with the maximum density
    # The `max` function with a lambda key finds the dict with the highest 'density' value
    target_object = max(object_details, key=lambda x: x['density'])

    # 4. Extract the subgrid corresponding to the target object's bounding box
    min_r, max_r, min_c, max_c = target_object['bbox']
    output_grid = []
    # Iterate through the rows of the bounding box
    for r in range(min_r, max_r + 1):
        # Append the slice of the row corresponding to the bounding box columns
        output_grid.append(input_grid[r][min_c : max_c + 1])

    return output_grid
```
