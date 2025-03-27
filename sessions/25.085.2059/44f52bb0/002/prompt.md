
Previous Code:
```python
import numpy as np
from collections import deque

"""
Transformation Rule Natural Language Description:

1. Find all distinct groups of connected red pixels (color 2) in the input grid. Connectivity includes horizontal, vertical, and diagonal neighbors (8-way connectivity).
2. Count the number of these distinct groups (connected components).
3. If the number of groups is greater than one, the output is a 1x1 grid containing a single blue pixel (color 1).
4. If there is exactly one group:
    a. Isolate the shape formed by the red pixels of this single group, creating a minimal bounding box representation where red pixels are 2 and others are 0.
    b. Check if this isolated shape possesses any of the following symmetries:
        i. 180-degree rotational symmetry (looks the same when rotated 180 degrees).
        ii. Horizontal reflectional symmetry (looks the same when flipped top-to-bottom).
        iii. Vertical reflectional symmetry (looks the same when flipped left-to-right).
    c. If the shape has at least one of these symmetries, the output is a 1x1 grid containing a single blue pixel (color 1).
    d. If the shape has none of these symmetries, the output is a 1x1 grid containing a single orange pixel (color 7).
"""

def find_connected_components(grid, target_color):
    """
    Finds all connected components of a specified color in a grid using 8-way connectivity.

    Args:
        grid (np.array): The input grid.
        target_color (int): The color of the pixels to form components.

    Returns:
        list: A list of components, where each component is a list of (row, col) tuples.
    """
    rows, cols = grid.shape
    visited = np.zeros_like(grid, dtype=bool)
    components = []

    for r in range(rows):
        for c in range(cols):
            if grid[r, c] == target_color and not visited[r, c]:
                # Start BFS for a new component
                component = []
                q = deque([(r, c)])
                visited[r, c] = True

                while q:
                    curr_r, curr_c = q.popleft()
                    component.append((curr_r, curr_c))

                    # Check 8 neighbors (including diagonals)
                    for dr in [-1, 0, 1]:
                        for dc in [-1, 0, 1]:
                            if dr == 0 and dc == 0:
                                continue # Skip self

                            nr, nc = curr_r + dr, curr_c + dc

                            # Check bounds, target color, and visited status
                            if 0 <= nr < rows and 0 <= nc < cols and \
                               grid[nr, nc] == target_color and not visited[nr, nc]:
                                visited[nr, nc] = True
                                q.append((nr, nc))
                
                if component:
                    components.append(component)
    return components

def extract_component_shape(grid, component):
    """
    Extracts the minimal bounding box shape of a component.

    Args:
        grid (np.array): The original input grid (needed for color).
        component (list): A list of (row, col) tuples for the component.

    Returns:
        np.array: A minimal grid representing the component's shape.
                  Pixels belonging to the component have their original color (usually 2), others are 0.
    """
    if not component:
        return np.array([[]])

    rows = [r for r, c in component]
    cols = [c for r, c in component]
    
    min_r, max_r = min(rows), max(rows)
    min_c, max_c = min(cols), max(cols)
    
    height = max_r - min_r + 1
    width = max_c - min_c + 1
    
    shape_grid = np.zeros((height, width), dtype=int)
    
    for r, c in component:
        # Use the original color from the grid, assuming it's the target color
        shape_grid[r - min_r, c - min_c] = grid[r, c] 
        
    return shape_grid

def check_rotational_symmetry_180(shape):
    """Checks for 180-degree rotational symmetry."""
    return np.array_equal(shape, np.rot90(shape, 2))

def check_horizontal_symmetry(shape):
    """Checks for horizontal reflectional symmetry (flip top-to-bottom)."""
    return np.array_equal(shape, np.flipud(shape))

def check_vertical_symmetry(shape):
    """Checks for vertical reflectional symmetry (flip left-to-right)."""
    return np.array_equal(shape, np.fliplr(shape))

def transform(input_grid):
    """
    Applies the transformation rule based on connected components of red pixels and their symmetry.

    Args:
        input_grid (np.array): The input grid as a NumPy array.

    Returns:
        np.array: A 1x1 output grid containing either 1 (blue) or 7 (orange).
    """
    
    # Convert input list of lists to numpy array if it's not already
    if not isinstance(input_grid, np.ndarray):
        input_grid = np.array(input_grid, dtype=int)
        
    red_color = 2
    blue_color = 1
    orange_color = 7

    # 1. Find connected components of red pixels
    components = find_connected_components(input_grid, red_color)

    # 2. Count the components
    num_components = len(components)

    # 3. If more than one component, output blue
    if num_components > 1:
        output_grid = np.array([[blue_color]], dtype=int)
    # 4. If exactly one component, check symmetry
    elif num_components == 1:
        # a. Isolate the shape
        single_component = components[0]
        shape = extract_component_shape(input_grid, single_component)

        # b. Check symmetries
        has_rot_sym = check_rotational_symmetry_180(shape)
        has_hor_sym = check_horizontal_symmetry(shape)
        has_ver_sym = check_vertical_symmetry(shape)

        # c. If any symmetry exists, output blue
        if has_rot_sym or has_hor_sym or has_ver_sym:
            output_grid = np.array([[blue_color]], dtype=int)
        # d. If no symmetry exists, output orange
        else:
            output_grid = np.array([[orange_color]], dtype=int)
    # Handle the case where there are no red pixels (although not present in examples, good practice)
    else: 
        # Default or based on further rules if needed. Let's assume blue based on multi-component logic extension.
        # Or maybe it should be an empty grid or a specific color? The examples don't cover this.
        # Given the pattern, >1 is blue, 1 with symmetry is blue, 1 without is orange. 0 could be argued as blue (not asymmetric single).
        # Let's default to blue for now.
        output_grid = np.array([[blue_color]], dtype=int) 


    return output_grid
```
Results for code_00.py:

Train Set Results:

## Example 1:
Input:
```
0 0 0
2 0 2
0 0 0
```
Expected Output:
```
1
```
Transformed Output:
```
1
```
Match: True
Pixels Off: 0
Size Correct: True
Color Palette Correct: True
Color Count Correct: True
Score: 0

## Example 2:
Input:
```
2 2 0
0 2 2
0 0 0
```
Expected Output:
```
7
```
Transformed Output:
```
1
```
Match: False
Pixels Off: 1
Size Correct: True
Color Palette Correct: False
Color Count Correct: False
Score: 400.0

## Example 3:
Input:
```
2 2 0
0 2 0
0 0 0
```
Expected Output:
```
7
```
Transformed Output:
```
7
```
Match: True
Pixels Off: 0
Size Correct: True
Color Palette Correct: True
Color Count Correct: True
Score: 0

## Example 4:
Input:
```
2 0 0
2 0 0
0 2 0
```
Expected Output:
```
7
```
Transformed Output:
```
7
```
Match: True
Pixels Off: 0
Size Correct: True
Color Palette Correct: True
Color Count Correct: True
Score: 0

## Example 5:
Input:
```
2 0 2
2 0 2
2 0 2
```
Expected Output:
```
1
```
Transformed Output:
```
1
```
Match: True
Pixels Off: 0
Size Correct: True
Color Palette Correct: True
Color Count Correct: True
Score: 0

## Example 6:
Input:
```
2 0 2
0 2 0
2 0 2
```
Expected Output:
```
1
```
Transformed Output:
```
1
```
Match: True
Pixels Off: 0
Size Correct: True
Color Palette Correct: True
Color Count Correct: True
Score: 0
