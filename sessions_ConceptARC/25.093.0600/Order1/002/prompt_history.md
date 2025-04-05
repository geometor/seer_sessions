
## train_1

**input:**
```
0 1 1 1 1 1 0 4 4 4 0 3 3 3 3 0 2 2 2 2 2 2 0
0 1 1 1 1 1 0 4 4 4 0 3 3 3 3 0 2 2 2 2 2 2 0
0 1 1 1 1 1 0 4 4 4 0 3 3 3 3 0 2 2 2 2 2 2 0
0 1 1 1 1 1 0 0 0 0 0 3 3 3 3 0 2 2 2 2 2 2 0
0 1 1 1 1 1 0 0 0 0 0 0 0 0 0 0 2 2 2 2 2 2 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 2 2 2 2 2 2 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 4 4 4 0 3 3 3 3 0 1 1 1 1 1 0 2 2 2 2 2 2 0
0 4 4 4 0 3 3 3 3 0 1 1 1 1 1 0 2 2 2 2 2 2 0
0 4 4 4 0 3 3 3 3 0 1 1 1 1 1 0 2 2 2 2 2 2 0
0 0 0 0 0 3 3 3 3 0 1 1 1 1 1 0 2 2 2 2 2 2 0
0 0 0 0 0 0 0 0 0 0 1 1 1 1 1 0 2 2 2 2 2 2 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 2 2 2 2 2 2 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```


## train_2

**input:**
```
5 5 5 5 5 5 0 0 0 0 0
5 0 0 0 0 5 0 0 0 0 0
5 0 0 0 0 5 0 0 0 0 0
5 0 0 0 0 5 0 0 0 0 0
5 0 0 0 0 5 0 0 0 0 0
5 5 5 5 5 5 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
2 2 2 2 0 0 0 0 0 0 0
2 0 0 2 0 0 0 0 0 0 0
2 0 0 2 0 0 0 0 0 0 0
2 2 2 2 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
7 7 7 0 0 0 0 0 0 0 0
7 0 7 0 0 0 0 0 0 0 0
7 7 7 0 0 0 0 0 0 0 0
```


**output:**
```
7 7 7 0 0 0 0 0 0 0 0
7 0 7 0 0 0 0 0 0 0 0
7 7 7 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
2 2 2 2 0 0 0 0 0 0 0
2 0 0 2 0 0 0 0 0 0 0
2 0 0 2 0 0 0 0 0 0 0
2 2 2 2 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
5 5 5 5 5 5 0 0 0 0 0
5 0 0 0 0 5 0 0 0 0 0
5 0 0 0 0 5 0 0 0 0 0
5 0 0 0 0 5 0 0 0 0 0
5 0 0 0 0 5 0 0 0 0 0
5 5 5 5 5 5 0 0 0 0 0
```

## Perception

The input and output are 2D grids containing integer values. The non-zero values appear to form distinct "objects" or "blobs", where each object consists of connected cells of the same number (color). The background is represented by zeros.

The core transformation involves rearranging these objects within the grid. The rearrangement happens along a primary axis, either horizontal or vertical.

1.  **Object Identification:** The first step is to identify all distinct connected components of non-zero cells having the same value. Each such component is an "object".
2.  **Axis Determination:** The overall spatial layout of these objects determines the axis of rearrangement. If the bounding box containing all non-zero cells is wider than it is tall, the rearrangement occurs horizontally. Otherwise (if taller or square), it occurs vertically.
3.  **Gap Identification:** The empty space (rows or columns of zeros) between adjacent objects along the primary axis in the input grid is identified. These gaps are preserved in the output.
4.  **Sorting:** The objects are reordered based on a rule that depends on the determined axis:
    *   **Vertical Axis:** Objects are sorted based on their topmost row index (minimum row index) in descending order. The object starting in the lowest row comes first in the output.
    *   **Horizontal Axis:** Objects are sorted based on their color value in descending order, *except* for the object that is rightmost in the input (the one with the largest minimum column index). This rightmost object retains its position as the last object in the sequence after the others are sorted.
5.  **Reconstruction:** The output grid is constructed by placing the objects in their new sorted order, maintaining the original gaps (in terms of width or height) between them along the primary axis. The placement starts from the top (for vertical) or left (for horizontal) edge of the grid, potentially including an initial gap if one existed before the first object in the input.

## Facts


```yaml
task_elements:
  - type: grid
    properties:
      - content: integers (0 for background, non-zero for objects)
      - dimensionality: 2D
  - type: object
    properties:
      - definition: maximal connected component of identical non-zero cells
      - attributes:
          - color: integer value of the cells
          - coordinates: list of (row, col) tuples for cells belonging to the object
          - bounding_box: (min_row, max_row, min_col, max_col)
          - min_row: topmost row index
          - min_col: leftmost column index
  - type: layout
    properties:
      - overall_bounding_box: (min_r, max_r, min_c, max_c) encompassing all non-zero cells
      - overall_height: max_r - min_r + 1
      - overall_width: max_c - min_c + 1
      - primary_axis: derived from overall dimensions ('horizontal' if overall_width > overall_height, else 'vertical')
  - type: gap
    properties:
      - definition: contiguous rows/columns of zeros separating objects along the primary_axis
      - size: number of rows (for vertical axis) or columns (for horizontal axis)
      - location: relative position between objects in the input order

actions:
  - action: identify_objects
    inputs: input_grid
    outputs: list of object descriptions (color, coordinates, bbox, etc.)
  - action: determine_axis
    inputs: list of objects (or overall_bounding_box)
    outputs: primary_axis ('horizontal' or 'vertical')
  - action: identify_gaps
    inputs: input_grid, list of objects, primary_axis
    outputs: list of gap sizes between adjacent objects along the axis in input order
  - action: sort_objects
    inputs: list of objects, primary_axis
    outputs: list of objects in the new order
    logic:
      - if primary_axis is 'vertical': sort by object.min_row descending
      - if primary_axis is 'horizontal': identify rightmost object (max of min_col); sort remaining objects by object.color descending; append rightmost object
  - action: reconstruct_grid
    inputs: output grid dimensions, sorted list of objects, list of gaps
    outputs: output_grid
    logic: place objects and gaps sequentially along the primary axis starting from the top/left

relationships:
  - relationship: object rearrangement
    notes: The core transformation is the reordering of objects.
  - relationship: gap preservation
    notes: The spacing between objects along the primary axis is maintained.
  - relationship: axis-dependent sorting
    notes: The rule for ordering objects depends on whether they are arranged primarily horizontally or vertically.
```


## Natural Language Program

1.  Parse the input grid to identify all distinct connected components (objects) of non-zero cells with the same value. For each object, record its color, its cell coordinates, and its bounding box (minimum/maximum row and column).
2.  Determine the overall bounding box encompassing all identified objects. Calculate the height and width of this overall bounding box.
3.  Determine the primary axis of rearrangement: if the overall width is greater than the overall height, the axis is 'horizontal'; otherwise, the axis is 'vertical'.
4.  Identify the sequence of objects based on their position along the primary axis in the input grid (top-to-bottom for vertical, left-to-right for horizontal).
5.  Calculate the size of the gaps (number of zero rows for vertical axis, number of zero columns for horizontal axis) between consecutive objects in the input sequence along the primary axis. Also, note any gap before the first object.
6.  Determine the target order of the objects based on the primary axis:
    a.  If the axis is 'vertical', sort the list of identified objects based on their minimum row index in descending order.
    b.  If the axis is 'horizontal', identify the object with the maximum minimum column index (the "rightmost" object). Remove this object temporarily. Sort the remaining objects based on their color value in descending order. Append the "rightmost" object to the end of this sorted list.
7.  Create a new empty grid with the same dimensions as the input grid.
8.  Iterate through the newly sorted list of objects and the identified gap sizes. Place the objects and gaps sequentially onto the new grid along the primary axis, starting from the top-left (row 0, col 0). Maintain the original content and relative positions of cells within each object. Ensure the gaps placed between objects have the correct sizes as identified in step 5. Fill any remaining space with zeros.
9.  Return the reconstructed grid as the output.
```python
import numpy as np
from collections import deque

"""
Transforms an input grid by rearranging connected components (objects) of non-zero cells.

1.  **Identify Objects:** Finds all distinct connected components (objects) of 
    non-zero cells with the same value. Records each object's color, 
    coordinates, and bounding box.
2.  **Determine Axis:** Calculates the overall bounding box of all objects. If 
    its width > height, the primary axis is 'horizontal'; otherwise, it's 
    'vertical'.
3.  **Identify Gaps:** Determines the spacing (rows/columns of zeros) between 
    objects along the primary axis in their original input order. Records the 
    initial gap before the first object and gaps between subsequent objects.
4.  **Sort Objects:** Reorders the objects based on the primary axis:
    *   Vertical Axis: Sorts objects by their top row index (min_row) in 
        descending order (bottom-most object first).
    *   Horizontal Axis: Identifies the object starting furthest to the right 
        (max of min_col). Sorts the *remaining* objects by color descending. 
        Appends the rightmost object to the end of the sorted list.
5.  **Reconstruct Grid:** Creates a new grid. Places the objects in their new 
    sorted order, maintaining the original gaps between them along the primary 
    axis, starting from the top/left edge.
"""

class GridObject:
    """Represents a connected component of non-zero cells."""
    def __init__(self, color, coords):
        if not coords:
            raise ValueError("Cannot create an object with no coordinates.")
        self.color = color
        # Store coords as a list of tuples for iteration during reconstruction
        self.coords = list(coords) 
        rows = [r for r, c in coords]
        cols = [c for r, c in coords]
        self.min_row = min(rows)
        self.max_row = max(rows)
        self.min_col = min(cols)
        self.max_col = max(cols)
        self.height = self.max_row - self.min_row + 1
        self.width = self.max_col - self.min_col + 1

    def __repr__(self):
         return (f"Obj(color={self.color}, "
                 f"bbox=({self.min_row},{self.min_col})-({self.max_row},{self.max_col}), "
                 f"size=({self.height}x{self.width}))")

def find_objects(grid):
    """Finds all connected components (objects) in the grid."""
    objects = []
    rows, cols = grid.shape
    visited = set()

    for r in range(rows):
        for c in range(cols):
            if grid[r, c] != 0 and (r, c) not in visited:
                color = grid[r, c]
                component_coords = set()
                q = deque([(r, c)])
                visited.add((r,c))
                
                while q:
                    row, col = q.popleft()
                    component_coords.add((row, col))
                    
                    # Check neighbors (up, down, left, right)
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = row + dr, col + dc
                        if 0 <= nr < rows and 0 <= nc < cols and \
                           (nr, nc) not in visited and \
                           grid[nr, nc] == color:
                            visited.add((nr, nc))
                            q.append((nr, nc))
                            
                if component_coords:
                    objects.append(GridObject(color, component_coords))
    return objects

def get_overall_bbox(objects):
    """Calculates the bounding box encompassing all objects."""
    if not objects:
        return None, 0, 0 # No bbox, height=0, width=0
        
    min_r = min(obj.min_row for obj in objects)
    max_r = max(obj.max_row for obj in objects)
    min_c = min(obj.min_col for obj in objects)
    max_c = max(obj.max_col for obj in objects)
    
    height = max_r - min_r + 1
    width = max_c - min_c + 1
    bbox = (min_r, max_r, min_c, max_c)
    return bbox, height, width

def identify_gaps(objects, primary_axis):
    """Identifies gaps between objects along the primary axis in input order."""
    if not objects:
        return [], [] # No gaps if no objects

    # Sort objects by their initial position along the axis
    if primary_axis == 'vertical':
        # Sort by top-most row
        sorted_objects_input_order = sorted(objects, key=lambda obj: obj.min_row)
        # Calculate initial gap (space above the first object)
        initial_gap = sorted_objects_input_order[0].min_row
        # Calculate gaps between consecutive objects
        gaps = []
        for i in range(len(sorted_objects_input_order) - 1):
            gap = sorted_objects_input_order[i+1].min_row - (sorted_objects_input_order[i].max_row + 1)
            gaps.append(max(0, gap)) # Ensure gap is not negative
            
    else: # primary_axis == 'horizontal'
        # Sort by left-most column
        sorted_objects_input_order = sorted(objects, key=lambda obj: obj.min_col)
        # Calculate initial gap (space left of the first object)
        initial_gap = sorted_objects_input_order[0].min_col
        # Calculate gaps between consecutive objects
        gaps = []
        for i in range(len(sorted_objects_input_order) - 1):
            gap = sorted_objects_input_order[i+1].min_col - (sorted_objects_input_order[i].max_col + 1)
            gaps.append(max(0, gap)) # Ensure gap is not negative

    return [initial_gap] + gaps, sorted_objects_input_order # Return gaps and the input order list

def transform(input_grid):
    """
    Applies the object rearrangement transformation to the input grid.
    """
    grid = np.array(input_grid)
    rows, cols = grid.shape
    output_grid = np.zeros_like(grid)

    # 1. Identify Objects
    objects = find_objects(grid)
    if not objects:
        return output_grid.tolist() # Return empty grid if no objects

    # 2. Determine Axis
    _, overall_height, overall_width = get_overall_bbox(objects)
    primary_axis = 'horizontal' if overall_width > overall_height else 'vertical'

    # 3. Identify Gaps (using original object order along the axis)
    gaps, objects_input_order = identify_gaps(objects, primary_axis)
    # We need the gaps list to correspond to the *final* sorted order later.
    # Create a mapping from object (by reference/id) to its preceding gap size in the input order.
    gap_map = {}
    gap_map['initial'] = gaps[0] # Gap before the first object in input order
    for i in range(len(objects_input_order) - 1):
         # The gap *after* objects_input_order[i] is gaps[i+1]
         # So, the gap *before* objects_input_order[i+1] is gaps[i+1]
        gap_map[id(objects_input_order[i+1])] = gaps[i+1]


    # 4. Sort Objects based on the determined rule
    if primary_axis == 'vertical':
        # Sort by min_row descending (bottom-most object first in the list)
        sorted_objects = sorted(objects, key=lambda obj: obj.min_row, reverse=True)
    else: # primary_axis == 'horizontal'
        # Find the rightmost object (max of min_col)
        if len(objects) <= 1:
             sorted_objects = objects # No sorting needed for 0 or 1 object
        else:
            rightmost_obj = max(objects, key=lambda obj: obj.min_col)
            other_objects = [obj for obj in objects if obj is not rightmost_obj]
            # Sort remaining objects by color descending
            other_objects_sorted = sorted(other_objects, key=lambda obj: obj.color, reverse=True)
            # Append the rightmost object
            sorted_objects = other_objects_sorted + [rightmost_obj]

    # 5. Reconstruct Grid
    current_pos = 0 # Tracks current row (for vertical) or col (for horizontal)

    # Add the initial gap (the gap before the *first object in the sorted list*)
    first_obj_id = id(sorted_objects[0])
    initial_gap_for_sorted = gap_map.get(first_obj_id, gap_map.get('initial', 0)) # Use initial overall gap if the first sorted obj was also first in input
    current_pos += initial_gap_for_sorted


    for i, obj in enumerate(sorted_objects):
        # Calculate the offset needed to place this object at current_pos
        if primary_axis == 'vertical':
            row_offset = current_pos - obj.min_row
            col_offset = 0
            # Add object's height to current_pos for the next iteration
            current_pos += obj.height
        else: # primary_axis == 'horizontal'
            row_offset = 0
            col_offset = current_pos - obj.min_col
            # Add object's width to current_pos for the next iteration
            current_pos += obj.width

        # Place the object's cells onto the output grid
        for r, c in obj.coords:
            nr, nc = r + row_offset, c + col_offset
            # Check bounds just in case offsets cause issues (shouldn't if logic is right)
            if 0 <= nr < rows and 0 <= nc < cols:
                output_grid[nr, nc] = obj.color
            else:
                 # This case indicates an error in gap/offset calculation or object placement logic
                 print(f"Warning: Coordinate ({nr}, {nc}) out of bounds for object {obj}")


        # Add the gap that should follow this object
        # This is the gap that preceded the *next* object in the sorted list,
        # which corresponds to the gap that *preceded* that next object in the *input* order.
        if i < len(sorted_objects) - 1:
             next_obj_id = id(sorted_objects[i+1])
             # Find the gap associated with the *start* of the next object in the input order
             gap_size = gap_map.get(next_obj_id, 0) # Default to 0 if not found (shouldn't happen)
             current_pos += gap_size


    return output_grid.tolist()
```
