
Previous Code:
```python
import numpy as np
from collections import deque

"""
Transforms an input grid based on the number and location of connected components 
formed by blue (1) and green (3) pixels ("pattern objects").

1. Initialize the output grid as a copy of the input grid, then set all 
   non-background (non-azure, 8) pixels to the background color (azure, 8).
2. Find all connected components consisting of blue (1) or green (3) pixels. 
   Connectivity is defined by adjacent (non-diagonal) cells. Blue and green 
   pixels are considered connected to each other. Count these components.
3. If exactly one component is found:
   a. Locate the column index of the single yellow (4) marker pixel.
   b. Fill this entire column in the output grid with red (2).
4. If more than one component is found:
   a. For each individual pattern object:
      i. Determine its minimum bounding box.
      ii. Fill the area within that bounding box in the output grid with red (2).
5. Return the modified output grid.
"""

def find_connected_components(grid, target_colors):
    """
    Finds all connected components of specified colors in the grid.
    Uses Breadth-First Search (BFS). Adjacent means sharing an edge (not diagonal).
    
    Args:
        grid (np.array): The input grid.
        target_colors (set): A set of integer color values to consider part of components.
        
    Returns:
        list: A list of sets, where each set contains the (row, col) tuples of a component.
    """
    rows, cols = grid.shape
    visited = np.zeros_like(grid, dtype=bool)
    components = []

    for r in range(rows):
        for c in range(cols):
            # If the cell has a target color and hasn't been visited yet, start a new search
            if grid[r, c] in target_colors and not visited[r, c]:
                component = set()
                q = deque([(r, c)])
                visited[r, c] = True
                
                # Perform BFS
                while q:
                    row, col = q.popleft()
                    component.add((row, col))
                    
                    # Check neighbors (up, down, left, right)
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = row + dr, col + dc
                        # Check if the neighbor is within bounds, has a target color, and hasn't been visited
                        if 0 <= nr < rows and 0 <= nc < cols and \
                           grid[nr, nc] in target_colors and not visited[nr, nc]:
                            visited[nr, nc] = True
                            q.append((nr, nc))
                
                # Add the found component to the list
                components.append(component)
                
    return components

def get_bounding_box(component):
    """
    Calculates the minimum bounding box (min_row, min_col, max_row, max_col) 
    for a given component.
    
    Args:
        component (set): A set of (row, col) tuples representing a component.
        
    Returns:
        tuple: (min_r, min_c, max_r, max_c) or None if the component is empty.
    """
    if not component:
        return None 
    
    # Find the min/max row and column indices from the component's coordinates
    min_r = min(r for r, c in component)
    min_c = min(c for r, c in component)
    max_r = max(r for r, c in component)
    max_c = max(c for r, c in component)
    return min_r, min_c, max_r, max_c

def transform(input_grid):
    """
    Applies the transformation rule based on pattern object count.
    """
    # Define colors used in the task
    background_color = 8  # azure
    pattern_colors = {1, 3} # Blue and Green
    marker_color_yellow = 4 # Yellow
    output_color = 2      # Red

    # Initialize output_grid as a copy of input, then set all non-background pixels to background
    output_grid = np.full_like(input_grid, background_color)
    
    rows, cols = input_grid.shape

    # Find pattern objects (connected components of blue or green)
    pattern_objects = find_connected_components(input_grid, pattern_colors)
    num_pattern_objects = len(pattern_objects)

    # Case 1: Exactly one pattern object
    if num_pattern_objects == 1:
        # Find the column of the yellow marker
        marker_col = -1
        yellow_locations = np.where(input_grid == marker_color_yellow)
        # Ensure a yellow marker was actually found
        if len(yellow_locations[1]) > 0: 
             marker_col = yellow_locations[1][0] # Assume only one yellow marker column is relevant
        
        # If a valid marker column was found, fill it
        if marker_col != -1:
            output_grid[:, marker_col] = output_color
        # else: If no yellow marker found, the output grid remains background (as initialized)
            
    # Case 2: More than one pattern object
    elif num_pattern_objects > 1:
        # Iterate through each found pattern object
        for component in pattern_objects:
            # Get the bounding box for the current component
            bbox = get_bounding_box(component)
            if bbox:
                min_r, min_c, max_r, max_c = bbox
                # Fill the rectangular area defined by the bounding box with the output color
                # Use slicing for efficient filling
                output_grid[min_r:max_r+1, min_c:max_c+1] = output_color
                        
    # Case 3: Zero pattern objects 
    # No specific action needed as output_grid is already initialized to background.

    return output_grid
```
Results for code_00.py:

Train Set Results:

## Example 1:
Input:
```
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 3 3 8 8 8 8 8 8 8 8 8 8 8
8 1 1 1 1 8 8 8 8 8 8 8 8 8 8
8 1 1 1 1 8 8 8 8 8 8 8 8 8 8
8 1 1 1 1 8 8 8 8 8 8 8 8 8 8
8 8 1 1 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 4 8 8 8 8 8 8
8 8 8 8 8 8 8 8 2 8 8 8 8 8 8
8 8 8 8 8 8 8 8 2 8 8 8 8 8 8
8 8 8 8 8 8 8 8 2 8 8 8 8 8 8
```
Expected Output:
```
8 8 8 8 8 8 8 8 2 8 8 8 8 8 8
8 8 8 8 8 8 8 8 2 8 8 8 8 8 8
8 8 8 8 8 8 8 8 2 8 8 8 8 8 8
8 8 8 8 8 8 8 8 2 8 8 8 8 8 8
8 8 8 8 8 8 8 8 2 8 8 8 8 8 8
8 8 8 8 8 8 8 8 2 8 8 8 8 8 8
8 8 8 8 8 8 8 8 2 8 8 8 8 8 8
8 8 8 8 8 8 8 8 2 8 8 8 8 8 8
8 8 8 8 8 8 8 8 2 8 8 8 8 8 8
8 8 8 8 8 8 8 8 2 8 8 8 8 8 8
8 8 8 8 8 8 8 8 2 8 8 8 8 8 8
8 8 8 8 8 8 8 8 2 8 8 8 8 8 8
8 8 8 8 8 8 8 8 2 8 8 8 8 8 8
```
Transformed Output:
```
8 8 8 8 8 8 8 8 2 8 8 8 8 8 8
8 8 8 8 8 8 8 8 2 8 8 8 8 8 8
8 8 8 8 8 8 8 8 2 8 8 8 8 8 8
8 8 8 8 8 8 8 8 2 8 8 8 8 8 8
8 8 8 8 8 8 8 8 2 8 8 8 8 8 8
8 8 8 8 8 8 8 8 2 8 8 8 8 8 8
8 8 8 8 8 8 8 8 2 8 8 8 8 8 8
8 8 8 8 8 8 8 8 2 8 8 8 8 8 8
8 8 8 8 8 8 8 8 2 8 8 8 8 8 8
8 8 8 8 8 8 8 8 2 8 8 8 8 8 8
8 8 8 8 8 8 8 8 2 8 8 8 8 8 8
8 8 8 8 8 8 8 8 2 8 8 8 8 8 8
8 8 8 8 8 8 8 8 2 8 8 8 8 8 8
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
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 3 3 8 8 8 8 8 1 1 8 8 8 8 8 8 8 8 3 3 8 8 8 8
8 1 1 1 1 8 8 8 1 1 1 3 8 8 8 8 8 8 1 1 1 1 8 8 8
8 1 1 1 1 8 8 8 1 1 1 3 8 8 8 8 8 8 1 1 1 1 8 8 8
8 8 1 1 8 8 8 8 8 1 1 8 8 8 8 8 8 8 8 1 1 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 3 3 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 1 1 1 1 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 1 1 1 1 1 1 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 1 1 1 1 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 1 1 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 4 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 2 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 2 8 8 8 8 8 8 8 8 8 8 8 8 8 8
```
Expected Output:
```
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 2 2 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 2 2 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 2 2 8 8 8 8
8 8 8 8 8 8 8 8 8 2 2 8 8 8 8 8 8 8 8 2 2 8 8 8 8
8 8 8 8 8 8 8 8 2 2 2 2 2 2 2 2 2 2 2 2 2 2 8 8 8
8 8 8 8 8 8 8 8 2 2 2 2 2 2 2 2 2 2 2 2 2 2 8 8 8
8 8 8 8 8 8 8 8 8 2 2 8 8 8 8 8 8 8 8 2 2 8 8 8 8
8 8 8 8 8 8 8 8 8 2 2 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 2 2 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 2 2 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 2 2 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 2 2 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 2 2 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 2 2 2 2 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 2 2 2 2 2 2 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 2 2 2 2 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 2 2 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 2 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 2 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 2 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 2 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 2 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 2 8 8 8 8 8 8 8 8 8 8 8 8 8 8
```
Transformed Output:
```
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 2 2 2 2 8 8 8 2 2 2 2 8 8 8 8 8 8 2 2 2 2 8 8 8
8 2 2 2 2 8 8 8 2 2 2 2 8 8 8 8 8 8 2 2 2 2 8 8 8
8 2 2 2 2 8 8 8 2 2 2 2 8 8 8 8 8 8 2 2 2 2 8 8 8
8 2 2 2 2 8 8 8 2 2 2 2 8 8 8 8 8 8 2 2 2 2 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 2 2 2 2 2 2 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 2 2 2 2 2 2 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 2 2 2 2 2 2 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 2 2 2 2 2 2 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 2 2 2 2 2 2 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
```
Match: False
Pixels Off: 70
Size Correct: True
Color Palette Correct: True
Color Count Correct: False
Score: 24.347826086956502

## Example 3:
Input:
```
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 1 1 8 8 8 8 8 8 8 8 8 8 1 1 8 8 8 8
8 8 8 1 1 1 1 8 8 8 8 8 8 8 8 1 1 1 1 8 8 8
8 8 1 1 1 1 1 1 8 8 8 8 8 8 3 1 1 1 1 1 8 8
8 8 1 1 1 1 1 1 8 8 8 8 8 8 3 1 1 1 1 1 8 8
8 8 8 1 1 1 1 8 8 8 8 8 8 8 8 1 1 1 1 8 8 8
8 8 8 8 3 3 8 8 8 8 8 8 8 8 8 8 1 1 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 1 1 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 1 1 1 1 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 3 1 1 1 1 1 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 3 1 1 1 1 1 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 1 1 1 1 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 1 1 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 4 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 2 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 2 8 8 8 8 8
```
Expected Output:
```
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 2 2 8 8 8 8 8 8 8 8 8 8 2 2 8 8 8 8
8 8 8 2 2 2 2 8 8 8 8 8 8 8 8 2 2 2 2 8 8 8
8 8 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 8 8
8 8 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 8 8
8 8 8 2 2 2 2 8 8 8 8 8 8 8 8 2 2 2 2 8 8 8
8 8 8 8 2 2 8 8 8 8 8 8 8 8 8 8 2 2 8 8 8 8
8 8 8 8 2 2 8 8 8 8 8 8 8 8 8 8 2 8 8 8 8 8
8 8 8 8 2 2 8 8 8 8 8 8 8 8 8 8 2 8 8 8 8 8
8 8 8 8 2 2 8 8 8 8 8 8 8 8 8 8 2 8 8 8 8 8
8 8 8 8 2 2 8 8 8 8 8 8 8 8 8 8 2 8 8 8 8 8
8 8 8 8 2 2 8 8 8 8 8 8 8 8 8 8 2 8 8 8 8 8
8 8 8 2 2 2 2 8 8 8 8 8 8 8 8 8 2 8 8 8 8 8
2 2 2 2 2 2 2 2 8 8 8 8 8 8 8 8 2 8 8 8 8 8
2 2 2 2 2 2 2 2 8 8 8 8 8 8 8 8 2 8 8 8 8 8
8 8 8 2 2 2 2 8 8 8 8 8 8 8 8 8 2 8 8 8 8 8
8 8 8 8 2 2 8 8 8 8 8 8 8 8 8 8 2 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 2 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 2 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 2 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 2 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 2 8 8 8 8 8
```
Transformed Output:
```
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 2 2 2 2 2 2 8 8 8 8 8 8 2 2 2 2 2 2 8 8
8 8 2 2 2 2 2 2 8 8 8 8 8 8 2 2 2 2 2 2 8 8
8 8 2 2 2 2 2 2 8 8 8 8 8 8 2 2 2 2 2 2 8 8
8 8 2 2 2 2 2 2 8 8 8 8 8 8 2 2 2 2 2 2 8 8
8 8 2 2 2 2 2 2 8 8 8 8 8 8 2 2 2 2 2 2 8 8
8 8 2 2 2 2 2 2 8 8 8 8 8 8 2 2 2 2 2 2 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 2 2 2 2 2 2 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 2 2 2 2 2 2 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 2 2 2 2 2 2 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 2 2 2 2 2 2 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 2 2 2 2 2 2 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 2 2 2 2 2 2 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
```
Match: False
Pixels Off: 75
Size Correct: True
Color Palette Correct: True
Color Count Correct: False
Score: 29.644268774703562

## Example 4:
Input:
```
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 1 1 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 1 1 1 1 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 1 1 1 1 1 3 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 1 1 1 1 1 3 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 1 1 1 1 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 1 1 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 1 1 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 3 1 1 1 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 1 1 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 4 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 2 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 2 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 2 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
```
Expected Output:
```
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 2 2 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 2 2 2 2 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2
8 8 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2
8 8 8 2 2 2 2 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 2 2 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 2 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 2 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 2 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 2 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 2 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 2 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 2 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 2 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 2 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 2 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 2 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 2 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 2 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 2 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
```
Transformed Output:
```
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 2 2 2 2 2 2 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 2 2 2 2 2 2 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 2 2 2 2 2 2 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 2 2 2 2 2 2 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 2 2 2 2 2 2 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 2 2 2 2 2 2 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 2 2 2 2 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 2 2 2 2 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 2 2 2 2 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
```
Match: False
Pixels Off: 66
Size Correct: True
Color Palette Correct: True
Color Count Correct: False
Score: 26.086956521739125
