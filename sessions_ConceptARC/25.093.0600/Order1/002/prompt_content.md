
Previous Code:
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
Results for code_00.py:

Train Set Results:

## Example 1:
Input:
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
Expected Output:
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
Transformed Output:
```
0 4 4 4 0 3 3 3 3 1 1 1 1 1 0 2 2 2 2 2 2 0 0
0 4 4 4 0 3 3 3 3 1 1 1 1 1 0 2 2 2 2 2 2 0 0
0 4 4 4 0 3 3 3 3 1 1 1 1 1 0 2 2 2 2 2 2 0 0
0 0 0 0 0 3 3 3 3 1 1 1 1 1 0 2 2 2 2 2 2 0 0
0 0 0 0 0 0 0 0 0 1 1 1 1 1 0 2 2 2 2 2 2 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 2 2 2 2 2 2 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```
Match: False
Pixels Off: 22
Size Correct: True
Color Palette Correct: True
Color Count Correct: True
Score: 7.971014492753625

## Example 2:
Input:
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
Expected Output:
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
Transformed Output:
```
0 0 0 0 0 0 0 0 0 0 0
7 7 7 0 0 0 0 0 0 0 0
7 0 7 0 0 0 0 0 0 0 0
7 7 7 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
2 2 2 2 0 0 0 0 0 0 0
2 0 0 2 0 0 0 0 0 0 0
2 0 0 2 0 0 0 0 0 0 0
2 2 2 2 0 0 0 0 0 0 0
5 5 5 5 5 5 0 0 0 0 0
5 0 0 0 0 5 0 0 0 0 0
5 0 0 0 0 5 0 0 0 0 0
5 0 0 0 0 5 0 0 0 0 0
5 0 0 0 0 5 0 0 0 0 0
5 5 5 5 5 5 0 0 0 0 0
```
Match: False
Pixels Off: 20
Size Correct: True
Color Palette Correct: True
Color Count Correct: True
Score: 12.121212121212125

Test Set Results:

## Example 1:
Input:
```
8 8 8 8 8 8 0 0 0 0 0 0 0
8 8 8 8 8 8 0 0 0 0 0 0 0
8 8 8 8 8 8 0 0 0 0 0 0 0
8 8 8 8 8 8 0 0 0 0 6 6 6
8 8 8 8 8 8 0 4 4 0 6 6 6
8 8 8 8 8 8 0 4 4 0 6 6 6
```
Expected Output:
```
0 0 0 0 0 0 0 8 8 8 8 8 8
0 0 0 0 0 0 0 8 8 8 8 8 8
0 0 0 0 0 0 0 8 8 8 8 8 8
0 0 0 6 6 6 0 8 8 8 8 8 8
4 4 0 6 6 6 0 8 8 8 8 8 8
4 4 0 6 6 6 0 8 8 8 8 8 8
```
Transformed Output:
```
8 8 8 8 8 8 0 0 0 0 0 0 0
8 8 8 8 8 8 0 0 0 0 0 0 0
8 8 8 8 8 8 0 0 0 0 0 0 0
8 8 8 8 8 8 0 0 0 0 6 6 6
8 8 8 8 8 8 0 4 4 0 6 6 6
8 8 8 8 8 8 0 4 4 0 6 6 6
```
Match: False
Pixels Off: 72
Size Correct: True
Color Palette Correct: True
Color Count Correct: True
Score: 92.3076923076923

## Example 2:
Input:
```
7 0 0 0 0 0
0 0 0 0 0 0
7 7 0 0 0 0
7 7 0 0 0 0
0 0 0 0 0 0
7 7 7 7 7 0
7 7 7 7 7 0
7 7 7 7 7 0
7 7 7 7 7 0
7 7 7 7 7 0
0 0 0 0 0 0
7 7 7 0 0 0
7 7 7 0 0 0
7 7 7 0 0 0
```
Expected Output:
```
7 0 0 0 0 0
0 0 0 0 0 0
7 7 0 0 0 0
7 7 0 0 0 0
0 0 0 0 0 0
7 7 7 0 0 0
7 7 7 0 0 0
7 7 7 0 0 0
0 0 0 0 0 0
7 7 7 7 7 0
7 7 7 7 7 0
7 7 7 7 7 0
7 7 7 7 7 0
7 7 7 7 7 0
```
Transformed Output:
```
0 0 0 0 0 0
7 7 7 0 0 0
7 7 7 0 0 0
7 7 7 0 0 0
0 0 0 0 0 0
7 7 7 7 7 0
7 7 7 7 7 0
7 7 7 7 7 0
7 7 7 7 7 0
7 7 7 7 7 0
0 0 0 0 0 0
7 7 0 0 0 0
7 7 0 0 0 0
7 0 0 0 0 0
```
Match: False
Pixels Off: 32
Size Correct: True
Color Palette Correct: True
Color Count Correct: True
Score: 38.095238095238095

## Example 3:
Input:
```
2 2 2 2 0 0 0 0 0 0
2 0 0 2 0 5 5 5 0 0
2 0 0 2 0 5 0 5 0 0
2 2 2 2 0 5 5 5 0 6
```
Expected Output:
```
0 0 0 0 0 0 2 2 2 2
0 0 5 5 5 0 2 0 0 2
0 0 5 0 5 0 2 0 0 2
6 0 5 5 5 0 2 2 2 2
```
Transformed Output:
```
0 0 0 0 2 2 2 2 0 0
0 5 5 5 2 0 0 2 0 0
0 5 0 5 2 0 0 2 0 0
0 5 5 5 2 2 2 2 0 6
```
Match: False
Pixels Off: 22
Size Correct: True
Color Palette Correct: True
Color Count Correct: True
Score: 55.0
