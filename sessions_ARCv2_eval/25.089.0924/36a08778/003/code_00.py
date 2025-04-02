import numpy as np
from collections import deque

"""
Transforms the input grid by filling areas within distinct vertical regions. 
Regions are defined by vertical magenta (6) lines or grid edges.
Within each region, find connected components (8-way adjacency) of orange (7) and red (2) pixels.
If a component contains at least one red (2) pixel, change all orange (7) pixels in that component to magenta (6).
Magenta (6) pixels act as impassable barriers for connectivity, both the region dividers and potentially others.
"""

def find_regions(input_grid, boundary_color):
    """
    Identifies vertical regions separated by columns containing the boundary color.

    Args:
        input_grid (np.array): The input grid.
        boundary_color (int): The color value acting as a vertical boundary.

    Returns:
        list: A list of tuples, where each tuple represents a region
              as (start_col, end_col) inclusive.
    """
    height, width = input_grid.shape
    boundary_cols = np.where(np.any(input_grid == boundary_color, axis=0))[0]
    boundary_cols = sorted(list(set(boundary_cols))) # Get unique sorted indices

    regions = []
    start_col = 0
    for b_col in boundary_cols:
        # Add region before the boundary column, if it's valid
        if start_col < b_col:
            regions.append((start_col, b_col - 1))
        # Next region starts after the boundary column
        start_col = b_col + 1
        
    # Add the last region after the final boundary column (or the whole grid if no boundaries)
    if start_col < width:
        regions.append((start_col, width - 1))
        
    # Handle case where grid is empty or only boundary columns exist
    if not regions and width > 0 and not boundary_cols:
         regions.append((0, width - 1))
    elif not regions and width > 0 and len(boundary_cols) == width:
         # Grid is entirely boundary columns, no processable regions
         pass


    return regions

def transform(input_grid):
    """
    Applies the region-based connected component fill transformation.

    Args:
        input_grid (np.array): A 2D numpy array representing the input grid.

    Returns:
        np.array: A 2D numpy array representing the transformed output grid.
    """
    # Define colors
    orange = 7
    red = 2
    magenta = 6
    boundary_color = magenta # Magenta defines regions

    # Get grid dimensions
    height, width = input_grid.shape
    
    # Initialize output_grid as a copy of the input
    output_grid = np.copy(input_grid)
    
    # Keep track of visited cells globally across all regions
    visited = np.zeros((height, width), dtype=bool)

    # 1. Identify Regions
    regions = find_regions(input_grid, boundary_color)

    # 2. Process Each Region
    for start_col, end_col in regions:
        # Iterate through each cell within the current region
        for r in range(height):
            for c in range(start_col, end_col + 1):
                # 3. Start Component Search within Region if applicable
                # Check if cell is orange or red AND not visited
                if not visited[r, c] and (input_grid[r, c] == orange or input_grid[r, c] == red):
                    
                    # Initialize for BFS
                    component_pixels = []  # Store coordinates (r, c) of cells in this component
                    found_source = False   # Flag: does this component contain a red pixel?
                    queue = deque([(r, c)]) # BFS queue
                    
                    # Mark starting cell as visited
                    visited[r, c] = True

                    # Perform BFS
                    while queue:
                        curr_r, curr_c = queue.popleft()
                        
                        # Add to current component list
                        component_pixels.append((curr_r, curr_c))
                        
                        # Check if it's a source color
                        if input_grid[curr_r, curr_c] == red:
                            found_source = True
                            
                        # Explore 8-way neighbors
                        for dr in [-1, 0, 1]:
                            for dc in [-1, 0, 1]:
                                if dr == 0 and dc == 0:
                                    continue # Skip self
                                    
                                nr, nc = curr_r + dr, curr_c + dc
                                
                                # Check neighbor validity for BFS expansion:
                                # - Within grid bounds?
                                # - Within current region's column bounds?
                                # - Not visited yet?
                                # - Not a boundary/blocking color (magenta)?
                                # - Is an orange or red cell (part of potential component)?
                                if (0 <= nr < height and 
                                    start_col <= nc <= end_col and # Check region bounds
                                    not visited[nr, nc] and
                                    input_grid[nr, nc] != magenta and 
                                    (input_grid[nr, nc] == orange or input_grid[nr, nc] == red)):
                                    
                                    visited[nr, nc] = True
                                    queue.append((nr, nc))

                    # 4. Conditional Fill within Region
                    # After BFS for this component is done, check if a source was found
                    if found_source:
                        # If yes, change all orange pixels in this component to magenta
                        for comp_r, comp_c in component_pixels:
                            if input_grid[comp_r, comp_c] == orange:
                                output_grid[comp_r, comp_c] = magenta
                                
    return output_grid