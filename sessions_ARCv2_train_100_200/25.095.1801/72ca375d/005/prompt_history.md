
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
```python
import numpy as np
from collections import deque
import math

"""
Identify all distinct connected non-zero objects in the input grid.
For each object, determine its bounding box, cell count, bounding box area, density (cell count / area), and the count of unique digits (including 0) within its bounding box.
Find the minimum count of unique digits found across all object bounding boxes.
Select all objects whose bounding box contains this minimum number of unique digits.
If only one object is selected, this is the target object.
If multiple objects are selected (tie in minimum unique digits):
  Calculate the absolute difference between each tied object's density and 0.75.
  Select the object(s) from this tied set whose density difference from 0.75 is the smallest.
If there is still a tie (multiple objects have the same minimum density difference):
  Select the object among these tied objects that has the largest bounding box area. (If still tied, the first one encountered is chosen).
Extract the rectangular region from the input grid defined by the bounding box of the finally selected object. This extracted region is the output grid.
"""

def _find_objects(grid: np.ndarray) -> list[dict]:
    """
    Finds all connected components of non-zero digits using Breadth-First Search (BFS).
    
    Args:
        grid: A NumPy array representing the input grid.

    Returns:
        A list of dictionaries, where each dictionary represents an object
        and contains its 'digit' and a list of its 'cells' (coordinates).
        Example: [{'digit': 4, 'cells': [(1, 2), (1, 3), (2, 2), (2, 3)]}, ...]
    """
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
                    
                    # Add neighbors to the queue (4-connectivity)
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = curr_r + dr, curr_c + dc
                        # Check bounds before adding to queue to avoid unnecessary checks later
                        if 0 <= nr < rows and 0 <= nc < cols and (nr, nc) not in visited:
                             q.append((nr, nc))

                if object_cells:
                     objects.append({'digit': digit, 'cells': object_cells})
                     
    return objects

def _calculate_properties(obj: dict, grid: np.ndarray) -> dict:
    """
    Calculates bounding box, area, cell count, density, and unique digit count 
    within the bounding box for a given object.

    Args:
        obj: A dictionary representing an object {'digit': ..., 'cells': ...}.
        grid: The full input NumPy array.

    Returns:
        The input object dictionary updated with calculated properties:
        'min_row', 'max_row', 'min_col', 'max_col', 'cell_count', 
        'bbox_area', 'density', 'unique_digits_in_bbox'.
        Returns None for properties if the object has no cells.
    """
    if not obj['cells']:
        # Should not happen with _find_objects logic, but safeguard
        return {**obj, 'min_row': -1, 'max_row': -1, 'min_col': -1, 'max_col': -1, 
                'cell_count': 0, 'bbox_area': 0, 'density': 0.0, 'unique_digits_in_bbox': 0}

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
        
    # Count unique digits within the bounding box
    bbox_subgrid = grid[min_row : max_row + 1, min_col : max_col + 1]
    unique_digits_in_bbox = len(np.unique(bbox_subgrid))
        
    return {
        **obj,
        'min_row': min_row,
        'max_row': max_row,
        'min_col': min_col,
        'max_col': max_col,
        'cell_count': cell_count,
        'bbox_area': bbox_area,
        'density': density,
        'unique_digits_in_bbox': unique_digits_in_bbox
    }

def transform(input_grid: list[list[int]]) -> list[list[int]]:  
    """
    Identifies non-zero objects, calculates properties including the number of unique
    digits within each object's bounding box. Selects the object based on minimizing 
    this unique digit count. Ties are broken by selecting the object whose density 
    is closest to 0.75. Further ties are broken by selecting the object with the 
    largest bounding box area. Finally, returns the subgrid corresponding to the 
    selected object's bounding box.
    """
    
    # Convert input to numpy array for easier manipulation
    grid_np = np.array(input_grid, dtype=int)
    
    # 1. Identify all distinct connected non-zero objects
    objects_raw = _find_objects(grid_np)
    
    # Handle case with no objects found
    if not objects_raw:
        return [] 

    # 2. Calculate properties for each object
    objects_with_props = [_calculate_properties(obj, grid_np) for obj in objects_raw]

    # 3. Find the minimum count of unique digits in bounding boxes
    min_unique_digits = min(obj['unique_digits_in_bbox'] for obj in objects_with_props)

    # 4. Filter objects by minimum unique digit count (Primary Candidates)
    primary_candidates = [obj for obj in objects_with_props if obj['unique_digits_in_bbox'] == min_unique_digits]
    
    # 5. Select the object based on tie-breaking rules
    selected_object = None
    if len(primary_candidates) == 1:
        # 5a. No tie in unique digits
        selected_object = primary_candidates[0]
    elif len(primary_candidates) > 1:
        # 5b. Tie in unique digits - use density proximity to 0.75
        target_density = 0.75
        min_density_diff = float('inf')
        for obj in primary_candidates:
            diff = abs(obj['density'] - target_density)
            min_density_diff = min(min_density_diff, diff)
        
        # Filter based on minimum density difference (Secondary Candidates)
        secondary_candidates = [obj for obj in primary_candidates if abs(obj['density'] - target_density) == min_density_diff]

        if len(secondary_candidates) == 1:
            # 5c. Tie broken by density proximity
            selected_object = secondary_candidates[0]
        elif len(secondary_candidates) > 1:
             # 5d. Tie in density proximity - use max bounding box area
             max_bbox_area = max(obj['bbox_area'] for obj in secondary_candidates)
             # Use next() to get the first object matching the max area in case of final ties
             selected_object = next(obj for obj in secondary_candidates if obj['bbox_area'] == max_bbox_area)
        else: # Should not happen if primary_candidates was > 1
             selected_object = primary_candidates[0] # Fallback: pick first primary candidate
             
    else: # Should not happen if objects_raw was not empty
        return []
        
    # Ensure an object was selected (mainly for robustness)
    if selected_object is None:
         return [] 

    # 6. Extract the subgrid based on the selected object's bounding box
    min_r, max_r = selected_object['min_row'], selected_object['max_row']
    min_c, max_c = selected_object['min_col'], selected_object['max_col']
    
    output_np = grid_np[min_r : max_r + 1, min_c : max_c + 1]
    
    # Convert output numpy array back to list of lists
    output_grid = output_np.tolist()

    return output_grid
```

Previous Code:
```python
import numpy as np
from collections import deque
import math

"""
Identify all distinct connected non-zero objects in the input grid.
For each object, determine its bounding box, cell count, bounding box area, density (cell count / area), and the count of unique digits (including 0) within its bounding box.
Find the minimum count of unique digits found across all object bounding boxes.
Select all objects whose bounding box contains this minimum number of unique digits.
If only one object is selected, this is the target object.
If multiple objects are selected (tie in minimum unique digits):
  Calculate the absolute difference between each tied object's density and 0.75.
  Select the object(s) from this tied set whose density difference from 0.75 is the smallest.
If there is still a tie (multiple objects have the same minimum density difference):
  Select the object among these tied objects that has the largest bounding box area. (If still tied, the first one encountered is chosen).
Extract the rectangular region from the input grid defined by the bounding box of the finally selected object. This extracted region is the output grid.
"""

def _find_objects(grid: np.ndarray) -> list[dict]:
    """
    Finds all connected components of non-zero digits using Breadth-First Search (BFS).
    
    Args:
        grid: A NumPy array representing the input grid.

    Returns:
        A list of dictionaries, where each dictionary represents an object
        and contains its 'digit' and a list of its 'cells' (coordinates).
        Example: [{'digit': 4, 'cells': [(1, 2), (1, 3), (2, 2), (2, 3)]}, ...]
    """
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
                    
                    # Add neighbors to the queue (4-connectivity)
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = curr_r + dr, curr_c + dc
                        # Check bounds before adding to queue to avoid unnecessary checks later
                        if 0 <= nr < rows and 0 <= nc < cols and (nr, nc) not in visited:
                             q.append((nr, nc))

                if object_cells:
                     objects.append({'digit': digit, 'cells': object_cells})
                     
    return objects

def _calculate_properties(obj: dict, grid: np.ndarray) -> dict:
    """
    Calculates bounding box, area, cell count, density, and unique digit count 
    within the bounding box for a given object.

    Args:
        obj: A dictionary representing an object {'digit': ..., 'cells': ...}.
        grid: The full input NumPy array.

    Returns:
        The input object dictionary updated with calculated properties:
        'min_row', 'max_row', 'min_col', 'max_col', 'cell_count', 
        'bbox_area', 'density', 'unique_digits_in_bbox'.
        Returns None for properties if the object has no cells.
    """
    if not obj['cells']:
        # Should not happen with _find_objects logic, but safeguard
        return {**obj, 'min_row': -1, 'max_row': -1, 'min_col': -1, 'max_col': -1, 
                'cell_count': 0, 'bbox_area': 0, 'density': 0.0, 'unique_digits_in_bbox': 0}

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
        
    # Count unique digits within the bounding box
    bbox_subgrid = grid[min_row : max_row + 1, min_col : max_col + 1]
    unique_digits_in_bbox = len(np.unique(bbox_subgrid))
        
    return {
        **obj,
        'min_row': min_row,
        'max_row': max_row,
        'min_col': min_col,
        'max_col': max_col,
        'cell_count': cell_count,
        'bbox_area': bbox_area,
        'density': density,
        'unique_digits_in_bbox': unique_digits_in_bbox
    }

def transform(input_grid: list[list[int]]) -> list[list[int]]:  
    """
    Identifies non-zero objects, calculates properties including the number of unique
    digits within each object's bounding box. Selects the object based on minimizing 
    this unique digit count. Ties are broken by selecting the object whose density 
    is closest to 0.75. Further ties are broken by selecting the object with the 
    largest bounding box area. Finally, returns the subgrid corresponding to the 
    selected object's bounding box.
    """
    
    # Convert input to numpy array for easier manipulation
    grid_np = np.array(input_grid, dtype=int)
    
    # 1. Identify all distinct connected non-zero objects
    objects_raw = _find_objects(grid_np)
    
    # Handle case with no objects found
    if not objects_raw:
        return [] 

    # 2. Calculate properties for each object
    objects_with_props = [_calculate_properties(obj, grid_np) for obj in objects_raw]

    # 3. Find the minimum count of unique digits in bounding boxes
    min_unique_digits = min(obj['unique_digits_in_bbox'] for obj in objects_with_props)

    # 4. Filter objects by minimum unique digit count (Primary Candidates)
    primary_candidates = [obj for obj in objects_with_props if obj['unique_digits_in_bbox'] == min_unique_digits]
    
    # 5. Select the object based on tie-breaking rules
    selected_object = None
    if len(primary_candidates) == 1:
        # 5a. No tie in unique digits
        selected_object = primary_candidates[0]
    elif len(primary_candidates) > 1:
        # 5b. Tie in unique digits - use density proximity to 0.75
        target_density = 0.75
        min_density_diff = float('inf')
        for obj in primary_candidates:
            diff = abs(obj['density'] - target_density)
            min_density_diff = min(min_density_diff, diff)
        
        # Filter based on minimum density difference (Secondary Candidates)
        secondary_candidates = [obj for obj in primary_candidates if abs(obj['density'] - target_density) == min_density_diff]

        if len(secondary_candidates) == 1:
            # 5c. Tie broken by density proximity
            selected_object = secondary_candidates[0]
        elif len(secondary_candidates) > 1:
             # 5d. Tie in density proximity - use max bounding box area
             max_bbox_area = max(obj['bbox_area'] for obj in secondary_candidates)
             # Use next() to get the first object matching the max area in case of final ties
             selected_object = next(obj for obj in secondary_candidates if obj['bbox_area'] == max_bbox_area)
        else: # Should not happen if primary_candidates was > 1
             selected_object = primary_candidates[0] # Fallback: pick first primary candidate
             
    else: # Should not happen if objects_raw was not empty
        return []
        
    # Ensure an object was selected (mainly for robustness)
    if selected_object is None:
         return [] 

    # 6. Extract the subgrid based on the selected object's bounding box
    min_r, max_r = selected_object['min_row'], selected_object['max_row']
    min_c, max_c = selected_object['min_col'], selected_object['max_col']
    
    output_np = grid_np[min_r : max_r + 1, min_c : max_c + 1]
    
    # Convert output numpy array back to list of lists
    output_grid = output_np.tolist()

    return output_grid
```
Results for code_00.py:

Train Set Results:

## Example 1:
Input:
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
Expected Output:
```
4 4
4 4
```
Transformed Output:
```
4 4
4 4
```
Match: True
Pixels Off: 0
Size Correct: True
Color Palette Correct: True
Color Count Correct: True
Score: 0.0

## Example 2:
Input:
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
Expected Output:
```
6 6 6 6
0 6 6 0
```
Transformed Output:
```
7
```
Match: False
Pixels Off: None
Size Correct: False
Color Palette Correct: False
Color Count Correct: False
Score: None

## Example 3:
Input:
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
Expected Output:
```
5 0 0 5
5 5 5 5
```
Transformed Output:
```
5 0 0 5
5 5 5 5
```
Match: True
Pixels Off: 0
Size Correct: True
Color Palette Correct: True
Color Count Correct: True
Score: 0.0
**General Assessment:**

The initial code (`code_00.py` based on the second provided logic: min unique digits -> min density diff -> max area) successfully solved Examples 1 and 3 but failed on Example 2 according to the provided results. However, a manual walkthrough of that code's logic suggests it *should* have selected the correct object (Object 6) for Example 2. There appears to be a discrepancy between the reported execution result for Example 2 (`7`) and the expected behavior of the provided `code_00.py`.

Assuming the *expected outputs* for all examples are the ground truth, the previous hypotheses (max density -> max area; min unique digits -> min density diff -> max area) are incorrect as they fail on at least one example when checked against the expected outputs.

A new hypothesis is needed. By analyzing the relationship between the input objects and the expected output object across all three examples, a pattern emerges: the selected object consistently corresponds to the *median* digit value among all unique object digits present in the input grid.

**Strategy:**

1.  Identify all distinct connected non-zero objects and their corresponding digit values.
2.  Determine the unique set of these digit values.
3.  Calculate the median of this unique set of digits.
4.  Select the object whose digit matches the calculated median.
5.  Extract the bounding box of this selected object as the output.

This strategy successfully explains all three training examples.

**Metrics:**


*code_execution:*
```python
import numpy as np
from collections import deque

# --- Helper functions ---
def _find_objects(grid: np.ndarray) -> list[dict]:
    rows, cols = grid.shape
    visited = set()
    objects = []
    for r in range(rows):
        for c in range(cols):
            if grid[r, c] != 0 and (r, c) not in visited:
                digit = grid[r, c]
                object_cells = []
                q = deque([(r, c)])
                visited.add((r, c)) # Mark starting cell visited
                while q:
                    curr_r, curr_c = q.popleft()
                    object_cells.append((curr_r, curr_c))
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = curr_r + dr, curr_c + dc
                        if 0 <= nr < rows and 0 <= nc < cols and \
                           grid[nr, nc] == digit and (nr, nc) not in visited:
                            visited.add((nr, nc))
                            q.append((nr, nc))
                if object_cells:
                    rows_obj = [row for row, col in object_cells]
                    cols_obj = [col for row, col in object_cells]
                    min_row, max_row = min(rows_obj), max(rows_obj)
                    min_col, max_col = min(cols_obj), max(cols_obj)
                    bbox_subgrid = grid[min_row : max_row + 1, min_col : max_col + 1]
                    objects.append({
                        'digit': digit, 
                        'cell_count': len(object_cells),
                        'bbox': [min_row, max_row, min_col, max_col],
                        'bbox_area': (max_row - min_row + 1) * (max_col - min_col + 1),
                        'unique_digits_in_bbox': len(np.unique(bbox_subgrid))
                    })
    return objects

def calculate_median(digits: list[int]) -> float | int | None:
    n = len(digits)
    if n == 0: return None
    sorted_digits = sorted(digits)
    mid = n // 2
    if n % 2 == 1: return sorted_digits[mid]
    else: return (sorted_digits[mid - 1] + sorted_digits[mid]) / 2

# --- Example Data ---
inputs = [
    np.array([[0,0,0,0,0,0,0,0,0,0],[0,0,4,4,0,0,0,0,0,0],[0,0,4,4,0,0,8,8,8,0],[0,0,0,0,0,0,8,0,8,8],[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,2,2,2,2,0,0,0,0],[0,2,2,2,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0]], dtype=int),
    np.array([[0,0,0,0,0,0,0,0,0,0],[0,2,2,0,0,0,0,0,0,0],[0,0,2,2,2,0,0,7,7,0],[0,0,0,0,0,0,7,0,7,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,6,6,6,6,0,0,0],[0,0,0,0,6,6,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0]], dtype=int),
    np.array([[0,0,0,0,0,0,0,0,0,0],[0,3,3,0,0,0,0,0,0,0],[0,0,3,0,0,5,0,0,5,0],[0,0,3,0,0,5,5,5,5,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,8,8,8,0,0,0,0],[8,8,8,8,0,8,8,0,0,0],[0,0,0,0,0,0,0,0,0,0]], dtype=int)
]
expected_outputs = [
    [[4, 4], [4, 4]],
    [[6, 6, 6, 6], [0, 6, 6, 0]],
    [[5, 0, 0, 5], [5, 5, 5, 5]]
]

# --- Calculations & Report ---
print("Example Analysis:")
for i, grid in enumerate(inputs):
    print(f"\n--- Example {i+1} ---")
    objects = _find_objects(grid)
    unique_digits = sorted(list(set(obj['digit'] for obj in objects)))
    median_digit = calculate_median(unique_digits)
    print(f"  Objects Found: {len(objects)}")
    print(f"  Unique Object Digits: {unique_digits}")
    print(f"  Median Digit: {median_digit}")
    
    selected_object = None
    for obj in objects:
        obj['density'] = obj['cell_count'] / obj['bbox_area'] if obj['bbox_area'] > 0 else 0
        print(f"    - Object Digit: {obj['digit']}, Cells: {obj['cell_count']}, BBox: {obj['bbox']}, Area: {obj['bbox_area']}, Density: {obj['density']:.3f}, UniqueDigitsInBox: {obj['unique_digits_in_bbox']}")
        if obj['digit'] == median_digit:
            selected_object = obj
            
    print(f"  Selected Object Digit (based on median): {selected_object['digit'] if selected_object else 'None'}")
    
    # Verify selected object's bounding box matches expected output shape
    if selected_object:
        min_r, max_r, min_c, max_c = selected_object['bbox']
        output_shape = (max_r - min_r + 1, max_c - min_c + 1)
        expected_shape = (len(expected_outputs[i]), len(expected_outputs[i][0]))
        print(f"  Selected Object BBox Shape: {output_shape}")
        print(f"  Expected Output Shape: {expected_shape}")
        print(f"  Shape Match: {output_shape == expected_shape}")
    else:
        print("  No object selected based on median digit.")


```

*code_execution_result:*
outcome: OUTCOME_OK
```
Example Analysis:

--- Example 1 ---
  Objects Found: 3
  Unique Object Digits: [np.int64(2), np.int64(4), np.int64(8)]
  Median Digit: 4
    - Object Digit: 4, Cells: 4, BBox: [1, 2, 2, 3], Area: 4, Density: 1.000, UniqueDigitsInBox: 1
    - Object Digit: 8, Cells: 6, BBox: [2, 3, 6, 9], Area: 8, Density: 0.750, UniqueDigitsInBox: 2
    - Object Digit: 2, Cells: 7, BBox: [7, 8, 1, 5], Area: 10, Density: 0.700, UniqueDigitsInBox: 2
  Selected Object Digit (based on median): 4
  Selected Object BBox Shape: (2, 2)
  Expected Output Shape: (2, 2)
  Shape Match: True

--- Example 2 ---
  Objects Found: 4
  Unique Object Digits: [np.int64(2), np.int64(6), np.int64(7)]
  Median Digit: 6
    - Object Digit: 2, Cells: 5, BBox: [1, 2, 1, 4], Area: 8, Density: 0.625, UniqueDigitsInBox: 2
    - Object Digit: 7, Cells: 3, BBox: [2, 3, 7, 8], Area: 4, Density: 0.750, UniqueDigitsInBox: 2
    - Object Digit: 7, Cells: 1, BBox: [3, 3, 6, 6], Area: 1, Density: 1.000, UniqueDigitsInBox: 1
    - Object Digit: 6, Cells: 6, BBox: [6, 7, 3, 6], Area: 8, Density: 0.750, UniqueDigitsInBox: 2
  Selected Object Digit (based on median): 6
  Selected Object BBox Shape: (2, 4)
  Expected Output Shape: (2, 4)
  Shape Match: True

--- Example 3 ---
  Objects Found: 3
  Unique Object Digits: [np.int64(3), np.int64(5), np.int64(8)]
  Median Digit: 5
    - Object Digit: 3, Cells: 4, BBox: [1, 3, 1, 2], Area: 6, Density: 0.667, UniqueDigitsInBox: 2
    - Object Digit: 5, Cells: 6, BBox: [2, 3, 5, 8], Area: 8, Density: 0.750, UniqueDigitsInBox: 2
    - Object Digit: 8, Cells: 9, BBox: [7, 8, 0, 6], Area: 14, Density: 0.643, UniqueDigitsInBox: 2
  Selected Object Digit (based on median): 5
  Selected Object BBox Shape: (2, 4)
  Expected Output Shape: (2, 4)
  Shape Match: True

```
**YAML Facts:**


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
      - bounding_box: The smallest rectangle containing all object cells [min_row, max_row, min_col, max_col].
  - element: unique_object_digits
    description: The set of unique digit values present across all non_zero_objects in the input grid.
    properties:
      - count: Number of unique digits.
      - values: List of the unique digits.
  - element: median_digit
    description: The median value calculated from the sorted list of unique_object_digits.
    constraints:
      - Assumes an odd number of unique_object_digits based on examples.
  - element: selected_object
    description: The non_zero_object whose digit_value matches the median_digit.
    constraints:
      - Assumes only one object will match the median_digit based on examples.
  - element: output_grid
    description: A rectangular subgrid extracted from the input grid.
    properties:
      - content: Matches the content within the bounding_box of the selected_object.
      - dimensions: Determined by the bounding box size of the selected_object.

transformation:
  input: input_grid
  output: output_grid
  steps:
    - action: identify_objects
      description: Find all distinct connected non-zero objects and their digit values in the input grid.
      input: input_grid
      output: list_of_objects
    - action: find_unique_digits
      description: Create a sorted list of unique digit values from all identified objects.
      input: list_of_objects
      output: unique_object_digits_list
    - action: calculate_median_digit
      description: Calculate the median value from the unique_object_digits_list.
      input: unique_object_digits_list
      output: median_digit_value
    - action: select_object_by_median
      description: Identify the object from list_of_objects whose digit_value equals the median_digit_value.
      input: list_of_objects, median_digit_value
      output: selected_object
    - action: determine_bounding_box
      description: Find the bounding box coordinates of the selected_object.
      input: selected_object
      output: bounding_box_coords
    - action: extract_subgrid
      description: Extract the subgrid from the input_grid corresponding to the bounding_box_coords.
      input: input_grid, bounding_box_coords
      output: output_grid

relationships:
  - The output_grid's content and dimensions are determined by the bounding_box of the selected_object.
  - The selected_object is chosen based on its digit_value matching the median of all unique object digit values in the input grid.
```


**Natural Language Program:**

1.  Identify all distinct connected groups (objects) of the same non-zero digit within the input grid.
2.  Create a list containing the unique digit value associated with each distinct object found.
3.  Sort this list of unique digit values in ascending order.
4.  Determine the median value from this sorted list. (For a list with an odd number of elements, this is the middle element).
5.  Find the specific object identified in step 1 whose digit value is equal to the calculated median value.
6.  Determine the bounding box (minimum and maximum row and column indices) of this selected object.
7.  Extract the rectangular subgrid from the original input grid defined by this bounding box. This subgrid is the final output.
