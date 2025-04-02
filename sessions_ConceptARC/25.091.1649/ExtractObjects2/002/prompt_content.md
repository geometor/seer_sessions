
Previous Code:
```python
import numpy as np
from collections import deque

"""
Identify the unique non-white color C such that all pixels of color C in the input grid form exactly one connected object (using 8-way adjacency).
Determine the bounding box of this single object.
Create an output grid sized to this bounding box.
Populate the output grid: place the target color C at the relative positions corresponding to the object's pixels in the input, and fill the rest with white (0).
"""

def find_objects(grid, color):
    """
    Finds all connected objects of a specific color in a grid using 8-way adjacency.

    Args:
        grid (np.array): The input grid.
        color (int): The color of the objects to find.

    Returns:
        list[set]: A list where each element is a set of (row, col) tuples
                   representing the coordinates of a single connected object.
    """
    rows, cols = grid.shape
    visited = np.zeros_like(grid, dtype=bool)
    objects = []

    # Define 8-way neighbors (including diagonals)
    neighbors = [(-1, -1), (-1, 0), (-1, 1),
                 (0, -1),           (0, 1),
                 (1, -1), (1, 0), (1, 1)]

    for r in range(rows):
        for c in range(cols):
            # If it's the target color and not yet visited, start a search (BFS)
            if grid[r, c] == color and not visited[r, c]:
                current_object = set()
                q = deque([(r, c)])
                visited[r, c] = True

                while q:
                    curr_r, curr_c = q.popleft()
                    current_object.add((curr_r, curr_c))

                    # Explore neighbors
                    for dr, dc in neighbors:
                        nr, nc = curr_r + dr, curr_c + dc

                        # Check bounds
                        if 0 <= nr < rows and 0 <= nc < cols:
                            # Check if neighbor is the target color and not visited
                            if grid[nr, nc] == color and not visited[nr, nc]:
                                visited[nr, nc] = True
                                q.append((nr, nc))
                
                # Add the found object to the list
                objects.append(current_object)

    return objects

def transform(input_grid):
    """
    Transforms the input grid based on the described logic.

    Args:
        input_grid (list[list[int]]): The input grid.

    Returns:
        list[list[int]]: The transformed output grid.
    """
    input_array = np.array(input_grid, dtype=int)
    rows, cols = input_array.shape
    
    # Find unique non-white colors
    unique_colors = np.unique(input_array)
    non_white_colors = unique_colors[unique_colors != 0]

    target_color = -1
    target_object_coords = None

    # Identify the target color (forms exactly one object)
    for color in non_white_colors:
        objects = find_objects(input_array, color)
        if len(objects) == 1:
            target_color = color
            target_object_coords = objects[0] # Get the set of coordinates
            break # Found the target color

    # Handle case where no suitable object is found (shouldn't happen based on examples)
    if target_color == -1 or not target_object_coords:
        # Return an empty grid or raise an error, depending on requirements
        # For now, return a 1x1 white grid as a placeholder
        return [[0]] 

    # Determine the bounding box of the target object
    min_row = rows
    max_row = -1
    min_col = cols
    max_col = -1
    for r, c in target_object_coords:
        min_row = min(min_row, r)
        max_row = max(max_row, r)
        min_col = min(min_col, c)
        max_col = max(max_col, c)

    # Calculate output grid dimensions
    output_height = max_row - min_row + 1
    output_width = max_col - min_col + 1

    # Create the output grid, initialized with white (0)
    output_array = np.zeros((output_height, output_width), dtype=int)

    # Populate the output grid
    for r, c in target_object_coords:
        # Calculate relative coordinates within the bounding box
        relative_r = r - min_row
        relative_c = c - min_col
        # Place the target color in the output grid
        output_array[relative_r, relative_c] = target_color

    # Convert the output numpy array back to a list of lists
    output_grid = output_array.tolist()

    return output_grid
```
Results for code_00.py:

Train Set Results:

## Example 1:
Input:
```
1 1 1 1 1 1 1 1 1 1 1 1 1 1
0 0 0 0 0 0 0 0 0 0 0 0 0 0
1 1 1 1 1 1 1 1 1 1 1 1 1 1
0 0 0 0 0 3 0 0 0 0 0 0 0 0
1 1 1 1 3 1 3 1 1 1 1 1 1 1
0 0 0 3 0 0 0 3 0 0 0 0 0 0
1 1 3 1 1 1 1 1 3 1 1 1 1 1
0 0 0 3 0 0 0 3 0 0 0 0 0 0
1 1 1 1 3 1 3 1 1 1 1 1 1 1
0 0 0 0 0 3 0 0 0 0 0 0 0 0
1 1 1 1 1 1 1 1 1 1 1 1 1 1
0 0 0 0 0 0 0 0 0 0 0 0 0 0
1 1 1 1 1 1 1 1 1 1 1 1 1 1
0 0 0 0 0 0 0 0 0 0 0 0 0 0
```
Expected Output:
```
0 0 0 3 0 0 0
0 0 3 0 3 0 0
0 3 0 0 0 3 0
3 0 0 0 0 0 3
0 3 0 0 0 3 0
0 0 3 0 3 0 0
0 0 0 3 0 0 0
```
Transformed Output:
```
0 0 0 3 0 0 0
0 0 3 0 3 0 0
0 3 0 0 0 3 0
3 0 0 0 0 0 3
0 3 0 0 0 3 0
0 0 3 0 3 0 0
0 0 0 3 0 0 0
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
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
2 0 2 0 2 0 2 0 2 0 2 0 2 0 2 0
0 2 0 2 0 2 0 2 0 2 0 2 0 2 0 2
0 0 0 9 9 9 9 9 0 0 0 0 0 0 0 0
4 0 4 9 4 0 4 9 4 0 4 0 4 0 4 0
0 4 0 9 0 4 0 9 0 4 0 4 0 4 0 4
0 0 0 9 0 0 0 9 0 0 0 0 0 0 0 0
6 0 6 9 9 9 9 9 6 0 6 0 6 0 6 0
0 6 0 6 0 6 0 6 0 6 0 6 0 6 0 6
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
8 0 8 0 8 0 8 0 8 0 8 0 8 0 8 0
0 8 0 8 0 8 0 8 0 8 0 8 0 8 0 8
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
5 0 5 0 5 0 5 0 5 0 5 0 5 0 5 0
0 5 0 5 0 5 0 5 0 5 0 5 0 5 0 5
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```
Expected Output:
```
9 9 9 9 9
9 0 0 0 9
9 0 0 0 9
9 0 0 0 9
9 9 9 9 9
```
Transformed Output:
```
2 0 2 0 2 0 2 0 2 0 2 0 2 0 2 0
0 2 0 2 0 2 0 2 0 2 0 2 0 2 0 2
```
Match: False
Pixels Off: None
Size Correct: False
Color Palette Correct: False
Color Count Correct: False
Score: None

## Example 3:
Input:
```
0 0 0 0 0 0 0 0 0 0 0
4 0 0 0 4 0 0 0 4 0 0
0 4 0 4 0 4 0 4 0 4 0
0 0 4 0 0 0 4 0 0 0 4
4 0 0 6 6 6 0 0 4 0 0
0 4 0 4 0 6 0 4 0 4 0
0 0 4 0 0 6 4 0 0 0 4
4 0 0 6 6 6 0 0 0 0 0
0 4 0 4 0 4 0 0 0 4 0
0 0 4 0 0 0 4 0 4 0 4
0 0 0 0 0 0 0 4 0 0 0
```
Expected Output:
```
6 6 6
0 0 6
0 0 6
6 6 6
```
Transformed Output:
```
6 6 6
0 0 6
0 0 6
6 6 6
```
Match: True
Pixels Off: 0
Size Correct: True
Color Palette Correct: True
Color Count Correct: True
Score: 0
