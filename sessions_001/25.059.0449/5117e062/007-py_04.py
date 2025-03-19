import numpy as np

def analyze_example(input_grid, output_grid):
    # 1. Find shapes in input and output
    def find_shapes(grid):
        shapes = []
        visited = set()
        rows, cols = grid.shape

        def is_valid(r, c):
            return 0 <= r < rows and 0 <= c < cols

        def dfs(r, c, shape_color, current_shape):
            if (r, c) in visited or not is_valid(r, c) or grid[r, c] != shape_color:
                return
            visited.add((r, c))
            current_shape.append((r, c))
            for dr, dc in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                dfs(r + dr, c + dc, shape_color, current_shape)

        for r in range(rows):
            for c in range(cols):
                if (r, c) not in visited:
                    shape_color = grid[r, c]
                    if shape_color != 0:  # Don't care about blank
                        current_shape = []
                        dfs(r, c, shape_color, current_shape)
                        shapes.append((shape_color, current_shape))
        return shapes

    input_shapes = find_shapes(input_grid)
    output_shapes = find_shapes(output_grid)

    # 2. Find largest yellow shape in input
    yellow_shapes = [shape for color, shape in input_shapes if color == 4]
    largest_yellow_shape = []
    max_size = 0
    for shape in yellow_shapes:
        size = len(shape)
        if size > max_size:
            max_size = size
            largest_yellow_shape = shape
    
    ly_min_r = min(r for r, c in largest_yellow_shape) if largest_yellow_shape else 0
    ly_max_r = max(r for r, c in largest_yellow_shape) if largest_yellow_shape else 0
    ly_min_c = min(c for r, c in largest_yellow_shape) if largest_yellow_shape else 0
    ly_max_c = max(c for r, c in largest_yellow_shape) if largest_yellow_shape else 0
    ly_area = len(largest_yellow_shape)

    # 3. Analyze output for enclosed shapes
    enclosed_shapes = []
    for color, shape in output_shapes:
        if color != 4:  # Not the yellow outline
          enclosed_shapes.append((color,shape))
            
    # determine area enclosed
    enclosed_area = 0
    if enclosed_shapes:
       for color, shape in enclosed_shapes:
          enclosed_area += len(shape)


    return {
        "largest_yellow_shape_area": ly_area,
        "largest_yellow_shape_bounds": (ly_min_r, ly_max_r, ly_min_c, ly_max_c),
        "enclosed_shapes": enclosed_shapes,
        "enclosed_area": enclosed_area,
    }

# Example Usage (replace with actual grid data)
example_data = [
  (np.array([[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,4,4,4,4,4,4,4,0,0,0,0,0,0,0],
[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,4,0,0,0,0,0,4,0,0,0,0,0,0,0],
[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,4,0,0,0,0,0,4,0,0,0,0,0,0,0],
[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,4,0,0,0,0,0,4,0,0,0,0,0,0,0],
[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,4,4,4,4,4,4,4,0,0,0,0,0,0,0],
[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]]),np.array([[4,4,4,4,4,4,4],
[4,0,0,0,0,0,4],
[4,0,0,0,0,0,4],
[4,0,0,0,0,0,4],
[4,4,4,4,4,4,4]])),
  (np.array([[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
[0,0,0,0,0,0,0,0,0,0,0,0,0,0,4,4,4,4,4,0,0],
[0,0,0,0,0,0,0,0,0,0,0,0,0,0,4,0,0,0,4,0,0],
[0,0,0,0,0,0,0,0,0,0,0,0,0,0,4,0,0,0,4,0,0],
[0,0,0,0,0,0,0,0,0,0,0,0,0,0,4,0,0,0,4,0,0],
[0,0,0,0,0,0,0,0,0,0,0,0,0,0,4,4,4,4,4,0,0],
[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]]),np.array([[4,4,4,4,4],
[4,0,0,0,4],
[4,0,0,0,4],
[4,0,0,0,4],
[4,4,4,4,4]])),
  (np.array([[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
[0,4,4,4,4,4,4,4,4,4,4,4,4,4,0],
[0,4,0,0,0,0,0,0,0,0,0,0,0,4,0],
[0,4,0,0,0,0,0,0,0,0,0,0,0,4,0],
[0,4,0,0,0,0,0,0,0,0,0,0,0,4,0],
[0,4,0,0,0,0,0,0,0,0,0,0,0,4,0],
[0,4,0,0,0,0,0,0,0,0,0,0,0,4,0],
[0,4,0,0,0,0,0,0,0,0,0,0,0,4,0],
[0,4,0,0,0,0,0,0,0,0,0,0,0,4,0],
[0,4,0,0,0,0,0,0,0,0,0,0,0,4,0],
[0,4,0,0,0,0,0,0,0,0,0,0,0,4,0],
[0,4,4,4,4,4,4,4,4,4,4,4,4,4,0],
[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]]),np.array([[4,4,4,4,4,4,4,4,4,4,4,4,4,4],
[4,0,0,0,0,0,0,0,0,0,0,0,0,4],
[4,0,0,0,0,0,0,0,0,0,0,0,0,4],
[4,0,0,0,0,0,0,0,0,0,0,0,0,4],
[4,0,0,0,0,0,0,0,0,0,0,0,0,4],
[4,0,0,0,0,0,0,0,0,0,0,0,0,4],
[4,0,0,0,0,0,0,0,0,0,0,0,0,4],
[4,0,0,0,0,0,0,0,0,0,0,0,0,4],
[4,0,0,0,0,0,0,0,0,0,0,0,0,4],
[4,0,0,0,0,0,0,0,0,0,0,0,0,4],
[4,4,4,4,4,4,4,4,4,4,4,4,4,4]])),
  (np.array([[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
[0,0,0,0,4,4,4,4,4,4,4,4,4,4,4,4,4,0,0],
[0,0,0,0,4,0,0,0,0,0,0,0,0,0,0,0,4,0,0],
[0,0,0,0,4,0,0,0,0,0,0,0,0,0,0,0,4,0,0],
[0,0,0,0,4,0,0,2,2,2,2,2,2,0,0,0,4,0,0],
[0,0,0,0,4,0,0,2,0,0,0,0,2,0,0,0,4,0,0],
[0,0,0,0,4,0,0,2,0,0,0,0,2,0,0,0,4,0,0],
[0,0,0,0,4,0,0,2,0,0,0,0,2,0,0,0,4,0,0],
[0,0,0,0,4,0,0,2,2,2,2,2,2,0,0,0,4,0,0],
[0,0,0,0,4,0,0,0,0,0,0,0,0,0,0,0,4,0,0],
[0,0,0,0,4,0,0,0,0,0,0,0,0,0,0,0,4,0,0],
[0,0,0,0,4,4,4,4,4,4,4,4,4,4,4,4,4,0,0],
[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]]),np.array([[4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4],
[4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,4],
[4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,4],
[4,0,0,2,2,2,2,2,2,0,0,0,4],
[4,0,0,2,0,0,0,0,2,0,0,0,4],
[4,0,0,2,0,0,0,0,2,0,0,0,4],
[4,0,0,2,0,0,0,0,2,0,0,0,4],
[4,0,0,2,2,2,2,2,2,0,0,0,4],
[4,0,0,0,0,0,0,0,0,0,0,0,4],
[4,0,0,0,0,0,0,0,0,0,0,0,4],
[4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4]]))
]

results = [analyze_example(inp, out) for inp, out in example_data]

for i, result in enumerate(results):
    print(f"Example {i+1}:")
    print(f"  Largest Yellow Shape Area: {result['largest_yellow_shape_area']}")
    print(f"  Largest Yellow Shape Bounds: {result['largest_yellow_shape_bounds']}")
    print(f"  Enclosed Shapes: {result['enclosed_shapes']}")
    print(f"  Enclosed Area: {result['enclosed_area']}")