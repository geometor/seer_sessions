
Previous Code:
```python
import numpy as np
from collections import deque

"""
Transformation rule:
1. Identify distinct contiguous shapes of non-white (0) and non-gray (5) colors in the input grid. These are "reference shapes". Store their relative pixel patterns (canonical forms) and their corresponding colors.
2. Identify distinct contiguous shapes of gray (5) color in the input grid. These are "target shapes". Store their relative pixel patterns (canonical forms) and the list of absolute pixel coordinates for each shape.
3. Initialize the output grid as a copy of the input grid.
4. For each identified target shape:
    a. Compare its canonical form with the canonical forms of all reference shapes.
    b. If a match is found with a reference shape's form, change the color of all pixels belonging to that target shape in the output grid to the color of the matching reference shape.
    c. If no match is found with any reference shape's form, change the color of all pixels belonging to that target shape in the output grid to the background color (white, 0).
5. Pixels that were not part of any gray target shape retain their original color from the input grid.
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
              'form': A tuple of sorted (dr, dc) tuples representing the
                      relative pixel coordinates (canonical form), normalized
                      to the top-leftmost pixel of the object.
    """
    rows, cols = grid.shape
    visited = np.zeros_like(grid, dtype=bool)
    objects = []
    
    for r in range(rows):
        for c in range(cols):
            color = grid[r, c]
            # Check if the current pixel matches one of the target colors and hasn't been visited
            if color in colors_to_find and not visited[r, c]:
                obj_pixels = [] # Store pixels belonging to the current object
                q = deque([(r, c)]) # Queue for BFS
                visited[r, c] = True
                min_r, min_c = r, c # Track the top-left corner for normalization
                
                # Use Breadth-First Search (BFS) to find all connected pixels of the same color
                while q:
                    row, col = q.popleft()
                    obj_pixels.append((row, col))
                    # Update the minimum row and column found so far
                    min_r = min(min_r, row)
                    min_c = min(min_c, col)
                    
                    # Explore 4 neighbors (up, down, left, right)
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = row + dr, col + dc
                        # Check if neighbor is within grid bounds
                        if 0 <= nr < rows and 0 <= nc < cols:
                           # Check if neighbor has the same color and hasn't been visited
                           if not visited[nr, nc] and grid[nr, nc] == color:
                                visited[nr, nc] = True
                                q.append((nr, nc))
                            
                # Calculate relative coordinates (form) normalized to the top-left corner (min_r, min_c)
                # Sort the relative coordinates to create a canonical representation of the shape
                relative_pixels = sorted([(p_r - min_r, p_c - min_c) for p_r, p_c in obj_pixels])
                # Convert to tuple for hashability (use as dictionary key)
                form = tuple(relative_pixels) 
                
                # Store the found object's details
                objects.append({
                    'color': color,
                    'pixels': obj_pixels, # Absolute coordinates
                    'form': form          # Canonical shape representation
                })
                
    return objects

def transform(input_grid):
    """
    Applies the transformation rule based on matching gray shapes to reference shapes.
    """
    # Initialize output_grid as a copy of the input grid.
    # Changes will be made directly to this copy.
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # 1. Identify reference shapes (all non-white, non-gray colors)
    # Determine all unique colors present in the grid
    all_colors = set(np.unique(input_grid))
    # Filter out white (0) and gray (5) to get the set of reference colors
    reference_colors = all_colors - {0, 5} 
    
    # Find all objects matching the reference colors
    # Handle edge case where there are no reference colors
    if not reference_colors:
        reference_objects = []
    else:
        reference_objects = find_objects(input_grid, reference_colors)
    
    # Store reference forms and their corresponding colors in a dictionary for quick lookup
    # The key is the canonical form (tuple of relative coordinates), value is the color.
    reference_forms = {obj['form']: obj['color'] for obj in reference_objects}

    # 2. Identify target shapes (gray color 5)
    # Find all objects with color 5 (gray)
    target_objects = find_objects(input_grid, {5})

    # 3. Iterate through target shapes and apply transformations based on form matching
    for target_obj in target_objects:
        target_form = target_obj['form'] # Get the canonical form of the gray shape
        
        # 4a. Compare target form with reference forms
        if target_form in reference_forms:
            # 4b. Match found: Recolor target shape with the matched reference color
            new_color = reference_forms[target_form]
            for r, c in target_obj['pixels']:
                 # Ensure coordinates are valid just in case (though BFS should keep them in bounds)
                 if 0 <= r < rows and 0 <= c < cols: 
                     output_grid[r, c] = new_color
        else:
            # 4c. No match found: Erase target shape (set to white, 0)
            new_color = 0 # Background color
            for r, c in target_obj['pixels']:
                 # Ensure coordinates are valid
                 if 0 <= r < rows and 0 <= c < cols:
                    output_grid[r, c] = new_color

    # 5. Pixels not part of a gray shape retain their original color (already handled by copying input)
    return output_grid
```
Results for code_00.py:

Train Set Results:

## Example 1:
Input:
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 4 4 4 0 3 3 3 0 1 1 1 1 1 0 2 2 2 2 2 2 2 0 0 0 0 0 0 0 0
0 4 4 4 0 3 0 3 0 1 0 1 0 1 0 2 0 2 0 2 0 2 0 0 0 0 0 0 0 0
0 4 4 4 0 3 3 3 0 1 1 1 1 1 0 2 2 2 2 2 2 2 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 5 5 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 5 5 5 0 0 0 5 5 5 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 5 5 0 5 5 0 5 5 5 5 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 5 5 0 5 5 0 5 5 0 0 0 0 0 0 0 0 0 0 5 5 5 5 5 5 0 0 0 0
0 0 0 5 5 5 5 0 0 0 0 0 5 5 0 0 0 0 0 5 5 0 0 0 5 5 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 5 5 5 0 0 0 0 5 5 5 5 5 5 5 0 0 0 0 0
0 0 0 0 0 0 0 0 0 5 5 5 5 5 0 0 0 5 5 0 0 0 5 5 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 5 5 5 5 0 0 0 0 5 5 5 5 5 5 5 0 0 0 0 0 0
0 0 0 0 0 5 0 0 0 0 0 0 0 0 0 0 0 0 5 5 5 0 0 0 0 0 0 0 0 0
0 0 0 5 5 5 5 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 5 0 0 5 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 5 5 5 5 0 0 0 0 0 0 0 5 5 0 0 0 0 0 0 0 0 5 5 5 5 0 0
0 0 0 5 5 5 0 0 0 0 0 0 5 5 5 5 5 0 0 0 0 0 5 5 5 0 5 5 0 0
0 0 0 0 0 0 0 0 0 0 0 0 5 0 5 0 5 0 0 0 0 5 5 5 5 0 0 5 0 0
0 0 0 0 0 0 5 5 5 5 0 0 5 5 5 5 5 5 0 0 0 5 5 0 5 5 5 5 0 0
0 0 0 0 0 5 5 5 0 5 0 0 5 0 5 5 5 0 0 0 0 5 5 0 0 5 5 5 0 0
0 0 0 5 5 5 5 5 0 5 0 0 5 5 5 0 0 0 0 0 0 0 5 5 5 5 5 0 0 0
0 0 5 5 5 5 0 5 5 5 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 5 5 0 5 0 5 5 5 0 0 0 0 0 0 0 5 5 5 0 0 0 0 0 0 0 0 0 0
0 0 5 5 5 5 5 5 5 5 0 0 0 0 0 0 5 5 5 5 5 5 0 0 0 0 0 0 0 0
0 0 5 5 0 5 5 5 5 0 0 0 0 0 0 0 5 5 5 5 5 5 0 0 0 0 0 0 0 0
0 0 0 5 5 5 5 5 0 0 0 0 0 0 0 0 0 5 5 5 0 0 0 0 0 0 0 0 0 0
```
Expected Output:
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 4 4 4 0 3 3 3 0 1 1 1 1 1 0 2 2 2 2 2 2 2 0 0 0 0 0 0 0 0
0 4 4 4 0 3 0 3 0 1 0 1 0 1 0 2 0 2 0 2 0 2 0 0 0 0 0 0 0 0
0 4 4 4 0 3 3 3 0 1 1 1 1 1 0 2 2 2 2 2 2 2 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 4 4 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 3 3 3 0 0 0 4 4 4 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 3 3 0 3 3 0 4 4 4 4 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 3 3 0 3 3 0 4 4 0 0 0 0 0 0 0 0 0 0 1 1 1 1 1 1 0 0 0 0
0 0 0 3 3 3 3 0 0 0 0 0 4 4 0 0 0 0 0 1 1 0 0 0 1 1 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 4 4 4 0 0 0 0 1 1 1 1 1 1 1 0 0 0 0 0
0 0 0 0 0 0 0 0 0 4 4 4 4 4 0 0 0 1 1 0 0 0 1 1 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 4 4 4 4 0 0 0 0 1 1 1 1 1 1 1 0 0 0 0 0 0
0 0 0 0 0 3 0 0 0 0 0 0 0 0 0 0 0 0 1 1 1 0 0 0 0 0 0 0 0 0
0 0 0 3 3 3 3 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 3 0 0 3 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 3 3 3 3 0 0 0 0 0 0 0 2 2 0 0 0 0 0 0 0 0 1 1 1 1 0 0
0 0 0 3 3 3 0 0 0 0 0 0 2 2 2 2 2 0 0 0 0 0 1 1 1 0 1 1 0 0
0 0 0 0 0 0 0 0 0 0 0 0 2 0 2 0 2 0 0 0 0 1 1 1 1 0 0 1 0 0
0 0 0 0 0 0 0 0 0 0 0 0 2 2 2 2 2 2 0 0 0 1 1 0 1 1 1 1 0 0
0 0 0 0 0 0 0 0 0 0 0 0 2 0 2 2 2 0 0 0 0 1 1 0 0 1 1 1 0 0
0 0 0 0 0 0 0 0 0 0 0 0 2 2 2 0 0 0 0 0 0 0 1 1 1 1 1 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 4 4 4 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 4 4 4 4 4 4 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 4 4 4 4 4 4 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 4 4 4 0 0 0 0 0 0 0 0 0 0
```
Transformed Output:
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 4 4 4 0 3 3 3 0 1 1 1 1 1 0 2 2 2 2 2 2 2 0 0 0 0 0 0 0 0
0 4 4 4 0 3 0 3 0 1 0 1 0 1 0 2 0 2 0 2 0 2 0 0 0 0 0 0 0 0
0 4 4 4 0 3 3 3 0 1 1 1 1 1 0 2 2 2 2 2 2 2 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```
Match: False
Pixels Off: 156
Size Correct: True
Color Palette Correct: True
Color Count Correct: False
Score: 34.66666666666666

## Example 2:
Input:
```
0 0 0 0 0 0 0 0 0 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 2 2 2 0 3 3 3 0 1 0 0 0 0 0 0 0 0 5 5 0 0 0 0 0 0 0 0 0 0
0 2 2 2 0 3 0 3 0 1 0 0 0 0 5 5 5 5 5 5 5 5 5 5 0 0 0 0 0 0
0 2 2 2 0 3 3 3 0 1 0 0 0 5 5 5 5 5 5 5 5 5 5 5 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 1 0 0 0 5 5 5 5 5 5 5 5 5 5 5 5 0 0 0 0 0
0 0 0 0 0 0 0 0 0 1 0 0 0 0 5 5 5 5 5 5 5 5 5 5 5 0 0 0 0 0
1 1 1 1 1 1 1 1 1 1 0 0 0 0 5 5 5 5 5 5 5 5 5 5 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 5 5 5 5 5 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 5 5 0 0
0 0 0 0 0 0 0 0 0 0 5 5 5 0 0 0 0 0 0 0 5 5 5 5 5 5 5 5 0 0
0 0 0 0 0 0 0 0 0 0 0 5 5 0 0 0 0 0 0 0 5 5 5 0 0 5 5 5 0 0
0 0 0 0 5 5 0 0 0 0 0 0 0 0 0 0 0 0 0 5 5 5 0 0 0 5 5 5 5 0
0 0 5 5 5 5 5 5 0 0 0 0 0 0 0 0 0 0 0 5 5 5 0 0 0 5 5 5 5 0
0 0 5 5 5 5 5 5 5 0 0 0 0 0 0 0 0 0 0 0 5 5 0 0 0 5 5 5 5 0
0 0 5 5 5 5 5 5 5 0 0 0 5 5 5 5 0 0 0 0 5 5 5 5 5 5 5 5 0 0
0 5 5 5 5 5 5 5 5 0 0 0 5 5 5 0 0 0 0 0 0 5 5 0 0 0 0 0 0 0
0 0 5 5 5 5 5 5 0 0 0 0 5 5 5 5 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 5 5 0 0 0 0 0 5 5 5 5 5 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 5 5 5 5 5 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 5 5 5 5 0 0 0 0 0 5 5 5 5 5 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 5 5 5 0 0 0 0 0 5 5 0 5 5 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 5 5 5 0 0 0 0 0 5 0 0 5 5 0 0 0 0 0
0 0 0 0 5 5 5 5 0 0 0 0 0 0 0 0 0 0 0 0 5 0 0 5 0 0 0 0 0 0
0 0 0 0 5 0 0 5 5 0 0 0 5 0 0 0 0 0 0 0 5 5 5 5 5 0 0 0 0 0
0 0 0 5 5 0 0 5 0 0 0 5 5 5 5 5 5 5 0 0 5 5 5 5 0 0 0 0 0 0
0 0 0 5 5 0 5 5 0 0 0 5 0 5 0 0 5 5 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 5 5 5 5 0 0 0 5 0 5 0 0 5 5 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 5 0 0 0 0 5 5 5 5 5 5 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 5 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```
Expected Output:
```
0 0 0 0 0 0 0 0 0 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 2 2 2 0 3 3 3 0 1 0 0 0 0 0 0 0 0 2 2 0 0 0 0 0 0 0 0 0 0
0 2 2 2 0 3 0 3 0 1 0 0 0 0 2 2 2 2 2 2 2 2 2 2 0 0 0 0 0 0
0 2 2 2 0 3 3 3 0 1 0 0 0 2 2 2 2 2 2 2 2 2 2 2 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 1 0 0 0 2 2 2 2 2 2 2 2 2 2 2 2 0 0 0 0 0
0 0 0 0 0 0 0 0 0 1 0 0 0 0 2 2 2 2 2 2 2 2 2 2 2 0 0 0 0 0
1 1 1 1 1 1 1 1 1 1 0 0 0 0 2 2 2 2 2 2 2 2 2 2 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 2 2 2 2 2 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 3 3 0 0
0 0 0 0 0 0 0 0 0 0 2 2 2 0 0 0 0 0 0 0 3 3 3 3 3 3 3 3 0 0
0 0 0 0 0 0 0 0 0 0 0 2 2 0 0 0 0 0 0 0 3 3 3 0 0 3 3 3 0 0
0 0 0 0 2 2 0 0 0 0 0 0 0 0 0 0 0 0 0 3 3 3 0 0 0 3 3 3 3 0
0 0 2 2 2 2 2 2 0 0 0 0 0 0 0 0 0 0 0 3 3 3 0 0 0 3 3 3 3 0
0 0 2 2 2 2 2 2 2 0 0 0 0 0 0 0 0 0 0 0 3 3 0 0 0 3 3 3 3 0
0 0 2 2 2 2 2 2 2 0 0 0 2 2 2 2 0 0 0 0 3 3 3 3 3 3 3 3 0 0
0 2 2 2 2 2 2 2 2 0 0 0 2 2 2 0 0 0 0 0 0 3 3 0 0 0 0 0 0 0
0 0 2 2 2 2 2 2 0 0 0 0 2 2 2 2 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 2 2 0 0 0 0 0 2 2 2 2 2 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 2 2 2 2 2 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 2 2 2 2 0 0 0 0 0 3 3 3 3 3 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 2 2 2 0 0 0 0 0 3 3 0 3 3 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 2 2 2 0 0 0 0 0 3 0 0 3 3 0 0 0 0 0
0 0 0 0 3 3 3 3 0 0 0 0 0 0 0 0 0 0 0 0 3 0 0 3 0 0 0 0 0 0
0 0 0 0 3 0 0 3 3 0 0 0 0 0 0 0 0 0 0 0 3 3 3 3 3 0 0 0 0 0
0 0 0 3 3 0 0 3 0 0 0 0 0 0 0 0 0 0 0 0 3 3 3 3 0 0 0 0 0 0
0 0 0 3 3 0 3 3 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 3 3 3 3 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 3 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```
Transformed Output:
```
0 0 0 0 0 0 0 0 0 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 2 2 2 0 3 3 3 0 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 2 2 2 0 3 0 3 0 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 2 2 2 0 3 3 3 0 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
1 1 1 1 1 1 1 1 1 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```
Match: False
Pixels Off: 223
Size Correct: True
Color Palette Correct: True
Color Count Correct: False
Score: 49.55555555555554
