```python
import collections
import copy

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Identifies distinct contiguous shapes (non-background color 7) in the input grid.
    For each pair of intersecting shapes (Shape1 of color C1, Shape2 of color C2),
    it finds the intersection coordinates.
    At each intersection coordinate (r, c), if the original color input_grid[r][c] was C1,
    the output_grid[r][c] is changed to C2. If the original color was C2, the
    output_grid[r][c] is changed to C1. Cells not part of any intersection
    retain their original color.
    """

    # Helper function to find connected components (shapes)
    def find_shapes(grid, background_color):
        rows = len(grid)
        cols = len(grid[0])
        visited = set()
        shapes = []

        for r in range(rows):
            for c in range(cols):
                if grid[r][c] != background_color and (r, c) not in visited:
                    color = grid[r][c]
                    current_shape_coords = set()
                    queue = collections.deque([(r, c)])
                    visited.add((r, c))

                    while queue:
                        row, col = queue.popleft()
                        current_shape_coords.add((row, col))

                        # Check neighbors (up, down, left, right)
                        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                            nr, nc = row + dr, col + dc
                            if 0 <= nr < rows and 0 <= nc < cols and \
                               (nr, nc) not in visited and \
                               grid[nr][nc] == color:
                                visited.add((nr, nc))
                                queue.append((nr, nc))

                    if current_shape_coords:
                        shapes.append({'color': color, 'coords': current_shape_coords})
        return shapes

    # Initialize output_grid as a deep copy of the input
    output_grid = [row[:] for row in input_grid]
    rows = len(input_grid)
    cols = len(input_grid[0])
    background_color = 7 # Based on observations

    # 1. Identify shapes
    shapes = find_shapes(input_grid, background_color)

    # 2. Find intersections between all pairs of shapes
    intersections = []
    num_shapes = len(shapes)
    for i in range(num_shapes):
        for j in range(i + 1, num_shapes):
            shape1 = shapes[i]
            shape2 = shapes[j]

            # Calculate intersection coordinates
            intersection_coords = shape1['coords'].intersection(shape2['coords'])

            if intersection_coords:
                intersections.append({
                    'coords': intersection_coords,
                    'shape1_color': shape1['color'],
                    'shape2_color': shape2['color']
                })

    # 3. Modify the output grid based on intersections
    for intersection in intersections:
        c1 = intersection['shape1_color']
        c2 = intersection['shape2_color']
        for r, c in intersection['coords']:
            original_color = input_grid[r][c]
            # Apply the color swap rule
            if original_color == c1:
                output_grid[r][c] = c2
            elif original_color == c2:
                 output_grid[r][c] = c1
            # Else (e.g., if somehow a background cell was included, though unlikely with this logic)
            # keep the original color from the copy, which is input_grid[r][c]

    return output_grid
```