import numpy as np

"""
Transforms an input grid based on the locations of non-white pixels (source points).

1. Identify all non-white pixels (source points) in the input grid, storing their 
   row, column, and color.
2. Create an output grid of the same dimensions as the input, initialized to white (0).
3. For each source point, fill its corresponding row and column in the output grid 
   with the source point's color. This effectively draws horizontal and vertical lines.
4. Iterate through all unique pairs of distinct source points. For each pair 
   (point1 at (r1, c1), point2 at (r2, c2)), mark the intersection pixels at 
   (r1, c2) and (r2, c1) with red (2).
5. Finally, ensure that the original locations of the source points in the output 
   grid retain their original colors, correcting any overwrites from the line drawing 
   or intersection marking steps.
"""

def find_source_points(grid):
    """Finds all non-white pixels and returns their coordinates and color."""
    points = []
    height, width = grid.shape
    for r in range(height):
        for c in range(width):
            color = grid[r, c]
            if color != 0:
                points.append({'r': r, 'c': c, 'color': color})
    return points

def transform(input_grid):
    """
    Applies the transformation rule to the input grid.
    """
    input_grid_np = np.array(input_grid)
    height, width = input_grid_np.shape

    # 1. Initialize output_grid with white (0)
    output_grid = np.zeros_like(input_grid_np)

    # 2. Find source points
    source_points = find_source_points(input_grid_np)

    # 3. Draw lines for each source point
    for point in source_points:
        r, c, clr = point['r'], point['c'], point['color']
        # Fill row r with color clr
        output_grid[r, :] = clr
        # Fill column c with color clr
        output_grid[:, c] = clr

    # 4. Mark intersections with red (2)
    num_points = len(source_points)
    for i in range(num_points):
        for j in range(i + 1, num_points): # Iterate through unique pairs
            p1 = source_points[i]
            p2 = source_points[j]
            
            # Intersection point 1: row of p1, column of p2
            output_grid[p1['r'], p2['c']] = 2
            # Intersection point 2: row of p2, column of p1
            output_grid[p2['r'], p1['c']] = 2

    # 5. Restore original source point colors
    for point in source_points:
        r, c, clr = point['r'], point['c'], point['color']
        output_grid[r, c] = clr

    return output_grid.tolist()