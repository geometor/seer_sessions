```python
import collections
import math
from copy import deepcopy

"""
Transforms a 2D grid by performing the following steps:

1.  **Identify Grid Components:**
    *   Determines the background color (most frequent integer).
    *   Locates exactly two distinct, connected non-background objects, identifying their colors and coordinates.

2.  **Determine Object Relationship:**
    *   Calculates the bounding box for each object.
    *   Determines if the objects are separated horizontally or vertically by at least one background cell.
    *   Orders the objects as object1 (left/top) and object2 (right/bottom).

3.  **Define Transformation Zones:**
    *   Calculates the 'Gap Range' (rows/columns strictly between the objects along the separation axis) and its size ('gap_size').
    *   Calculates the 'Overlap Range' (rows/columns where the objects overlap along the non-separation axis).
    *   Calculates the 'Fill Extent' along the non-separation axis, which is the Overlap Range expanded by one cell outwards (clamped to grid boundaries).

4.  **Apply Transformation based on Gap Size:**
    *   Creates a copy of the input grid.
    *   Iterates through the cells defined by the intersection of the Gap Range (on the separation axis) and the Fill Extent (on the non-separation axis).
    *   If a cell in this area contains the background color in the original input grid:
        *   **If 'gap_size' is even:** Calculate a midpoint boundary. Fill the cell with the color of the object on the corresponding side of the boundary.
        *   **If 'gap_size' is odd:** Calculate the exact middle index (row/column) of the gap. If the current cell is *not* at this middle index, fill it with the color of the closer object. If the cell *is* at the middle index, leave it unchanged (keep background color).

5.  **Return Result:** Returns the modified grid. Original objects and background cells outside the defined fill area remain unchanged. If exactly two suitable objects are not found, the original grid is returned.
"""

# --- Helper Functions ---

def find_background(grid: list[list[int]]) -> int:
    """Finds the most frequent color in the grid, assuming it's the background."""
    counts = collections.Counter()
    if not grid or not grid[0]:
        return -1 # Indicate error or empty grid
    rows, cols = len(grid), len(grid[0])
    for r in range(rows):
        for c in range(cols):
            counts[grid[r][c]] += 1
    if not counts:
        return -1 # Should not happen if grid is not empty, but safer
    # Return the most common element
    return counts.most_common(1)[0][0]

def find_objects(grid: list[list[int]], background_color: int) -> list[tuple[int, set[tuple[int, int]]]]:
    """Finds connected regions of non-background colors using BFS."""
    if not grid or not grid[0]:
        return []
    rows, cols = len(grid), len(grid[0])
    visited = set()
    objects = []
    
    for r in range(rows):
        for c in range(cols):
            # Check if cell is part of the grid, not background, and not visited
            if grid[r][c] != background_color and (r, c) not in visited:
                obj_color = grid[r][c]
                obj_coords = set()
                queue = collections.deque([(r, c)])
                visited.add((r, c))
                
                # Perform BFS to find all connected cells of the same color
                while queue:
                    row, col = queue.popleft()
                    obj_coords.add((row, col))
                    
                    # Check neighbors (up, down, left, right)
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = row + dr, col + dc
                        # Check bounds and if neighbor is same color and not visited
                        if 0 <= nr < rows and 0 <= nc < cols and \
                           (nr, nc) not in visited and \
                           grid[nr][nc] == obj_color:
                            visited.add((nr, nc))
                            queue.append((nr, nc))
                            
                # Store the found object (color and coordinates)
                if obj_coords:
                    objects.append((obj_color, obj_coords))
                    
    return objects

def get_bounding_box(coordinates: set[tuple[int, int]]) -> tuple[int, int, int, int]:
    """Calculates the bounding box (min_row, max_row, min_col, max_col) for a set of coordinates."""
    if not coordinates:
        return (-1, -1, -1, -1) # Return invalid box if no coordinates
    min_r = min(r for r, c in coordinates)
    max_r = max(r for r, c in coordinates)
    min_c = min(c for r, c in coordinates)
    max_c = max(c for r, c in coordinates)
    return min_r, max_r, min_c, max_c

# --- Main Transformation Function ---

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Applies the described transformation rule to the input grid.
    """
    
    # Handle empty or invalid input
    if not input_grid or not input_grid[0]:
        return []

    rows = len(input_grid)
    cols = len(input_grid[0])
    
    # Initialize output_grid as a deep copy of the input
    output_grid = deepcopy(input_grid)

    # 1. Identify Grid Components
    background_color = find_background(input_grid)
    if background_color == -1: return output_grid # Return copy if grid was empty/error
    
    objects = find_objects(input_grid, background_color)
    
    # Expect exactly two objects based on examples
    if len(objects) != 2:
        # If not exactly two objects, return the original grid copy
        return output_grid
        
    obj1_color, obj1_coords = objects[0]
    obj2_color, obj2_coords = objects[1]
    
    # 2. Determine Object Relationship
    obj1_bbox = get_bounding_box(obj1_coords)
    obj2_bbox = get_bounding_box(obj2_coords)
    min_r1, max_r1, min_c1, max_c1 = obj1_bbox
    min_r2, max_r2, min_c2, max_c2 = obj2_bbox

    # Check for horizontal separation (gap in columns, potential overlap in rows)
    # Ensure objects are truly separated (gap > 0) and not touching or overlapping on the primary axis
    is_horizontally_separated = (max_c1 < min_c2 - 1) or (max_c2 < min_c1 - 1)
    is_vertically_separated = (max_r1 < min_r2 - 1) or (max_r2 < min_r1 - 1)

    if is_horizontally_separated:
        # Ensure obj1 is left, obj2 is right for consistent processing
        if min_c1 > min_c2:
            # Swap all properties if obj1 was initially on the right
            obj1_color, obj2_color = obj2_color, obj1_color
            min_r1, max_r1, min_c1, max_c1 = obj2_bbox
            min_r2, max_r2, min_c2, max_c2 = obj1_bbox
            
        # 3. Define Transformation Zones
        # Gap range along the separation axis (columns)
        gap_start = max_c1 + 1
        gap_end = min_c2 - 1
        gap_size = gap_end - gap_start + 1
        
        # Overlap range along the non-separation axis (rows)
        overlap_min = max(min_r1, min_r2)
        overlap_max = min(max_r1, max_r2)

        # Fill extent along the non-separation axis (rows), clamped to grid bounds
        fill_extent_min = max(0, overlap_min - 1)
        fill_extent_max = min(rows - 1, overlap_max + 1)
        
        # 4. Apply Transformation
        is_gap_odd = (gap_size % 2 != 0)
        middle_index = -1
        if is_gap_odd:
            middle_index = gap_start + (gap_size // 2)
        else:
            # Midpoint boundary for even gap (columns < boundary fill with obj1)
            midpoint_boundary = (gap_start + gap_end + 1) / 2 

        # Iterate through the relevant rows ('Fill Extent')
        for r in range(fill_extent_min, fill_extent_max + 1):
            # Iterate through the relevant columns ('Gap Range')
            for c in range(gap_start, gap_end + 1):
                 # Check if the cell in the *original* grid is background
                if input_grid[r][c] == background_color:
                    if is_gap_odd:
                        # Odd Gap: Skip middle column, fill others based on side
                        if c == middle_index:
                            continue # Leave background color
                        elif c < middle_index:
                            output_grid[r][c] = obj1_color
                        else: # c > middle_index
                            output_grid[r][c] = obj2_color
                    else:
                        # Even Gap: Fill based on midpoint boundary
                        if c < midpoint_boundary:
                            output_grid[r][c] = obj1_color
                        else:
                            output_grid[r][c] = obj2_color
                        
    elif is_vertically_separated:
        # Ensure obj1 is top, obj2 is bottom
        if min_r1 > min_r2:
            # Swap all properties if obj1 was initially on the bottom
            obj1_color, obj2_color = obj2_color, obj1_color
            min_r1, max_r1, min_c1, max_c1 = obj2_bbox
            min_r2, max_r2, min_c2, max_c2 = obj1_bbox

        # 3. Define Transformation Zones
        # Gap range along the separation axis (rows)
        gap_start = max_r1 + 1
        gap_end = min_r2 - 1
        gap_size = gap_end - gap_start + 1

        # Overlap range along the non-separation axis (columns)
        overlap_min = max(min_c1, min_c2)
        overlap_max = min(max_c1, max_c2)
        
        # Fill extent along the non-separation axis (columns), clamped to grid bounds
        fill_extent_min = max(0, overlap_min - 1)
        fill_extent_max = min(cols - 1, overlap_max + 1)

        # 4. Apply Transformation
        is_gap_odd = (gap_size % 2 != 0)
        middle_index = -1
        if is_gap_odd:
            middle_index = gap_start + (gap_size // 2)
        else:
            # Midpoint boundary for even gap (rows < boundary fill with obj1)
            midpoint_boundary = (gap_start + gap_end + 1) / 2

        # Iterate through the relevant columns ('Fill Extent')
        for c in range(fill_extent_min, fill_extent_max + 1):
             # Iterate through the relevant rows ('Gap Range')
             for r in range(gap_start, gap_end + 1):
                 # Check if the cell in the *original* grid is background
                if input_grid[r][c] == background_color:
                    if is_gap_odd:
                        # Odd Gap: Skip middle row, fill others based on side
                         if r == middle_index:
                             continue # Leave background color
                         elif r < middle_index:
                             output_grid[r][c] = obj1_color
                         else: # r > middle_index
                              output_grid[r][c] = obj2_color
                    else:
                        # Even Gap: Fill based on midpoint boundary
                        if r < midpoint_boundary:
                            output_grid[r][c] = obj1_color
                        else:
                             output_grid[r][c] = obj2_color
    else:
        # Objects might be touching, overlapping in complex ways, or not separated as expected.
        # Return the original grid copy in these cases based on example behavior.
        pass # output_grid is already a copy

    # 5. Return Result
    return output_grid
```