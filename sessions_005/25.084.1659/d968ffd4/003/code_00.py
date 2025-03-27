import numpy as np
from collections import deque

"""
Identifies two distinct rectangular objects within a background color.
Determines if the objects are aligned horizontally or vertically with a gap of background color between them.
Fills the gap between the objects, within the bounding box encompassing both objects, based on proximity.
If horizontally aligned:
  - The gap is defined by the columns between the right edge of the left object and the left edge of the right object.
  - The rows to be filled span from the minimum row of both objects to the maximum row of both objects.
  - The gap columns are split roughly in half horizontally. Columns closer to the left object get its color, columns closer to the right object get its color. If the gap width is odd, the middle column remains the background color.
If vertically aligned:
  - The gap is defined by the rows between the bottom edge of the top object and the top edge of the bottom object.
  - The columns to be filled span from the minimum column of both objects to the maximum column of both objects.
  - The gap rows are split roughly in half vertically. Rows closer to the top object get its color (using ceiling division for the split), rows closer to the bottom object get its color (using floor division).
If exactly two objects are not found, or they are not aligned horizontally or vertically with a gap, the original grid is returned.
"""

def _find_objects(grid, background_color):
    """
    Finds contiguous objects of non-background colors in the grid using BFS.

    Args:
        grid (np.ndarray): The input grid.
        background_color (int): The background color.

    Returns:
        list: A list of dictionaries, each representing an object with
              'color', 'coords' (set of (r, c) tuples),
              'min_row', 'min_col', 'max_row', 'max_col'.
    """
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
    """
    Fills the gap between two aligned objects based on their colors and proximity,
    considering the combined bounding box of the objects.
    """
    # Initialize output_grid as a copy of the input
    output_grid = np.copy(input_grid)
    rows, cols = output_grid.shape

    # 1. Identify the background color (most frequent color)
    colors, counts = np.unique(input_grid, return_counts=True)
    if len(counts) > 0:
        background_color = colors[np.argmax(counts)]
    else: # Handle empty grid case
        return output_grid 

    # 2. Find all contiguous non-background objects
    objects = _find_objects(output_grid, background_color)

    # 3. Ensure exactly two objects are found
    if len(objects) != 2:
        return output_grid 

    obj1 = objects[0]
    obj2 = objects[1]
    
    # Extract bounding boxes
    bb1_min_row, bb1_min_col, bb1_max_row, bb1_max_col = obj1['min_row'], obj1['min_col'], obj1['max_row'], obj1['max_col']
    bb2_min_row, bb2_min_col, bb2_max_row, bb2_max_col = obj2['min_row'], obj2['min_col'], obj2['max_row'], obj2['max_col']

    # Calculate the union bounding box
    union_min_row = min(bb1_min_row, bb2_min_row)
    union_max_row = max(bb1_max_row, bb2_max_row)
    union_min_col = min(bb1_min_col, bb2_min_col)
    union_max_col = max(bb1_max_col, bb2_max_col)

    # 4. Determine alignment (Horizontal or Vertical)
    
    # Check for Horizontal Alignment: Separated columns, potentially overlapping rows
    # A gap must exist between the objects horizontally.
    col_separated_gap_exists = (bb1_max_col + 1 < bb2_min_col) or (bb2_max_col + 1 < bb1_min_col)

    if col_separated_gap_exists:
        # Identify Left and Right objects
        if bb1_min_col < bb2_min_col:
            left_obj = obj1
            right_obj = obj2
        else:
            left_obj = obj2
            right_obj = obj1
            
        # Calculate gap columns
        gap_start_col = left_obj['max_col'] + 1
        gap_end_col = right_obj['min_col'] - 1
        gap_width = gap_end_col - gap_start_col + 1

        # Check if the gap consists only of background color within the union rows
        is_gap_background = True
        if gap_width > 0:
            for r in range(union_min_row, union_max_row + 1):
                for c in range(gap_start_col, gap_end_col + 1):
                     if 0 <= r < rows and 0 <= c < cols: # Boundary check
                        if output_grid[r, c] != background_color:
                            is_gap_background = False
                            break
                if not is_gap_background:
                    break
        else: # No gap width means no horizontal alignment case to fill
             is_gap_background = False


        if gap_width > 0 and is_gap_background:
            # Calculate fill counts (integer division for floor)
            fill_count = gap_width // 2 
            
            # Fill left part of the gap within the union bounding box rows
            output_grid[union_min_row : union_max_row + 1, 
                        gap_start_col : gap_start_col + fill_count] = left_obj['color']
            
            # Fill right part of the gap within the union bounding box rows
            # Note: The start index calculation ensures the middle column is skipped if gap_width is odd
            output_grid[union_min_row : union_max_row + 1, 
                        gap_end_col - fill_count + 1 : gap_end_col + 1] = right_obj['color']
            
            # Successfully filled, return the result
            return output_grid 

    # Check for Vertical Alignment: Separated rows, potentially overlapping columns
    # A gap must exist between the objects vertically.
    row_separated_gap_exists = (bb1_max_row + 1 < bb2_min_row) or (bb2_max_row + 1 < bb1_min_row)
    
    if row_separated_gap_exists:
        # Identify Top and Bottom objects
        if bb1_min_row < bb2_min_row:
            top_obj = obj1
            bottom_obj = obj2
        else:
            top_obj = obj2
            bottom_obj = obj1

        # Calculate gap rows
        gap_start_row = top_obj['max_row'] + 1
        gap_end_row = bottom_obj['min_row'] - 1
        gap_height = gap_end_row - gap_start_row + 1

        # Check if the gap consists only of background color within the union columns
        is_gap_background = True
        if gap_height > 0:
            for r in range(gap_start_row, gap_end_row + 1):
                for c in range(union_min_col, union_max_col + 1):
                    if 0 <= r < rows and 0 <= c < cols: # Boundary check
                        if output_grid[r, c] != background_color:
                            is_gap_background = False
                            break
                if not is_gap_background:
                    break
        else: # No gap height means no vertical alignment case to fill
            is_gap_background = False

        if gap_height > 0 and is_gap_background:
            # Calculate fill counts using ceiling for top and floor for bottom
            top_fill_count = (gap_height + 1) // 2 
            bottom_fill_count = gap_height // 2
            
            # Fill top part of the gap within the union bounding box columns
            output_grid[gap_start_row : gap_start_row + top_fill_count, 
                        union_min_col : union_max_col + 1] = top_obj['color']
            
            # Fill bottom part of the gap within the union bounding box columns
            output_grid[gap_end_row - bottom_fill_count + 1 : gap_end_row + 1, 
                        union_min_col : union_max_col + 1] = bottom_obj['color']

            # Successfully filled, return the result
            return output_grid

    # 6. If no alignment or gap fill condition was met, return the original grid
    return output_grid