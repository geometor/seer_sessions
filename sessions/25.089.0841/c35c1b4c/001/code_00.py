import numpy as np
from collections import deque

"""
Transformation Rule Natural Language Description:

1.  **Identify the Dominant Object:** Find the largest connected component (LCC) of pixels of the same color in the input grid, considering both orthogonal and diagonal adjacency. Determine the color of this LCC ('dominant_color').
2.  **Identify External Regions:** Perform a search (e.g., Breadth-First Search) starting from all border cells of the grid. This search propagates to adjacent cells (orthogonally and diagonally) but cannot pass through any cell with the 'dominant_color'. Mark all reachable cells from the border without crossing the 'dominant_color' as "externally reachable".
3.  **Identify and Fill Cavities:** Create a copy of the input grid. Iterate through each cell of the grid. If a cell in the input grid does *not* have the 'dominant_color' and was *not* marked as "externally reachable", change its color in the copied grid to the 'dominant_color'.
4.  **Output:** The modified copied grid is the final output. Cells that are part of the LCC or are externally reachable retain their original colors.
"""

def find_largest_connected_component(grid):
    """
    Finds the largest connected component (LCC) in the grid.
    Connectivity includes diagonals.

    Args:
        grid (np.ndarray): The input grid.

    Returns:
        tuple: (dominant_color, set_of_coordinates) of the LCC.
               Returns (None, set()) if the grid is empty.
    """
    height, width = grid.shape
    visited = np.zeros_like(grid, dtype=bool)
    max_size = 0
    lcc_color = None
    lcc_coords = set()

    # Define 8 directions for connectivity (orthogonal + diagonal)
    directions = [(0, 1), (0, -1), (1, 0), (-1, 0),
                  (1, 1), (1, -1), (-1, 1), (-1, -1)]

    for r in range(height):
        for c in range(width):
            if not visited[r, c]:
                component_color = grid[r, c]
                component_coords = set()
                q = deque([(r, c)])
                visited[r, c] = True
                component_coords.add((r, c))

                while q:
                    curr_r, curr_c = q.popleft()

                    for dr, dc in directions:
                        nr, nc = curr_r + dr, curr_c + dc

                        if 0 <= nr < height and 0 <= nc < width and \
                           not visited[nr, nc] and grid[nr, nc] == component_color:
                            visited[nr, nc] = True
                            q.append((nr, nc))
                            component_coords.add((nr, nc))

                if len(component_coords) > max_size:
                    max_size = len(component_coords)
                    lcc_color = component_color
                    lcc_coords = component_coords

    return lcc_color, lcc_coords


def find_externally_reachable(grid, dominant_color):
    """
    Finds all cells reachable from the border without crossing the dominant color.
    Connectivity includes diagonals.

    Args:
        grid (np.ndarray): The input grid.
        dominant_color (int): The color of the LCC.

    Returns:
        set: A set of coordinates (r, c) of externally reachable cells.
    """
    height, width = grid.shape
    reachable = set()
    q = deque()

    # Define 8 directions for connectivity
    directions = [(0, 1), (0, -1), (1, 0), (-1, 0),
                  (1, 1), (1, -1), (-1, 1), (-1, -1)]

    # Add border cells to queue if they are not the dominant color
    for r in range(height):
        for c in range(width):
            if r == 0 or r == height - 1 or c == 0 or c == width - 1:
                if grid[r, c] != dominant_color and (r, c) not in reachable:
                    q.append((r, c))
                    reachable.add((r, c))

    # Perform BFS
    while q:
        curr_r, curr_c = q.popleft()

        for dr, dc in directions:
            nr, nc = curr_r + dr, curr_c + dc

            if 0 <= nr < height and 0 <= nc < width and \
               grid[nr, nc] != dominant_color and (nr, nc) not in reachable:
                reachable.add((nr, nc))
                q.append((nr, nc))

    return reachable


def transform(input_grid_list):
    """
    Transforms the input grid based on the described rule:
    Finds the largest connected component (LCC), identifies cells not
    belonging to the LCC that are enclosed by it (not reachable from the border
    without crossing the LCC), and fills these enclosed cells with the LCC's color.

    Args:
        input_grid_list (list of list of int): The input grid.

    Returns:
        list of list of int: The transformed output grid.
    """
    # Convert input to numpy array for easier processing
    input_grid = np.array(input_grid_list, dtype=int)
    height, width = input_grid.shape
    
    # --- Step 1: Identify the Dominant Object (LCC) ---
    dominant_color, lcc_coords = find_largest_connected_component(input_grid)

    # Handle edge case where grid might be empty or uniform background
    if dominant_color is None:
        return input_grid_list # Return original if no component found

    # --- Step 2: Identify External Regions ---
    # Find all cells reachable from the border without passing through the dominant color
    externally_reachable_coords = find_externally_reachable(input_grid, dominant_color)

    # --- Step 3: Identify and Fill Cavities ---
    # Create a copy of the input grid to modify
    output_grid = np.copy(input_grid)

    # Iterate through all cells
    for r in range(height):
        for c in range(width):
            # Check if the cell is NOT the dominant color AND is NOT externally reachable
            # Note: We don't need to check if it's part of lcc_coords explicitly,
            # because if it were, its color would be dominant_color.
            if input_grid[r, c] != dominant_color and (r, c) not in externally_reachable_coords:
                # This cell is inside a cavity, fill it with the dominant color
                output_grid[r, c] = dominant_color

    # --- Step 4: Finalize Output ---
    # Convert the numpy array back to a list of lists
    return output_grid.tolist()