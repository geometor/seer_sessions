def analyze_example(input_grid, output_grid):
    input_objects = find_objects(input_grid)
    output_objects = find_objects(output_grid)

    print("Input Objects:")
    for i, (color, pixels) in enumerate(input_objects):
        rows = [p[0] for p in pixels]
        cols = [p[1] for p in pixels]
        min_row, max_row = min(rows), max(rows)
        min_col, max_col = min(cols), max(cols)
        height = max_row - min_row + 1
        width = max_col - min_col + 1
        print(f"  Object {i+1}:")
        print(f"    Color: {color}")
        print(f"    Bounding Box: ({min_row}, {min_col}) to ({max_row}, {max_col})")
        print(f"    Height: {height}, Width: {width}")
        print(f"    Number of Pixels: {len(pixels)}")

    print("\nOutput Objects:")
    for i, (color, pixels) in enumerate(output_objects):
        rows = [p[0] for p in pixels]
        cols = [p[1] for p in pixels]
        min_row, max_row = min(rows), max(rows)
        min_col, max_col = min(cols), max(cols)
        height = max_row - min_row + 1
        width = max_col - min_col + 1
        print(f"  Object {i+1}:")
        print(f"    Color: {color}")
        print(f"    Bounding Box: ({min_row}, {min_col}) to ({max_row}, {max_col})")
        print(f"    Height: {height}, Width: {width}")
        print(f"    Number of Pixels: {len(pixels)}")
    print(f"Result: {np.array_equal(transform(input_grid), output_grid)}")

# Hypothetical code execution for each example (using the provided example grids).
# I've added example data here so you can imagine how this runs. You CANNOT run this yourself.

example_pairs = [
    (
        [[0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 1, 0, 0, 0], [0, 0, 3, 0, 0, 0], [0, 0, 3, 0, 0, 0]],
        [[1, 3], [1, 3], [1, 3]]
    ),
      (
        [[0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0], [0, 0, 8, 8, 8, 0, 0], [0, 0, 8, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0]],
        [[8, 8, 8], [8, 8, 8], [8, 8, 8]]
      ),
      (
         [[6, 6, 6, 6], [6, 6, 6, 6], [6, 6, 6, 6], [6, 6, 6, 6]],
         [[6, 6, 6, 6], [6, 6, 6, 6], [6, 6, 6, 6], [6, 6, 6, 6]]
      ),
      (
        [[0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 1, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 3, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0]],
        [[7, 7], [7, 7]]
      ),
      (
          [[0, 0, 0, 0, 0, 0, 0], [0, 0, 5, 5, 5, 0, 0], [0, 0, 5, 5, 5, 0, 0], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 3, 0], [0, 0, 0, 0, 0, 0, 0]],
          [[7, 7], [7, 7]]
      )
]

for input_grid, output_grid in example_pairs:
  analyze_example(input_grid, output_grid)
  print("-" * 20)