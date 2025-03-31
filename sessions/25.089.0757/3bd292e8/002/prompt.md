
Previous Code:
```python
import numpy as np
from collections import deque

"""
Transforms an input grid based on the adjacency of connected Orange (7) pixel components to Red (2) pixels.

1.  Identifies connected components of Orange (7) pixels using 4-way adjacency (up, down, left, right).
2.  For each Orange component:
    a.  Checks if any pixel within the component is 4-way adjacent to any Red (2) pixel in the input grid.
    b.  If adjacency is found, all pixels of that component are colored Green (3) in the output grid.
    c.  If no adjacency is found, all pixels of that component are colored Gray (5) in the output grid.
3.  Red (2) pixels remain unchanged in their original positions.
4.  The output grid has the same dimensions as the input grid.
"""

def find_connected_components(grid, target_color):
    """
    Finds all connected components of a target color in a grid using 4-way adjacency.

    Args:
        grid (np.ndarray): The input grid.
        target_color (int): The color of the pixels to form components from.

    Returns:
        list: A list where each element is a list of (row, col) tuples representing a connected component.
    """
    rows, cols = grid.shape
    visited = np.zeros_like(grid, dtype=bool)
    components = []

    for r in range(rows):
        for c in range(cols):
            # If it's the target color and not yet visited, start a BFS
            if grid[r, c] == target_color and not visited[r, c]:
                component = []
                q = deque([(r, c)])
                visited[r, c] = True

                while q:
                    row, col = q.popleft()
                    component.append((row, col))

                    # Check 4-way neighbors
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = row + dr, col + dc
                        # Check bounds, target color, and visited status
                        if 0 <= nr < rows and 0 <= nc < cols and \
                           grid[nr, nc] == target_color and not visited[nr, nc]:
                            visited[nr, nc] = True
                            q.append((nr, nc))
                
                if component:
                    components.append(component)
    return components

def is_adjacent_to_color(grid, component_pixels, check_color):
    """
    Checks if any pixel in a component is adjacent (4-way) to a pixel of a specific color.

    Args:
        grid (np.ndarray): The input grid.
        component_pixels (list): List of (row, col) tuples for the component.
        check_color (int): The color to check for adjacency.

    Returns:
        bool: True if any component pixel is adjacent to check_color, False otherwise.
    """
    rows, cols = grid.shape
    for r, c in component_pixels:
        # Check 4-way neighbors
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nr, nc = r + dr, c + dc
            # Check bounds and if the neighbor has the check_color
            if 0 <= nr < rows and 0 <= nc < cols and grid[nr, nc] == check_color:
                return True
    return False

def transform(input_grid):
    """
    Applies the transformation rule to the input grid.

    Args:
        input_grid (list of lists): The input grid represented as a list of lists.

    Returns:
        list of lists: The transformed output grid.
    """
    # Convert input to numpy array for easier manipulation
    input_np = np.array(input_grid, dtype=int)
    
    # Initialize output grid as a copy of the input
    output_grid = np.copy(input_np)
    
    # Define colors
    orange_color = 7
    red_color = 2
    green_color = 3
    gray_color = 5

    # Find all connected components of Orange pixels
    orange_components = find_connected_components(input_np, orange_color)

    # Process each Orange component
    for component in orange_components:
        # Check if the component is adjacent to any Red pixel
        adjacent_to_red = is_adjacent_to_color(input_np, component, red_color)

        # Determine the new color for this component
        new_color = green_color if adjacent_to_red else gray_color

        # Update the output grid for all pixels in this component
        for r, c in component:
            output_grid[r, c] = new_color
            
    # Red pixels inherently remain unchanged as they are copied initially 
    # and not part of the orange components being modified.

    # Convert back to list of lists for the expected output format
    return output_grid.tolist()
```
Results for code_00.py:

Train Set Results:

## Example 1:
Input:
```
7 7 2 7 7 7 7
7 7 2 2 2 7 7
7 7 7 7 2 7 7
2 2 7 7 2 2 2
7 2 7 7 7 7 7
7 2 2 2 2 7 7
7 7 7 7 2 7 7
```
Expected Output:
```
3 3 2 5 5 5 5
3 3 2 2 2 5 5
3 3 3 3 2 5 5
2 2 3 3 2 2 2
5 2 3 3 3 3 3
5 2 2 2 2 3 3
5 5 5 5 2 3 3
```
Transformed Output:
```
3 3 2 3 3 3 3
3 3 2 2 2 3 3
3 3 3 3 2 3 3
2 2 3 3 2 2 2
3 2 3 3 3 3 3
3 2 2 2 2 3 3
3 3 3 3 2 3 3
```
Match: False
Pixels Off: 14
Size Correct: True
Color Palette Correct: True
Color Count Correct: False
Score: 57.14285714285714

## Example 2:
Input:
```
2 7 7 7 7 7 7
2 7 7 7 7 7 7
2 7 7 7 7 7 7
2 2 2 7 7 7 7
7 7 2 7 7 7 7
7 7 2 2 2 7 7
7 7 7 7 2 2 2
```
Expected Output:
```
2 3 3 3 3 3 3
2 3 3 3 3 3 3
2 3 3 3 3 3 3
2 2 2 3 3 3 3
5 5 2 3 3 3 3
5 5 2 2 2 3 3
5 5 5 5 2 2 2
```
Transformed Output:
```
2 3 3 3 3 3 3
2 3 3 3 3 3 3
2 3 3 3 3 3 3
2 2 2 3 3 3 3
3 3 2 3 3 3 3
3 3 2 2 2 3 3
3 3 3 3 2 2 2
```
Match: False
Pixels Off: 8
Size Correct: True
Color Palette Correct: True
Color Count Correct: False
Score: 32.65306122448979

## Example 3:
Input:
```
7 7 7 7 7 2 7 7
7 7 7 7 7 2 7 7
2 2 2 2 7 2 7 7
7 7 7 2 7 2 7 7
7 7 7 2 7 2 7 7
2 2 7 2 7 2 2 7
7 2 7 2 7 7 2 2
7 2 7 2 7 7 7 7
```
Expected Output:
```
5 5 5 5 5 2 3 3
5 5 5 5 5 2 3 3
2 2 2 2 5 2 3 3
3 3 3 2 5 2 3 3
3 3 3 2 5 2 3 3
2 2 3 2 5 2 2 3
5 2 3 2 5 5 2 2
5 2 3 2 5 5 5 5
```
Transformed Output:
```
3 3 3 3 3 2 3 3
3 3 3 3 3 2 3 3
2 2 2 2 3 2 3 3
3 3 3 2 3 2 3 3
3 3 3 2 3 2 3 3
2 2 3 2 3 2 2 3
3 2 3 2 3 3 2 2
3 2 3 2 3 3 3 3
```
Match: False
Pixels Off: 22
Size Correct: True
Color Palette Correct: True
Color Count Correct: False
Score: 68.75
