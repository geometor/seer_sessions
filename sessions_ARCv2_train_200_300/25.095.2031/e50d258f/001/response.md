```python
"""
Identifies all distinct connected components of non-zero digits (1, 2, or 8) in the input grid, treating 0 as a separator.
For each component, calculates its minimal bounding box.
Finds the single component whose bounding box subgrid in the original input contains *only* non-zero digits (a "solid" bounding box).
Extracts and returns the subgrid corresponding to this solid bounding box.
"""

from collections import deque

def _find_components(grid: list[list[int]]) -> list[list[tuple[int, int]]]:
    """
    Finds all connected components of non-zero elements in the grid.

    Args:
        grid: The input grid.

    Returns:
        A list of components, where each component is a list of (row, col) tuples.
    """
    rows = len(grid)
    cols = len(grid[0])
    visited = set()
    components = []

    for r in range(rows):
        for c in range(cols):
            if grid[r][c] != 0 and (r, c) not in visited:
                # Start BFS to find a new component
                current_component = []
                q = deque([(r, c)])
                visited.add((r, c))

                while q:
                    curr_r, curr_c = q.popleft()
                    current_component.append((curr_r, curr_c))

                    # Check neighbors (up, down, left, right)
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = curr_r + dr, curr_c + dc

                        # Check bounds and if neighbor is non-zero and not visited
                        if 0 <= nr < rows and 0 <= nc < cols and \
                           grid[nr][nc] != 0 and (nr, nc) not in visited:
                            visited.add((nr, nc))
                            q.append((nr, nc))
                
                components.append(current_component)

    return components

def _get_bounding_box(component: list[tuple[int, int]]) -> tuple[int, int, int, int]:
    """
    Calculates the minimal bounding box for a component.

    Args:
        component: A list of (row, col) tuples representing the component.

    Returns:
        A tuple (min_row, min_col, max_row, max_col).
    """
    if not component:
        return (0, 0, -1, -1) # Indicate empty or invalid

    min_r = min(r for r, c in component)
    min_c = min(c for r, c in component)
    max_r = max(r for r, c in component)
    max_c = max(c for r, c in component)

    return min_r, min_c, max_r, max_c

def _is_solid(grid: list[list[int]], bbox: tuple[int, int, int, int]) -> bool:
    """
    Checks if the subgrid defined by the bounding box contains only non-zero elements.

    Args:
        grid: The input grid.
        bbox: The bounding box tuple (min_row, min_col, max_row, max_col).

    Returns:
        True if the bounding box area is solid (no zeros), False otherwise.
    """
    min_r, min_c, max_r, max_c = bbox
    if min_r > max_r or min_c > max_c: # Handle empty case if needed
        return False

    for r in range(min_r, max_r + 1):
        for c in range(min_c, max_c + 1):
            if grid[r][c] == 0:
                return False
    return True

def _extract_subgrid(grid: list[list[int]], bbox: tuple[int, int, int, int]) -> list[list[int]]:
    """
    Extracts the subgrid defined by the bounding box.

    Args:
        grid: The input grid.
        bbox: The bounding box tuple (min_row, min_col, max_row, max_col).

    Returns:
        The extracted subgrid as a list of lists.
    """
    min_r, min_c, max_r, max_c = bbox
    subgrid = []
    for r in range(min_r, max_r + 1):
        subgrid.append(grid[r][min_c : max_c + 1])
    return subgrid

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Transforms the input grid by finding the solid non-zero component and extracting its bounding box.

    Args:
        input_grid: A 2D list of integers representing the input grid.

    Returns:
        A 2D list of integers representing the extracted solid subgrid.
    """
    
    # 1. Identify Non-Zero Components
    components = _find_components(input_grid)
    
    solid_bbox = None

    # Iterate through components to find the solid one
    for component in components:
        if not component:
            continue
            
        # 2. Determine Bounding Boxes for each component
        bbox = _get_bounding_box(component)
        
        # 3. Find Solid Bounding Box
        if _is_solid(input_grid, bbox):
            # 4. Select Target Component (assuming only one solid)
            solid_bbox = bbox
            break # Found the solid bounding box

    if solid_bbox is None:
        # Handle case where no solid bounding box is found, though examples suggest one always exists
        return [] 

    # 5. Extract Output
    output_grid = _extract_subgrid(input_grid, solid_bbox)

    return output_grid
```