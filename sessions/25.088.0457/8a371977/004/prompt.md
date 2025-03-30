
Previous Code:
```python
import numpy as np
from collections import deque

"""
Recolor connected components of white pixels (0) based on their adjacency to the grid's border.

1. Initialize the output grid as a copy of the input grid.
2. Create a 'visited' grid to track processed white pixels.
3. Iterate through each pixel (r, c) of the input grid.
4. If a pixel is white (0) and hasn't been visited:
    a. Start a search (e.g., Breadth-First Search) to find all connected white pixels forming a component. Use 8-way adjacency (including diagonals).
    b. Keep track of all coordinates belonging to this component.
    c. During the search, determine if *any* pixel within the component is adjacent to the grid's absolute border (row 0, row H-1, col 0, or col W-1). Set a flag `is_border_adjacent` if this occurs.
    d. Mark all pixels in the component as visited.
    e. After finding the complete component:
        i. If `is_border_adjacent` is True, change the color of all pixels in this component in the output grid to red (2).
        ii. If `is_border_adjacent` is False, change the color of all pixels in this component in the output grid to green (3).
5. Pixels that were not white initially remain unchanged.
6. Return the modified output grid.
"""

def _is_valid(r, c, height, width):
    """Checks if coordinates are within grid bounds."""
    return 0 <= r < height and 0 <= c < width

def _is_border_pixel(r, c, height, width):
    """Checks if a pixel coordinate is on the absolute border."""
    return r == 0 or r == height - 1 or c == 0 or c == width - 1

def transform(input_grid):
    """
    Transforms the input grid by recoloring connected components of white pixels.
    Components adjacent to the border become red (2).
    Components not adjacent to the border become green (3).
    Other pixels remain unchanged.
    """
    # Convert input to numpy array for efficient operations
    input_array = np.array(input_grid, dtype=int)
    height, width = input_array.shape
    
    # Initialize output_grid as a copy of the input
    output_array = np.copy(input_array)
    
    # Keep track of visited white pixels to avoid processing components multiple times
    visited = np.zeros_like(input_array, dtype=bool)

    # Iterate through each pixel of the grid
    for r in range(height):
        for c in range(width):
            # Check if the current pixel is white (0) and hasn't been processed yet
            if input_array[r, c] == 0 and not visited[r, c]:
                
                # Found the start of a new white component, perform BFS
                component_coords = []
                is_component_border_adjacent = False
                q = deque([(r, c)])
                visited[r, c] = True

                while q:
                    curr_r, curr_c = q.popleft()
                    component_coords.append((curr_r, curr_c))

                    # Check if this specific pixel is adjacent to the border
                    # Optimization: only need to check once per component
                    if not is_component_border_adjacent:
                        # Check 8 neighbours of the current pixel
                        for dr in [-1, 0, 1]:
                            for dc in [-1, 0, 1]:
                                if dr == 0 and dc == 0:
                                    continue
                                nr, nc = curr_r + dr, curr_c + dc
                                # Check if the neighbour coordinate itself is a border coordinate
                                # We don't care about the neighbour's color, just its position
                                if _is_border_pixel(nr, nc, height, width):
                                    # Check if the border pixel is *actually* a border pixel,
                                    # not just out of bounds. A simple way is to check if the current
                                    # pixel itself is one step away from the edge.
                                    if curr_r == 1 or curr_r == height - 2 or curr_c == 1 or curr_c == width - 2:
                                      is_component_border_adjacent = True
                                      # No need to check further neighbours for *this* pixel
                                      # but continue BFS to find rest of component
                                      # break # Incorrect place to break inner loop
                                # No need for inner breaks, just set the flag once

                    # Explore neighbours for BFS continuation
                    for dr in [-1, 0, 1]:
                        for dc in [-1, 0, 1]:
                            if dr == 0 and dc == 0:
                                continue
                            
                            nr, nc = curr_r + dr, curr_c + dc
                            
                            # Check if the neighbour is valid, is white, and not visited
                            if _is_valid(nr, nc, height, width) and \
                               input_array[nr, nc] == 0 and \
                               not visited[nr, nc]:
                                
                                visited[nr, nc] = True
                                q.append((nr, nc))

                # After BFS, determine the color for the entire component
                target_color = 2 if is_component_border_adjacent else 3
                
                # Apply the color to all pixels in the found component
                for comp_r, comp_c in component_coords:
                    output_array[comp_r, comp_c] = target_color
            
            # If pixel is not white or already visited, do nothing

    # Convert the numpy array back to a list of lists for the expected output format
    return output_array.tolist()

```
Results for code_00.py:

Train Set Results:

## Example 1:
Input:
```
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
```
Expected Output:
```
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
1 2 1 2 1 2 1 2 1 2 1 2 1 2 1 2 1 2 1 2 1 2 1
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
1 2 1 3 1 3 1 3 1 3 1 3 1 3 1 3 1 3 1 3 1 2 1
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
1 2 1 3 1 3 1 3 1 3 1 3 1 3 1 3 1 3 1 3 1 2 1
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
1 2 1 3 1 3 1 3 1 3 1 3 1 3 1 3 1 3 1 3 1 2 1
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
1 2 1 3 1 3 1 3 1 3 1 3 1 3 1 3 1 3 1 3 1 2 1
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
1 2 1 3 1 3 1 3 1 3 1 3 1 3 1 3 1 3 1 3 1 2 1
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
1 2 1 3 1 3 1 3 1 3 1 3 1 3 1 3 1 3 1 3 1 2 1
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
1 2 1 3 1 3 1 3 1 3 1 3 1 3 1 3 1 3 1 3 1 2 1
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
1 2 1 3 1 3 1 3 1 3 1 3 1 3 1 3 1 3 1 3 1 2 1
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
1 2 1 3 1 3 1 3 1 3 1 3 1 3 1 3 1 3 1 3 1 2 1
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
1 2 1 2 1 2 1 2 1 2 1 2 1 2 1 2 1 2 1 2 1 2 1
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
```
Transformed Output:
```
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
1 2 1 2 1 2 1 2 1 2 1 2 1 2 1 2 1 2 1 2 1 2 1
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
1 2 1 3 1 3 1 3 1 3 1 3 1 3 1 3 1 3 1 3 1 2 1
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
1 2 1 3 1 3 1 3 1 3 1 3 1 3 1 3 1 3 1 3 1 2 1
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
1 2 1 3 1 3 1 3 1 3 1 3 1 3 1 3 1 3 1 3 1 2 1
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
1 2 1 3 1 3 1 3 1 3 1 3 1 3 1 3 1 3 1 3 1 2 1
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
1 2 1 3 1 3 1 3 1 3 1 3 1 3 1 3 1 3 1 3 1 2 1
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
1 2 1 3 1 3 1 3 1 3 1 3 1 3 1 3 1 3 1 3 1 2 1
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
1 2 1 3 1 3 1 3 1 3 1 3 1 3 1 3 1 3 1 3 1 2 1
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
1 2 1 3 1 3 1 3 1 3 1 3 1 3 1 3 1 3 1 3 1 2 1
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
1 2 1 3 1 3 1 3 1 3 1 3 1 3 1 3 1 3 1 3 1 2 1
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
1 2 1 2 1 2 1 2 1 2 1 2 1 2 1 2 1 2 1 2 1 2 1
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
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
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
1 0 0 0 0 1 1 0 0 0 0 1 1 0 0 0 0 1 1
1 0 0 0 0 1 1 0 0 0 0 1 1 0 0 0 0 1 1
1 0 0 0 0 1 1 0 0 0 0 1 1 0 0 0 0 1 1
1 0 0 0 0 1 1 0 0 0 0 1 1 0 0 0 0 1 1
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
1 0 0 0 0 1 1 0 0 0 0 1 1 0 0 0 0 1 1
1 0 0 0 0 1 1 0 0 0 0 1 1 0 0 0 0 1 1
1 0 0 0 0 1 1 0 0 0 0 1 1 0 0 0 0 1 1
1 0 0 0 0 1 1 0 0 0 0 1 1 0 0 0 0 1 1
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
1 0 0 0 0 1 1 0 0 0 0 1 1 0 0 0 0 1 1
1 0 0 0 0 1 1 0 0 0 0 1 1 0 0 0 0 1 1
1 0 0 0 0 1 1 0 0 0 0 1 1 0 0 0 0 1 1
1 0 0 0 0 1 1 0 0 0 0 1 1 0 0 0 0 1 1
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
```
Expected Output:
```
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
1 2 2 2 2 1 1 2 2 2 2 1 1 2 2 2 2 1 1
1 2 2 2 2 1 1 2 2 2 2 1 1 2 2 2 2 1 1
1 2 2 2 2 1 1 2 2 2 2 1 1 2 2 2 2 1 1
1 2 2 2 2 1 1 2 2 2 2 1 1 2 2 2 2 1 1
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
1 2 2 2 2 1 1 3 3 3 3 1 1 2 2 2 2 1 1
1 2 2 2 2 1 1 3 3 3 3 1 1 2 2 2 2 1 1
1 2 2 2 2 1 1 3 3 3 3 1 1 2 2 2 2 1 1
1 2 2 2 2 1 1 3 3 3 3 1 1 2 2 2 2 1 1
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
1 2 2 2 2 1 1 2 2 2 2 1 1 2 2 2 2 1 1
1 2 2 2 2 1 1 2 2 2 2 1 1 2 2 2 2 1 1
1 2 2 2 2 1 1 2 2 2 2 1 1 2 2 2 2 1 1
1 2 2 2 2 1 1 2 2 2 2 1 1 2 2 2 2 1 1
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
```
Transformed Output:
```
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
1 2 2 2 2 1 1 2 2 2 2 1 1 2 2 2 2 1 1
1 2 2 2 2 1 1 2 2 2 2 1 1 2 2 2 2 1 1
1 2 2 2 2 1 1 2 2 2 2 1 1 2 2 2 2 1 1
1 2 2 2 2 1 1 2 2 2 2 1 1 2 2 2 2 1 1
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
1 2 2 2 2 1 1 3 3 3 3 1 1 3 3 3 3 1 1
1 2 2 2 2 1 1 3 3 3 3 1 1 3 3 3 3 1 1
1 2 2 2 2 1 1 3 3 3 3 1 1 3 3 3 3 1 1
1 2 2 2 2 1 1 3 3 3 3 1 1 3 3 3 3 1 1
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
1 2 2 2 2 1 1 3 3 3 3 1 1 3 3 3 3 1 1
1 2 2 2 2 1 1 3 3 3 3 1 1 3 3 3 3 1 1
1 2 2 2 2 1 1 3 3 3 3 1 1 3 3 3 3 1 1
1 2 2 2 2 1 1 3 3 3 3 1 1 3 3 3 3 1 1
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
```
Match: False
Pixels Off: 48
Size Correct: True
Color Palette Correct: True
Color Count Correct: False
Score: 26.59279778393352

## Example 3:
Input:
```
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
1 0 0 0 1 0 0 0 1 0 0 0 1 0 0 0 1 0 0 0 1 0 0 0 1
1 0 0 0 1 0 0 0 1 0 0 0 1 0 0 0 1 0 0 0 1 0 0 0 1
1 0 0 0 1 0 0 0 1 0 0 0 1 0 0 0 1 0 0 0 1 0 0 0 1
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
1 0 0 0 1 0 0 0 1 0 0 0 1 0 0 0 1 0 0 0 1 0 0 0 1
1 0 0 0 1 0 0 0 1 0 0 0 1 0 0 0 1 0 0 0 1 0 0 0 1
1 0 0 0 1 0 0 0 1 0 0 0 1 0 0 0 1 0 0 0 1 0 0 0 1
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
1 0 0 0 1 0 0 0 1 0 0 0 1 0 0 0 1 0 0 0 1 0 0 0 1
1 0 0 0 1 0 0 0 1 0 0 0 1 0 0 0 1 0 0 0 1 0 0 0 1
1 0 0 0 1 0 0 0 1 0 0 0 1 0 0 0 1 0 0 0 1 0 0 0 1
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
1 0 0 0 1 0 0 0 1 0 0 0 1 0 0 0 1 0 0 0 1 0 0 0 1
1 0 0 0 1 0 0 0 1 0 0 0 1 0 0 0 1 0 0 0 1 0 0 0 1
1 0 0 0 1 0 0 0 1 0 0 0 1 0 0 0 1 0 0 0 1 0 0 0 1
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
1 0 0 0 1 0 0 0 1 0 0 0 1 0 0 0 1 0 0 0 1 0 0 0 1
1 0 0 0 1 0 0 0 1 0 0 0 1 0 0 0 1 0 0 0 1 0 0 0 1
1 0 0 0 1 0 0 0 1 0 0 0 1 0 0 0 1 0 0 0 1 0 0 0 1
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
1 0 0 0 1 0 0 0 1 0 0 0 1 0 0 0 1 0 0 0 1 0 0 0 1
1 0 0 0 1 0 0 0 1 0 0 0 1 0 0 0 1 0 0 0 1 0 0 0 1
1 0 0 0 1 0 0 0 1 0 0 0 1 0 0 0 1 0 0 0 1 0 0 0 1
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
```
Expected Output:
```
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
1 2 2 2 1 2 2 2 1 2 2 2 1 2 2 2 1 2 2 2 1 2 2 2 1
1 2 2 2 1 2 2 2 1 2 2 2 1 2 2 2 1 2 2 2 1 2 2 2 1
1 2 2 2 1 2 2 2 1 2 2 2 1 2 2 2 1 2 2 2 1 2 2 2 1
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
1 2 2 2 1 3 3 3 1 3 3 3 1 3 3 3 1 3 3 3 1 2 2 2 1
1 2 2 2 1 3 3 3 1 3 3 3 1 3 3 3 1 3 3 3 1 2 2 2 1
1 2 2 2 1 3 3 3 1 3 3 3 1 3 3 3 1 3 3 3 1 2 2 2 1
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
1 2 2 2 1 3 3 3 1 3 3 3 1 3 3 3 1 3 3 3 1 2 2 2 1
1 2 2 2 1 3 3 3 1 3 3 3 1 3 3 3 1 3 3 3 1 2 2 2 1
1 2 2 2 1 3 3 3 1 3 3 3 1 3 3 3 1 3 3 3 1 2 2 2 1
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
1 2 2 2 1 3 3 3 1 3 3 3 1 3 3 3 1 3 3 3 1 2 2 2 1
1 2 2 2 1 3 3 3 1 3 3 3 1 3 3 3 1 3 3 3 1 2 2 2 1
1 2 2 2 1 3 3 3 1 3 3 3 1 3 3 3 1 3 3 3 1 2 2 2 1
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
1 2 2 2 1 3 3 3 1 3 3 3 1 3 3 3 1 3 3 3 1 2 2 2 1
1 2 2 2 1 3 3 3 1 3 3 3 1 3 3 3 1 3 3 3 1 2 2 2 1
1 2 2 2 1 3 3 3 1 3 3 3 1 3 3 3 1 3 3 3 1 2 2 2 1
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
1 2 2 2 1 2 2 2 1 2 2 2 1 2 2 2 1 2 2 2 1 2 2 2 1
1 2 2 2 1 2 2 2 1 2 2 2 1 2 2 2 1 2 2 2 1 2 2 2 1
1 2 2 2 1 2 2 2 1 2 2 2 1 2 2 2 1 2 2 2 1 2 2 2 1
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
```
Transformed Output:
```
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
1 2 2 2 1 2 2 2 1 2 2 2 1 2 2 2 1 2 2 2 1 2 2 2 1
1 2 2 2 1 2 2 2 1 2 2 2 1 2 2 2 1 2 2 2 1 2 2 2 1
1 2 2 2 1 2 2 2 1 2 2 2 1 2 2 2 1 2 2 2 1 2 2 2 1
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
1 2 2 2 1 3 3 3 1 3 3 3 1 3 3 3 1 3 3 3 1 2 2 2 1
1 2 2 2 1 3 3 3 1 3 3 3 1 3 3 3 1 3 3 3 1 2 2 2 1
1 2 2 2 1 3 3 3 1 3 3 3 1 3 3 3 1 3 3 3 1 2 2 2 1
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
1 2 2 2 1 3 3 3 1 3 3 3 1 3 3 3 1 3 3 3 1 2 2 2 1
1 2 2 2 1 3 3 3 1 3 3 3 1 3 3 3 1 3 3 3 1 2 2 2 1
1 2 2 2 1 3 3 3 1 3 3 3 1 3 3 3 1 3 3 3 1 2 2 2 1
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
1 2 2 2 1 3 3 3 1 3 3 3 1 3 3 3 1 3 3 3 1 2 2 2 1
1 2 2 2 1 3 3 3 1 3 3 3 1 3 3 3 1 3 3 3 1 2 2 2 1
1 2 2 2 1 3 3 3 1 3 3 3 1 3 3 3 1 3 3 3 1 2 2 2 1
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
1 2 2 2 1 3 3 3 1 3 3 3 1 3 3 3 1 3 3 3 1 2 2 2 1
1 2 2 2 1 3 3 3 1 3 3 3 1 3 3 3 1 3 3 3 1 2 2 2 1
1 2 2 2 1 3 3 3 1 3 3 3 1 3 3 3 1 3 3 3 1 2 2 2 1
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
1 2 2 2 1 2 2 2 1 2 2 2 1 2 2 2 1 2 2 2 1 2 2 2 1
1 2 2 2 1 2 2 2 1 2 2 2 1 2 2 2 1 2 2 2 1 2 2 2 1
1 2 2 2 1 2 2 2 1 2 2 2 1 2 2 2 1 2 2 2 1 2 2 2 1
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
```
Match: True
Pixels Off: 0
Size Correct: True
Color Palette Correct: True
Color Count Correct: True
Score: 0
