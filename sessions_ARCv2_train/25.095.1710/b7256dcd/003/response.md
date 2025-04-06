```python
import copy
from collections import deque

"""
Transforms a 2D grid of integers based on connected components of non-7 values.

1. Identifies connected components of cells with values other than 7 using 4-way adjacency (up, down, left, right). Cells with value 7 act as boundaries.
2. For each component, determines its properties: size, unique values, and minimum value from the input grid.
3. Determines which single transformation rule applies to the entire component based on these properties.
4. Applies the determined rule to all cells within the component in the output grid.

Rules:
- Rule_Size1: Component size is 1 -> all cells become 7.
- Rule_Size4_Only6: Component size is 4 AND all values are 6 -> all cells remain 6.
- Rule_Size5_Only6: Component size is 5 AND all values are 6 -> all cells become 4.
- Rule_General: None of the above rules apply -> cells with the original minimum value become 7, all other cells become the minimum value.

Cells with the value 7 in the input grid remain unchanged.
"""

def _get_neighbors(r, c, rows, cols):
    """Yields valid neighbor coordinates (up, down, left, right)."""
    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
        nr, nc = r + dr, c + dc
        if 0 <= nr < rows and 0 <= nc < cols:
            yield nr, nc

def _find_component_and_properties(start_r, start_c, grid, visited):
    """
    Finds a connected component using BFS starting from (start_r, start_c)
    and returns its cells, size, unique values, and minimum value.
    Marks visited cells in the `visited` grid.
    """
    rows = len(grid)
    cols = len(grid[0])
    
    # Should not happen if called correctly, but safety check
    if visited[start_r][start_c] or grid[start_r][start_c] == 7:
        return None, 0, set(), float('inf') 

    component_cells = []
    component_values = []
    q = deque([(start_r, start_c)])
    visited[start_r][start_c] = True

    # BFS to find all connected non-7 cells
    while q:
        r, c = q.popleft()
        component_cells.append((r, c))
        component_values.append(grid[r][c])

        for nr, nc in _get_neighbors(r, c, rows, cols):
            if not visited[nr][nc] and grid[nr][nc] != 7:
                visited[nr][nc] = True
                q.append((nr, nc))

    # Calculate component properties
    size = len(component_cells)
    unique_values = set(component_values)
    min_value = min(component_values) if component_values else float('inf') # Handle empty case theoretically

    return component_cells, size, unique_values, min_value


def transform(input_grid: list[list[int]]) -> list[list[int]]:
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
                component_cells, size, unique_values, min_value = _find_component_and_properties(r, c, input_grid, visited)

                # Should always find a component if initial check passes, but check anyway
                if not component_cells:
                    continue 

                # Determine which single rule applies to this component
                apply_rule = None
                if size == 1:
                    apply_rule = "Rule_Size1"
                elif size == 4 and unique_values == {6}:
                    apply_rule = "Rule_Size4_Only6"
                elif size == 5 and unique_values == {6}:
                    apply_rule = "Rule_Size5_Only6"
                else:
                    apply_rule = "Rule_General"

                # Apply the determined transformation rule to all cells in the component
                for cell_r, cell_c in component_cells:
                    if apply_rule == "Rule_Size1":
                        output_grid[cell_r][cell_c] = 7
                    elif apply_rule == "Rule_Size4_Only6":
                        # No change needed, value remains 6
                        pass 
                    elif apply_rule == "Rule_Size5_Only6":
                        output_grid[cell_r][cell_c] = 4
                    elif apply_rule == "Rule_General":
                        original_value = input_grid[cell_r][cell_c]
                        if original_value == min_value:
                            output_grid[cell_r][cell_c] = 7
                        else:
                            output_grid[cell_r][cell_c] = min_value
                            
    # Return the modified grid
    return output_grid
```