import numpy as np

"""
1. Define the background color as white (0).
2. Scan the input grid to identify all contiguous groups (components) of pixels whose color is not the background color (white). Use 8-way adjacency (including diagonals).
3. Filter these components: Remove any component where any of its pixels are located on the absolute outer border of the input grid (row 0, last row, column 0, or last column).
4. From the remaining ("internal") components, select the one with the largest size (number of pixels). 
5. Determine the minimum bounding box of the selected largest internal component.
6. Create a new output grid whose dimensions match the height and width of the bounding box.
7. Copy the pixels from the input grid within the calculated bounding box into the new output grid, preserving their relative positions.
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

def is_on_border(r, c, height, width):
    """Checks if a coordinate is on the absolute border of the grid."""
    return r == 0 or r == height - 1 or c == 0 or c == width - 1

def transform(input_grid):
    """
    Extracts the largest contiguous non-background, non-border object from the input grid.

    Args:
        input_grid (list[list[int]]): The 2D input grid.

    Returns:
        list[list[int]]: The extracted subgrid containing the largest internal object.
    """
    input_grid_np = np.array(input_grid)
    height, width = input_grid_np.shape
    background_color = 0

    # 1. Find all connected components of non-background pixels
    all_components = find_connected_components(input_grid_np, background_color)

    # 2. Filter out components touching the border
    internal_components = []
    for component in all_components:
        touches_border = False
        for r, c in component:
            if is_on_border(r, c, height, width):
                touches_border = True
                break
        if not touches_border:
            internal_components.append(component)

    # Handle case where there are no internal non-background objects
    if not internal_components:
        # Based on examples, this seems unlikely for valid inputs.
        # If it happens, returning a minimal grid might be appropriate.
        # Let's return a 1x1 white grid.
        return [[background_color]] 

    # 3. Find the largest internal component based on the number of pixels
    largest_internal_component = max(internal_components, key=len)

    # 4. Determine the bounding box of the largest internal component
    min_row, min_col, max_row, max_col = get_bounding_box(largest_internal_component)

    # 5. Extract the subgrid defined by the bounding box
    output_grid_np = input_grid_np[min_row : max_row + 1, min_col : max_col + 1]

    # Convert back to list of lists for the required output format
    return output_grid_np.tolist()