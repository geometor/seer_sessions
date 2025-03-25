"""
1.  **Find Connected Components:** Identify all connected components of green (3) pixels in the input grid.
2.  **Analyze Each Component:** For each connected component:
    *   If the component is a vertical line, change the topmost green pixel to azure (8).
    *   If the component is a horizontal line, change the leftmost green pixel to azure (8).
    *  If it is a 2x2 block take the top left most green pixel and convert it to azure (8).
    *   If the component forms an "L-shape" (a combination of a vertical and horizontal line that share a corner pixel and can be of any greater dimension than 2x1, 1x2) change the corner pixel where the lines meet to azure (8).
    *   If none of the above conditions are met, consider the other shapes and determine the transformation rule based on the examples. The rule so far is unclear for shapes that are neither lines nor L-shapes.
3. **Output the updated output grid.**
"""

import numpy as np

def get_neighbors(grid, row, col):
    """Gets the valid neighbors of a cell in a grid."""
    rows, cols = grid.shape
    neighbors = []
    if row > 0:
        neighbors.append((row - 1, col))  # Up
    if row < rows - 1:
        neighbors.append((row + 1, col))  # Down
    if col > 0:
        neighbors.append((row, col - 1))  # Left
    if col < cols - 1:
        neighbors.append((row, col + 1))  # Right
    return neighbors

def get_connected_component(grid, start_row, start_col, color):
    """Gets a connected component of a given color starting from a given cell."""
    rows, cols = grid.shape
    component = []
    visited = set()
    queue = [(start_row, start_col)]

    while queue:
        row, col = queue.pop(0)
        if (row, col) in visited or grid[row, col] != color:
            continue
        visited.add((row, col))
        component.append((row, col))
        neighbors = get_neighbors(grid, row, col)
        for neighbor_row, neighbor_col in neighbors:
            queue.append((neighbor_row, neighbor_col))
    return component

def is_vertical_line(component, grid):
    """Checks if a component is a vertical line."""
    if not component:
        return False
    rows, _ = grid.shape
    if len(set(col for _, col in component)) == 1:
      if len(component) > 1:
        return True
    return False

def is_horizontal_line(component, grid):
    """Checks if a component is a horizontal line."""
    if not component:
        return False
    _, cols = grid.shape

    if len(set(row for row, _ in component)) == 1:
      if len(component) > 1:
          return True
    return False

def is_l_shape(component):
    """Checks if a component is an L-shape (can be larger than 2x1 or 1x2)."""
    rows = sorted(list(set(r for r,c in component)))
    cols = sorted(list(set(c for r,c in component)))
    if len(rows) >= 2 and len(cols) >= 2:
        # Check if it's a rectangle or just an L.
        row_counts = {}
        col_counts = {}

        for r, c in component:
          row_counts[r] = row_counts.get(r,0) + 1
          col_counts[c] = col_counts.get(c,0) + 1

        num_rows_with_multiple_cols = sum(1 for count in row_counts.values() if count >1 )
        num_cols_with_multiple_rows = sum(1 for count in col_counts.values() if count>1)

        if num_rows_with_multiple_cols == 1 and num_cols_with_multiple_rows==1:
            return True

    return False
def is_2x2_block(component):
    """check to see if the component is a 2x2 block"""
    rows = sorted(list(set(r for r,c in component)))
    cols = sorted(list(set(c for r,c in component)))
    if len(rows) == 2 and len(cols) == 2 and len(component) == 4:
      return True
    return False

def find_corner(component):
    """finds the corner of the L"""
    rows = [r for r, _ in component]
    cols = [c for _, c in component]
    row_counts = {}
    col_counts = {}

    for r in rows:
        row_counts[r] = row_counts.get(r, 0) + 1
    for c in cols:
        col_counts[c] = col_counts.get(c, 0) + 1

    corner_row = [r for r, count in row_counts.items() if count > 1][0]
    corner_col = [c for c, count in col_counts.items() if count > 1][0]
    return (corner_row, corner_col)


def transform(input_grid):
    """Transforms the input grid according to the specified rule."""
    # Initialize output_grid as a copy of input_grid
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape
    visited = set()

    # Iterate through the grid to find connected components of green (3) pixels
    for row in range(rows):
        for col in range(cols):
            if input_grid[row, col] == 3 and (row, col) not in visited:
                component = get_connected_component(input_grid, row, col, 3)
                visited.update(component)

                # Check the shape of the component and apply the transformation
                if is_vertical_line(component, input_grid):
                    topmost_pixel = min(component, key=lambda p: p[0])
                    output_grid[topmost_pixel] = 8
                elif is_horizontal_line(component, input_grid):
                    leftmost_pixel = min(component, key=lambda p: p[1])
                    output_grid[leftmost_pixel] = 8
                elif is_2x2_block(component):
                    top_left_pixel = min(component, key = lambda p: (p[0],p[1]))
                    output_grid[top_left_pixel] = 8
                elif is_l_shape(component):
                  corner = find_corner(component)
                  output_grid[corner]=8

    return output_grid