import numpy as np
from collections import deque

"""
Identifies two distinct objects within a background color.
Determines if the objects are aligned horizontally or vertically with a gap of background color between their bounding boxes.
Fills the rectangular region defined by the gap rows/columns, extending across the full grid dimension orthogonal to the alignment, based on proximity to the objects.

If horizontally aligned:
  - The gap is defined by the columns between the right edge of the left object's bounding box and the left edge of the right object's bounding box.
  - The rows to be filled span the entire height of the grid (0 to grid_height - 1).
  - The gap columns are split roughly in half. Columns closer to the left object get its color, columns closer to the right object get its color. If the gap width is odd, the middle column remains the background color.

If vertically aligned:
  - The gap is defined by the rows between the bottom edge of the top object's bounding box and the top edge of the bottom object's bounding box.
  - The columns to be filled span the entire width of the grid (0 to grid_width - 1).
  - The gap rows are split roughly in half. Rows closer to the top object get its color (using ceiling division for the split), rows closer to the bottom object get its color (using floor division). If the gap height is odd, the middle row remains the background color.

If exactly two objects are not found, or they are not aligned horizontally or vertically with a gap between their bounding boxes, the original grid is returned.
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
    """
    Fills the gap between two aligned objects based on their colors and proximity,
    extending the fill across the full grid dimension orthogonal to the alignment.
    """
    # Initialize output_grid as a copy of the input
    output_grid = np.copy(input_grid)
    rows, cols = output_grid.shape

    # Handle empty grid case
    if input_grid.size == 0:
        return output_grid

    # 1. Identify the background color (most frequent color)
    colors, counts = np.unique(input_grid, return_counts=True)
    # Check if grid contains only one color or is empty
    if len(counts) == 0:
        return output_grid # Return unchanged if empty
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
    
    # 4. Determine alignment (Horizontal or Vertical) based on bounding box separation
    
    # Check for Horizontal Alignment: BBoxes separated by columns
    # Determine left and right objects first
    if obj1['min_col'] < obj2['min_col']:
        left_obj = obj1
        right_obj = obj2
    else:
        left_obj = obj2
        right_obj = obj1
    
    # Check if there's a horizontal gap
    if left_obj['max_col'] < right_obj['min_col']:
        gap_start_col = left_obj['max_col'] + 1
        gap_end_col = right_obj['min_col'] - 1
        gap_width = gap_end_col - gap_start_col + 1

        if gap_width > 0:
            # Calculate fill counts (integer division for floor)
            fill_count = gap_width // 2 
            
            # Fill left part of the gap across ALL rows
            output_grid[:, gap_start_col : gap_start_col + fill_count] = left_obj['color']
            
            # Fill right part of the gap across ALL rows
            # Note: The start index calculation ensures the middle column is skipped if gap_width is odd
            output_grid[:, gap_end_col - fill_count + 1 : gap_end_col + 1] = right_obj['color']
            
            # Successfully filled horizontally, return the result
            return output_grid 

    # Check for Vertical Alignment: BBoxes separated by rows
    # Determine top and bottom objects first
    if obj1['min_row'] < obj2['min_row']:
        top_obj = obj1
        bottom_obj = obj2
    else:
        top_obj = obj2
        bottom_obj = obj1

    # Check if there's a vertical gap
    if top_obj['max_row'] < bottom_obj['min_row']:
        gap_start_row = top_obj['max_row'] + 1
        gap_end_row = bottom_obj['min_row'] - 1
        gap_height = gap_end_row - gap_start_row + 1

        if gap_height > 0:
            # Calculate fill counts using ceiling for top and floor for bottom
            top_fill_count = (gap_height + 1) // 2 
            bottom_fill_count = gap_height // 2
            
            # Fill top part of the gap across ALL columns
            output_grid[gap_start_row : gap_start_row + top_fill_count, :] = top_obj['color']
            
            # Fill bottom part of the gap across ALL columns
            output_grid[gap_end_row - bottom_fill_count + 1 : gap_end_row + 1, :] = bottom_obj['color']

            # Successfully filled vertically, return the result
            return output_grid

    # 5. If no alignment or gap fill condition was met, return the original grid
    return output_grid