```python
import numpy as np
from collections import deque

"""
Identifies distinct non-white shapes in the input grid. Groups these shapes into 
horizontal rows based on vertical overlap. For each row, determines the colors 
of the shapes, ordered left-to-right. Reverses this order for each row. 
Determines the maximum number of shapes in any row (`max_width`). Creates an 
output grid where each row corresponds to an input row group. Each output row 
contains the reversed color sequence. If a row has fewer colors than `max_width`, 
it's padded at the beginning (left) with the first color of its reversed sequence 
(which corresponds to the rightmost shape in the original input row).
"""

def find_objects(grid):
    """
    Finds all contiguous objects of the same non-background color in the grid.

    Args:
        grid (np.array): The input grid.

    Returns:
        list: A list of dictionaries, each representing an object with its 
              color, pixels, and bounding box.
    """
    rows, cols = grid.shape
    visited = np.zeros_like(grid, dtype=bool)
    objects = []
    
    for r in range(rows):
        for c in range(cols):
            color = grid[r, c]
            # Check for non-background color and if not visited
            if color != 0 and not visited[r, c]:
                obj_pixels = set()
                q = deque([(r, c)])
                visited[r, c] = True
                min_r, max_r = r, r
                min_c, max_c = c, c
                
                while q:
                    curr_r, curr_c = q.popleft()
                    obj_pixels.add((curr_r, curr_c))
                    
                    # Update bounding box
                    min_r = min(min_r, curr_r)
                    max_r = max(max_r, curr_r)
                    min_c = min(min_c, curr_c)
                    max_c = max(max_c, curr_c)
                    
                    # Explore neighbors (4-connectivity)
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = curr_r + dr, curr_c + dc
                        
                        # Check bounds, color match, and visited status
                        if 0 <= nr < rows and 0 <= nc < cols and \
                           grid[nr, nc] == color and not visited[nr, nc]:
                            visited[nr, nc] = True
                            q.append((nr, nc))
                            
                objects.append({
                    'color': color,
                    'pixels': obj_pixels,
                    'min_row': min_r,
                    'max_row': max_r,
                    'min_col': min_c,
                    'max_col': max_c
                })
                
    return objects

def group_objects_by_row(objects):
    """
    Groups objects into rows based on vertical overlap.

    Args:
        objects (list): A list of object dictionaries.

    Returns:
        list: A list of lists, where each inner list contains objects 
              belonging to the same conceptual row, ordered top-to-bottom.
    """
    if not objects:
        return []

    # Sort objects primarily by top row, then left column
    objects.sort(key=lambda o: (o['min_row'], o['min_col']))

    rows_of_objects = []
    current_row = []

    for obj in objects:
        # Check if the object belongs to the current row being built
        belongs_to_current = False
        if not current_row:
            # First object starts the first row
            belongs_to_current = True
        else:
            # Check for vertical overlap with ANY object already in the current row
            for existing_obj in current_row:
                # Vertical overlap condition
                if max(obj['min_row'], existing_obj['min_row']) <= min(obj['max_row'], existing_obj['max_row']):
                    belongs_to_current = True
                    break 
        
        if belongs_to_current:
            current_row.append(obj)
        else:
            # Finalize the previous row
            if current_row:
                 # Sort the completed row by min_col before adding
                current_row.sort(key=lambda o: o['min_col'])
                rows_of_objects.append(current_row)
            # Start a new row with the current object
            current_row = [obj]

    # Add the last row after the loop finishes
    if current_row:
        # Sort the final row by min_col before adding
        current_row.sort(key=lambda o: o['min_col'])
        rows_of_objects.append(current_row)
        
    return rows_of_objects


def transform(input_grid):
    """
    Transforms the input grid based on identified object rows.

    Args:
        input_grid (list): A list of lists representing the input grid.

    Returns:
        list: A list of lists representing the transformed output grid.
    """
    input_np = np.array(input_grid, dtype=int)

    # 1. Identify all distinct, contiguous, non-white shapes
    objects = find_objects(input_np)
    
    # 2. Group the identified shapes into horizontal "rows"
    #    The grouping function already orders rows top-to-bottom implicitly by processing sorted objects.
    object_rows = group_objects_by_row(objects)

    # 3. For each group (row), get the list of colors (sorted left-to-right by default from grouping)
    color_rows = []
    max_width = 0
    for row in object_rows:
        # Objects within each row are already sorted by min_col in group_objects_by_row
        colors = [obj['color'] for obj in row]
        color_rows.append(colors)
        max_width = max(max_width, len(colors))

    # 4. Determine output dimensions
    output_height = len(color_rows)
    if output_height == 0: # Handle empty input case
        return [] 
        
    # 5. Initialize output grid
    output_np = np.zeros((output_height, max_width), dtype=int)

    # 6. Process each row for the output
    for i, colors in enumerate(color_rows):
        # a. Reverse the order of colors
        reversed_colors = colors[::-1]
        
        # b. Get current width
        current_width = len(reversed_colors)
        
        # c. Pad if necessary
        if current_width < max_width:
            if not reversed_colors: # Handle case of an empty row (shouldn't happen with current logic but good practice)
                 padding_color = 0 # Default to background if row was empty
            else:
                padding_color = reversed_colors[0] # Padding color is the first in reversed list
            
            padding = [padding_color] * (max_width - current_width)
            final_row_colors = padding + reversed_colors
        else:
            final_row_colors = reversed_colors
            
        # d. Place into output grid
        output_np[i, :] = final_row_colors

    # 7. Return the completed output grid as a list of lists
    return output_np.tolist()

```