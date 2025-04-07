import collections

"""
Identify the largest monochromatic connected component (LMC) in the input grid. 
Extract the subgrid corresponding to the LMC's bounding box. Within this subgrid, 
preserve all original non-zero colors from the input grid, and replace all 
original background (0) cells with the color of the LMC.
"""

# Helper function for Breadth-First Search (BFS) to find a single monochromatic connected component
def _bfs_mono(grid: list[list[int]], start_row: int, start_col: int, visited_component: set[tuple[int, int]], target_color: int) -> set[tuple[int, int]]:
    """
    Performs BFS to find a connected component of cells matching a specific target_color.
    Marks cells visited *within this specific component search*.

    Args:
        grid: The input grid.
        start_row: The starting row for the search.
        start_col: The starting column for the search.
        visited_component: A set to keep track of visited cells during this specific BFS run. 
                           This set is modified by the function.
        target_color: The specific color to look for in the component.

    Returns:
        A set of (row, col) tuples representing the coordinates of the found component.
    """
    rows, cols = len(grid), len(grid[0])
    component = set() # Stores coordinates of cells in this component
    queue = collections.deque([(start_row, start_col)]) # Queue for BFS

    # Mark start cell as visited *for this component* and add to component set
    visited_component.add((start_row, start_col)) 
    component.add((start_row, start_col))

    while queue:
        r, c = queue.popleft() # Get next cell

        # Explore neighbors (4-directional: up, down, left, right)
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nr, nc = r + dr, c + dc

            # Check if neighbor is within grid boundaries
            if 0 <= nr < rows and 0 <= nc < cols:
                # Check if neighbor has the target color and hasn't been visited *for this component* yet
                if grid[nr][nc] == target_color and (nr, nc) not in visited_component:
                    visited_component.add((nr, nc)) # Mark visited for this BFS
                    component.add((nr, nc))       # Add to the component set
                    queue.append((nr, nc))        # Add to queue for further exploration
                    
    return component

# Helper function to find the largest monochromatic component
def _find_largest_mono_component(grid: list[list[int]]) -> tuple[set[tuple[int, int]], int]:
    """
    Finds the largest monochromatic (single-color) connected component in the grid.

    Args:
        grid: The input grid.

    Returns:
        A tuple containing:
        - A set of (row, col) tuples representing the coordinates of the largest component.
        - The integer color of the largest component.
        Returns an empty set and color 0 if no non-zero cells exist.
    """
    # Handle empty grid case
    if not grid or not grid[0]:
        return set(), 0
        
    rows, cols = len(grid), len(grid[0])
    # visited_overall tracks cells that are already part of *any* found component
    # This prevents re-starting BFS for cells already assigned to a component.
    visited_overall = set() 
    largest_component_coords = set()
    largest_size = 0
    largest_component_color = 0

    # Iterate through each cell of the grid
    for r in range(rows):
        for c in range(cols):
            color = grid[r][c]
            # If it's a non-zero cell and not yet part of any previously found component
            if color != 0 and (r, c) not in visited_overall:
                # Use a temporary visited set specifically for the current BFS search
                # This prevents infinite loops within a single BFS run.
                visited_component_search = set() 
                
                # Find the full monochromatic component starting from (r, c)
                current_component = _bfs_mono(grid, r, c, visited_component_search, color)
                current_size = len(current_component)
                
                # Mark all cells of the found component as visited overall
                # so we don't start new searches from them later.
                visited_overall.update(current_component) 

                # Check if this component is the largest found so far
                if current_size > largest_size:
                    largest_size = current_size
                    largest_component_coords = current_component
                    largest_component_color = color
                    
    return largest_component_coords, largest_component_color

# Helper function to calculate the bounding box of a component
def _get_bounding_box(component_coords: set[tuple[int, int]]) -> tuple[int, int, int, int]:
    """
    Calculates the minimum bounding box (min_row, max_row, min_col, max_col) 
    for a given set of component coordinates.

    Args:
        component_coords: A set of (row, col) tuples.

    Returns:
        A tuple (min_row, max_row, min_col, max_col). 
        Returns (0, -1, 0, -1) if the component_coords set is empty.
    """
    # Handle empty component case
    if not component_coords:
        return 0, -1, 0, -1 # Represents an invalid/empty box

    # Determine the min/max row and column indices from the coordinates
    min_r = min(r for r, c in component_coords)
    max_r = max(r for r, c in component_coords)
    min_c = min(c for r, c in component_coords)
    max_c = max(c for r, c in component_coords)
    return min_r, max_r, min_c, max_c

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Transforms the input grid based on its largest monochromatic component (LMC).
    """
    
    # 1. Find the largest monochromatic component and its color
    largest_component_coords, lmc_color = _find_largest_mono_component(input_grid)

    # Handle edge case: no non-zero components found in the input grid
    if not largest_component_coords:
        return [] # Return an empty list if no component exists

    # 2. Calculate the bounding box of the largest component
    min_r, max_r, min_c, max_c = _get_bounding_box(largest_component_coords)
    
    # Handle potential edge case: invalid bounding box (shouldn't typically happen if a component was found)
    if max_r < min_r or max_c < min_c:
         return []

    # 3. Calculate output grid dimensions based on the bounding box
    out_rows = max_r - min_r + 1
    out_cols = max_c - min_c + 1

    # 4. Create the output grid (e.g., initialize with zeros)
    output_grid = [[0 for _ in range(out_cols)] for _ in range(out_rows)] 

    # 5. Copy the rectangular slice defined by the bounding box from input_grid to output_grid
    for r_out, r_in in enumerate(range(min_r, max_r + 1)):
        for c_out, c_in in enumerate(range(min_c, max_c + 1)):
            output_grid[r_out][c_out] = input_grid[r_in][c_in]
            
    # 6. Iterate through the output grid and replace background '0's with the LMC color
    for r in range(out_rows):
        for c in range(out_cols):
            if output_grid[r][c] == 0:
                output_grid[r][c] = lmc_color
                
    # 7. Return the fully constructed output grid
    return output_grid