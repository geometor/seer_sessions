```python
import copy
import collections

"""
Identifies non-zero shapes (8-way connected components) and zero components (4-way connected components) in the input grid.
Determines if a zero component constitutes a "hole" within a single, unique non-zero shape instance by checking if all of the zero component's non-zero orthogonal neighbors belong exclusively to that single shape instance.
If a zero component is identified as a hole, a fill color (F) is determined based on the enclosing shape's color (C) and the colors of other shapes present in the grid, according to specific rules:
- C=3 -> F=3
- C=7 -> F=7
- C=8 -> F=1
- C=2 -> F=7
- C=4 -> Depends on the minimum border color (min_obd) of *other* distinct shape instances:
    - If min_obd=5 -> F=5
    - If min_obd=3 -> F=6
    - Otherwise -> F=None (no fill)
- Other C (e.g., 5) -> F=None (no fill)
If a fill color F is determined, all cells within the identified hole (the zero component) are updated to F in the output grid. Cells that are not part of such a fillable hole remain unchanged.
"""


def _find_shapes(grid: list[list[int]]) -> tuple[list[dict], dict[tuple[int, int], int]]:
    """
    Finds all connected components of identical non-zero digits (8-way adjacency).
    Assigns a unique integer ID to each shape.

    Args:
        grid: The input grid.

    Returns:
        A tuple containing:
        - A list of dictionaries, where each dictionary represents a shape
          and contains 'color' (the digit), 'cells' (a set of (row, col) tuples),
          and 'id' (a unique integer).
        - A dictionary mapping each cell (r, c) belonging to a shape to its shape ID.
    """
    rows = len(grid)
    cols = len(grid[0])
    visited = set()
    shapes = []
    cell_to_shape_id_map = {}
    next_shape_id = 0

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
                
                # Assign unique ID and create shape object
                current_shape_id = next_shape_id
                current_shape = {'color': color, 'cells': shape_cells, 'id': current_shape_id} 
                shapes.append(current_shape)
                for cell in shape_cells:
                    cell_to_shape_id_map[cell] = current_shape_id # Map cell to the shape ID
                next_shape_id += 1 # Increment ID for the next shape
                    
    return shapes, cell_to_shape_id_map

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
                if component_cells: # Only add if component has cells
                    zero_components.append(component_cells)
                
    return zero_components

def _determine_fill_color(enclosing_shape: dict, all_shapes: list[dict]) -> int | None:
    """
    Determines the fill color based on the enclosing shape's color and other shapes present.

    Args:
        enclosing_shape: The shape dictionary ({'color', 'cells', 'id'}) enclosing the hole.
        all_shapes: A list of all shape dictionaries found in the grid.

    Returns:
        The fill color (int) or None if no fill should occur.
    """
    shape_color = enclosing_shape['color']
    shape_id = enclosing_shape['id']
    
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
            # Compare using the unique shape ID
            if shape['id'] != shape_id: 
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

    # Step 1: Identify all non-zero shapes (8-way) and create a cell -> shape ID map
    all_shapes, cell_to_shape_id_map = _find_shapes(input_grid)
    if not all_shapes: # No shapes, no holes possible, return copy
        return output_grid 

    # Step 1b: Create a lookup map from shape ID to shape object for convenience
    shape_lookup = {shape['id']: shape for shape in all_shapes}

    # Step 2: Find all connected components of zeros (4-way)
    zero_components = _find_zero_components(input_grid)
    
    # Step 3: Process each zero component to see if it's a hole
    for zero_comp_cells in zero_components:
        neighbor_shape_ids = set() # Store unique IDs of neighboring shapes
        
        # Step 3a: Find all unique non-zero orthogonal neighbors and their shape IDs
        for rz, cz in zero_comp_cells:
            for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]: # Orthogonal neighbors
                nr, nc = rz + dr, cz + dc
                if 0 <= nr < rows and 0 <= nc < cols:
                    neighbor_pos = (nr, nc)
                    # Check if the neighbor is non-zero and belongs to a shape
                    if neighbor_pos in cell_to_shape_id_map:
                        neighbor_shape_ids.add(cell_to_shape_id_map[neighbor_pos])
        
        # Step 3b: Check if it's a hole (all non-zero neighbors belong to exactly one shape ID)
        if len(neighbor_shape_ids) == 1:
            enclosing_shape_id = list(neighbor_shape_ids)[0] # Get the single enclosing shape ID
            enclosing_shape = shape_lookup[enclosing_shape_id] # Get the shape object
            
            # Step 4: Determine the fill color based on the enclosing shape and context
            fill_color = _determine_fill_color(enclosing_shape, all_shapes)

            # Step 5: Apply the fill color to the output grid if determined
            if fill_color is not None:
                for r_fill, c_fill in zero_comp_cells:
                     # Check if the cell is still 0 (safety, might be filled by another hole's logic if overlaps occurred, though unlikely with this definition)
                     if output_grid[r_fill][c_fill] == 0:
                          output_grid[r_fill][c_fill] = fill_color

    # Step 6: Return the modified grid
    return output_grid
```