```python
"""
Extracts all instances of repeating 3x3 patterns from the input grid. 
Each pattern consists of a single non-white color against a white background within its 3x3 area.
The extracted patterns are then arranged adjacent to each other (vertically or horizontally) 
in the output grid based on their overall spatial distribution in the input. 
Patterns are ordered top-to-bottom for vertical arrangement and left-to-right for horizontal arrangement.

Color mapping (for reference):
0: white, 1: blue, 2: red, 3: green, 4: yellow, 
5: gray, 6: magenta, 7: orange, 8: azure, 9: maroon
"""

import numpy as np
from collections import deque

def find_connected_component(grid, start_r, start_c, visited):
    """
    Finds all connected cells of the same color starting from (start_r, start_c) using BFS.
    Updates the visited set. Returns the set of coordinates for the component.
    Uses 4-way connectivity (up, down, left, right).
    """
    rows, cols = grid.shape
    color = grid[start_r, start_c]
    
    # Ignore background color (0) or cells already visited as part of another component
    if color == 0 or (start_r, start_c) in visited: 
        return set()

    q = deque([(start_r, start_c)])
    component = set()
    
    while q:
        r, c = q.popleft()
        
        # Check bounds, visited status, and if the color matches the component's color
        if not (0 <= r < rows and 0 <= c < cols) or (r, c) in visited or grid[r, c] != color:
            continue
            
        visited.add((r, c)) # Mark cell as visited for this component search
        component.add((r, c)) # Add cell to the current component
        
        # Add valid neighbors to the queue for exploration
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nr, nc = r + dr, c + dc
            # Add to queue regardless of visited status; the check at the start of the loop handles it.
            q.append((nr, nc))
                 
    return component

def get_bounding_box(coords):
    """
    Calculates the bounding box (min_r, min_c, max_r, max_c) 
    for a non-empty set of coordinates {(r, c), ...}.
    """
    if not coords:
        # This should ideally not be reached if called after finding a non-empty component
        raise ValueError("Cannot get bounding box for empty set of coordinates.") 
        
    min_r = min(r for r, c in coords)
    min_c = min(c for r, c in coords)
    max_r = max(r for r, c in coords)
    max_c = max(c for r, c in coords)
    return min_r, min_c, max_r, max_c

def transform(input_grid):
    """
    Identifies 3x3 patterns in the input grid, determines their overall spatial layout 
    (predominantly vertical or horizontal), sorts them accordingly, and concatenates 
    them into the output grid.
    """
    grid_np = np.array(input_grid, dtype=int)
    rows, cols = grid_np.shape
    
    # Handle empty input grid case
    if rows == 0 or cols == 0:
        return []
        
    visited = set() # Keep track of pixels already assigned to a component
    patterns = [] # Stores tuples: (top_left_row, top_left_col, extracted_3x3_subgrid_np_array)

    # Step 1: Scan grid to find connected components of non-white colors
    for r in range(rows):
        for c in range(cols):
            # If pixel is non-white and not yet visited
            if grid_np[r, c] != 0 and (r, c) not in visited:
                # Find the full connected component of the same color
                component_coords = find_connected_component(grid_np, r, c, visited)
                
                # Skip if the component finding didn't yield coordinates (e.g., started on visited cell)
                if not component_coords:
                    continue

                # Step 2: Calculate the bounding box of the found component
                min_r, min_c, max_r, max_c = get_bounding_box(component_coords)
                
                # Step 3: Check if the bounding box dimensions are exactly 3x3
                height = max_r - min_r + 1
                width = max_c - min_c + 1
                
                if height == 3 and width == 3:
                    # Step 4: Extract the 3x3 subgrid from the input grid corresponding to the bounding box
                    # This subgrid contains the pattern including any background pixels within the 3x3 area
                    subgrid_3x3 = grid_np[min_r:min_r+3, min_c:min_c+3]
                    
                    # Store the pattern's top-left corner coordinates and the extracted grid data
                    patterns.append((min_r, min_c, subgrid_3x3))

    # Step 5: Handle cases based on the number of patterns found
    if not patterns:
        # No patterns matching the criteria were found
        return [] 
    if len(patterns) == 1:
        # Only one pattern found, output is just that pattern
        return patterns[0][2].tolist()

    # Step 6: Determine the overall spatial arrangement (vertical or horizontal)
    # Collect the top-left coordinates of all found patterns
    coords = [(r, c) for r, c, _ in patterns]
    min_r_all = min(r for r, c in coords)
    max_r_all = max(r for r, c in coords)
    min_c_all = min(c for r, c in coords)
    max_c_all = max(c for r, c in coords)
    
    # Calculate the vertical and horizontal span covering all pattern top-left corners
    height_span = max_r_all - min_r_all
    width_span = max_c_all - min_c_all
    
    # Determine arrangement: if height span is greater, stack vertically. Otherwise (including equal span), stack horizontally.
    arrangement = 'vertical' if height_span > width_span else 'horizontal'

    # Step 7: Sort the patterns based on their original position and the determined arrangement
    if arrangement == 'vertical':
        # Sort primarily by the top row index (min_r) for top-to-bottom order
        patterns.sort(key=lambda p: p[0]) 
    else: # arrangement == 'horizontal'
        # Sort primarily by the left column index (min_c) for left-to-right order
        patterns.sort(key=lambda p: p[1])

    # Step 8: Construct the final output grid by concatenating the sorted patterns
    # Get the list of 3x3 numpy arrays in the correct sorted order
    sorted_grids = [p[2] for p in patterns]
    
    if arrangement == 'vertical':
        # Stack the 3x3 grids one above the other
        output_np = np.vstack(sorted_grids)
    else: # arrangement == 'horizontal'
        # Stack the 3x3 grids side-by-side
        output_np = np.hstack(sorted_grids)
        
    # Step 9: Convert the final numpy array back to the required list of lists format
    return output_np.tolist()
```