
Previous Code:
```python
"""
Transforms the input grid based on the following rules:
1. Identify all connected components of green pixels (value 3) using 4-way (von Neumann) adjacency.
2. Select components with a size (number of pixels) of 3 or more.
3. For each selected component:
    a. Check if it consists *exactly* of 5 pixels forming a 2x2 square plus one additional green pixel connected (4-way) to exactly one pixel of the square (a "tail").
    b. If it is the specific "2x2 plus tail" shape (size 5), mark only the 4 pixels forming the 2x2 square for color change.
    c. Otherwise (if the component size is >= 3 but not the specific "2x2 plus tail" shape), mark all pixels in the component for color change.
4. Change the color of all marked pixels from green (3) to azure (8).
"""

import numpy as np
from collections import deque
import itertools

def find_connected_components_4way(grid, target_color):
    """
    Finds all connected components of a specific color in a grid using 4-way connectivity.

    Args:
        grid (np.ndarray): The input grid.
        target_color (int): The color of the pixels to form components.

    Returns:
        list: A list of components, where each component is a list of (row, col) tuples.
    """
    rows, cols = grid.shape
    visited = np.zeros_like(grid, dtype=bool)
    components = []

    # Define 4 directions for neighbors (no diagonals)
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    for r in range(rows):
        for c in range(cols):
            # If we find a pixel of the target color that hasn't been visited
            if grid[r, c] == target_color and not visited[r, c]:
                current_component = []
                q = deque([(r, c)])
                visited[r, c] = True

                # Start Breadth-First Search (BFS)
                while q:
                    curr_r, curr_c = q.popleft()
                    current_component.append((curr_r, curr_c))

                    # Check all 4 neighbors
                    for dr, dc in directions:
                        nr, nc = curr_r + dr, curr_c + dc

                        # Check if neighbor is within bounds
                        if 0 <= nr < rows and 0 <= nc < cols:
                            # Check if neighbor is the target color and not visited
                            if grid[nr, nc] == target_color and not visited[nr, nc]:
                                visited[nr, nc] = True
                                q.append((nr, nc))
                
                # Add the found component to the list
                components.append(current_component)

    return components

def check_if_2x2(coords):
    """Checks if a set of 4 coordinates forms a 2x2 square."""
    if len(coords) != 4: 
        return False
    coords_set = set(coords)
    rows = sorted(list(set(r for r, c in coords_set)))
    cols = sorted(list(set(c for r, c in coords_set)))
    # Must have exactly 2 unique rows and 2 unique columns
    if len(rows) != 2 or len(cols) != 2: 
        return False
    # Rows must be adjacent, cols must be adjacent
    if rows[1] != rows[0] + 1 or cols[1] != cols[0] + 1: 
        return False
    # Check if all 4 combinations exist by reconstructing the square
    expected_coords = set([(r, c) for r in rows for c in cols])
    return coords_set == expected_coords

def count_4way_neighbors_in_set(pixel, target_set):
    """Counts how many 4-way neighbors of pixel are in target_set."""
    r, c = pixel
    count = 0
    neighbors = [(r - 1, c), (r + 1, c), (r, c - 1), (r, c + 1)]
    target_coords_set = set(target_set) # Ensure it's a set for efficient lookup
    for nr, nc in neighbors:
        if (nr, nc) in target_coords_set:
            count += 1
    return count

def is_2x2_plus_tail(component):
    """
    Checks if a component is exactly a 2x2 square plus a single pixel tail 
    connected to exactly one square pixel (4-way).
    
    Args:
        component (list): List of (row, col) tuples for the component pixels.

    Returns:
        tuple: (bool, list | None)
               - bool: True if it matches the pattern, False otherwise.
               - list | None: If True, returns the list of 4 coordinates 
                              forming the 2x2 square. Otherwise, None.
    """
    if len(component) != 5:
        return False, None
    
    component_set = set(component)
    
    # Iterate through all combinations of 4 pixels out of 5
    for square_candidate_tuple in itertools.combinations(component, 4):
        square_candidate_list = list(square_candidate_tuple)
        if check_if_2x2(square_candidate_list):
            # Found a potential 2x2 square within the component
            square_candidate_set = set(square_candidate_list)
            # Find the 5th pixel (tail)
            tail_pixel = (component_set - square_candidate_set).pop() 
            
            # Check if the tail is 4-way adjacent to exactly one pixel in the square
            neighbor_count = count_4way_neighbors_in_set(tail_pixel, square_candidate_set)
            
            if neighbor_count == 1:
                # Pattern matched!
                return True, square_candidate_list 
                
    # If no combination of 4 forms a square with the 5th attached correctly
    return False, None

def transform(input_grid):
    """
    Applies the transformation rule based on 4-way green components.
    Changes components >= size 3, with special handling for "2x2 plus tail" shape.
    """
    # Initialize output_grid as a copy of the input grid
    output_grid = np.copy(input_grid)
    
    # Define colors
    target_color = 3  # green
    replacement_color = 8  # azure

    # Find all 4-way connected components of green pixels
    components = find_connected_components_4way(output_grid, target_color)

    # Set to store coordinates of pixels to be changed
    pixels_to_change = set()

    # Process each component
    for component in components:
        # Only consider components of size 3 or more
        if len(component) >= 3:
            # Check for the special "2x2 plus tail" case (which requires size 5)
            is_special_case, square_pixels = is_2x2_plus_tail(component)
            
            if is_special_case:
                # If it's the special case, only mark the square pixels
                pixels_to_change.update(square_pixels)
            else:
                # Otherwise, mark all pixels in the component
                pixels_to_change.update(component)

    # Apply the color change to the marked pixels
    for r, c in pixels_to_change:
        # Ensure the pixel is actually green before changing (safety check)
        if output_grid[r, c] == target_color:
            output_grid[r, c] = replacement_color

    # Return the modified grid
    return output_grid
```
Results for code_00.py:

Train Set Results:

## Example 1:
Input:
```
3 3 0 3
3 3 0 0
3 0 0 3
0 0 3 3
```
Expected Output:
```
8 8 0 3
8 8 0 0
8 0 0 8
0 0 8 8
```
Transformed Output:
```
8 8 0 3
8 8 0 0
3 0 0 8
0 0 8 8
```
Match: False
Pixels Off: 1
Size Correct: True
Color Palette Correct: True
Color Count Correct: False
Score: 12.5

## Example 2:
Input:
```
0 3 0 0 0 3
0 3 3 3 0 0
0 0 0 0 3 0
0 3 0 0 0 0
```
Expected Output:
```
0 8 0 0 0 3
0 8 8 8 0 0
0 0 0 0 3 0
0 3 0 0 0 0
```
Transformed Output:
```
0 8 0 0 0 3
0 8 8 8 0 0
0 0 0 0 3 0
0 3 0 0 0 0
```
Match: True
Pixels Off: 0
Size Correct: True
Color Palette Correct: True
Color Count Correct: True
Score: 0

## Example 3:
Input:
```
3 3 0 0 0 0
0 3 0 0 3 0
3 0 0 0 0 0
0 3 3 0 0 0
0 3 3 0 0 3
```
Expected Output:
```
8 8 0 0 0 0
0 8 0 0 3 0
3 0 0 0 0 0
0 8 8 0 0 0
0 8 8 0 0 3
```
Transformed Output:
```
8 8 0 0 0 0
0 8 0 0 3 0
3 0 0 0 0 0
0 8 8 0 0 0
0 8 8 0 0 3
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
3 3 0
0 3 0
3 0 3
```
Expected Output:
```
8 8 0
0 8 0
3 0 3
```
Transformed Output:
```
8 8 0
0 8 0
3 0 3
```
Match: True
Pixels Off: 0
Size Correct: True
Color Palette Correct: True
Color Count Correct: True
Score: 0
## Assessment

The previous code correctly identified the core concept of finding connected green components and changing their color based on size. However, it derived an overly specific rule ("2x2 plus tail") from the first example, which caused it to fail on that same example while coincidentally working for the others.

The failure on Example 1, where the code *correctly* identified the "2x2 plus tail" shape but only colored the square part, while the expected output colored the entire shape, indicates that the special rule was incorrect. The success on the other examples suggests the underlying principle of component size is likely correct, but the special shape handling needs removal.

The simplest hypothesis that fits all examples is: Identify all 4-way connected green components. If a component consists of 3 or more pixels, change all pixels in that component to azure.

**Strategy:**
1.  Verify the component sizes for each input using 4-way connectivity.
2.  Confirm that changing all green pixels in components of size >= 3 to azure matches the expected output for all examples.
3.  Update the natural language program and facts based on this simpler, verified rule.

## Metrics Gathering

Let's analyze the green components (value 3) using 4-way connectivity in each training input.



*code_execution:*
```python
import numpy as np
from collections import deque

def find_connected_components_4way(grid, target_color):
    rows, cols = grid.shape
    visited = np.zeros_like(grid, dtype=bool)
    components = []
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    for r in range(rows):
        for c in range(cols):
            if grid[r, c] == target_color and not visited[r, c]:
                current_component = []
                q = deque([(r, c)])
                visited[r, c] = True
                while q:
                    curr_r, curr_c = q.popleft()
                    current_component.append((curr_r, curr_c))
                    for dr, dc in directions:
                        nr, nc = curr_r + dr, curr_c + dc
                        if 0 <= nr < rows and 0 <= nc < cols:
                            if grid[nr, nc] == target_color and not visited[nr, nc]:
                                visited[nr, nc] = True
                                q.append((nr, nc))
                components.append(current_component)
    return components

# Example Inputs
inputs = [
    np.array([[3, 3, 0, 3], [3, 3, 0, 0], [3, 0, 0, 3], [0, 0, 3, 3]]),
    np.array([[0, 3, 0, 0, 0, 3], [0, 3, 3, 3, 0, 0], [0, 0, 0, 0, 3, 0], [0, 3, 0, 0, 0, 0]]),
    np.array([[3, 3, 0, 0, 0, 0], [0, 3, 0, 0, 3, 0], [3, 0, 0, 0, 0, 0], [0, 3, 3, 0, 0, 0], [0, 3, 3, 0, 0, 3]]),
    np.array([[3, 3, 0], [0, 3, 0], [3, 0, 3]])
]

target_color = 3  # green

# Analyze components for each input
results = {}
for i, input_grid in enumerate(inputs):
    components = find_connected_components_4way(input_grid, target_color)
    component_sizes = [len(comp) for comp in components]
    results[f"Example {i+1}"] = {"component_sizes": component_sizes}

print(results)
```

*code_execution_result:*
outcome: 1
```
{'Example 1': {'component_sizes': [5, 1, 3]}, 'Example 2': {'component_sizes': [4, 1, 1, 1]}, 'Example 3': {'component_sizes': [3, 1, 1, 4, 1]}, 'Example 4': {'component_sizes': [3, 1, 1]}}

```
## Facts


```yaml
task_description: Identify specific groups of green pixels and change their color based on the group's size.

definitions:
  - object: Green Component
    description: A contiguous group of green (3) pixels connected using 4-way adjacency (up, down, left, right).
    properties:
      - size: The number of pixels in the component.

transformations:
  - action: Identify Green Components
    input: Input grid
    output: A list of Green Components.
    condition: Pixels must be green (3) and connected 4-way.

  - action: Filter Components by Size
    input: List of Green Components
    output: Filtered list of Green Components.
    condition: Component size must be greater than or equal to 3.

  - action: Change Color
    input: Filtered list of Green Components and the original grid.
    output: Modified grid.
    rule: For each pixel coordinate within the filtered components, change its color in the grid from green (3) to azure (8).
    condition: The pixel's original color is green.

constants:
  - input_color: green (3)
  - output_color: azure (8)
  - size_threshold: 3
  - connectivity: 4-way (von Neumann)
```


## Natural Language Program

1.  Identify all distinct groups (components) of connected green (3) pixels within the input grid. Connectivity is defined by 4-way adjacency (pixels sharing an edge, not just a corner).
2.  For each identified green component, count the number of pixels it contains (its size).
3.  Select only those green components whose size is 3 or more.
4.  Create the output grid by copying the input grid.
5.  For every pixel belonging to any of the selected components (those with size >= 3), change its color in the output grid from green (3) to azure (8).
6.  Leave all other pixels (pixels not part of a green component of size >= 3) unchanged from their original color in the input grid.
