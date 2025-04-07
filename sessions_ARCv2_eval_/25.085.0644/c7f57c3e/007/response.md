```python
import numpy as np
from collections import Counter
import copy

"""
Applies a cyclical color transformation to three specific non-background colors, 
leaving other colors unchanged. The three colors are selected based on their 
object count (fewest first), total area (smallest first), and color value 
(highest first for ties). The cycle maps the first selected color (C1) to the 
third (C3), the second (C2) to the first (C1), and the third (C3) to the second (C2).

1. Determine the background color (most frequent).
2. Find all non-background colors, count their distinct objects (4-neighbor), 
   and calculate their total area.
3. Sort these colors by object count (asc), then area (asc), then color value (desc).
4. If fewer than three such colors exist, return the original grid.
5. Select the first three colors from the sorted list: C1, C2, C3.
6. Create a transformation mapping: C1 -> C3, C2 -> C1, C3 -> C2.
7. Apply this mapping to all pixels in the grid. Pixels not matching C1, C2, 
   or C3 remain unchanged.
"""

def find_objects(grid, color):
    """
    Finds all contiguous objects of a specific color in the grid using 4-neighbor adjacency.

    Args:
        grid (np.array): The input grid.
        color (int): The color of the objects to find.

    Returns:
        list: A list of objects, where each object is represented by a set
              of (row, col) tuples. Returns an empty list if the color
              is not found or forms no objects.
    """
    rows, cols = grid.shape
    visited = np.zeros_like(grid, dtype=bool)
    objects = []

    for r in range(rows):
        for c in range(cols):
            if grid[r, c] == color and not visited[r, c]:
                current_object = set()
                q = [(r, c)]
                visited[r, c] = True
                while q:
                    row, col = q.pop(0)
                    current_object.add((row, col))
                    # Check 4 neighbors (up, down, left, right)
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = row + dr, col + dc
                        if 0 <= nr < rows and 0 <= nc < cols and \
                           grid[nr, nc] == color and not visited[nr, nc]:
                            visited[nr, nc] = True
                            q.append((nr, nc))
                if current_object:
                    objects.append(current_object)
    return objects

def transform(input_grid):
    """
    Applies the cyclical color transformation based on object count, area, and color value.
    """
    # Convert input list of lists to numpy array
    input_array = np.array(input_grid, dtype=int)
    
    # Handle empty grid case
    if input_array.size == 0:
        return []
        
    rows, cols = input_array.shape

    # 1. Determine the background color
    flat_array = input_array.flatten()
    color_counts = Counter(flat_array)
    
    # Handle case with only one color
    if len(color_counts) <= 1:
        return input_grid # Return original grid
        
    background_color = color_counts.most_common(1)[0][0]

    # 2. Identify non-background colors and their properties
    color_properties = []
    for color, count in color_counts.items():
        if color != background_color:
            # 3. Count objects and get total area
            objects = find_objects(input_array, color)
            num_objects = len(objects)
            total_area = count # Total pixels of this color
            if num_objects > 0: # Only consider colors actually forming objects
                 # 4. Create list of properties
                 color_properties.append({'color': color, 'obj_count': num_objects, 'area': total_area})

    # 4 & 6. Check if at least three non-background colors exist
    if len(color_properties) < 3:
        return input_grid # Return original grid unchanged

    # 5. Sort the list of colors
    # Primary key: object count (ascending)
    # Secondary key: total area (ascending)
    # Tertiary key: color value (descending)
    color_properties.sort(key=lambda x: (x['obj_count'], x['area'], -x['color']))

    # 7. Select the first three colors
    color1_props = color_properties[0]
    color2_props = color_properties[1]
    color3_props = color_properties[2]

    c1 = color1_props['color']
    c2 = color2_props['color']
    c3 = color3_props['color']

    # 8. Create the transformation mapping
    transformation_map = {
        c1: c3,
        c2: c1,
        c3: c2
    }

    # 9. Create output grid and apply transformation
    output_array = np.copy(input_array)
    for r in range(rows):
        for c in range(cols):
            original_color = input_array[r, c]
            if original_color in transformation_map:
                output_array[r, c] = transformation_map[original_color]
            # else: color remains unchanged (already handled by copy)

    # 10. Return the modified grid as list of lists
    return output_array.tolist()

```