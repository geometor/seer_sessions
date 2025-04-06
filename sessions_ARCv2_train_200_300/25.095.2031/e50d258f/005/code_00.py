"""
Transforms the input grid by:
1. Identifying all distinct connected components of non-zero digits (1, 2, 8), treating 0 as background.
2. Filtering these components to keep only those that are "solid rectangles" (their non-zero cells exactly fill their minimal bounding box).
3. Further filtering the solid rectangles to keep only those whose bounding box touches at least one edge of the 10x10 input grid.
4. Selecting the single target component from the filtered list based on minimum area, then minimum top-row index, then minimum left-column index as tie-breakers.
5. Extracting and returning the subgrid corresponding to the selected component's bounding box.
"""

from collections import deque
import sys # Used for float('inf') as initial minimum value

def _find_solid_rect_components(grid: list[list[int]]) -> list[dict]:
    """
    Finds all solid rectangular connected components of non-zero elements
    in the grid and calculates their properties.

    Args:
        grid: The input grid (list of lists).

    Returns:
        A list of dictionaries, where each dictionary represents a solid
        rectangular component and contains:
        - 'bbox': tuple(min_r, min_c, max_r, max_c)
        - 'area': int
        - 'touches_edge': bool
        - 'top_left': tuple(min_r, min_c)
    """
    rows = len(grid)
    cols = len(grid[0])
    visited = set()
    solid_components_info = []

    for r in range(rows):
        for c in range(cols):
            # Start BFS if cell is non-zero and not visited
            if grid[r][c] != 0 and (r, c) not in visited:
                component_cells = []
                q = deque([(r, c)])
                visited.add((r, c))
                min_r, min_c, max_r, max_c = r, c, r, c

                while q:
                    curr_r, curr_c = q.popleft()
                    component_cells.append((curr_r, curr_c))
                    # Update bounding box coordinates dynamically
                    min_r = min(min_r, curr_r)
                    min_c = min(min_c, curr_c)
                    max_r = max(max_r, curr_r)
                    max_c = max(max_c, curr_c)

                    # Check neighbors (up, down, left, right)
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = curr_r + dr, curr_c + dc

                        # Check bounds and if neighbor is non-zero and not visited
                        if 0 <= nr < rows and 0 <= nc < cols and \
                           grid[nr][nc] != 0 and (nr, nc) not in visited:
                            visited.add((nr, nc))
                            q.append((nr, nc))

                # Calculate properties after finding the full component
                bbox = (min_r, min_c, max_r, max_c)
                height = max_r - min_r + 1
                width = max_c - min_c + 1
                bbox_area = height * width
                cell_count = len(component_cells)

                # Check if it's a solid rectangle
                if cell_count == bbox_area:
                    # Check if it touches the edge
                    touches_edge = (min_r == 0 or min_c == 0 or max_r == rows - 1 or max_c == cols - 1)
                    
                    solid_components_info.append({
                        'bbox': bbox,
                        'area': bbox_area,
                        'touches_edge': touches_edge,
                        'top_left': (min_r, min_c)
                    })

    return solid_components_info

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
    Applies the transformation logic to find and extract the target solid
    rectangular component touching the edge.
    """
    # 1. Identify Solid Rectangular Components
    all_solid_components = _find_solid_rect_components(input_grid)

    # 2. Filter by Edge Contact
    candidate_components = [
        comp for comp in all_solid_components if comp['touches_edge']
    ]

    # Handle case where no edge-touching solid component is found
    if not candidate_components:
        return [] # Or handle as appropriate for the specific problem constraints

    # 3. Select the Target Component
    best_component = None
    min_area = sys.float_info.max
    min_row = sys.maxsize # Using maxsize for integer comparison
    min_col = sys.maxsize

    for comp in candidate_components:
        area = comp['area']
        r, c = comp['top_left']

        # Apply selection criteria: min area -> min row -> min col
        if area < min_area:
            min_area = area
            min_row = r
            min_col = c
            best_component = comp
        elif area == min_area:
            if r < min_row:
                min_row = r
                min_col = c
                best_component = comp
            elif r == min_row:
                if c < min_col:
                    min_col = c
                    best_component = comp

    # Ensure a component was selected (should always happen if candidates exist)
    if best_component is None:
         # This case should ideally not be reached if candidate_components is not empty
        return [] 

    # 4. Extract Output using the bounding box of the selected component
    output_grid = _extract_subgrid(input_grid, best_component['bbox'])

    return output_grid