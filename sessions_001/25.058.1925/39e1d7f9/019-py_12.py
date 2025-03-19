import numpy as np

def describe_grid(grid):
    """Provides a basic description of the grid."""
    rows, cols = grid.shape
    unique_colors = np.unique(grid)
    print(f"Grid size: {rows}x{cols}")
    print(f"Unique colors: {unique_colors}")

def find_objects(grid):
    """Finds all contiguous regions of the same color."""
    objects = []
    visited = np.zeros_like(grid, dtype=bool)
    rows, cols = grid.shape

    def dfs(r, c, color, obj_coords):
        if (r < 0 or r >= rows or c < 0 or c >= cols or
                visited[r, c] or grid[r, c] != color):
            return
        visited[r, c] = True
        obj_coords.append((r, c))
        dfs(r + 1, c, color, obj_coords)
        dfs(r - 1, c, color, obj_coords)
        dfs(r, c + 1, color, obj_coords)
        dfs(r, c - 1, color, obj_coords)

    for r in range(rows):
        for c in range(cols):
            if not visited[r, c]:
                color = grid[r, c]
                obj_coords = []
                dfs(r, c, color, obj_coords)
                objects.append((color, obj_coords))
    return objects

def is_3x3(obj_coords):
    """Checks if an object is 3x3."""
    rows, cols = zip(*obj_coords)
    return (max(rows) - min(rows) + 1) == 3 and (max(cols) - min(cols) + 1) == 3

def analyze_example(input_grid, output_grid, transformed_grid):
    """Analyzes a single example."""
    print("--- Input Grid ---")
    describe_grid(input_grid)
    print(input_grid)
    input_objects = find_objects(input_grid)
    print(f"Input objects: {len(input_objects)}")

    print("\n--- Expected Output Grid ---")
    describe_grid(output_grid)
    print(output_grid)

    print("\n--- Transformed Grid ---")
    describe_grid(transformed_grid)
    print(transformed_grid)

    print("\n--- Comparison ---")
    if np.array_equal(output_grid, transformed_grid):
        print("Transformation successful!")
    else:
        print("Transformation FAILED.")
        diff = output_grid != transformed_grid
        print("Differences (True where they differ):\n", diff)

    print("-" * 30)


# Example data (replace with your actual data)
example_inputs = [
    np.array([[4, 4, 4, 0, 0, 0, 0, 0, 0],
              [4, 4, 4, 0, 0, 0, 0, 0, 0],
              [4, 4, 4, 0, 0, 0, 0, 0, 0],
              [2, 2, 2, 0, 0, 6, 6, 6, 6],
              [2, 2, 2, 0, 0, 6, 6, 6, 6],
              [2, 2, 2, 0, 0, 6, 6, 6, 6]]),
    np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0, 0],
              [4, 4, 4, 0, 0, 6, 6, 6, 6],
              [4, 4, 4, 0, 0, 6, 6, 6, 6],
              [4, 4, 4, 0, 0, 6, 6, 6, 6]]),
    np.array([[4, 4, 4, 0, 0, 0, 0, 0, 0],
              [4, 4, 4, 0, 0, 0, 0, 0, 0],
              [4, 4, 4, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 6, 6, 6, 6],
              [0, 0, 0, 0, 0, 6, 6, 6, 6],
              [0, 0, 0, 0, 0, 6, 6, 6, 6]])
]
example_outputs = [
     np.array([[2, 2, 2, 0, 0, 0, 0, 0, 0],
               [2, 2, 2, 0, 0, 0, 0, 0, 0],
               [2, 2, 2, 0, 0, 6, 6, 6, 6],
               [4, 4, 4, 0, 0, 6, 6, 6, 6],
               [4, 4, 4, 0, 0, 6, 6, 6, 6],
               [4, 4, 4, 0, 0, 6, 6, 6, 6]]),
    np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0, 0],
              [4, 4, 4, 0, 0, 6, 6, 6, 6],
              [4, 4, 4, 0, 0, 6, 6, 6, 6],
              [4, 4, 4, 0, 0, 6, 6, 6, 6]]),
    np.array([[4, 4, 4, 0, 0, 0, 0, 0, 0],
              [4, 4, 4, 0, 0, 0, 0, 0, 0],
              [4, 4, 4, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 6, 6, 6, 6],
              [0, 0, 0, 0, 0, 6, 6, 6, 6],
              [0, 0, 0, 0, 0, 6, 6, 6, 6]])
]


def transform(input_grid):
    # Initialize output_grid as a copy of the input_grid
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # Find all objects
    objects = find_objects(input_grid)

    # Filter 3x3 objects of color 2 or 4
    filtered_objects = [(color, coords) for color, coords in objects
                         if is_3x3(coords) and color in (2, 4)]

    # Group by column for vertical stacking check.  Use a dictionary keyed by the
    # leftmost column of the object.
    objects_by_column = {}
    for color, coords in filtered_objects:
        min_col = min(c for _, c in coords)
        if min_col not in objects_by_column:
            objects_by_column[min_col] = []
        objects_by_column[min_col].append((color, coords))

    # Check for vertical stacking and perform swaps
    for col_objects in objects_by_column.values():
        # Sort objects by row to check stacking in order
        col_objects.sort(key=lambda x: min(r for r, _ in x[1]))
        
        for i in range(len(col_objects)):
          for j in range(i + 1, len(col_objects)):
            color1, coords1 = col_objects[i]
            color2, coords2 = col_objects[j]
            
            if are_vertically_stacked(coords1, coords2):              
              # Swap colors within the stacked objects
              for r, c in coords1:
                  if output_grid[r, c] == 2:
                      output_grid[r, c] = 4
                  elif output_grid[r, c] == 4:
                      output_grid[r, c] = 2
              for r, c in coords2:
                  if output_grid[r, c] == 2:
                      output_grid[r, c] = 4
                  elif output_grid[r, c] == 4:
                      output_grid[r, c] = 2

    return output_grid

transformed_grids = [transform(inp) for inp in example_inputs]

for i, (inp, exp, trans) in enumerate(zip(example_inputs, example_outputs, transformed_grids)):
    print(f"Example {i+1}:")
    analyze_example(inp, exp, trans)
