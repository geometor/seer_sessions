```python
import numpy as np
import math

"""
Transforms an input grid according to the following rule:
1. Initialize the output grid as a copy of the input grid.
2. Assume the border color is magenta (6) and the internal background color is orange (7). Define the color to place on the opposite side as white (0).
3. Identify all distinct connected objects within the grid that are neither the border color nor the background color.
4. For each identified object:
    a. Calculate its geometric center coordinates (average row `center_r`, average column `center_c`).
    b. Determine the integer floor of the center coordinates: `derived_row = floor(center_r)`, `derived_col = floor(center_c)`.
    c. Determine the primary projection axis and target border:
        i.  If `derived_col` is less than `derived_row`, project horizontally (Left or Right).
            * Determine the target border: If `derived_col` is closer to the left edge (index 0) than the right edge (index `grid_cols - 1`), the target border is Left. Otherwise, it's Right. (Check: `derived_col < (grid_cols - 1 - derived_col)`).
        ii. Else (`derived_row` is less than or equal to `derived_col`), project vertically (Top or Bottom).
            * Determine the target border: If `derived_row` is closer to the top edge (index 0) than the bottom edge (index `grid_rows - 1`), the target border is Top. Otherwise, it's Bottom. (Check: `derived_row < (grid_rows - 1 - derived_row)`).
    d. Determine the projection coordinate along the target border:
        i.  If projecting horizontally (Left/Right), the projection coordinate is `derived_row`.
        ii. If projecting vertically (Top/Bottom), the projection coordinate is `derived_col`.
    e. Determine the target cell coordinates on the chosen border using the projection coordinate.
    f. Determine the opposite cell coordinates on the directly opposite border, using the same projection coordinate.
    g. Modify the output grid: Set the target cell to the object's color and the opposite cell to white (0).
5. Return the modified output grid.
"""

def find_objects(grid, border_color, background_color):
    """
    Finds connected components (objects) in the grid that are not of the border or background color.

    Args:
        grid (np.array): The input grid.
        border_color (int): The color of the border.
        background_color (int): The color of the internal background.

    Returns:
        list: A list of dictionaries, where each dictionary represents an object
              and contains 'color' and 'center' (r, c tuple).
    """
    objects = []
    visited = np.zeros_like(grid, dtype=bool)
    rows, cols = grid.shape

    for r in range(rows):
        for c in range(cols):
            color = grid[r, c]
            # Skip if border, background, or already visited
            if color == border_color or color == background_color or visited[r, c]:
                continue

            obj_pixels = []
            obj_color = color
            q = [(r, c)]
            visited[r, c] = True
            sum_r, sum_c = 0, 0

            # Breadth-First Search (BFS) to find connected pixels of same color
            while q:
                curr_r, curr_c = q.pop(0)
                obj_pixels.append((curr_r, curr_c))
                sum_r += curr_r
                sum_c += curr_c

                # Check 4 neighbors (von Neumann)
                for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                    nr, nc = curr_r + dr, curr_c + dc
                    # Check bounds, color match, and visited status
                    if 0 <= nr < rows and 0 <= nc < cols and \
                       not visited[nr, nc] and grid[nr, nc] == obj_color:
                        visited[nr, nc] = True
                        q.append((nr, nc))

            # Calculate center and add object if pixels found
            if obj_pixels:
                center_r = sum_r / len(obj_pixels)
                center_c = sum_c / len(obj_pixels)
                objects.append({
                    'color': obj_color,
                    'center': (center_r, center_c)
                })
    return objects

def transform(input_grid):
    """
    Transforms the input grid by projecting object colors onto borders based on derived coordinates.

    Args:
        input_grid (list of lists): The input grid represented as a list of lists.

    Returns:
        list of lists: The transformed grid.
    """
    grid = np.array(input_grid, dtype=int)
    output_grid = grid.copy()
    rows, cols = grid.shape
    max_row_idx = rows - 1
    max_col_idx = cols - 1

    # --- Assumptions ---
    border_color = 6 # magenta
    background_color = 7 # orange
    opposite_color = 0 # white
    # -------------------

    # 1. Find all distinct objects
    objects = find_objects(grid, border_color, background_color)

    # 2. Process each object
    for obj in objects:
        obj_color = obj['color']
        center_r, center_c = obj['center']

        # 2a. Calculate derived row and column (floor of center)
        derived_row = math.floor(center_r)
        derived_col = math.floor(center_c)

        # 2b. Determine projection axis and target border
        target_border = None
        project_horizontally = False

        if derived_col < derived_row:
            project_horizontally = True
            # Compare distance to left vs right edge
            if derived_col < (max_col_idx - derived_col):
                target_border = 'Left'
            else:
                target_border = 'Right'
        else: # derived_row <= derived_col
            project_horizontally = False
            # Compare distance to top vs bottom edge
            if derived_row < (max_row_idx - derived_row):
                target_border = 'Top'
            else:
                target_border = 'Bottom'

        # 2c. Determine projection coordinate
        projection_coordinate = -1
        if project_horizontally: # Left or Right
            projection_coordinate = derived_row
        else: # Top or Bottom
            projection_coordinate = derived_col

        # 2d. Determine target and opposite cells
        target_cell = None
        opposite_cell = None

        if target_border == 'Top':
            target_cell = (0, projection_coordinate)
            opposite_cell = (max_row_idx, projection_coordinate)
        elif target_border == 'Bottom':
            target_cell = (max_row_idx, projection_coordinate)
            opposite_cell = (0, projection_coordinate)
        elif target_border == 'Left':
            target_cell = (projection_coordinate, 0)
            opposite_cell = (projection_coordinate, max_col_idx)
        elif target_border == 'Right':
            target_cell = (projection_coordinate, max_col_idx)
            opposite_cell = (projection_coordinate, 0)

        # 2e. Modify output grid (ensure coordinates are valid)
        if target_cell is not None and \
           0 <= target_cell[0] < rows and 0 <= target_cell[1] < cols:
            output_grid[target_cell] = obj_color

        if opposite_cell is not None and \
           0 <= opposite_cell[0] < rows and 0 <= opposite_cell[1] < cols:
            output_grid[opposite_cell] = opposite_color

    # 3. Return the final grid
    return output_grid.tolist()
```