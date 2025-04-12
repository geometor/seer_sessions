```python
import copy
import collections
import math

"""
Transforms an input grid based on interactions within multi-color connected components.

1. Identifies connected components (8-way adjacency) of non-zero cells.
2. For components with multiple distinct non-zero colors:
    a. Determines the maximum color (`max_color`).
    b. **Removal Logic:**
        i. If `max_color` is 7: Removes *all* cells with color 7 within the component.
        ii. If `max_color` is not 7: Finds interface cells (adjacent to a different non-zero color within the component) and removes only those interface cells that have the `max_color`.
    c. **Propagation Column Identification Logic:**
        i. If `max_color` was 7: Identifies the median column among all columns where a 7 was removed.
        ii. If `max_color` was not 7: Identifies columns where a removed `max_color` interface cell was the topmost cell of the component in that specific column.
    d. **Propagation Logic:** For each identified propagation column, finds the minimum row (`min_row_col`) the component occupied in that column. Then, fills the contiguous block of background (0) cells located directly above this position (ending at `min_row_col - 1`) with the `max_color`.
3. Components with only one non-zero color are left unchanged.
4. The transformation primarily models the behavior seen in Training Examples 2 and 3, acknowledging that Example 1 might follow a different rule.
"""

def get_neighbors(r, c, rows, cols):
    """ Helper function to get 8-way neighbors within grid bounds. """
    neighbors = []
    for dr in [-1, 0, 1]:
        for dc in [-1, 0, 1]:
            if dr == 0 and dc == 0:
                continue
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols:
                neighbors.append((nr, nc))
    return neighbors

def find_components(grid: list[list[int]]) -> list[tuple[set[tuple[int, int]], set[int]]]:
    """
    Finds all connected components of non-zero cells using BFS.

    Args:
        grid: The input grid.

    Returns:
        A list of tuples, where each tuple contains:
        - A set of (row, col) coordinates belonging to the component.
        - A set of unique non-zero colors present in the component.
    """
    rows = len(grid)
    cols = len(grid[0]) if rows > 0 else 0
    visited = set()
    components = []

    for r in range(rows):
        for c in range(cols):
            if grid[r][c] != 0 and (r, c) not in visited:
                component_cells = set()
                component_colors = set()
                q = collections.deque([(r, c)])
                visited.add((r, c))

                while q:
                    curr_r, curr_c = q.popleft()
                    component_cells.add((curr_r, curr_c))
                    component_colors.add(grid[curr_r][curr_c])

                    for nr, nc in get_neighbors(curr_r, curr_c, rows, cols):
                        if grid[nr][nc] != 0 and (nr, nc) not in visited:
                            visited.add((nr, nc))
                            q.append((nr, nc))

                # Ensure only non-zero colors are stored
                component_colors.discard(0)
                if component_colors: # Only add components with actual colors
                    components.append((component_cells, component_colors))
    return components

def find_interface_cells(grid: list[list[int]], component_cells: set[tuple[int, int]]) -> set[tuple[int, int]]:
    """
    Identifies interface cells within a component. An interface cell is adjacent
    (8-way) to another cell *within the same component* that has a *different non-zero* color.

    Args:
        grid: The input grid.
        component_cells: Set of (row, col) coordinates for the component.

    Returns:
        A set of (row, col) coordinates of all interface cells.
    """
    rows = len(grid)
    cols = len(grid[0]) if rows > 0 else 0
    interface_cells = set()
    
    # Pre-fetch colors for faster lookup
    component_data = {cell: grid[cell[0]][cell[1]] for cell in component_cells}
    
    for r, c in component_cells:
        cell_color = component_data[(r, c)]
        # Skip background cells if they somehow got included
        if cell_color == 0: continue 
            
        is_interface = False
        for nr, nc in get_neighbors(r, c, rows, cols):
            # Check if neighbor is in the same component
            if (nr, nc) in component_data: 
                neighbor_color = component_data[(nr, nc)]
                # Check if neighbor has a different non-zero color
                if neighbor_color != 0 and neighbor_color != cell_color:
                    is_interface = True
                    break
        if is_interface:
            interface_cells.add((r, c))
            
    return interface_cells

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    # initialize output_grid as a deep copy
    output_grid = copy.deepcopy(input_grid)
    rows = len(input_grid)
    cols = len(input_grid[0]) if rows > 0 else 0

    # Find all connected components
    components = find_components(input_grid)

    # Process each component
    for component_cells, component_colors in components:
        # Skip components with only one color
        if len(component_colors) <= 1:
            continue

        # Determine max color
        max_color = max(component_colors)

        # Calculate minimum row for each column within the component
        min_row_in_col = collections.defaultdict(lambda: rows)
        for r_comp, c_comp in component_cells:
            min_row_in_col[c_comp] = min(min_row_in_col[c_comp], r_comp)

        propagation_columns = set()
        removed_max_cells = set() # Keep track of removed max_color cells

        # --- Removal Step ---
        if max_color == 7:
            # Case 1: Max color is 7 - remove all 7s
            cells_to_remove = set()
            removed_cols_list = []
            for r_comp, c_comp in component_cells:
                if input_grid[r_comp][c_comp] == 7:
                    cells_to_remove.add((r_comp, c_comp))
                    removed_cols_list.append(c_comp)
            
            for r_rem, c_rem in cells_to_remove:
                output_grid[r_rem][c_rem] = 0
                removed_max_cells.add((r_rem, c_rem)) # Track removed 7s

            # Determine propagation column (median)
            if removed_cols_list:
                unique_sorted_cols = sorted(list(set(removed_cols_list)))
                median_index = math.floor(len(unique_sorted_cols) / 2)
                if median_index < len(unique_sorted_cols): # Ensure index is valid
                    propagation_columns.add(unique_sorted_cols[median_index])

        else:
            # Case 2: Max color is not 7 - remove max_color interface cells
            interface_cells = find_interface_cells(input_grid, component_cells)
            cells_to_remove = set()

            for r_int, c_int in interface_cells:
                if input_grid[r_int][c_int] == max_color:
                    cells_to_remove.add((r_int, c_int))
                    # Check if this removed cell is the topmost in its column
                    if r_int == min_row_in_col[c_int]:
                         propagation_columns.add(c_int)

            for r_rem, c_rem in cells_to_remove:
                 output_grid[r_rem][c_rem] = 0
                 removed_max_cells.add((r_rem, c_rem)) # Track removed max cells

        # --- Propagation Step ---
        for c_prop in propagation_columns:
            # Get the minimum row for this component in this column (already calculated)
            min_row_col = min_row_in_col[c_prop]
            
            # Trace upwards from min_row_col - 1 in the *input* grid to find the block of 0s
            fill_cells = []
            r_trace = min_row_col - 1
            # Use input_grid for tracing background
            while r_trace >= 0 and input_grid[r_trace][c_prop] == 0:
                fill_cells.append((r_trace, c_prop))
                r_trace -= 1
            
            # Fill the identified block in the *output* grid with max_color
            for r_fill, c_fill in fill_cells:
                 output_grid[r_fill][c_fill] = max_color

    return output_grid
```