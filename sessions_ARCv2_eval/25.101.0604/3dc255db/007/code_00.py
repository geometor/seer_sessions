import copy
import collections
import math

"""
Transforms an input grid based on interactions within multi-color connected components. 
The logic primarily models behavior seen in Training Examples 2 and 3, with specific handling based on max_color and min_color.

1. Identifies connected components (8-way adjacency) of non-zero cells.
2. For components with multiple distinct non-zero colors:
    a. Determines the minimum (`min_color`) and maximum (`max_color`) colors.
    b. **Removal & Propagation Column Logic (Conditional):**
        i. If `max_color` is 7 AND `min_color` > 3 (like Example 3): 
           - Removes *all* cells with color 7 within the component.
           - Identifies the median column among all columns where a 7 was removed for vertical propagation.
        ii. If `max_color` is not 7 (like Example 2):
           - Finds interface cells (adjacent to a different non-zero color within the component).
           - Removes only those interface cells that have the `max_color`.
           - Identifies all columns where any `max_color` interface cell was removed for vertical propagation. (Known Issue: May select too many columns).
        iii. If `max_color` is 7 AND `min_color` <= 3 (like Example 1):
           - This case represents an anomaly observed in Example 1 where the rules differ (interface 7s removed, horizontal modification). 
           - The current code does *not* implement the specific rules for this anomaly and will likely produce incorrect results for such cases. It defaults to the "max_color is not 7" removal logic but skips propagation.
    c. **Vertical Propagation Logic (Applies to Cases i and ii):** 
       For each identified propagation column, finds the minimum row (`min_row_col`) the component occupied in that column. Then, fills the contiguous block of background (0) cells in the *input* grid located directly above this position (ending at `min_row_col - 1`) with the `max_color` in the *output* grid.
3. Components with only one non-zero color are left unchanged.
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
            # Start BFS from an unvisited non-zero cell
            if grid[r][c] != 0 and (r, c) not in visited:
                component_cells = set()
                component_colors = set()
                q = collections.deque([(r, c)])
                visited.add((r, c))

                while q:
                    curr_r, curr_c = q.popleft()
                    component_cells.add((curr_r, curr_c))
                    component_colors.add(grid[curr_r][curr_c])

                    # Explore neighbors
                    for nr, nc in get_neighbors(curr_r, curr_c, rows, cols):
                        if grid[nr][nc] != 0 and (nr, nc) not in visited:
                            visited.add((nr, nc))
                            q.append((nr, nc))

                # Ensure only non-zero colors are stored and component is not empty
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
    
    # Pre-fetch colors for faster lookup within the component
    component_data = {cell: grid[cell[0]][cell[1]] for cell in component_cells}
    
    for r, c in component_cells:
        cell_color = component_data.get((r, c), 0) # Use .get for safety
        # Skip background cells if they somehow got included
        if cell_color == 0: continue 
            
        is_interface = False
        # Check neighbors
        for nr, nc in get_neighbors(r, c, rows, cols):
            # Check if neighbor is in the same component
            if (nr, nc) in component_data: 
                neighbor_color = component_data[(nr, nc)]
                # Check if neighbor has a different non-zero color
                if neighbor_color != 0 and neighbor_color != cell_color:
                    is_interface = True
                    break # Found an interface neighbor, no need to check further
        if is_interface:
            interface_cells.add((r, c))
            
    return interface_cells


def transform(input_grid: list[list[int]]) -> list[list[int]]:  
    # Initialize output_grid as a deep copy to avoid modifying the input
    output_grid = copy.deepcopy(input_grid)
    rows = len(input_grid)
    cols = len(input_grid[0]) if rows > 0 else 0

    # Find all connected components of non-zero cells
    components = find_components(input_grid)

    # Process each component
    for component_cells, component_colors in components:
        
        # Skip components with only one non-zero color
        if len(component_colors) <= 1:
            continue

        # Determine min and max colors for this multi-color component
        min_color = min(component_colors)
        max_color = max(component_colors)

        # Calculate minimum row for each column within the component for later propagation reference
        min_row_in_col = collections.defaultdict(lambda: rows)
        for r_comp, c_comp in component_cells:
            min_row_in_col[c_comp] = min(min_row_in_col[c_comp], r_comp)

        # Initialize set to store columns where propagation should occur
        propagation_columns = set()
        perform_propagation = True # Flag to control propagation step

        # --- Removal Step & Propagation Column Determination (Conditional Logic) ---
        
        # Case A: max_color is 7 AND min_color > 3 (like Example 3)
        if max_color == 7 and min_color > 3:
            cells_to_remove = set()
            removed_cols_list = []
            # Identify all cells with color 7 in this component
            for r_comp, c_comp in component_cells:
                if input_grid[r_comp][c_comp] == 7:
                    cells_to_remove.add((r_comp, c_comp))
                    removed_cols_list.append(c_comp) # Track columns containing removed 7s
            
            # Remove the identified cells in the output grid
            for r_rem, c_rem in cells_to_remove:
                output_grid[r_rem][c_rem] = 0

            # Determine propagation column (median of unique columns where 7s were removed)
            if removed_cols_list:
                unique_sorted_cols = sorted(list(set(removed_cols_list)))
                median_index = math.floor(len(unique_sorted_cols) / 2) 
                if median_index < len(unique_sorted_cols): 
                    propagation_columns.add(unique_sorted_cols[median_index])
            else: # If no 7s were actually found (edge case), don't propagate
                 perform_propagation = False 

        # Case C: max_color is 7 AND min_color <= 3 (Anomaly like Example 1)
        elif max_color == 7 and min_color <= 3:
             # This case follows different rules (remove interface 7s, horizontal changes)
             # Implementing the removal part similar to Case B for now, but skipping propagation.
             interface_cells = find_interface_cells(input_grid, component_cells)
             cells_to_remove = set()
             for r_int, c_int in interface_cells:
                 if input_grid[r_int][c_int] == max_color: # Remove interface 7s
                     cells_to_remove.add((r_int, c_int))
             for r_rem, c_rem in cells_to_remove:
                 output_grid[r_rem][c_rem] = 0
             perform_propagation = False # Skip vertical propagation for this anomalous case

        # Case B: max_color is not 7 (like Example 2)
        else: 
            interface_cells = find_interface_cells(input_grid, component_cells)
            cells_to_remove = set()
            # Identify interface cells that have the max_color
            for r_int, c_int in interface_cells:
                if input_grid[r_int][c_int] == max_color:
                    cells_to_remove.add((r_int, c_int))
                    # Add the column of *any* removed max_color interface cell for propagation
                    propagation_columns.add(c_int) 
            # Remove the identified cells in the output grid
            for r_rem, c_rem in cells_to_remove:
                 output_grid[r_rem][c_rem] = 0
            
            if not propagation_columns: # If no max interface cells were removed, don't propagate
                perform_propagation = False


        # --- Vertical Propagation Step (Only if perform_propagation is True) ---
        if perform_propagation:
            for c_prop in propagation_columns:
                # Get the minimum row the component occupied in this column
                min_row_col = min_row_in_col.get(c_prop, rows) # Use .get for safety
                if min_row_col == rows: continue # Skip if component wasn't actually in this column

                # Trace upwards from the cell just above the component's top in this column
                fill_cells = []
                r_trace = min_row_col - 1
                # Use the *input_grid* to find the block of 0s
                while r_trace >= 0 and input_grid[r_trace][c_prop] == 0:
                    fill_cells.append((r_trace, c_prop))
                    r_trace -= 1
                
                # Fill the identified block in the *output_grid* with the component's max_color
                for r_fill, c_fill in fill_cells:
                     # Check bounds again just in case
                     if 0 <= r_fill < rows and 0 <= c_fill < cols:
                         output_grid[r_fill][c_fill] = max_color

    # Return the modified grid
    return output_grid