import numpy as np
from collections import Counter

"""
Transformation Rule:
1. Define the background color as white (0).
2. Define the "inner grid" as the input grid excluding the 1-pixel border (top/bottom rows, left/right columns).
3. Identify the 'target_color' by finding the most frequent non-background color within the inner grid.
4. Find all contiguous components of non-background pixels in the *entire* original grid using 8-way adjacency.
5. Filter these components to keep only those containing at least one pixel of the 'target_color'.
6. Select the component from the filtered list that has the largest size (number of pixels). This is the 'target_component'.
7. Determine the minimum bounding box of the 'target_component'.
8. Extract the subgrid corresponding to this bounding box from the original input grid.
"""

def find_connected_components(grid, background_color=0):
    """
    Finds all connected components of non-background pixels in a grid using 8-way adjacency.

    Args:
        grid (np.ndarray): The input grid.
        background_color (int): The value representing the background.

    Returns:
        list: A list of components, where each component is a list of 
              (row, col) tuples representing the coordinates of the pixels 
              in that component. Returns an empty list if no non-background pixels exist.
    """
    height, width = grid.shape
    visited = set()
    components = []

    for r in range(height):
        for c in range(width):
            # If the pixel is not background and not visited yet, start a search
            if grid[r, c] != background_color and (r, c) not in visited:
                current_component = []
                q = [(r, c)] # Queue for BFS
                visited.add((r, c))

                while q:
                    curr_r, curr_c = q.pop(0)
                    current_component.append((curr_r, curr_c))

                    # Check all 8 neighbors (including diagonals)
                    for dr in [-1, 0, 1]:
                        for dc in [-1, 0, 1]:
                            if dr == 0 and dc == 0:
                                continue # Skip self

                            nr, nc = curr_r + dr, curr_c + dc

                            # Check bounds
                            if 0 <= nr < height and 0 <= nc < width:
                                # If neighbor is valid, not background, and not visited
                                if grid[nr, nc] != background_color and (nr, nc) not in visited:
                                    visited.add((nr, nc))
                                    q.append((nr, nc))
                
                if current_component:
                    components.append(current_component)
                    
    return components

def get_dominant_inner_color(grid, background_color=0):
    """
    Finds the most frequent non-background color in the inner part of the grid.

    Args:
        grid (np.ndarray): The input grid.
        background_color (int): The value representing the background.

    Returns:
        int or None: The most frequent color, or None if no non-background
                     colors exist in the inner grid or grid is too small.
    """
    height, width = grid.shape
    # Inner grid requires at least 3x3 dimensions
    if height < 3 or width < 3:
        return None 
        
    inner_grid = grid[1:-1, 1:-1]
    colors, counts = np.unique(inner_grid[inner_grid != background_color], return_counts=True)
    
    if len(colors) == 0:
        return None # No non-background colors found in the inner grid
        
    dominant_color_index = np.argmax(counts)
    return colors[dominant_color_index]

def get_bounding_box(component):
    """
    Calculates the bounding box for a given component.

    Args:
        component (list): A list of (row, col) tuples.

    Returns:
        tuple: (min_row, min_col, max_row, max_col) or None if component is empty.
    """
    if not component:
        return None
    
    rows = [r for r, c in component]
    cols = [c for r, c in component]
    
    min_row = min(rows)
    min_col = min(cols)
    max_row = max(rows)
    max_col = max(cols)
    
    return min_row, min_col, max_row, max_col

def transform(input_grid):
    """
    Extracts the largest connected component containing the dominant inner color.
    """
    input_grid_np = np.array(input_grid, dtype=int)
    height, width = input_grid_np.shape
    background_color = 0

    # 1. Handle grids too small to have an inner area
    if height < 3 or width < 3:
         # Default behavior might need adjustment based on task specifics for small grids
         # Returning a 1x1 background grid is a safe placeholder
         return [[background_color]]

    # 2. Find the dominant non-background color in the inner grid
    target_color = get_dominant_inner_color(input_grid_np, background_color)

    # 3. If no dominant color found (e.g., inner grid is all background), handle appropriately
    if target_color is None:
        # Could return empty, background, or maybe find largest overall component if required
        # Returning 1x1 background for now
        return [[background_color]] 

    # 4. Find all connected components in the *entire* grid
    all_components = find_connected_components(input_grid_np, background_color)
    
    # 5. Filter components to keep only those containing the target_color
    target_color_components = []
    for component in all_components:
        # Check if any pixel in this component matches the target_color
        component_colors = {input_grid_np[r, c] for r, c in component}
        if target_color in component_colors:
            target_color_components.append(component)

    # 6. Handle case where no components contain the target color
    if not target_color_components:
         # This case seems unlikely given the problem structure, but handle defensively
         return [[background_color]]

    # 7. Find the largest component among the filtered ones
    target_component = max(target_color_components, key=len)

    # 8. Get the bounding box of the target component
    bounding_box = get_bounding_box(target_component)
    if bounding_box is None: # Should not happen if target_component is valid
        return [[background_color]] 
    min_row, min_col, max_row, max_col = bounding_box

    # 9. Extract the subgrid defined by the bounding box
    output_grid_np = input_grid_np[min_row : max_row + 1, min_col : max_col + 1]

    # 10. Convert back to list of lists for the required output format
    return output_grid_np.tolist()