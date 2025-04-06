```python
"""
Transforms the input grid by:
1. Identifying all distinct connected components of non-zero digits (1, 2, or 8), treating 0 as background.
2. Calculating the bounding box, area, and cell count for each component.
3. Filtering to find components that perfectly fill their bounding box (area equals cell count).
4. Selecting the perfectly filled component with the minimum bounding box area.
5. Extracting and returning the subgrid corresponding to the selected component's bounding box.
"""

from collections import deque
import sys # Used for float('inf') as initial minimum area

def _find_components(grid: list[list[int]]) -> list[list[tuple[int, int]]]:
    """
    Finds all connected components of non-zero elements in the grid using BFS.

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
            # Start BFS if cell is non-zero and not visited
            if grid[r][c] != 0 and (r, c) not in visited:
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
                
                components.append(current_component) # Add the completed component

    return components

def _get_bounding_box(component: list[tuple[int, int]]) -> tuple[int, int, int, int]:
    """
    Calculates the minimal bounding box for a component.

    Args:
        component: A list of (row, col) tuples representing the component.

    Returns:
        A tuple (min_row, min_col, max_row, max_col). Returns (0, 0, -1, -1) for empty components.
    """
    if not component:
        return (0, 0, -1, -1) # Indicate empty or invalid

    # Find min/max row and column from the component's cell coordinates
    min_r = min(r for r, c in component)
    min_c = min(c for r, c in component)
    max_r = max(r for r, c in component)
    max_c = max(c for r, c in component)

    return min_r, min_c, max_r, max_c

def _calculate_bbox_area(bbox: tuple[int, int, int, int]) -> int:
    """Calculates the area of a bounding box."""
    min_r, min_c, max_r, max_c = bbox
    if min_r > max_r or min_c > max_c: # Handle invalid/empty bbox
        return 0
    height = max_r - min_r + 1
    width = max_c - min_c + 1
    return height * width

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
    if min_r > max_r or min_c > max_c: # Handle invalid/empty bbox
        return []
        
    subgrid = []
    for r in range(min_r, max_r + 1):
        # Extract the row slice corresponding to the bbox columns
        subgrid.append(grid[r][min_c : max_c + 1])
    return subgrid


def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Applies the transformation logic to find and extract the smallest, 
    perfectly filled, non-zero component from the input grid.
    """
    
    # 1. Identify Non-Zero Components
    components = _find_components(input_grid)
    
    min_area = sys.float_info.max # Initialize with positive infinity
    best_bbox = None

    # 2. Calculate Component Properties & 3. Find Perfectly Filled Components
    for component in components:
        if not component:
            continue # Skip empty components if any occur

        cell_count = len(component)
        bbox = _get_bounding_box(component)
        bbox_area = _calculate_bbox_area(bbox)

        # Check if the component perfectly fills its bounding box
        is_perfectly_filled = (bbox_area == cell_count)

        # 4. Select Smallest Perfectly Filled Component
        if is_perfectly_filled:
            # If this component is smaller than the current best, update
            if bbox_area < min_area:
                min_area = bbox_area
                best_bbox = bbox

    # Handle case where no perfectly filled component is found
    if best_bbox is None:
        return [] 

    # 5. Extract Output using the bounding box of the selected component
    output_grid = _extract_subgrid(input_grid, best_bbox)

    return output_grid
```