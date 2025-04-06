
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

*   **Perception:** The task involves processing a 10x10 grid containing several distinct "objects" composed of non-zero digits against a background of zeros. The goal is to identify a specific object based on certain properties and extract its bounding box as the output grid.

*   **YAML Facts:**
    
```yaml
    task_elements:
      - element: input_grid
        description: A 10x10 grid of single digits (0-9).
        properties:
          - dimensions: [10, 10]
          - background_digit: 0
          - contains: non_zero_objects
      - element: non_zero_objects
        description: Connected components of identical non-zero digits.
        properties:
          - digit_value: The digit making up the object (1-9).
          - cells: List of coordinates [(row, col), ...] occupied by the object.
          - cell_count: Number of cells in the object.
          - bounding_box: The smallest rectangle containing all object cells [min_row, max_row, min_col, max_col].
          - bbox_area: The area of the bounding box ((max_row - min_row + 1) * (max_col - min_col + 1)).
          - density: Ratio of cell_count to bbox_area.
      - element: output_grid
        description: A rectangular subgrid extracted from the input grid.
        properties:
          - content: Matches the content within the bounding box of a selected non_zero_object from the input.
          - dimensions: Determined by the bounding box size of the selected object.

    transformation:
      input: input_grid
      output: output_grid
      steps:
        - action: identify_objects
          description: Find all distinct connected non-zero objects in the input grid.
          input: input_grid
          output: list_of_objects_with_properties
        - action: calculate_properties
          description: For each object, calculate its cell_count, bounding_box, bbox_area, and density.
          input: list_of_objects_with_properties
          output: list_of_objects_with_calculated_properties
        - action: find_max_density
          description: Determine the maximum density value among all objects.
          input: list_of_objects_with_calculated_properties
          output: max_density_value
        - action: filter_by_max_density
          description: Identify all objects having the maximum density.
          input: list_of_objects_with_calculated_properties, max_density_value
          output: candidate_objects
        - action: select_object
          description: >
            If only one candidate object exists, select it.
            If multiple candidate objects exist (tie in density), select the one with the largest bounding box area among them.
          input: candidate_objects
          output: selected_object
        - action: extract_subgrid
          description: Extract the subgrid from the input_grid corresponding to the bounding_box of the selected_object.
          input: input_grid, selected_object.bounding_box
          output: output_grid

    relationships:
      - The output_grid's content and dimensions are directly derived from the bounding box of the selected_object.
      - The selected_object is chosen based on maximizing density, with bounding box area used as a tie-breaker.
    ```


*   **Natural Language Program:**
    1.  Identify all distinct connected groups (objects) of non-zero digits in the input grid.
    2.  For each identified object:
        a.  Determine its bounding box (the smallest rectangle enclosing the object).
        b.  Calculate the area of the bounding box.
        c.  Count the number of cells occupied by the object.
        d.  Calculate the object's density by dividing its cell count by its bounding box area.
    3.  Find the maximum density value among all calculated densities.
    4.  Select all objects that have this maximum density.
    5.  If only one object has the maximum density, choose this object.
    6.  If multiple objects share the maximum density, choose the object among them that has the largest bounding box area.
    7.  Extract the rectangular region from the input grid defined by the bounding box of the chosen object. This extracted region is the output grid.
```python
import numpy as np
from collections import deque

"""
1.  Identify all distinct connected groups (objects) of non-zero digits in the input grid.
2.  For each identified object:
    a.  Determine its bounding box (the smallest rectangle enclosing the object).
    b.  Calculate the area of the bounding box.
    c.  Count the number of cells occupied by the object.
    d.  Calculate the object's density by dividing its cell count by its bounding box area.
3.  Find the maximum density value among all calculated densities.
4.  Select all objects that have this maximum density.
5.  If only one object has the maximum density, choose this object.
6.  If multiple objects share the maximum density, choose the object among them that has the largest bounding box area.
7.  Extract the rectangular region from the input grid defined by the bounding box of the chosen object. This extracted region is the output grid.
"""

def _find_objects(grid: np.ndarray) -> list[dict]:
    """Finds all connected components of non-zero digits."""
    rows, cols = grid.shape
    visited = set()
    objects = []
    
    for r in range(rows):
        for c in range(cols):
            # If the cell is non-zero and not visited, start a search (BFS)
            if grid[r, c] != 0 and (r, c) not in visited:
                digit = grid[r, c]
                object_cells = []
                q = deque([(r, c)])
                
                while q:
                    curr_r, curr_c = q.popleft()
                    
                    # Check bounds and if already visited or not the correct digit
                    if not (0 <= curr_r < rows and 0 <= curr_c < cols) or \
                       (curr_r, curr_c) in visited or \
                       grid[curr_r, curr_c] != digit:
                        continue
                        
                    visited.add((curr_r, curr_c))
                    object_cells.append((curr_r, curr_c))
                    
                    # Add neighbors to the queue
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = curr_r + dr, curr_c + dc
                        if (nr, nc) not in visited : # Optimization: only add if not visited
                             q.append((nr, nc))

                if object_cells:
                     objects.append({'digit': digit, 'cells': object_cells})
                     
    return objects

def _calculate_properties(obj: dict) -> dict:
    """Calculates bounding box, area, cell count, and density for an object."""
    if not obj['cells']:
        return {**obj, 'min_row': -1, 'max_row': -1, 'min_col': -1, 'max_col': -1, 
                'cell_count': 0, 'bbox_area': 0, 'density': 0.0}

    rows = [r for r, c in obj['cells']]
    cols = [c for r, c in obj['cells']]
    
    min_row, max_row = min(rows), max(rows)
    min_col, max_col = min(cols), max(cols)
    
    cell_count = len(obj['cells'])
    bbox_height = max_row - min_row + 1
    bbox_width = max_col - min_col + 1
    bbox_area = bbox_height * bbox_width
    
    density = 0.0
    if bbox_area > 0:
        density = cell_count / bbox_area
        
    return {
        **obj,
        'min_row': min_row,
        'max_row': max_row,
        'min_col': min_col,
        'max_col': max_col,
        'cell_count': cell_count,
        'bbox_area': bbox_area,
        'density': density
    }


def transform(input_grid: list[list[int]]) -> list[list[int]]:  
    """
    Identifies non-zero objects in the grid, calculates their density 
    (cell count / bounding box area), selects the object with the highest 
    density (using largest bounding box area as a tie-breaker), and returns 
    the subgrid corresponding to that object's bounding box.
    """
    
    # Convert input to numpy array for easier manipulation
    grid_np = np.array(input_grid, dtype=int)
    
    # 1. Identify all distinct connected non-zero objects
    objects_raw = _find_objects(grid_np)
    
    if not objects_raw:
        # Handle case with no objects found (e.g., all zeros grid)
        return [] 

    # 2. Calculate properties for each object
    objects_with_props = [_calculate_properties(obj) for obj in objects_raw]

    # 3. Find the maximum density
    max_density = 0.0
    if objects_with_props:
         max_density = max(obj['density'] for obj in objects_with_props)

    # 4. Filter objects by maximum density
    max_density_objects = [obj for obj in objects_with_props if obj['density'] == max_density]
    
    # 5. & 6. Select the object (handle ties with max bbox area)
    selected_object = None
    if len(max_density_objects) == 1:
        selected_object = max_density_objects[0]
    elif len(max_density_objects) > 1:
        max_bbox_area = max(obj['bbox_area'] for obj in max_density_objects)
        # In case of a tie in both density and area, just pick the first one.
        # The problem description doesn't specify further tie-breaking.
        selected_object = next(obj for obj in max_density_objects if obj['bbox_area'] == max_bbox_area)
        
    if selected_object is None:
         # Should not happen if there were initial objects, but safeguard
         return [] 

    # 7. Extract the subgrid based on the selected object's bounding box
    min_r, max_r = selected_object['min_row'], selected_object['max_row']
    min_c, max_c = selected_object['min_col'], selected_object['max_col']
    
    output_np = grid_np[min_r : max_r + 1, min_c : max_c + 1]
    
    # Convert output numpy array back to list of lists
    output_grid = output_np.tolist()

    return output_grid
```
