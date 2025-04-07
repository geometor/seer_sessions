```python
import numpy as np
from collections import deque

"""
Transformation rule:
1. Identify distinct contiguous shapes of non-white (0) and non-gray (5) colors in the input grid. These are "reference shapes". Store their relative pixel patterns (forms) and colors.
2. Identify distinct contiguous shapes of gray (5) color in the input grid. These are "target shapes".
3. For each target shape:
    a. Compare its relative pixel pattern (form) with the forms of all reference shapes.
    b. If a match is found with a reference shape, change the color of all pixels belonging to that target shape in the output grid to the color of the matching reference shape.
    c. If no match is found, change the color of all pixels belonging to that target shape in the output grid to the background color (white, 0).
4. All pixels not part of a gray target shape retain their original color in the output grid.
"""

def find_objects(grid, colors_to_find):
    """
    Finds all contiguous objects of specified colors in the grid.

    Args:
        grid (np.array): The input grid.
        colors_to_find (set): A set of color values to search for.

    Returns:
        list: A list of dictionaries, where each dictionary represents an object
              and contains:
              'color': The color of the object.
              'pixels': A list of (row, col) tuples for the object's pixels.
              'form': A tuple of sorted (row, col) tuples representing the
                      relative pixel coordinates (canonical form).
    """
    rows, cols = grid.shape
    visited = np.zeros_like(grid, dtype=bool)
    objects = []
    
    for r in range(rows):
        for c in range(cols):
            color = grid[r, c]
            if color in colors_to_find and not visited[r, c]:
                obj_pixels = []
                q = deque([(r, c)])
                visited[r, c] = True
                min_r, min_c = r, c
                
                # Use BFS to find all connected pixels of the same color
                while q:
                    row, col = q.popleft()
                    obj_pixels.append((row, col))
                    min_r = min(min_r, row)
                    min_c = min(min_c, col)
                    
                    # Check 4 neighbors (up, down, left, right)
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = row + dr, col + dc
                        if 0 <= nr < rows and 0 <= nc < cols and \
                           not visited[nr, nc] and grid[nr, nc] == color:
                            visited[nr, nc] = True
                            q.append((nr, nc))
                            
                # Calculate relative coordinates (form)
                relative_pixels = sorted([(p_r - min_r, p_c - min_c) for p_r, p_c in obj_pixels])
                form = tuple(relative_pixels) # Use tuple for hashability
                
                objects.append({
                    'color': color,
                    'pixels': obj_pixels,
                    'form': form
                })
                
    return objects

def transform(input_grid):
    """
    Applies the transformation rule to the input grid.
    """
    # Initialize output_grid as a copy of the input
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # 1. Identify reference shapes (all non-white, non-gray colors)
    all_colors = set(np.unique(input_grid))
    reference_colors = all_colors - {0, 5} # Exclude white (0) and gray (5)
    
    # Handle edge case where there are no reference colors
    if not reference_colors:
        # If no references, all gray shapes become white
        reference_objects = []
    else:
        reference_objects = find_objects(input_grid, reference_colors)
    
    # Store reference forms and their colors
    reference_forms = {obj['form']: obj['color'] for obj in reference_objects}

    # 2. Identify target shapes (gray color 5)
    target_objects = find_objects(input_grid, {5})

    # 3. Iterate through target shapes and apply transformations
    for target_obj in target_objects:
        target_form = target_obj['form']
        matched = False
        
        # Check if the target form matches any reference form
        if target_form in reference_forms:
            # Match found: Recolor target shape with reference color
            new_color = reference_forms[target_form]
            for r, c in target_obj['pixels']:
                if 0 <= r < rows and 0 <= c < cols: # Ensure coordinates are valid
                     output_grid[r, c] = new_color
            matched = True
            
        if not matched:
            # No match found: Erase target shape (set to white 0)
            for r, c in target_obj['pixels']:
                 if 0 <= r < rows and 0 <= c < cols: # Ensure coordinates are valid
                    output_grid[r, c] = 0

    # 4. Pixels not part of a gray shape retain their original color (already handled by copying)
    return output_grid
```