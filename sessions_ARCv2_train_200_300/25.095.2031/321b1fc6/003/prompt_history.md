
## train_1

**input:**
```
0 0 0 0 0 0 0 0 0 0
0 8 8 0 0 0 0 0 0 0
0 8 8 8 0 0 8 8 0 0
0 0 0 0 0 0 8 8 8 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 7 7 0 0 0
0 0 0 0 0 6 6 6 0 0
0 0 0 8 8 0 0 0 0 0
0 0 0 8 8 8 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0
0 7 7 0 0 0 0 0 0 0
0 6 6 6 0 0 7 7 0 0
0 0 0 0 0 0 6 6 6 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 7 7 0 0 0 0 0
0 0 0 6 6 6 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```


## train_2

**input:**
```
0 0 0 0 0 0 0 0 0 0
0 7 6 0 0 0 0 0 0 0
0 9 4 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 8 8 0 0 0
0 0 0 0 0 8 8 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 8 8 0 0 0 0 0 0
0 0 8 8 0 0 0 0 8 8
0 0 0 0 0 0 0 0 8 8
```


**output:**
```
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 7 6 0 0 0
0 0 0 0 0 9 4 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 7 6 0 0 0 0 0 0
0 0 9 4 0 0 0 0 7 6
0 0 0 0 0 0 0 0 9 4
```

Okay, let's analyze the transformation.

**Perception of Elements:**

1.  **Input/Output Structure:** Both input and output are 2D grids (10x10) containing single digits (0-9).
2.  **Key Digit:** The digit '8' seems to play a special role in the input. Objects composed solely of '8' are targets for transformation.
3.  **Pattern Digits:** Other non-zero digits (like '6', '7', '9', '4' in the examples) form distinct shapes or "patterns" in the input.
4.  **Background:** The digit '0' represents the empty background.
5.  **Objects:** Connected components of non-zero digits form distinct objects within the grid. We can differentiate between "target objects" (made of '8') and "pattern objects" (made of other non-zero digits).
6.  **Transformation:** The core transformation involves replacing each "target object" ('8' shape) with one of the "pattern objects". The original "pattern objects" are removed from their initial positions.
7.  **Replacement Logic:**
    *   Multiple '8' objects and potentially multiple pattern objects can exist.
    *   The '8' objects appear to be processed in a specific order (likely top-to-bottom, then left-to-right based on their top-left corner).
    *   The available pattern objects also seem to have an order (likely top-to-bottom, then left-to-right based on their top-left corner).
    *   The replacement cycles through the available pattern objects. For instance, if there are two patterns (P1, P2) and four target objects (T1, T2, T3, T4) ordered by position, the replacements would be T1->P1, T2->P2, T3->P1, T4->P2.
8.  **Placement:** When a target object is replaced by a pattern object, the pattern object is placed such that its top-left corner aligns with the top-left corner of the bounding box of the original target object. The internal structure and digit values of the pattern object are preserved in the copy.

**YAML Facts:**


```yaml
Grid_Properties:
  - Type: 2D Array
  - Dimensions: 10x10
  - Cell_Values: Integers (0-9)
  - Background_Value: 0

Object_Types:
  - Target_Object:
      - Definition: Connected component of non-zero cells.
      - Property: All cells have the value 8.
      - Role: Is replaced during transformation.
  - Pattern_Object:
      - Definition: Connected component of non-zero cells.
      - Property: Contains cell values other than 0 or 8.
      - Role: Serves as a template for replacing Target_Objects. Original instance is removed.

Relationships_and_Actions:
  - Identification:
      - Identify all distinct connected components (objects) of non-zero cells in the input grid.
      - Categorize objects into Target_Objects and Pattern_Objects.
  - Ordering:
      - Order Pattern_Objects based on their top-most, then left-most cell coordinate.
      - Order Target_Objects based on their top-most, then left-most cell coordinate.
  - Transformation:
      - Create an empty output grid (all zeros).
      - Iterate through the ordered Target_Objects.
      - For each Target_Object, select the next Pattern_Object from the ordered list (cycling through if necessary).
      - Determine the top-left coordinate of the Target_Object's bounding box.
      - Copy the selected Pattern_Object's structure and cell values onto the output grid, aligning the pattern's top-left corner with the target's top-left coordinate.
  - Removal:
      - Original Pattern_Objects are not copied to the output grid at their original locations.

Connectivity:
  - Assume 8-way connectivity (including diagonals) for defining connected components.
```


**Natural Language Program:**

1.  Initialize an empty output grid with the same dimensions as the input grid, filled with zeros.
2.  Scan the input grid to identify all distinct connected components (objects) formed by non-zero digits, using 8-way connectivity.
3.  Separate these objects into two lists: `target_objects` (those composed entirely of the digit 8) and `pattern_objects` (those containing digits other than 0 and 8).
4.  If there are no `pattern_objects`, return the empty output grid.
5.  Sort the `pattern_objects` list based on the row index of their top-most cell, breaking ties using the column index of their left-most cell.
6.  Sort the `target_objects` list using the same sorting criteria (top-most row, then left-most column).
7.  Iterate through the sorted `target_objects` list, keeping track of the index `i` (starting from 0).
8.  For each `target_object` at index `i`:
    a.  Select the `pattern_object` from the sorted list at index `j = i % number_of_pattern_objects`.
    b.  Determine the minimum row (`target_min_row`) and minimum column (`target_min_col`) coordinates occupied by the current `target_object`.
    c.  Determine the minimum row (`pattern_min_row`) and minimum column (`pattern_min_col`) coordinates occupied by the selected `pattern_object`.
    d.  For each cell `(r, c)` within the selected `pattern_object` having a value `v`:
        i.  Calculate its relative position within the pattern: `rel_row = r - pattern_min_row`, `rel_col = c - pattern_min_col`.
        ii. Calculate the corresponding position in the output grid: `output_row = target_min_row + rel_row`, `output_col = target_min_col + rel_col`.
        iii. If `output_row` and `output_col` are within the grid boundaries, set the cell `(output_row, output_col)` in the output grid to the value `v`.
9.  Return the final output grid.
```python
import numpy as np
from scipy.ndimage import label, find_objects

"""
Transforms an input grid based on the following rules:
1. Identify connected components (objects) of non-zero cells using 8-way connectivity.
2. Categorize objects into 'target_objects' (composed entirely of the digit 8) and 'pattern_objects' (composed of other non-zero digits).
3. Sort both target_objects and pattern_objects based on their top-most, then left-most cell coordinate.
4. If no pattern_objects exist, return an empty grid.
5. Initialize an empty output grid (all zeros).
6. Iterate through the sorted target_objects. For each target_object, select the next pattern_object from the sorted list, cycling through the patterns if necessary (using modulo arithmetic).
7. Determine the top-left corner coordinate of the current target_object.
8. Copy the selected pattern_object onto the output grid, aligning the pattern's top-left corner (relative to its own bounding box) with the target_object's top-left corner coordinate.
9. The original pattern_objects are not copied to their original locations in the output.
"""

def _find_objects(grid: np.ndarray) -> tuple[list[dict], list[dict]]:
    """
    Finds and categorizes connected components in the grid.

    Args:
        grid: The input NumPy array.

    Returns:
        A tuple containing two lists: (pattern_objects, target_objects).
        Each object is represented as a dictionary with keys:
        'cells': list of (row, col, value) tuples
        'top_left': (min_row, min_col) tuple
        'is_target': boolean indicating if it's a target (all 8s) object
    """
    # Define connectivity (8-way)
    structure = np.array([[1, 1, 1],
                          [1, 1, 1],
                          [1, 1, 1]], dtype=bool)

    # Label connected components of non-zero cells
    labeled_grid, num_labels = label(grid > 0, structure=structure)
    
    # Find the locations (slices) of each labeled object
    object_slices = find_objects(labeled_grid)

    pattern_objects = []
    target_objects = []

    for i in range(num_labels):
        label_id = i + 1
        slices = object_slices[i]
        
        # Extract coordinates and values for the current object
        coords = np.argwhere(labeled_grid[slices] == label_id)
        min_row = slices[0].start
        min_col = slices[1].start
        
        obj_cells = []
        is_target_candidate = True
        
        for r_rel, c_rel in coords:
            r_abs = min_row + r_rel
            c_abs = min_col + c_rel
            value = grid[r_abs, c_abs]
            obj_cells.append((r_abs, c_abs, value))
            if value != 8:
                is_target_candidate = False
        
        # Determine actual top-left based on absolute coords
        abs_rows = [r for r, c, v in obj_cells]
        abs_cols = [c for r, c, v in obj_cells]
        obj_min_row = min(abs_rows)
        obj_min_col = min(abs_cols)
        
        obj_data = {
            'cells': obj_cells,
            'top_left': (obj_min_row, obj_min_col),
            'is_target': is_target_candidate
        }

        if is_target_candidate:
            target_objects.append(obj_data)
        else:
            # Check if it's actually a pattern (not just background 0 picked up somehow)
             if any(v != 0 for r,c,v in obj_cells):
                 pattern_objects.append(obj_data)


    # Sort objects based on top-left corner (row, then column)
    sort_key = lambda obj: obj['top_left']
    pattern_objects.sort(key=sort_key)
    target_objects.sort(key=sort_key)

    return pattern_objects, target_objects


def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Applies the transformation rule to the input grid.

    Args:
        input_grid: A list of lists representing the input grid.

    Returns:
        A list of lists representing the transformed output grid.
    """
    # Convert input to numpy array for easier processing
    grid_np = np.array(input_grid, dtype=int)
    rows, cols = grid_np.shape

    # Initialize output grid with zeros
    output_grid_np = np.zeros_like(grid_np)

    # Find and categorize pattern and target objects
    pattern_objects, target_objects = _find_objects(grid_np)

    # If there are no patterns to use for replacement, return the empty grid
    if not pattern_objects:
        return output_grid_np.tolist()

    num_patterns = len(pattern_objects)

    # Iterate through the sorted target objects and replace them with patterns
    for i, target_obj in enumerate(target_objects):
        # Select the pattern object to use, cycling through the list
        pattern_obj = pattern_objects[i % num_patterns]

        target_top_left_row, target_top_left_col = target_obj['top_left']
        pattern_origin_row, pattern_origin_col = pattern_obj['top_left']

        # Place the selected pattern onto the output grid
        for r_pat, c_pat, value in pattern_obj['cells']:
            # Calculate relative position within the pattern object
            rel_row = r_pat - pattern_origin_row
            rel_col = c_pat - pattern_origin_col

            # Calculate the destination position in the output grid
            dest_row = target_top_left_row + rel_row
            dest_col = target_top_left_col + rel_col

            # Place the pattern cell value if within grid bounds
            if 0 <= dest_row < rows and 0 <= dest_col < cols:
                output_grid_np[dest_row, dest_col] = value

    # Convert the final numpy array back to a list of lists
    return output_grid_np.tolist()
```

Previous Code:
```python
import numpy as np
from scipy.ndimage import label, find_objects

"""
Transforms an input grid based on the following rules:
1. Identify connected components (objects) of non-zero cells using 8-way connectivity.
2. Categorize objects into 'target_objects' (composed entirely of the digit 8) and 'pattern_objects' (composed of other non-zero digits).
3. Sort both target_objects and pattern_objects based on their top-most, then left-most cell coordinate.
4. If no pattern_objects exist, return an empty grid.
5. Initialize an empty output grid (all zeros).
6. Iterate through the sorted target_objects. For each target_object, select the next pattern_object from the sorted list, cycling through the patterns if necessary (using modulo arithmetic).
7. Determine the top-left corner coordinate of the current target_object.
8. Copy the selected pattern_object onto the output grid, aligning the pattern's top-left corner (relative to its own bounding box) with the target_object's top-left corner coordinate.
9. The original pattern_objects are not copied to their original locations in the output.
"""

def _find_objects(grid: np.ndarray) -> tuple[list[dict], list[dict]]:
    """
    Finds and categorizes connected components in the grid.

    Args:
        grid: The input NumPy array.

    Returns:
        A tuple containing two lists: (pattern_objects, target_objects).
        Each object is represented as a dictionary with keys:
        'cells': list of (row, col, value) tuples
        'top_left': (min_row, min_col) tuple
        'is_target': boolean indicating if it's a target (all 8s) object
    """
    # Define connectivity (8-way)
    structure = np.array([[1, 1, 1],
                          [1, 1, 1],
                          [1, 1, 1]], dtype=bool)

    # Label connected components of non-zero cells
    labeled_grid, num_labels = label(grid > 0, structure=structure)
    
    # Find the locations (slices) of each labeled object
    object_slices = find_objects(labeled_grid)

    pattern_objects = []
    target_objects = []

    for i in range(num_labels):
        label_id = i + 1
        slices = object_slices[i]
        
        # Extract coordinates and values for the current object
        coords = np.argwhere(labeled_grid[slices] == label_id)
        min_row = slices[0].start
        min_col = slices[1].start
        
        obj_cells = []
        is_target_candidate = True
        
        for r_rel, c_rel in coords:
            r_abs = min_row + r_rel
            c_abs = min_col + c_rel
            value = grid[r_abs, c_abs]
            obj_cells.append((r_abs, c_abs, value))
            if value != 8:
                is_target_candidate = False
        
        # Determine actual top-left based on absolute coords
        abs_rows = [r for r, c, v in obj_cells]
        abs_cols = [c for r, c, v in obj_cells]
        obj_min_row = min(abs_rows)
        obj_min_col = min(abs_cols)
        
        obj_data = {
            'cells': obj_cells,
            'top_left': (obj_min_row, obj_min_col),
            'is_target': is_target_candidate
        }

        if is_target_candidate:
            target_objects.append(obj_data)
        else:
            # Check if it's actually a pattern (not just background 0 picked up somehow)
             if any(v != 0 for r,c,v in obj_cells):
                 pattern_objects.append(obj_data)


    # Sort objects based on top-left corner (row, then column)
    sort_key = lambda obj: obj['top_left']
    pattern_objects.sort(key=sort_key)
    target_objects.sort(key=sort_key)

    return pattern_objects, target_objects


def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Applies the transformation rule to the input grid.

    Args:
        input_grid: A list of lists representing the input grid.

    Returns:
        A list of lists representing the transformed output grid.
    """
    # Convert input to numpy array for easier processing
    grid_np = np.array(input_grid, dtype=int)
    rows, cols = grid_np.shape

    # Initialize output grid with zeros
    output_grid_np = np.zeros_like(grid_np)

    # Find and categorize pattern and target objects
    pattern_objects, target_objects = _find_objects(grid_np)

    # If there are no patterns to use for replacement, return the empty grid
    if not pattern_objects:
        return output_grid_np.tolist()

    num_patterns = len(pattern_objects)

    # Iterate through the sorted target objects and replace them with patterns
    for i, target_obj in enumerate(target_objects):
        # Select the pattern object to use, cycling through the list
        pattern_obj = pattern_objects[i % num_patterns]

        target_top_left_row, target_top_left_col = target_obj['top_left']
        pattern_origin_row, pattern_origin_col = pattern_obj['top_left']

        # Place the selected pattern onto the output grid
        for r_pat, c_pat, value in pattern_obj['cells']:
            # Calculate relative position within the pattern object
            rel_row = r_pat - pattern_origin_row
            rel_col = c_pat - pattern_origin_col

            # Calculate the destination position in the output grid
            dest_row = target_top_left_row + rel_row
            dest_col = target_top_left_col + rel_col

            # Place the pattern cell value if within grid bounds
            if 0 <= dest_row < rows and 0 <= dest_col < cols:
                output_grid_np[dest_row, dest_col] = value

    # Convert the final numpy array back to a list of lists
    return output_grid_np.tolist()
```
Results for code_00.py:

Train Set Results:

## Example 1:
Input:
```
0 0 0 0 0 0 0 0 0 0
0 8 8 0 0 0 0 0 0 0
0 8 8 8 0 0 8 8 0 0
0 0 0 0 0 0 8 8 8 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 7 7 0 0 0
0 0 0 0 0 6 6 6 0 0
0 0 0 8 8 0 0 0 0 0
0 0 0 8 8 8 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```
Expected Output:
```
0 0 0 0 0 0 0 0 0 0
0 7 7 0 0 0 0 0 0 0
0 6 6 6 0 0 7 7 0 0
0 0 0 0 0 0 6 6 6 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 7 7 0 0 0 0 0
0 0 0 6 6 6 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```
Transformed Output:
```
0 0 0 0 0 0 0 0 0 0
0 0 0 7 7 0 0 0 0 0
0 0 0 6 6 6 0 0 7 7
0 8 8 0 0 0 0 0 6 6
0 8 8 8 0 0 8 8 0 0
0 0 0 0 0 0 8 8 8 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```
Match: False
Pixels Off: 30
Size Correct: True
Color Palette Correct: False
Color Count Correct: False
Score: 120.0

## Example 2:
Input:
```
0 0 0 0 0 0 0 0 0 0
0 7 6 0 0 0 0 0 0 0
0 9 4 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 8 8 0 0 0
0 0 0 0 0 8 8 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 8 8 0 0 0 0 0 0
0 0 8 8 0 0 0 0 8 8
0 0 0 0 0 0 0 0 8 8
```
Expected Output:
```
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 7 6 0 0 0
0 0 0 0 0 9 4 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 7 6 0 0 0 0 0 0
0 0 9 4 0 0 0 0 7 6
0 0 0 0 0 0 0 0 9 4
```
Transformed Output:
```
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 7 6 0 0 0
0 0 0 0 0 9 4 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 7 6 0 0 0 0 0 0
0 0 9 4 0 0 0 0 7 6
0 0 0 0 0 0 0 0 9 4
```
Match: True
Pixels Off: 0
Size Correct: True
Color Palette Correct: True
Color Count Correct: True
Score: 0.0
**General Assessment and Strategy**

The initial code failed on Example 1 because the object identification logic incorrectly merged distinct pattern and target objects due to the 8-way connectivity rule applied to all non-zero cells simultaneously. Example 2 succeeded because the relevant objects were sufficiently separated.

The core issue lies in the definition and identification of objects. The connectivity analysis should be performed separately for potential target shapes (all '8's) and potential pattern shapes (other non-zero digits).

**Strategy:**

1.  **Separate Object Identification:** Modify the `_find_objects` function (or create separate functions) to first identify connected components consisting *only* of the target value (8) and then, independently, identify connected components consisting *only* of non-zero, non-target values.
2.  **Refine Data Structures:** Ensure that each identified object stores its constituent cell coordinates and values accurately, along with its calculated top-left corner.
3.  **Maintain Core Logic:** The sorting and placement logic from the original attempt seems correct in principle and should work once provided with correctly identified and separated objects.

**Metrics and Observations:**

*   **Example 1 (Failed):**
    *   Input Objects (Intended): 3 Targets (all 8s), 2 Patterns (7s, 6s).
    *   Code Identified Objects (Incorrect): 2 Targets, 1 Pattern (merged P1, P2, T3).
    *   Failure Cause: 8-way connectivity on all non-zero cells linked the '6's shape (P2) diagonally to the bottom-left '8's shape (T3), creating a single large component containing non-'8' values, thus classified as a pattern.
*   **Example 2 (Passed):**
    *   Input Objects (Intended): 3 Targets (all 8s), 1 Pattern (7,6,9,4).
    *   Code Identified Objects (Correct): 3 Targets, 1 Pattern.
    *   Success Cause: Objects were spatially separated, preventing incorrect merging by the connectivity rule.

**YAML Facts**


```yaml
Grid_Properties:
  - Type: 2D Array
  - Dimensions: Variable (e.g., 10x10 in examples)
  - Cell_Values: Integers (0-9)
  - Background_Value: 0
  - Target_Value: 8

Object_Identification:
  - Target_Object:
      - Definition: A connected component where all cells have the value specified by `Target_Value` (8).
      - Identification: Apply connected components algorithm (e.g., `scipy.ndimage.label`) to a mask of the input grid where only cells equal to `Target_Value` are considered foreground.
      - Connectivity: 8-way (cells touching orthogonally or diagonally are connected).
  - Pattern_Object:
      - Definition: A connected component where all cells have values that are non-zero and not equal to `Target_Value`. Can contain multiple different non-target digits.
      - Identification: Apply connected components algorithm to a mask of the input grid where only cells not equal to 0 AND not equal to `Target_Value` are considered foreground.
      - Connectivity: 8-way.

Object_Properties:
  - Each object (Target or Pattern) requires:
      - `cells`: A list of tuples `(row, column, value)` for each cell belonging to the object, using values from the original input grid.
      - `top_left`: The `(minimum_row, minimum_column)` coordinate among all cells in the object. This serves as the object's reference point for sorting and placement.

Relationships_and_Actions:
  - Sorting:
      - Sort identified `Pattern_Objects` based on their `top_left` coordinates (row first, then column).
      - Sort identified `Target_Objects` based on their `top_left` coordinates (row first, then column).
  - Transformation:
      - Create an empty output grid (all zeros) of the same dimensions as the input.
      - If no `Pattern_Objects` are identified, return the empty grid.
      - Let `N` be the number of `Pattern_Objects`.
      - Iterate through the sorted `Target_Objects` using index `i` (from 0).
      - For each `Target_Object`:
          - Select the `Pattern_Object` at index `j = i % N` from the sorted list.
          - Get the `top_left` coordinate `(Tr, Tc)` of the `Target_Object`.
          - Get the `top_left` coordinate `(Pr, Pc)` of the selected `Pattern_Object`.
          - For each cell `(r, c, v)` within the selected `Pattern_Object`:
              - Calculate its relative position within the pattern: `rel_row = r - Pr`, `rel_col = c - Pc`.
              - Calculate the destination position in the output grid: `dest_row = Tr + rel_row`, `dest_col = Tc + rel_col`.
              - Check if `(dest_row, dest_col)` is within the grid boundaries.
              - If within bounds, set the output grid cell `(dest_row, dest_col)` to the value `v`.
  - Exclusion: Original `Pattern_Objects` are implicitly excluded from the output unless copied during the replacement process. Original `Target_Objects` are replaced.

Assumptions:
  - The two identification processes (for Targets and Patterns) correctly partition all relevant non-zero shapes.
  - `Target_Value` (8) is consistent across all examples for this specific task.
```


**Natural Language Program**

1.  Define the target value as 8.
2.  Initialize an empty list for `target_objects` and an empty list for `pattern_objects`.
3.  **Identify Target Objects:**
    a.  Create a boolean mask from the input grid where `True` indicates a cell value equals the target value (8).
    b.  Find all distinct 8-way connected components in this mask.
    c.  For each component, determine the set of absolute coordinates `(row, col)` it covers. Extract the original values (all 8s) for these coordinates from the input grid. Calculate the minimum row and minimum column (`top_left`). Store the object's cells `[(row, col, value), ...]` and its `top_left` coordinate in the `target_objects` list.
4.  **Identify Pattern Objects:**
    a.  Create a boolean mask from the input grid where `True` indicates a cell value is not 0 AND not the target value (8).
    b.  Find all distinct 8-way connected components in this mask.
    c.  For each component, determine the set of absolute coordinates `(row, col)` it covers. Extract the original values for these coordinates from the input grid. Calculate the minimum row and minimum column (`top_left`). Store the object's cells `[(row, col, value), ...]` and its `top_left` coordinate in the `pattern_objects` list.
5.  Initialize an empty output grid with the same dimensions as the input grid, filled with zeros.
6.  If the `pattern_objects` list is empty, return the empty output grid.
7.  Sort the `pattern_objects` list based on their `top_left` coordinates (row first, then column).
8.  Sort the `target_objects` list based on their `top_left` coordinates (row first, then column).
9.  Let `N` be the number of objects in the sorted `pattern_objects` list.
10. Iterate through the sorted `target_objects` list using an index `i` (starting from 0).
11. For the `target_object` at index `i`:
    a.  Select the `pattern_object` from the sorted list at index `j = i % N`.
    b.  Get the `top_left` corner `(Tr, Tc)` of the current `target_object`.
    c.  Get the `top_left` corner `(Pr, Pc)` of the selected `pattern_object`.
    d.  For each cell `(r, c, v)` belonging to the selected `pattern_object`:
        i.  Calculate the cell's relative position within its pattern: `rel_row = r - Pr`, `rel_col = c - Pc`.
        ii. Calculate the destination position in the output grid: `output_row = Tr + rel_row`, `output_col = Tc + rel_col`.
        iii. If `output_row` and `output_col` are within the grid boundaries, set the cell `(output_row, output_col)` in the output grid to the value `v`.
12. Return the final output grid.
