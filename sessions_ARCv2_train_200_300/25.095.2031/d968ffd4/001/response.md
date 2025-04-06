```python
import collections
import math
from copy import deepcopy

def find_background(grid: list[list[int]]) -> int:
    """Finds the most frequent color in the grid, assuming it's the background."""
    counts = collections.Counter()
    for r in range(len(grid)):
        for c in range(len(grid[0])):
            counts[grid[r][c]] += 1
    if not counts:
        return -1 # Or raise error for empty grid
    # Return the most common element
    return counts.most_common(1)[0][0]

def find_objects(grid: list[list[int]], background_color: int) -> list[tuple[int, set[tuple[int, int]]]]:
    """Finds connected regions of non-background colors using BFS."""
    rows, cols = len(grid), len(grid[0])
    visited = set()
    objects = []
    
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] != background_color and (r, c) not in visited:
                obj_color = grid[r][c]
                obj_coords = set()
                queue = collections.deque([(r, c)])
                visited.add((r, c))
                
                while queue:
                    row, col = queue.popleft()
                    obj_coords.add((row, col))
                    
                    # Check neighbors (up, down, left, right)
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = row + dr, col + dc
                        if 0 <= nr < rows and 0 <= nc < cols and \
                           (nr, nc) not in visited and \
                           grid[nr][nc] == obj_color:
                            visited.add((nr, nc))
                            queue.append((nr, nc))
                            
                objects.append((obj_color, obj_coords))
                
    return objects

def get_bounding_box(coordinates: set[tuple[int, int]]) -> tuple[int, int, int, int]:
    """Calculates the bounding box (min_row, max_row, min_col, max_col) for a set of coordinates."""
    if not coordinates:
        return (-1, -1, -1, -1)
    min_r = min(r for r, c in coordinates)
    max_r = max(r for r, c in coordinates)
    min_c = min(c for r, c in coordinates)
    max_c = max(c for r, c in coordinates)
    return min_r, max_r, min_c, max_c

"""
Transforms a 2D grid by identifying two distinct non-background objects separated by the background color.
It then fills the background area between these objects, within their overlapping range on the non-separation axis.
The filling uses the colors of the respective objects, extending towards the middle point between them.
If the gap between objects is even, the space is divided equally; if odd, the middle row/column is assigned based on rounding.
The original objects and the rest of the background remain unchanged.
"""

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Applies the transformation rule to the input grid.

    Args:
        input_grid: A list of lists representing the input 2D grid of integers.

    Returns:
        A list of lists representing the transformed 2D grid.
    """
    
    # Handle empty or invalid input
    if not input_grid or not input_grid[0]:
        return []

    rows = len(input_grid)
    cols = len(input_grid[0])
    
    # Initialize output_grid as a deep copy of the input
    output_grid = deepcopy(input_grid)

    # 1. Find background color
    background_color = find_background(input_grid)
    
    # 2. Find non-background objects
    objects = find_objects(input_grid, background_color)
    
    # Expect exactly two objects based on examples
    if len(objects) != 2:
        # If not exactly two objects, return the original grid (or handle as error)
        # print(f"Warning: Expected 2 objects, found {len(objects)}. Returning original grid.")
        return output_grid
        
    obj1_color, obj1_coords = objects[0]
    obj2_color, obj2_coords = objects[1]
    
    # 3. Get bounding boxes
    obj1_bbox = get_bounding_box(obj1_coords)
    obj2_bbox = get_bounding_box(obj2_coords)
    min_r1, max_r1, min_c1, max_c1 = obj1_bbox
    min_r2, max_r2, min_c2, max_c2 = obj2_bbox

    # 4. Determine separation axis and overlapping range
    
    # Check for horizontal separation (gap in columns, overlap in rows)
    if max_c1 < min_c2 or max_c2 < min_c1:
        separation_axis = 'horizontal'
        # Ensure obj1 is left, obj2 is right
        if min_c1 > min_c2:
            obj1_color, obj2_color = obj2_color, obj1_color
            obj1_coords, obj2_coords = obj2_coords, obj1_coords
            min_r1, max_r1, min_c1, max_c1 = obj2_bbox
            min_r2, max_r2, min_c2, max_c2 = obj1_bbox
            
        # Determine overlapping rows
        overlap_min_r = max(min_r1, min_r2)
        overlap_max_r = min(max_r1, max_r2)
        
        # Determine gap columns
        gap_start_c = max_c1 + 1
        gap_end_c = min_c2 - 1
        
        # Calculate midpoint (handle potential floating point carefully for splitting)
        # Midpoint represents the boundary; columns < mid fill with obj1, >= mid fill with obj2
        mid_col_boundary = (gap_start_c + gap_end_c + 1) / 2 
        
        # 5. Perform fill
        for r in range(overlap_min_r, overlap_max_r + 1):
            for c in range(gap_start_c, gap_end_c + 1):
                 # Only fill if the cell is currently background
                if output_grid[r][c] == background_color:
                    if c < mid_col_boundary:
                        output_grid[r][c] = obj1_color
                    else:
                        output_grid[r][c] = obj2_color
                        
    # Check for vertical separation (gap in rows, overlap in columns)
    elif max_r1 < min_r2 or max_r2 < min_r1:
        separation_axis = 'vertical'
        # Ensure obj1 is top, obj2 is bottom
        if min_r1 > min_r2:
            obj1_color, obj2_color = obj2_color, obj1_color
            obj1_coords, obj2_coords = obj2_coords, obj1_coords
            min_r1, max_r1, min_c1, max_c1 = obj2_bbox
            min_r2, max_r2, min_c2, max_c2 = obj1_bbox

        # Determine overlapping columns
        overlap_min_c = max(min_c1, min_c2)
        overlap_max_c = min(max_c1, max_c2)

        # Determine gap rows
        gap_start_r = max_r1 + 1
        gap_end_r = min_r2 - 1

        # Calculate midpoint boundary
        mid_row_boundary = (gap_start_r + gap_end_r + 1) / 2

        # 5. Perform fill
        for c in range(overlap_min_c, overlap_max_c + 1):
             for r in range(gap_start_r, gap_end_r + 1):
                 # Only fill if the cell is currently background
                if output_grid[r][c] == background_color:
                    if r < mid_row_boundary:
                        output_grid[r][c] = obj1_color
                    else:
                         output_grid[r][c] = obj2_color
    else:
        # Objects might be overlapping or touching in a way not covered by examples
        # print("Warning: Objects are not clearly separated horizontally or vertically. Returning original grid.")
        return output_grid # Or handle differently

    return output_grid
```