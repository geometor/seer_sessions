import copy

"""
Identifies solid rectangular blocks of color 4 within the input grid. 
For each identified rectangle, it determines a fill color (1 or 2) based on the rectangle's height (H) and width (W).
Rule 1: If H > W, the fill color is 2.
Rule 2: If W > H, the fill color is W - H.
Rule 3: If H == W:
    - If H > 4, the fill color is 2.
    - If H <= 4, the fill color is 1.
The interior cells (excluding the border) of the rectangle in the output grid are then replaced with this calculated fill color, while the border cells remain color 4.
"""

def find_components(grid: list[list[int]], color_to_find: int) -> list[list[tuple[int, int]]]:
    """Finds connected components of a specific color in the grid."""
    rows = len(grid)
    cols = len(grid[0])
    visited = [[False for _ in range(cols)] for _ in range(rows)]
    components = []

    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == color_to_find and not visited[r][c]:
                component = []
                q = [(r, c)]
                visited[r][c] = True
                min_r, max_r = r, r
                min_c, max_c = c, c
                
                while q:
                    row, col = q.pop(0)
                    component.append((row, col))
                    min_r = min(min_r, row)
                    max_r = max(max_r, row)
                    min_c = min(min_c, col)
                    max_c = max(max_c, col)

                    # Explore neighbors (up, down, left, right)
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = row + dr, col + dc
                        if 0 <= nr < rows and 0 <= nc < cols and \
                           grid[nr][nc] == color_to_find and not visited[nr][nc]:
                            visited[nr][nc] = True
                            q.append((nr, nc))
                
                # Basic check if it could be a rectangle before adding
                # A more robust check is done later
                components.append(component)
                
    return components

def get_bounding_box(component: list[tuple[int, int]]) -> tuple[int, int, int, int]:
    """Calculates the minimum and maximum row and column for a component."""
    if not component:
        return -1, -1, -1, -1
    min_r = min(r for r, c in component)
    max_r = max(r for r, c in component)
    min_c = min(c for r, c in component)
    max_c = max(c for r, c in component)
    return min_r, max_r, min_c, max_c

def is_solid_rectangle(grid: list[list[int]], component: list[tuple[int, int]], bbox: tuple[int, int, int, int], expected_color: int) -> bool:
    """Checks if the component perfectly fills its bounding box."""
    min_r, max_r, min_c, max_c = bbox
    height = max_r - min_r + 1
    width = max_c - min_c + 1
    
    # Check if the number of cells in the component matches the bbox area
    if len(component) != height * width:
        return False
        
    # Verify all cells within the bbox have the expected color
    # This also implicitly checks for holes if the component count matched
    for r in range(min_r, max_r + 1):
        for c in range(min_c, max_c + 1):
            if grid[r][c] != expected_color:
                return False # Found a cell within bbox not matching expected color
                
    return True

def determine_fill_color(H: int, W: int) -> int:
    """Determines the fill color based on rectangle height and width."""
    if H > W:
        return 2
    elif W > H:
        # Ensure fill color is at least 1, though examples don't show W-H <= 0
        # Example 1: Rect 1: H=5, W=5 -> 1 (Rule 3b); Rect 2: H=3, W=4 -> 4-3=1 (Rule 2) -- Mistake here, example shows 1.
        # Example 2: Rect 1: H=4, W=4 -> 1 (Rule 3b); Rect 2: H=4, W=6 -> 6-4=2 (Rule 2) 
        # Okay, let's re-evaluate Rule 2 vs Example 1, Rect 2 (H=3, W=4)
        # Input: 3x4 block of 4s. Output: interior is 1. W-H = 4-3 = 1. Rule holds.
        # Let's re-evaluate Rule 3 for Example 1, Rect 1 (H=5, W=5)
        # Input: 5x5 block of 4s. Output: interior is 2. H=5, W=5. H > 4. Rule 3a says 2. Rule holds.
        # It seems the rules derived in the dream phase were correct.
        return W - H
    else: # H == W
        if H > 4:
            return 2
        else: # H <= 4
            return 1

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Identifies solid rectangular blocks of color 4, calculates a fill color (1 or 2) 
    based on dimensions, and replaces the interior of the rectangle with the fill color.
    """
    # Initialize output_grid as a deep copy of the input
    output_grid = copy.deepcopy(input_grid)
    rows = len(input_grid)
    cols = len(input_grid[0])
    visited = [[False for _ in range(cols)] for _ in range(rows)] # Keep track of visited cells for component finding

    # Iterate through the grid to find starting points of potential components
    for r in range(rows):
        for c in range(cols):
            # If we find a color 4 cell that hasn't been visited yet, start exploring
            if input_grid[r][c] == 4 and not visited[r][c]:
                component = []
                q = [(r, c)]
                visited[r][c] = True
                current_component_visited = set([(r,c)]) # Track visited within this specific component search

                # Use BFS to find all connected cells of color 4
                while q:
                    row, col = q.pop(0)
                    component.append((row, col))

                    # Explore neighbors (up, down, left, right)
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = row + dr, col + dc
                        if 0 <= nr < rows and 0 <= nc < cols and \
                           input_grid[nr][nc] == 4 and (nr, nc) not in current_component_visited:
                            visited[nr][nc] = True # Mark globally visited
                            current_component_visited.add((nr,nc))
                            q.append((nr, nc))

                # Process the found component
                if component:
                    bbox = get_bounding_box(component)
                    min_r, max_r, min_c, max_c = bbox
                    
                    # Verify it's a solid rectangle
                    if is_solid_rectangle(input_grid, component, bbox, 4):
                        height = max_r - min_r + 1
                        width = max_c - min_c + 1
                        
                        # Determine the fill color if it's a valid rectangle > 1x1
                        # (A 1xN or Nx1 rectangle has no interior)
                        if height > 1 and width > 1:
                             fill_color = determine_fill_color(height, width)
                             
                             # Fill the interior in the output grid
                             for ir in range(min_r + 1, max_r):
                                 for ic in range(min_c + 1, max_c):
                                     output_grid[ir][ic] = fill_color
                                     
    return output_grid