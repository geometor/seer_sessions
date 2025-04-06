import copy
from collections import deque

"""
Transforms a 2D grid of integers based on connected components of non-7 values.

The transformation operates on connected components of cells with values other than 7, 
using 4-way adjacency. Cells with value 7 act as boundaries and remain unchanged.

For each connected component, its properties (size, unique values, minimum value, 
second minimum value, and the locations of cells holding these minimum values) 
determine how the cells within that component are transformed in the output grid.

Specific Rules Applied:
1.  Rule S1 (Size 1): If component size is 1, the cell becomes 7.
2.  Rule S2 (Size 2, All 6s): If size is 2 and the only value is 6, both cells become 3.
3.  Rule S3 (Size 3, All 6s): If size is 3 and the only value is 6, all cells remain 6.
4.  Rule S4 (Size 4, All 6s): If size is 4 and the only value is 6, all cells remain 6.
5.  Rule S5 (Size 5, All 6s): If size is 5 and the only value is 6, all cells become 4.
6.  Rule G1 (General - 1 Unique Value, Not 6): If size > 1 and there's only one unique value (not 6), all cells become 7.
7.  Rule G2 (General - 2 Unique Values): If there are exactly two unique values:
    - Cells originally holding the minimum value become 7.
    - All other cells become the minimum value.
8.  Rule G3 (General - 3+ Unique Values): If there are three or more unique values:
    - Identify the minimum (`min_val`) and second minimum (`second_min_val`) values.
    - Identify cells originally holding these values (`min_cells`, `second_min_cells`).
    - Cells in `min_cells` and `second_min_cells` become 7.
    - For all other cells in the component:
        - Calculate the shortest path distance within the component to any cell in `min_cells`.
        - Calculate the shortest path distance within the component to any cell in `second_min_cells`.
        - If the distance to a `min_cell` is less than or equal to the distance to a `second_min_cell`, the cell becomes `min_val`.
        - Otherwise, the cell becomes `second_min_val`.
"""

def _get_neighbors(r, c, rows, cols):
    """Yields valid neighbor coordinates (up, down, left, right)."""
    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
        nr, nc = r + dr, c + dc
        if 0 <= nr < rows and 0 <= nc < cols:
            yield nr, nc

def _find_component_and_properties(start_r, start_c, grid, visited):
    """
    Finds a connected component using BFS and calculates its properties.
    Marks visited cells.
    Returns: component_cells (list of ((r,c), value)), size, unique_values (sorted list), 
             min_val, min_cells (set of (r,c)), second_min_val, second_min_cells.
    """
    rows = len(grid)
    cols = len(grid[0])
    
    if visited[start_r][start_c] or grid[start_r][start_c] == 7:
        return None, 0, [], float('inf'), set(), float('inf'), set()

    component_cells_dict = {} # Store {(r, c): value}
    q = deque([(start_r, start_c)])
    visited[start_r][start_c] = True
    
    component_cells_set = set() # Keep track of component coordinates efficiently

    while q:
        r, c = q.popleft()
        component_cells_dict[(r, c)] = grid[r][c]
        component_cells_set.add((r,c))

        for nr, nc in _get_neighbors(r, c, rows, cols):
            if not visited[nr][nc] and grid[nr][nc] != 7:
                visited[nr][nc] = True
                q.append((nr, nc))

    component_cells_list = list(component_cells_dict.items())
    size = len(component_cells_list)
    
    if not component_cells_list:
         return [], 0, [], float('inf'), set(), float('inf'), set()

    values = [v for (r,c), v in component_cells_list]
    unique_values = sorted(list(set(values)))
    
    min_val = unique_values[0]
    min_cells = {pos for pos, val in component_cells_list if val == min_val}
    
    second_min_val = float('inf')
    second_min_cells = set()
    if len(unique_values) >= 2:
        second_min_val = unique_values[1]
        second_min_cells = {pos for pos, val in component_cells_list if val == second_min_val}

    return component_cells_dict, size, unique_values, min_val, min_cells, second_min_val, second_min_cells, component_cells_set

def _bfs_distance(component_cells_set, start_cells, grid_rows, grid_cols):
    """
    Performs BFS within a component to find shortest distances from start_cells.
    Returns a dictionary {(r, c): distance} for cells reachable from start_cells.
    """
    distances = {}
    q = deque()
    
    # Initialize queue with start cells and distance 0
    for r, c in start_cells:
        if (r, c) in component_cells_set: # Ensure start cell is part of the component
             distances[(r,c)] = 0
             q.append(((r, c), 0)) # Store ((r,c), dist)
             
    processed = set(start_cells) # Keep track of cells added to queue

    while q:
        (r, c), dist = q.popleft()

        for nr, nc in _get_neighbors(r, c, grid_rows, grid_cols):
            neighbor_pos = (nr, nc)
            # Check if neighbor is within the component and not yet processed
            if neighbor_pos in component_cells_set and neighbor_pos not in processed:
                processed.add(neighbor_pos)
                distances[neighbor_pos] = dist + 1
                q.append((neighbor_pos, dist + 1))
                
    return distances


def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Applies the transformation rules to the input grid based on connected components.
    """
    # Handle empty grid case
    if not input_grid or not input_grid[0]:
        return []

    rows = len(input_grid)
    cols = len(input_grid[0])

    # Initialize output_grid as a deep copy of the input
    output_grid = copy.deepcopy(input_grid)

    # Keep track of visited cells to avoid reprocessing components
    visited = [[False for _ in range(cols)] for _ in range(rows)]

    # Iterate through each cell to find components
    for r in range(rows):
        for c in range(cols):
            # If cell is active (not 7) and not yet visited, it's the start of a new component
            if input_grid[r][c] != 7 and not visited[r][c]:
                
                # Find the component and its properties
                component_cells_dict, size, unique_values, min_val, min_cells, second_min_val, second_min_cells, component_cells_set = \
                    _find_component_and_properties(r, c, input_grid, visited)

                # Should always find a component if initial check passes, but check anyway
                if not component_cells_dict:
                    continue 

                # --- Determine and Apply Transformation Rule ---
                
                # Rule S1 (Size 1)
                if size == 1:
                    cell_r, cell_c = list(component_cells_dict.keys())[0]
                    output_grid[cell_r][cell_c] = 7
                
                # Rules for components containing only 6s
                elif unique_values == [6]:
                    new_val = 6 # Default for S3, S4
                    if size == 2: # Rule S2
                        new_val = 3
                    elif size == 5: # Rule S5
                        new_val = 4
                    # Apply for S2, S3, S4, S5 (and potentially others if size>5 all 6s exist)
                    for cell_r, cell_c in component_cells_dict:
                         output_grid[cell_r][cell_c] = new_val

                # Rule G1 (General - 1 Unique Value, Not 6)
                elif len(unique_values) == 1: # Size > 1 implicitly (handled S1) and value != 6 (handled above)
                    for cell_r, cell_c in component_cells_dict:
                        output_grid[cell_r][cell_c] = 7

                # Rule G2 (General - 2 Unique Values)
                elif len(unique_values) == 2:
                    for (cell_r, cell_c), original_value in component_cells_dict.items():
                        if original_value == min_val:
                            output_grid[cell_r][cell_c] = 7
                        else: # Must be the second unique value
                            output_grid[cell_r][cell_c] = min_val
                
                # Rule G3 (General - 3+ Unique Values)
                elif len(unique_values) >= 3:
                    # Calculate distances needed for G3
                    dist_to_min = _bfs_distance(component_cells_set, min_cells, rows, cols)
                    dist_to_second = _bfs_distance(component_cells_set, second_min_cells, rows, cols)

                    for (cell_r, cell_c), original_value in component_cells_dict.items():
                        # Cells that were originally min or second min become 7
                        if original_value == min_val or original_value == second_min_val:
                            output_grid[cell_r][cell_c] = 7
                        else:
                            # For other cells, compare distances
                            d1 = dist_to_min.get((cell_r, cell_c), float('inf'))
                            d2 = dist_to_second.get((cell_r, cell_c), float('inf'))
                            
                            if d1 <= d2:
                                output_grid[cell_r][cell_c] = min_val
                            else:
                                output_grid[cell_r][cell_c] = second_min_val

    # Return the modified grid
    return output_grid