import copy
import collections

"""
Identifies non-zero shapes (8-way connected components) and zero components (4-way connected components).
Determines if a zero component is a "hole" within a single shape instance by checking if all its non-zero orthogonal neighbors belong exclusively to that shape.
If a zero component is identified as a hole, a fill color (F) is determined based on the enclosing shape's color (C) and the colors of other shapes present:
- C=3 -> F=3
- C=7 -> F=7
- C=8 -> F=1
- C=2 -> F=7
- C=4 -> Depends on the minimum border color (min_obd) of *other* shapes:
    - If min_obd=5 -> F=5
    - If min_obd=3 -> F=6
    - Otherwise -> F=None (no fill)
- Other C (e.g., 5) -> F=None (no fill)
If a fill color F is determined, all cells within the hole (the zero component) are updated to F in the output grid. Other cells remain unchanged.
"""


def _find_shapes(grid: list[list[int]]) -> tuple[list[dict], dict[tuple[int, int], dict]]:
    """
    Finds all connected components of identical non-zero digits (8-way adjacency).
    Assigns a unique object reference as an ID to each shape.

    Args:
        grid: The input grid.

    Returns:
        A tuple containing:
        - A list of dictionaries, where each dictionary represents a shape
          and contains 'color' (the digit) and 'cells' (a set of (row, col) tuples).
          The dictionary object itself serves as the unique ID.
        - A dictionary mapping each cell (r, c) belonging to a shape to its shape object.
    """
    rows = len(grid)
    cols = len(grid[0])
    visited = set()
    shapes = []
    cell_to_shape_map = {}

    for r in range(rows):
        for c in range(cols):
            if grid[r][c] != 0 and (r, c) not in visited:
                color = grid[r][c]
                shape_cells = set()
                q = collections.deque([(r, c)])
                visited.add((r, c))
                shape_cells.add((r, c))

                while q:
                    row, col = q.popleft()
                    # Check 8-way neighbors (orthogonal and diagonal)
                    for dr in [-1, 0, 1]:
                        for dc in [-1, 0, 1]:
                            if dr == 0 and dc == 0:
                                continue
                            nr, nc = row + dr, col + dc
                            if 0 <= nr < rows and 0 <= nc < cols and \
                               (nr, nc) not in visited and grid[nr][nc] == color:
                                visited.add((nr, nc))
                                shape_cells.add((nr, nc))
                                q.append((nr, nc))
                
                # The dictionary object itself acts as a unique ID
                current_shape = {'color': color, 'cells': shape_cells} 
                shapes.append(current_shape)
                for cell in shape_cells:
                    cell_to_shape_map[cell] = current_shape # Map cell to the shape object
                    
    return shapes, cell_to_shape_map

def _find_zero_components(grid: list[list[int]]) -> list[set[tuple[int, int]]]:
    """
    Finds all connected components of zero-valued cells (4-way adjacency).

    Args:
        grid: The input grid.

    Returns:
        A list of sets, where each set contains the (row, col) tuples
        of cells belonging to a single connected component of zeros.
    """
    rows = len(grid)
    cols = len(grid[0])
    visited_zeros = set()
    zero_components = []

    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == 0 and (r, c) not in visited_zeros:
                component_cells = set()
                q = collections.deque([(r, c)])
                visited_zeros.add((r, c))
                component_cells.add((r, c))

                while q:
                    row, col = q.popleft()
                    # Check 4-way neighbors (orthogonal only)
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = row + dr, col + dc
                        if 0 <= nr < rows and 0 <= nc < cols and \
                           grid[nr][nc] == 0 and (nr, nc) not in visited_zeros:
                            visited_zeros.add((nr, nc))
                            component_cells.add((nr, nc))
                            q.append((nr, nc))
                zero_components.append(component_cells)
                
    return zero_components

def _determine_fill_color(enclosing_shape: dict, all_shapes: list[dict]) -> int | None:
    """
    Determines the fill color based on the enclosing shape's color and other shapes present.

    Args:
        enclosing_shape: The shape dictionary enclosing the current hole.
        all_shapes: A list of all shape dictionaries found in the grid.

    Returns:
        The fill color (int) or None if no fill should occur.
    """
    shape_color = enclosing_shape['color']
    
    # Rules based directly on enclosing shape color
    if shape_color == 3:
        return 3
    if shape_color == 7:
        return 7
    if shape_color == 8:
        return 1
    if shape_color == 2:
        return 7
        
    # Rule for C=4 depends on other shapes
    if shape_color == 4:
        other_border_colors = set()
        for shape in all_shapes:
            # Compare using the shape object reference (unique ID)
            if shape is not enclosing_shape: 
                 other_border_colors.add(shape['color'])

        if not other_border_colors:
            return None # No other shapes

        min_obd = min(other_border_colors)
        if min_obd == 5:
            return 5
        if min_obd == 3:
            return 6
        else:
            return None # Min other border color is not 5 or 3
            
    # Default case (includes C=5 and any other unspecified colors)
    return None

def transform(input_grid: list[list[int]]) -> list[list[int]]:  
    # Handle empty grid case
    if not input_grid or not input_grid[0]:
        return []
        
    rows = len(input_grid)
    cols = len(input_grid[0])

    # initialize output_grid as a deep copy
    output_grid = copy.deepcopy(input_grid)

    # 1. Identify all non-zero shapes (8-way) and create a cell -> shape map
    all_shapes, cell_to_shape_map = _find_shapes(input_grid)
    if not all_shapes: # No shapes, no holes possible
        return output_grid 

    # 2. Find all connected components of zeros (4-way)
    zero_components = _find_zero_components(input_grid)
    
    # 3. Process each zero component to see if it's a hole
    for zero_comp_cells in zero_components:
        neighbor_shapes = set()
        has_zero_neighbor = False # Flag if component touches other zeros (or boundary implicitly) - may not be needed with explicit shape check
        
        # 3a. Find all unique non-zero orthogonal neighbors and their shapes
        non_zero_neighbors = set()
        for rz, cz in zero_comp_cells:
            for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                nr, nc = rz + dr, cz + dc
                if 0 <= nr < rows and 0 <= nc < cols:
                    neighbor_val = input_grid[nr][nc]
                    neighbor_pos = (nr, nc)
                    if neighbor_val != 0:
                        non_zero_neighbors.add(neighbor_pos)
                    #elif neighbor_pos not in zero_comp_cells: # Optional check if needed
                    #    has_zero_neighbor = True 
                else:
                    # Touches boundary - might imply not a hole, but let shape check decide
                    pass 
        
        if not non_zero_neighbors: # Isolated zero component surrounded by zeros (or only boundary)
             continue

        # 3b. Get the shape instances corresponding to the non-zero neighbors
        for r_neigh, c_neigh in non_zero_neighbors:
             if (r_neigh, c_neigh) in cell_to_shape_map:
                  neighbor_shapes.add(cell_to_shape_map[(r_neigh, c_neigh)])
        
        # 3c. Check if it's a hole (all non-zero neighbors belong to exactly one shape)
        if len(neighbor_shapes) == 1:
            enclosing_shape = list(neighbor_shapes)[0] # Get the single enclosing shape object
            
            # 4. Determine the fill color based on the enclosing shape and context
            fill_color = _determine_fill_color(enclosing_shape, all_shapes)

            # 5. Apply the fill color to the output grid if determined
            if fill_color is not None:
                for r_fill, c_fill in zero_comp_cells:
                     # Check if the cell is still 0 (safety, shouldn't be needed if logic is sound)
                     if output_grid[r_fill][c_fill] == 0:
                          output_grid[r_fill][c_fill] = fill_color

    return output_grid