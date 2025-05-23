import numpy as np

"""
Identify all contiguous groups of non-background (non-white/0) pixels in the input grid, considering 8-way adjacency (including diagonals). 
Select the group with the largest number of pixels. Determine the minimum bounding box containing this largest group. 
Extract the portion of the input grid defined by this bounding box as the output grid.
"""

def find_connected_components(grid, background_color=0):
    """
    Finds all connected components of non-background pixels in a grid.

    Args:
        grid (np.ndarray): The input grid.
        background_color (int): The value representing the background.

    Returns:
        list: A list of components, where each component is a list of 
              (row, col) tuples representing the coordinates of the pixels 
              in that component.
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
    Extracts the largest contiguous non-background object from the input grid.

    Args:
        input_grid (np.ndarray): The 2D input grid.

    Returns:
        np.ndarray: The extracted subgrid containing the largest object.
    """
    input_grid_np = np.array(input_grid)
    background_color = 0

    # 1. Find all connected components of non-background pixels
    components = find_connected_components(input_grid_np, background_color)

    # Handle case where there are no non-background objects
    if not components:
        # Return an empty grid or handle as appropriate for the specific ARC task context
        # Based on examples, this is unlikely, but good practice.
        # Let's return a 1x1 grid of background color for now.
        return np.array([[background_color]]) 

    # 2. Find the largest component based on the number of pixels
    largest_component = max(components, key=len)

    # 3. Determine the bounding box of the largest component
    min_row, min_col, max_row, max_col = get_bounding_box(largest_component)

    # 4. Extract the subgrid defined by the bounding box
    output_grid = input_grid_np[min_row : max_row + 1, min_col : max_col + 1]

    return output_grid.tolist() # Return as list of lists per ARC standard format
