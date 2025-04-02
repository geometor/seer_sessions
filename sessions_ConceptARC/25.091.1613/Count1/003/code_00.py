import numpy as np
from collections import defaultdict

"""
Counts "significant entities" in the input grid and represents this count as yellow 
pixels in a fixed-size 1x6 output row.

An entity is defined based on contiguous components of the same non-white color:
1. Find all contiguous components of non-white pixels and their sizes.
2. Group components by color.
3. For each color:
   - If any component of that color has size >= 2 ("major component"), 
     count the number of *major components* for that color.
   - If all components of that color have size < 2 (i.e., size 1, "minor components"), 
     count the presence of that color as 1 entity.
4. Sum these counts across all colors to get the total entity count 'N'.
5. Create a 1x6 output grid. Fill the first min(N, 6) cells with yellow (4) 
   and the rest with white (0).
"""

def find_components_detailed(grid):
    """
    Finds distinct contiguous components of the same non-white color,
    returning details about each component (color, size).

    Args:
        grid (np.array): The input grid.

    Returns:
        list: A list of dictionaries, each describing a component:
              {'color': int, 'size': int}
    """
    rows, cols = grid.shape
    visited = np.zeros_like(grid, dtype=bool)
    components = []
    q = [] # Queue for BFS

    for r in range(rows):
        for c in range(cols):
            # Check if the cell is non-white (not 0) and hasn't been visited yet
            if grid[r, c] != 0 and not visited[r, c]:
                # Start of a new component
                component_color = grid[r, c]
                component_size = 0
                
                # Start BFS from this cell
                q.append((r, c))
                visited[r, c] = True

                while q:
                    curr_r, curr_c = q.pop(0)
                    component_size += 1

                    # Check 4 cardinal neighbors (up, down, left, right)
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = curr_r + dr, curr_c + dc

                        # Check if the neighbor is within bounds
                        if 0 <= nr < rows and 0 <= nc < cols:
                            # Check if the neighbor has the same color and hasn't been visited
                            if not visited[nr, nc] and grid[nr, nc] == component_color:
                                visited[nr, nc] = True
                                q.append((nr, nc))
                
                # Store component details
                components.append({
                    'color': component_color,
                    'size': component_size
                })
    return components

def transform(input_grid):
    """
    Transforms the input grid based on the count of significant entities.

    Args:
        input_grid (list[list[int]]): A 2D list representing the input grid.

    Returns:
        list[list[int]]: A 1x6 list of lists representing the output grid.
    """
    # Convert input to numpy array for easier processing
    input_grid_np = np.array(input_grid, dtype=int)

    # Find all components and their details
    all_components = find_components_detailed(input_grid_np)

    # Group components by color
    components_by_color = defaultdict(list)
    for comp in all_components:
        components_by_color[comp['color']].append(comp)

    # --- Calculate the total entity count 'N' based on the refined logic ---
    total_entity_count = 0
    size_threshold = 2 # Components must be at least this size to count individually

    # Iterate through each color found in the grid
    for color, components in components_by_color.items():
        major_components_count = 0
        has_major_component = False
        
        # Analyze components for this specific color
        for comp in components:
            if comp['size'] >= size_threshold:
                major_components_count += 1
                has_major_component = True
        
        # Add to total count based on rules
        if has_major_component:
            # If there are major components, count only them
            total_entity_count += major_components_count
        elif components: # Ensure the color actually exists (not an empty list)
             # If there are only minor components (size < threshold), count the color's presence once
            total_entity_count += 1
            
    # --- Create the output grid ---
    output_height = 1
    output_width = 6
    
    # Initialize the output grid with white (0)
    output_grid = np.zeros((output_height, output_width), dtype=int)

    # Determine how many yellow cells to draw (capped by output width)
    num_yellow = min(total_entity_count, output_width)

    # Fill the beginning of the output row with yellow (4)
    for i in range(num_yellow):
        output_grid[0, i] = 4

    # Convert the numpy array back to a list of lists for the ARC standard
    return output_grid.tolist()