"""
Identifies exactly two distinct, non-background objects in a grid.
Determines if these objects are aligned horizontally or vertically with a gap of background color strictly between their bounding boxes.
If aligned, fills the rectangular region defined by the gap rows/columns, extending across the full grid dimension orthogonal to the alignment. The fill is based on proximity to the objects, using their respective colors.

Specifically:
- The background color is the most frequent color in the grid.
- Objects are contiguous areas of the same non-background color.
- Alignment requires a gap (at least one row/column) of only background color between the bounding boxes.

Gap Filling Logic:
- Calculate the number of rows/columns to fill from each side towards the center: `fill_count = gap_size // 2` (integer division).
- If horizontally aligned (left_obj, right_obj, gap_width):
    - Fill `fill_count` columns starting from the gap's left edge with left_obj's color, across all rows.
    - Fill `fill_count` columns ending at the gap's right edge with right_obj's color, across all rows.
    - If `gap_width` is odd, the middle column remains the background color.
- If vertically aligned (top_obj, bottom_obj, gap_height):
    - Fill `fill_count` rows starting from the gap's top edge with top_obj's color, across all columns.
    - Fill `fill_count` rows ending at the gap's bottom edge with bottom_obj's color, across all columns.
    - If `gap_height` is odd, the middle row remains the background color.

If exactly two objects are not found, or they are not aligned with a gap, the original grid is returned.
"""

import numpy as np
from collections import deque

def _find_objects(grid, background_color):
    """
    Finds contiguous objects of non-background colors in the grid using BFS.

    Args:
        grid (np.ndarray): The input grid.
        background_color (int): The background color.

    Returns:
        list: A list of dictionaries, each representing an object with
              'color', 'coords' (set of (r, c) tuples),
              'min_row', 'min_col', 'max_row', 'max_col'. Returns empty list if grid is empty.
    """
    if grid.size == 0:
        return []
    rows, cols = grid.shape
    visited = np.zeros_like(grid, dtype=bool)
    objects = []

    for r in range(rows):
        for c in range(cols):
            # If it's a non-background pixel and hasn't been visited yet, start BFS
            if grid[r, c] != background_color and not visited[r, c]:
                color = grid[r, c]
                obj_coords = set()
                q = deque([(r, c)])
                visited[r, c] = True
                min_r, max_r = r, r
                min_c, max_c = c, c

                while q:
                    row, col = q.popleft()
                    obj_coords.add((row, col))
                    # Update bounding box
                    min_r = min(min_r, row)
                    max_r = max(max_r, row)
                    min_c = min(min_c, col)
                    max_c = max(max_c, col)

                    # Check neighbors (4-connectivity: up, down, left, right)
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = row + dr, col + dc
                        # Check bounds, color match, and visited status
                        if 0 <= nr < rows and 0 <= nc < cols and \
                           not visited[nr, nc] and grid[nr, nc] == color:
                            visited[nr, nc] = True
                            q.append((nr, nc))
                
                # Store found object details
                objects.append({
                    'color': color,
                    'coords': obj_coords,
                    'min_row': min_r,
                    'min_col': min_c,
                    'max_row': max_r,
                    'max_col': max_c
                })

    return objects

def transform(input_grid):
    # Initialize output_grid as a copy of the input
    output_grid = np.copy(input_grid)
    
    # Handle empty grid case
    if input_grid.size == 0:
        return output_grid
        
    rows, cols = output_grid.shape

    # 1. Identify the background color (most frequent color)
    colors, counts = np.unique(input_grid, return_counts=True)
    if len(counts) == 0: # Should not happen if grid.size != 0, but safe check
        return output_grid 
    background_color = colors[np.argmax(counts)]
    
    # Handle case where grid might be all one color (no distinct objects)
    if len(colors) <= 1:
        return output_grid

    # 2. Find all contiguous non-background objects
    objects = _find_objects(output_grid, background_color)

    # 3. Ensure exactly two objects are found
    if len(objects) != 2:
        return output_grid 

    obj1 = objects[0]
    obj2 = objects[1]
    
    # 4. Check for Horizontal Alignment and Gap
    # Determine potential left and right objects
    if obj1['min_col'] < obj2['min_col']:
        left_obj = obj1
        right_obj = obj2
    else:
        left_obj = obj2
        right_obj = obj1
    
    # Check if there's a horizontal gap (at least one column wide)
    if left_obj['max_col'] < right_obj['min_col'] - 1:
        gap_start_col = left_obj['max_col'] + 1
        gap_end_col = right_obj['min_col'] - 1
        
        # Verify the gap contains only background color
        is_gap_clear = np.all(output_grid[:, gap_start_col : gap_end_col + 1] == background_color)
        
        if is_gap_clear:
            gap_width = gap_end_col - gap_start_col + 1
            fill_count = gap_width // 2 # Number of columns to fill from each side
            
            # Fill left part of the gap across ALL rows
            output_grid[:, gap_start_col : gap_start_col + fill_count] = left_obj['color']
            
            # Fill right part of the gap across ALL rows
            # Start index calculation handles even/odd gap widths correctly
            output_grid[:, gap_end_col - fill_count + 1 : gap_end_col + 1] = right_obj['color']
            
            # Successfully filled horizontally, return the result
            return output_grid 

    # 5. Check for Vertical Alignment and Gap
    # Determine potential top and bottom objects
    if obj1['min_row'] < obj2['min_row']:
        top_obj = obj1
        bottom_obj = obj2
    else:
        top_obj = obj2
        bottom_obj = obj1

    # Check if there's a vertical gap (at least one row wide)
    if top_obj['max_row'] < bottom_obj['min_row'] - 1:
        gap_start_row = top_obj['max_row'] + 1
        gap_end_row = bottom_obj['min_row'] - 1
        
        # Verify the gap contains only background color
        is_gap_clear = np.all(output_grid[gap_start_row : gap_end_row + 1, :] == background_color)

        if is_gap_clear:
            gap_height = gap_end_row - gap_start_row + 1
            fill_count = gap_height // 2 # Number of rows to fill from each side

            # Fill top part of the gap across ALL columns
            output_grid[gap_start_row : gap_start_row + fill_count, :] = top_obj['color']
            
            # Fill bottom part of the gap across ALL columns
            # Start index calculation handles even/odd gap heights correctly
            output_grid[gap_end_row - fill_count + 1 : gap_end_row + 1, :] = bottom_obj['color']

            # Successfully filled vertically, return the result
            return output_grid

    # 6. If no alignment with a clear gap was found, return the original grid
    return output_grid