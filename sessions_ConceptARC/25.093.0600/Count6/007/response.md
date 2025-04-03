```python
"""
Identify specific non-zero 'target' cells within a 2D input grid based on their 
spatial relationship to the background and boundary. Target cells are defined as 
non-zero cells that are not directly adjacent (4-way connectivity) to the 
outermost layer of background (0-valued) cells connected to the grid edges.
Count these target cells. Produce a fixed-size output sequence (list, length 7) 
containing the digit '4' for each identified target cell, followed by padding 
'0's to reach the fixed length. Each digit in the sequence corresponds to a 
distinct item/line in the final output representation expected by the evaluator.
"""

import numpy as np
import collections

def _find_outer_background_coords(grid: np.ndarray) -> set:
    """
    Identifies the coordinates of all background (0) cells connected to the 
    grid edges using Breadth-First Search (BFS).

    Args:
        grid: A numpy array representing the input grid.

    Returns:
        A set containing tuples (row, col) of the outer background cells.
    """
    rows, cols = grid.shape
    outer_background = set()
    q = collections.deque()
    visited = set() # Keep track of visited 0s to avoid cycles and redundant checks

    # Seed the queue with all 0-valued cells on the border
    for r in range(rows):
        for c in [0, cols - 1]: # Left and right edges
            if grid[r, c] == 0 and (r, c) not in visited:
                q.append((r, c))
                visited.add((r, c))
                outer_background.add((r, c))
    # Use range(cols) instead of range(1, cols-1) to include corners if they are 0
    for c in range(cols): 
        for r in [0, rows - 1]: # Top and bottom edges
             if grid[r, c] == 0 and (r, c) not in visited:
                q.append((r, c))
                visited.add((r, c))
                outer_background.add((r, c))

    # Perform BFS to find all connected 0s from the border
    while q:
        r, c = q.popleft()
        # Check 4 neighbours (up, down, left, right)
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nr, nc = r + dr, c + dc
            # Check if the neighbour is within grid bounds
            if 0 <= nr < rows and 0 <= nc < cols:
                # Check if the neighbour is a 0 and not visited yet
                if grid[nr, nc] == 0 and (nr, nc) not in visited:
                    visited.add((nr, nc))
                    outer_background.add((nr, nc))
                    q.append((nr, nc)) # Add neighbour to the queue

    return outer_background

def _find_boundary_coords(grid: np.ndarray, outer_background_coords: set) -> set:
    """
    Identifies the coordinates of all non-zero cells adjacent (4-way) to the 
    outer background cells.

    Args:
        grid: A numpy array representing the input grid.
        outer_background_coords: A set of coordinates for the outer background cells.

    Returns:
        A set containing tuples (row, col) of the boundary cells.
    """
    rows, cols = grid.shape
    boundary_coords = set()

    # Iterate through all cells identified as outer background
    for r_bg, c_bg in outer_background_coords:
        # Check 4 neighbours of each outer background cell
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nr, nc = r_bg + dr, c_bg + dc
            # Check if the neighbour is within bounds and is non-zero
            if 0 <= nr < rows and 0 <= nc < cols and grid[nr, nc] != 0:
                # If it's a non-zero neighbor of the outer background, it's a boundary cell
                boundary_coords.add((nr, nc))
    
    # Alternative implementation: Iterate through all non-zero cells and check neighbours
    # for r in range(rows):
    #     for c in range(cols):
    #         # Consider only non-zero cells
    #         if grid[r, c] != 0:
    #             is_boundary = False
    #             # Check 4 neighbours
    #             for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
    #                 nr, nc = r + dr, c + dc
    #                 # Check if the neighbour is within bounds and is part of the outer background
    #                 if 0 <= nr < rows and 0 <= nc < cols and (nr, nc) in outer_background_coords:
    #                     is_boundary = True
    #                     break # Found an outer background neighbor, no need to check further
    #             # If it's adjacent to the outer background, add it to the boundary set
    #             if is_boundary:
    #                 boundary_coords.add((r, c))

    return boundary_coords

def _count_target_cells(grid: np.ndarray, boundary_coords: set) -> int:
    """
    Counts the number of non-zero cells that are not boundary cells.

    Args:
        grid: A numpy array representing the input grid.
        boundary_coords: A set of coordinates for the boundary cells.

    Returns:
        The integer count of target cells.
    """
    rows, cols = grid.shape
    target_count = 0
    # Iterate through all cells
    for r in range(rows):
        for c in range(cols):
            # A cell is a target if it's non-zero AND its coordinate is not in the boundary set
            if grid[r, c] != 0 and (r, c) not in boundary_coords:
                target_count += 1
    return target_count

def transform(input_grid) -> list:
    """
    Transforms the input grid into a fixed-length list representing the count 
    of spatially defined 'target' cells.
    
    Args:
        input_grid: A list of lists or numpy array representing the grid.

    Returns:
        A list of integers (length 7) representing the count of target cells, 
        with each target cell represented by a 4, padded with 0s.
    """
    # Convert input to numpy array for easier processing
    grid = np.array(input_grid)
    
    # Define the fixed length for the output list
    fixed_output_length = 7
    
    # --- Workflow ---
    
    # 1. Find coordinates of the outer background (0s connected to edges)
    outer_background_coords = _find_outer_background_coords(grid)

    # 2. Find coordinates of boundary cells (non-zero cells adjacent to outer background)
    boundary_coords = _find_boundary_coords(grid, outer_background_coords)

    # 3. Count target cells (non-zero cells that are not boundary cells)
    target_cell_count = _count_target_cells(grid, boundary_coords)

    # 4. Construct the output list
    output_list = []
    
    # Add a '4' for each target cell found, up to the fixed length
    num_fours = min(target_cell_count, fixed_output_length)
    for _ in range(num_fours):
        output_list.append(4)

    # Pad with '0's until the list reaches the fixed length
    num_zeros = fixed_output_length - len(output_list)
    for _ in range(num_zeros):
        output_list.append(0)

    # Return the final list of 7 integers
    return output_list
```