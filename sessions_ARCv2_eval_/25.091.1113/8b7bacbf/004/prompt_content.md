
Previous Code:
```python
import numpy as np
from collections import deque

"""
Transformation Rule:
1. Initialize the output grid as a copy of the input grid.
2. Scan the input grid to find the unique 'fill color' pixel (either yellow/4 or orange/7). Store this fill color.
3. Find all connected components (regions) of white (0) pixels in the input grid.
4. For each white component:
    a. Check if the component touches the grid edge. If it does, ignore it.
    b. Determine all pixels immediately adjacent (up, down, left, right) to the component that are *not* part of the component itself. These are the boundary neighbors.
    c. Check if all boundary neighbors exist and have the *exact same* single non-white color. Store this boundary color. If not uniform or if white, ignore the component.
    d. Apply a filter based on the fill color and the boundary color:
        i. If the fill color is orange (7), the component is only valid if its boundary color is red (2) or gray (5).
        ii. If the fill color is yellow (4), the component is only valid if its boundary color is red (2).
    e. If the component is valid (passes edge check, uniform non-white boundary check, and the filter check), then change the color of all pixels belonging to this component in the *output* grid to the stored 'fill color'.
5. Return the modified output grid.
"""

def find_fill_color(grid):
    """Scans the grid to find the unique yellow (4) or orange (7) pixel."""
    height, width = grid.shape
    for r in range(height):
        for c in range(width):
            pixel_color = grid[r, c]
            if pixel_color == 4 or pixel_color == 7:
                return pixel_color
    # Fallback, though examples suggest a fill color always exists
    return -1 # Use -1 to indicate not found, distinct from valid colors

def get_neighbors(r, c, height, width):
    """Gets valid adjacent neighbor coordinates (up, down, left, right)."""
    neighbors = []
    if r > 0: neighbors.append((r - 1, c))
    if r < height - 1: neighbors.append((r + 1, c))
    if c > 0: neighbors.append((r, c - 1))
    if c < width - 1: neighbors.append((r, c + 1))
    return neighbors

def find_connected_components(grid, color_to_find):
    """Finds all connected components of a specific color using BFS."""
    height, width = grid.shape
    visited = np.zeros_like(grid, dtype=bool)
    components = []

    for r in range(height):
        for c in range(width):
            if grid[r, c] == color_to_find and not visited[r, c]:
                # Start BFS for a new component
                component = set()
                q = deque([(r, c)])
                visited[r, c] = True
                component.add((r, c))

                while q:
                    row, col = q.popleft()
                    for nr, nc in get_neighbors(row, col, height, width):
                        if grid[nr, nc] == color_to_find and not visited[nr, nc]:
                            visited[nr, nc] = True
                            component.add((nr, nc))
                            q.append((nr, nc))
                
                components.append(component)
    return components

def check_enclosure_and_filter(component, grid, fill_color):
    """
    Checks if a component of white pixels is enclosed by a single non-white color,
    does not touch the grid edge, and meets the color filter criteria.
    Returns True if enclosed and filtered, False otherwise.
    """
    height, width = grid.shape
    boundary_colors = set()
    first_boundary_color = -1 # Initialize
    touches_edge = False
    has_boundary_neighbors = False

    for r, c in component:
        # Check if the component pixel is on the edge
        if r == 0 or r == height - 1 or c == 0 or c == width - 1:
            touches_edge = True
            # Can stop checking edges, but still need to find boundary colors
            # Break here is only safe if we don't care about boundary color yet.
            # Let's continue to find all boundary colors for the uniformity check.

        # Find neighbors of the current component pixel
        for nr, nc in get_neighbors(r, c, height, width):
            # If the neighbor is NOT part of the component, it's a boundary neighbor
            if (nr, nc) not in component:
                has_boundary_neighbors = True
                neighbor_color = grid[nr, nc]
                boundary_colors.add(neighbor_color)
                if first_boundary_color == -1:
                    first_boundary_color = neighbor_color

    # Condition 1: Must not touch the edge
    if touches_edge:
        return False
        
    # Condition 2: Must have boundary neighbors
    if not has_boundary_neighbors:
        return False

    # Condition 3: All boundary neighbors must have the same color, and it must not be white (0)
    is_uniform_non_white = len(boundary_colors) == 1 and 0 not in boundary_colors
    if not is_uniform_non_white:
        return False
        
    # If conditions 1, 2, 3 are met, proceed to filter
    boundary_color = first_boundary_color # Since it's uniform, first one is the one

    # Condition 4: Apply color filter
    if fill_color == 7: # Orange fill
        if boundary_color == 2 or boundary_color == 5: # Red or Gray boundary
            return True
    elif fill_color == 4: # Yellow fill
        if boundary_color == 2: # Red boundary only
            return True

    # If filter conditions are not met
    return False


def transform(input_grid):
    """
    Applies the transformation rule: finds the fill color (orange/yellow),
    identifies white regions enclosed by specific boundary colors (depending on fill color),
    and fills those regions with the fill color.
    """
    # Convert input to numpy array for easier manipulation
    grid = np.array(input_grid, dtype=int)
    output_grid = grid.copy()
    height, width = grid.shape

    # Step 1: Find the fill color
    fill_color = find_fill_color(grid)
    if fill_color == -1: # Handle case where fill color isn't found
         print("Warning: Fill color (4 or 7) not found in input grid.")
         return output_grid.tolist() 

    # Step 2: Find all connected components of white (0) pixels
    white_components = find_connected_components(grid, 0)

    # Step 3 & 4: Check each white component for enclosure, filter, and fill if necessary
    for component in white_components:
        # Check enclosure conditions and color filter
        if check_enclosure_and_filter(component, grid, fill_color):
            # Step 5: Fill the valid enclosed region in the output grid
            for r, c in component:
                output_grid[r, c] = fill_color

    # Return the modified grid as a list of lists
    return output_grid.tolist()
```
Results for code_00.py:

Train Set Results:

## Example 1:
Input:
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 5 5 0 0
0 2 2 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 5 0 0 5 0
2 0 0 2 0 0 0 0 0 2 2 0 0 0 0 0 0 0 0 5 0 0 5 0
2 0 0 2 0 0 0 0 2 0 0 2 0 0 0 0 0 0 0 1 5 5 1 0
0 2 2 1 0 0 0 0 2 0 0 2 0 0 0 0 0 2 1 0 0 0 1 0
0 0 0 0 1 1 1 1 1 2 2 1 0 0 0 0 2 0 2 2 0 0 1 0
0 0 0 0 0 0 0 0 0 0 0 1 0 0 0 2 0 0 0 0 2 0 1 0
0 0 0 0 0 0 1 1 1 1 1 0 0 0 0 0 2 0 0 2 2 0 1 0
0 0 0 0 0 1 0 0 0 0 0 0 0 0 0 0 1 2 2 0 0 0 1 0
0 0 0 1 1 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0 0 0 1 0
0 0 0 0 0 0 0 3 3 0 0 0 0 0 0 0 1 0 0 0 0 0 1 0
0 0 0 0 0 0 3 0 0 3 0 0 0 2 2 1 0 0 0 0 0 0 1 0
0 0 0 0 0 0 3 0 0 3 0 0 2 0 0 2 0 0 0 0 0 0 1 0
0 0 0 1 0 0 1 3 3 1 1 1 2 0 0 2 0 0 0 0 0 0 1 0
0 0 0 1 1 1 0 0 0 0 0 2 0 0 0 2 0 0 0 0 0 0 1 0
0 0 0 0 0 0 0 0 0 0 0 2 0 0 2 0 0 0 0 0 0 0 1 0
0 0 0 0 0 0 0 0 0 0 0 0 2 2 0 0 0 0 0 0 0 0 1 1
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 7
```
Expected Output:
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 5 5 0 0
0 2 2 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 5 7 7 5 0
2 0 0 2 0 0 0 0 0 2 2 0 0 0 0 0 0 0 0 5 7 7 5 0
2 0 0 2 0 0 0 0 2 0 0 2 0 0 0 0 0 0 0 1 5 5 1 0
0 2 2 1 0 0 0 0 2 0 0 2 0 0 0 0 0 2 1 0 0 0 1 0
0 0 0 0 1 1 1 1 1 2 2 1 0 0 0 0 2 7 2 2 0 0 1 0
0 0 0 0 0 0 0 0 0 0 0 1 0 0 0 2 7 7 7 7 2 0 1 0
0 0 0 0 0 0 1 1 1 1 1 0 0 0 0 0 2 7 7 2 2 0 1 0
0 0 0 0 0 1 0 0 0 0 0 0 0 0 0 0 1 2 2 0 0 0 1 0
0 0 0 1 1 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0 0 0 1 0
0 0 0 0 0 0 0 3 3 0 0 0 0 0 0 0 1 0 0 0 0 0 1 0
0 0 0 0 0 0 3 7 7 3 0 0 0 2 2 1 0 0 0 0 0 0 1 0
0 0 0 0 0 0 3 7 7 3 0 0 2 7 7 2 0 0 0 0 0 0 1 0
0 0 0 1 0 0 1 3 3 1 1 1 2 7 7 2 0 0 0 0 0 0 1 0
0 0 0 1 1 1 0 0 0 0 0 2 7 7 7 2 0 0 0 0 0 0 1 0
0 0 0 0 0 0 0 0 0 0 0 2 7 7 2 0 0 0 0 0 0 0 1 0
0 0 0 0 0 0 0 0 0 0 0 0 2 2 0 0 0 0 0 0 0 0 1 1
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 7
```
Transformed Output:
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 5 5 0 0
0 2 2 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 5 7 7 5 0
2 7 7 2 0 0 0 0 0 2 2 0 0 0 0 0 0 0 0 5 7 7 5 0
2 7 7 2 0 0 0 0 2 7 7 2 0 0 0 0 0 0 0 1 5 5 1 0
0 2 2 1 0 0 0 0 2 7 7 2 0 0 0 0 0 2 1 0 0 0 1 0
0 0 0 0 1 1 1 1 1 2 2 1 0 0 0 0 2 7 2 2 0 0 1 0
0 0 0 0 0 0 0 0 0 0 0 1 0 0 0 2 7 7 7 7 2 0 1 0
0 0 0 0 0 0 1 1 1 1 1 0 0 0 0 0 2 7 7 2 2 0 1 0
0 0 0 0 0 1 0 0 0 0 0 0 0 0 0 0 1 2 2 0 0 0 1 0
0 0 0 1 1 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0 0 0 1 0
0 0 0 0 0 0 0 3 3 0 0 0 0 0 0 0 1 0 0 0 0 0 1 0
0 0 0 0 0 0 3 0 0 3 0 0 0 2 2 1 0 0 0 0 0 0 1 0
0 0 0 0 0 0 3 0 0 3 0 0 2 7 7 2 0 0 0 0 0 0 1 0
0 0 0 1 0 0 1 3 3 1 1 1 2 7 7 2 0 0 0 0 0 0 1 0
0 0 0 1 1 1 0 0 0 0 0 2 7 7 7 2 0 0 0 0 0 0 1 0
0 0 0 0 0 0 0 0 0 0 0 2 7 7 2 0 0 0 0 0 0 0 1 0
0 0 0 0 0 0 0 0 0 0 0 0 2 2 0 0 0 0 0 0 0 0 1 1
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 7
```
Match: False
Pixels Off: 12
Size Correct: True
Color Palette Correct: True
Color Count Correct: False
Score: 5.555555555555571

## Example 2:
Input:
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 2 2 0 0 0 0 0 0 0 2 2 0 0
0 0 0 2 2 0 2 0 0 2 0 0 0 0 0 2 0 0 2 0
0 0 2 0 0 2 2 0 0 2 0 0 2 2 0 2 0 0 2 0
0 0 2 0 0 2 1 2 2 0 0 2 0 0 2 0 2 2 1 0
0 0 0 2 2 1 1 1 0 0 0 2 0 0 2 0 0 1 0 0
0 0 0 1 0 0 0 0 1 1 0 0 2 2 0 0 1 0 0 0
0 0 0 1 0 0 0 0 0 1 1 0 0 0 0 1 0 0 0 0
0 0 1 1 0 0 0 0 0 0 1 1 0 0 1 0 0 0 0 0
0 0 1 0 0 0 0 0 0 0 0 1 1 1 0 0 0 2 2 0
1 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 2 0 0 2
4 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 2 0 0 2
```
Expected Output:
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 2 2 0 0 0 0 0 0 0 2 2 0 0
0 0 0 2 2 0 2 4 4 2 0 0 0 0 0 2 4 4 2 0
0 0 2 4 4 2 2 4 4 2 0 0 2 2 0 2 4 4 2 0
0 0 2 4 4 2 1 2 2 0 0 2 0 0 2 0 2 2 1 0
0 0 0 2 2 1 1 1 0 0 0 2 0 0 2 0 0 1 0 0
0 0 0 1 0 0 0 0 1 1 0 0 2 2 0 0 1 0 0 0
0 0 0 1 0 0 0 0 0 1 1 0 0 0 0 1 0 0 0 0
0 0 1 1 0 0 0 0 0 0 1 1 0 0 1 0 0 0 0 0
0 0 1 0 0 0 0 0 0 0 0 1 1 1 0 0 0 2 2 0
1 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 2 0 0 2
4 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 2 0 0 2
```
Transformed Output:
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 2 2 0 0 0 0 0 0 0 2 2 0 0
0 0 0 2 2 0 2 4 4 2 0 0 0 0 0 2 4 4 2 0
0 0 2 4 4 2 2 4 4 2 0 0 2 2 0 2 4 4 2 0
0 0 2 4 4 2 1 2 2 0 0 2 4 4 2 0 2 2 1 0
0 0 0 2 2 1 1 1 0 0 0 2 4 4 2 0 0 1 0 0
0 0 0 1 0 0 0 0 1 1 0 0 2 2 0 0 1 0 0 0
0 0 0 1 0 0 0 0 0 1 1 0 0 0 0 1 0 0 0 0
0 0 1 1 0 0 0 0 0 0 1 1 0 0 1 0 0 0 0 0
0 0 1 0 0 0 0 0 0 0 0 1 1 1 0 0 0 2 2 0
1 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 2 0 0 2
4 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 2 0 0 2
```
Match: False
Pixels Off: 4
Size Correct: True
Color Palette Correct: True
Color Count Correct: False
Score: 3.333333333333343

## Example 3:
Input:
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 2 2
0 0 2 2 0 0 0 0 0 0 0 2 2 0 0 0 0 2 0 0
0 2 0 0 2 0 0 0 0 0 2 0 0 2 0 0 0 2 0 0
0 2 0 0 2 0 0 0 0 0 2 0 0 2 0 0 0 3 2 2
0 1 2 2 1 1 1 1 1 1 1 2 2 1 0 0 0 3 0 0
0 1 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0 3 0 0
0 0 1 0 0 0 0 0 0 0 0 0 1 0 0 0 0 0 3 0
1 1 0 0 0 0 0 2 2 1 1 1 0 0 0 0 2 2 3 0
0 1 0 0 0 0 2 0 0 2 0 0 0 0 0 2 0 0 2 0
1 1 0 0 0 0 2 0 0 2 0 0 0 0 0 2 0 0 2 0
0 0 0 0 0 0 1 2 2 0 0 0 0 0 0 3 2 2 0 0
0 0 0 0 0 1 0 0 0 0 0 0 0 0 0 3 0 0 0 0
0 0 0 0 1 0 0 0 0 0 0 3 3 2 2 3 0 0 0 0
0 0 2 2 1 0 0 0 0 0 3 0 2 0 0 2 0 0 0 0
0 2 0 0 2 0 0 0 3 3 3 0 2 0 0 2 0 0 0 0
0 2 0 0 2 0 0 0 3 4 3 0 0 2 2 0 0 0 0 0
```
Expected Output:
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 2 2
0 0 2 2 0 0 0 0 0 0 0 2 2 0 0 0 0 2 4 4
0 2 0 0 2 0 0 0 0 0 2 0 0 2 0 0 0 2 4 4
0 2 0 0 2 0 0 0 0 0 2 0 0 2 0 0 0 3 2 2
0 1 2 2 1 1 1 1 1 1 1 2 2 1 0 0 0 3 0 0
0 1 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0 3 0 0
0 0 1 0 0 0 0 0 0 0 0 0 1 0 0 0 0 0 3 0
1 1 0 0 0 0 0 2 2 1 1 1 0 0 0 0 2 2 3 0
0 1 0 0 0 0 2 0 0 2 0 0 0 0 0 2 4 4 2 0
1 1 0 0 0 0 2 0 0 2 0 0 0 0 0 2 4 4 2 0
0 0 0 0 0 0 1 2 2 0 0 0 0 0 0 3 2 2 0 0
0 0 0 0 0 1 0 0 0 0 0 0 0 0 0 3 0 0 0 0
0 0 0 0 1 0 0 0 0 0 0 3 3 2 2 3 0 0 0 0
0 0 2 2 1 0 0 0 0 0 3 0 2 4 4 2 0 0 0 0
0 2 0 0 2 0 0 0 3 3 3 0 2 4 4 2 0 0 0 0
0 2 0 0 2 0 0 0 3 4 3 0 0 2 2 0 0 0 0 0
```
Transformed Output:
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 2 2
0 0 2 2 0 0 0 0 0 0 0 2 2 0 0 0 0 2 0 0
0 2 4 4 2 0 0 0 0 0 2 4 4 2 0 0 0 2 0 0
0 2 4 4 2 0 0 0 0 0 2 4 4 2 0 0 0 3 2 2
0 1 2 2 1 1 1 1 1 1 1 2 2 1 0 0 0 3 0 0
0 1 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0 3 0 0
0 0 1 0 0 0 0 0 0 0 0 0 1 0 0 0 0 0 3 0
1 1 0 0 0 0 0 2 2 1 1 1 0 0 0 0 2 2 3 0
0 1 0 0 0 0 2 4 4 2 0 0 0 0 0 2 4 4 2 0
1 1 0 0 0 0 2 4 4 2 0 0 0 0 0 2 4 4 2 0
0 0 0 0 0 0 1 2 2 0 0 0 0 0 0 3 2 2 0 0
0 0 0 0 0 1 0 0 0 0 0 0 0 0 0 3 0 0 0 0
0 0 0 0 1 0 0 0 0 0 0 3 3 2 2 3 0 0 0 0
0 0 2 2 1 0 0 0 0 0 3 0 2 4 4 2 0 0 0 0
0 2 0 0 2 0 0 0 3 3 3 0 2 4 4 2 0 0 0 0
0 2 0 0 2 0 0 0 3 4 3 0 0 2 2 0 0 0 0 0
```
Match: False
Pixels Off: 16
Size Correct: True
Color Palette Correct: True
Color Count Correct: False
Score: 10.0

## Example 4:
Input:
```
0 0 2 2 0 0 0 0
0 2 0 0 2 0 0 0
0 2 0 0 2 0 0 0
0 0 2 2 0 1 0 0
0 0 0 0 0 0 1 0
0 0 0 0 0 1 0 0
0 0 0 0 0 0 1 1
0 0 0 0 0 0 1 4
```
Expected Output:
```
0 0 2 2 0 0 0 0
0 2 4 4 2 0 0 0
0 2 4 4 2 0 0 0
0 0 2 2 0 1 0 0
0 0 0 0 0 0 1 0
0 0 0 0 0 1 0 0
0 0 0 0 0 0 1 1
0 0 0 0 0 0 1 4
```
Transformed Output:
```
0 0 2 2 0 0 0 0
0 2 4 4 2 0 0 0
0 2 4 4 2 0 0 0
0 0 2 2 0 1 0 0
0 0 0 0 0 0 1 0
0 0 0 0 0 1 0 0
0 0 0 0 0 0 1 1
0 0 0 0 0 0 1 4
```
Match: True
Pixels Off: 0
Size Correct: True
Color Palette Correct: True
Color Count Correct: True
Score: 0
