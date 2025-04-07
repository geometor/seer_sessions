```python
import copy
import collections

"""
Transforms the input grid based on the following rule:
Find all connected regions of cells with the value 0.
For each such region, examine its complete perimeter, which includes all cells 
(including diagonals) that are adjacent to any cell within the region but are not 
part of the region itself.
If and only if every cell in this complete perimeter has the value 5, then change 
all the 0s within that specific region to 2s in the output grid.
Otherwise, the 0s in the region remain 0s.
Cells with the value 5 remain unchanged.
Cells on the grid boundary cannot be part of a fillable region because their perimeter 
implicitly includes coordinates outside the grid, which cannot be '5'.
"""

def _find_connected_region(grid: list[list[int]], start_r: int, start_c: int, visited_main: list[list[bool]]) -> set[tuple[int, int]]:
    """
    Finds a connected region of 0s using Breadth-First Search (BFS).

    Args:
        grid: The input grid.
        start_r: The starting row index.
        start_c: The starting column index.
        visited_main: The main visited grid to mark cells as processed.

    Returns:
        A set of (row, col) tuples representing the connected region of 0s.
    """
    rows = len(grid)
    cols = len(grid[0])
    region_cells = set()
    q = collections.deque([(start_r, start_c)])
    
    # Mark the starting cell as visited and add to region
    visited_main[start_r][start_c] = True
    region_cells.add((start_r, start_c))
    
    moves = [(0, 1), (0, -1), (1, 0), (-1, 0)] # 4-directional connectivity

    while q:
        r, c = q.popleft()
        
        for dr, dc in moves:
            nr, nc = r + dr, c + dc
            
            # Check bounds and if it's a '0' and not yet visited
            if 0 <= nr < rows and 0 <= nc < cols and \
               grid[nr][nc] == 0 and not visited_main[nr][nc]:
                visited_main[nr][nc] = True
                region_cells.add((nr, nc))
                q.append((nr, nc))
                
    return region_cells

def _get_perimeter(region_cells: set[tuple[int, int]], grid_rows: int, grid_cols: int) -> set[tuple[int, int]]:
    """
    Calculates the complete perimeter (8-directional adjacency) of a region.

    Args:
        region_cells: A set of (row, col) tuples for the region.
        grid_rows: Number of rows in the grid.
        grid_cols: Number of columns in the grid.

    Returns:
        A set of (row, col) tuples representing the perimeter cells.
    """
    perimeter_cells = set()
    # Check all 8 neighbors for each cell in the region
    moves = [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)] 
    
    for r, c in region_cells:
        for dr, dc in moves:
            nr, nc = r + dr, c + dc
            
            # Check if neighbor is within bounds
            if 0 <= nr < grid_rows and 0 <= nc < grid_cols:
                neighbor_coord = (nr, nc)
                # If the neighbor is not part of the original region, it's a perimeter cell
                if neighbor_coord not in region_cells:
                    perimeter_cells.add(neighbor_coord)
            else:
                # If a neighbor would be outside the grid, the region touches the boundary.
                # Add a special marker or handle appropriately later. For now, adding None.
                # (Alternatively, could return an empty set immediately if boundary touched)
                 perimeter_cells.add(None) # Indicate boundary contact


    return perimeter_cells

def _check_perimeter_is_all_5(perimeter_cells: set[tuple[int, int]], grid: list[list[int]]) -> bool:
    """
    Checks if all cells in the perimeter set exist and have the value 5.

    Args:
        perimeter_cells: The set of perimeter cell coordinates. Includes None if boundary touched.
        grid: The input grid.

    Returns:
        True if all perimeter cells are '5', False otherwise.
    """
    if not perimeter_cells: # Empty region? Should not happen if called correctly.
        return False
        
    if None in perimeter_cells: # Touched boundary
        return False
        
    for r, c in perimeter_cells:
        # This check should be redundant if _get_perimeter ensures bounds, but good practice.
        # Check if coordinates are valid (already done by _get_perimeter logic)
        # Now, check the value
        if grid[r][c] != 5:
            return False
            
    return True

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    # initialize output_grid as a deep copy
    output_grid = copy.deepcopy(input_grid)
    rows = len(input_grid)
    if rows == 0:
        return []
    cols = len(input_grid[0])
    if cols == 0:
        return [[] for _ in range(rows)]

    # Keep track of visited cells to avoid re-processing regions
    visited_main = [[False for _ in range(cols)] for _ in range(rows)]

    # Iterate through each cell of the grid
    for r in range(rows):
        for c in range(cols):
            # If we find an unvisited '0' cell, start processing its region
            if input_grid[r][c] == 0 and not visited_main[r][c]:
                
                # 1. Find the connected region of 0s this cell belongs to
                #    The visited_main grid is updated within this function
                region = _find_connected_region(input_grid, r, c, visited_main)
                
                # 2. Get the perimeter of this region
                perimeter = _get_perimeter(region, rows, cols)
                
                # 3. Check if the entire perimeter consists of '5's
                if _check_perimeter_is_all_5(perimeter, input_grid):
                    # 4. If yes, fill the region with '2's in the output grid
                    for rr, cc in region:
                        output_grid[rr][cc] = 2
                # Else (perimeter not all 5s), do nothing, cells remain 0 in the copied output_grid

    return output_grid
```