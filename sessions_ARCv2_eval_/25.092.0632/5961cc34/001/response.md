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
   a. For each component, determine its minimum bounding box.
   b. Calculate the union of all these bounding boxes.
   c. Fill all cells within the union of the bounding boxes in the output 
      grid with red (2).
5. Return the modified output grid.
"""

def find_connected_components(grid, target_colors):
    """
    Finds all connected components of specified colors in the grid.
    Uses Breadth-First Search (BFS).
    """
    rows, cols = grid.shape
    visited = np.zeros_like(grid, dtype=bool)
    components = []

    for r in range(rows):
        for c in range(cols):
            if grid[r, c] in target_colors and not visited[r, c]:
                # Start BFS for a new component
                component = set()
                q = deque([(r, c)])
                visited[r, c] = True
                
                while q:
                    row, col = q.popleft()
                    component.add((row, col))
                    
                    # Check neighbors (up, down, left, right)
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = row + dr, col + dc
                        if 0 <= nr < rows and 0 <= nc < cols and \
                           grid[nr, nc] in target_colors and not visited[nr, nc]:
                            visited[nr, nc] = True
                            q.append((nr, nc))
                
                components.append(component)
                
    return components

def get_bounding_box(component):
    """Calculates the bounding box of a component."""
    if not component:
        return None # Or raise an error
    
    min_r = min(r for r, c in component)
    min_c = min(c for r, c in component)
    max_r = max(r for r, c in component)
    max_c = max(c for r, c in component)
    return min_r, min_c, max_r, max_c

def transform(input_grid):
    """
    Applies the transformation rule based on pattern object count.
    """
    # Define colors
    background_color = 8
    pattern_colors = {1, 3} # Blue and Green
    marker_color_yellow = 4
    output_color = 2 # Red

    # Initialize output_grid as a copy of input, then clear non-background
    output_grid = np.copy(input_grid)
    output_grid[output_grid != background_color] = background_color
    
    rows, cols = input_grid.shape

    # Find pattern objects (connected components of blue or green)
    pattern_objects = find_connected_components(input_grid, pattern_colors)
    num_pattern_objects = len(pattern_objects)

    # Case 1: Exactly one pattern object
    if num_pattern_objects == 1:
        # Find the column of the yellow marker
        marker_col = -1
        yellow_locations = np.where(input_grid == marker_color_yellow)
        if len(yellow_locations[1]) > 0: # Check if yellow marker exists
             marker_col = yellow_locations[1][0] # Assume only one yellow marker
        
        # Check if marker was found (robustness)
        if marker_col != -1:
            # Fill the marker column with the output color
            output_grid[:, marker_col] = output_color
        else:
            # Fallback or error handling if no yellow marker found, 
            # although the problem description implies it will be there.
            # For now, leave the grid as background if marker is missing.
            pass 

    # Case 2: More than one pattern object
    elif num_pattern_objects > 1:
        # Calculate the union of bounding boxes
        min_union_r, min_union_c = rows, cols
        max_union_r, max_union_c = -1, -1
        found_box = False

        for component in pattern_objects:
            bbox = get_bounding_box(component)
            if bbox:
                found_box = True
                min_r, min_c, max_r, max_c = bbox
                min_union_r = min(min_union_r, min_r)
                min_union_c = min(min_union_c, min_c)
                max_union_r = max(max_union_r, max_r)
                max_union_c = max(max_union_c, max_c)

        # Fill the union of bounding boxes if any boxes were found
        if found_box:
            for r in range(min_union_r, max_union_r + 1):
                for c in range(min_union_c, max_union_c + 1):
                     # Check bounds just in case something weird happened with initialization
                    if 0 <= r < rows and 0 <= c < cols:
                        output_grid[r, c] = output_color
                        
    # Case 3: Zero pattern objects (implicitly handled, output grid remains background)
    # No specific action needed as output grid is already initialized to background.

    return output_grid
```