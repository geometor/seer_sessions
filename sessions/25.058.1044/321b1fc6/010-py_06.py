"""
1.  **Identify:** Locate all contiguous regions of azure (8) pixels within the input grid.
2.  **Determine New Color:** For each region, compare to row index. Top part of azure (8) is replaced by Orange color (7). Bottom part of azure (8) is replaced by magenta color (6).
3.  **Substitute:** Replace all pixels within each identified region with the new color that was determined in step 2.
4.  **Output:** Produce the modified grid with the color substitutions. All other colors remain the same.
"""

import numpy as np

def find_regions(grid, color):
    """Finds contiguous regions of a specific color in the grid."""
    visited = np.zeros_like(grid, dtype=bool)
    regions = []

    def dfs(row, col, current_region):
        """Depth-first search to explore a region."""
        if (row < 0 or row >= grid.shape[0] or col < 0 or col >= grid.shape[1] or
                visited[row, col] or grid[row, col] != color):
            return
        visited[row, col] = True
        current_region.append((row, col))
        dfs(row + 1, col, current_region)
        dfs(row - 1, col, current_region)
        dfs(row, col + 1, current_region)
        dfs(row, col - 1, current_region)

    for row in range(grid.shape[0]):
        for col in range(grid.shape[1]):
            if grid[row, col] == color and not visited[row, col]:
                current_region = []
                dfs(row, col, current_region)
                regions.append(current_region)
    return regions

def transform(input_grid):
    """Transforms the input grid according to the specified rule."""
    
    input_grid = np.array(input_grid) # ensure numpy array
    output_grid = np.copy(input_grid)

    # Find all azure (8) regions
    azure_regions = find_regions(input_grid, 8)

    # Iterate through each azure region
    for region in azure_regions:
        # Determine new colors based on vertical position
        
        # get rows for this region
        rows = [r for r, _ in region]
        
        # if orange (7) is present on same row, replace with orange
        if 7 in input_grid[rows, :]:
            for row, col in region:
                output_grid[row, col] = 7
        # if magenta (6) is present on same row, replace with magenta            
        elif 6 in input_grid[rows, :]:
            for row, col in region:
                output_grid[row, col] = 6
        # check input grid and change according to the presence of 7 and 6:
        elif any(7 in input_grid[row,:] for row,_ in region):  
             for row, col in region:
                output_grid[row,col] = 7
        elif any(6 in input_grid[row,:] for row,_ in region):
            for row, col in region:
                output_grid[row,col] = 6
        else:
            # if not 6 or 7, determine color based on first row
            first_row = region[0][0]
            if first_row < 4:
                new_color = 7
            else:
                new_color = 6
            
            for row, col in region:
                output_grid[row, col] = new_color


    return output_grid