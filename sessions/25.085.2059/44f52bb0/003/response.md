```python
"""
Transformation Rule Natural Language Description:

1.  Identify Red Components: Find all distinct groups of connected red pixels (color 2) in the input grid. Connectivity includes horizontal, vertical, and diagonal neighbors (8-way connectivity).
2.  Count Components: Count the number of these distinct red groups.
3.  Determine Output based on Count and Symmetry:
    *   If the number of red components is greater than one, the output is a 1x1 grid containing a single blue pixel (color 1).
    *   If the number of red components is exactly one:
        *   Isolate the shape formed by the red pixels of this single component within its minimal bounding box.
        *   Check if this isolated shape has horizontal reflectional symmetry (looks the same when flipped top-to-bottom).
        *   Check if this isolated shape has vertical reflectional symmetry (looks the same when flipped left-to-right).
        *   If the shape possesses either horizontal or vertical symmetry (or both), the output is a 1x1 grid containing a single blue pixel (color 1).
        *   If the shape possesses neither horizontal nor vertical symmetry, the output is a 1x1 grid containing a single orange pixel (color 7).
    *   If the number of red components is zero, the output is a 1x1 grid containing a single blue pixel (color 1). (This handles cases not present in the examples, assuming a default behavior consistent with the multi-component rule).
4.  Produce Output: Create the 1x1 output grid with the determined color.
"""

import numpy as np
from collections import deque

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
                  Pixels belonging to the component have their original color, others are 0.
                  Returns an empty array if the component is empty.
    """
    if not component:
        # Return an empty array or handle as appropriate if an empty component is possible
        return np.array([[]], dtype=int) 

    rows = [r for r, c in component]
    cols = [c for r, c in component]
    
    min_r, max_r = min(rows), max(rows)
    min_c, max_c = min(cols), max(cols)
    
    height = max_r - min_r + 1
    width = max_c - min_c + 1
    
    shape_grid = np.zeros((height, width), dtype=int)
    
    target_color = grid[component[0][0], component[0][1]] # Get color from first pixel

    for r, c in component:
        # Place the target color in the relative position within the bounding box
        shape_grid[r - min_r, c - min_c] = target_color
        
    return shape_grid

def check_horizontal_symmetry(shape):
    """Checks for horizontal reflectional symmetry (flip top-to-bottom)."""
    if shape.size == 0: # Handle empty shape case
        return False 
    return np.array_equal(shape, np.flipud(shape))

def check_vertical_symmetry(shape):
    """Checks for vertical reflectional symmetry (flip left-to-right)."""
    if shape.size == 0: # Handle empty shape case
        return False
    return np.array_equal(shape, np.fliplr(shape))

def transform(input_grid):
    # Ensure input is a numpy array
    if not isinstance(input_grid, np.ndarray):
        input_grid = np.array(input_grid, dtype=int)
        
    # Define colors
    red_color = 2
    blue_color = 1
    orange_color = 7
    
    output_color = blue_color # Default output color

    # 1. Find connected components of red pixels
    components = find_connected_components(input_grid, red_color)

    # 2. Count the components
    num_components = len(components)

    # 3. Determine output based on count and symmetry
    if num_components == 1:
        # a. Isolate the shape
        single_component = components[0]
        shape = extract_component_shape(input_grid, single_component)

        # b. Check horizontal and vertical symmetries
        has_hor_sym = check_horizontal_symmetry(shape)
        has_ver_sym = check_vertical_symmetry(shape)

        # c. If NEITHER symmetry exists, output orange
        if not has_hor_sym and not has_ver_sym:
            output_color = orange_color
        # d. Otherwise (at least one symmetry exists), output remains blue (default)
        # else: output_color = blue_color (already default)

    # If num_components > 1 or num_components == 0, output remains blue (default)
    # else: output_color = blue_color (already default)

    # 4. Produce the 1x1 output grid
    output_grid = np.array([[output_color]], dtype=int)

    return output_grid
```