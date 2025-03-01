import numpy as np

def analyze_example(input_grid, output_grid):
    input_grid = np.array(input_grid)
    output_grid = np.array(output_grid)
    input_objects = _find_objects(input_grid)
    output_objects = _find_objects(output_grid)

    print("Input Grid Dimensions:", input_grid.shape)
    print("Output Grid Dimensions:", output_grid.shape)
    print("Number of Input Objects:", len(input_objects))
    print("Number of Output Objects:", len(output_objects))

    for i, obj in enumerate(input_objects):
        print(f"Input Object {i+1}:")
        print(f"  Color: {obj['color']}")
        print(f"  Top Left: {obj['top_left']}")
        print(f"  Dimensions: {obj['rows']}x{obj['cols']}")
        print(f"  Size: {len(obj['coords'])}")

    for i, obj in enumerate(output_objects):
        print(f"Output Object {i+1}:")
        print(f"  Color: {obj['color']}")
        print(f"  Top Left: {obj['top_left']}")
        print(f"  Dimensions: {obj['rows']}x{obj['cols']}")
        print(f"  Size: {len(obj['coords'])}")

# Example Usage (replace with actual data)
examples = [
    (
[[0, 0, 0, 0, 0, 0, 0, 0], [0, 8, 8, 8, 8, 8, 8, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 2, 2, 2, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 3, 3, 3, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 1, 1, 0, 0, 0, 0, 0]],
[[8, 8, 8, 8, 8, 8, 0, 0], [2, 2, 2, 0, 0, 0, 0, 0], [3, 3, 3, 0, 0, 0, 0, 0], [1, 1, 0, 0, 0, 0, 0, 0]]
    ),
    (
[[0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 4, 4, 4, 4, 0], [0, 0, 0, 0, 0, 4, 4, 4, 4, 0], [0, 0, 0, 0, 0, 4, 4, 4, 4, 0], [0, 0, 0, 0, 0, 4, 4, 4, 4, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 3, 3, 3, 0, 0, 0], [0, 0, 0, 0, 3, 3, 3, 0, 0, 0], [0, 0, 0, 0, 3, 3, 3, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]],
[[4, 4, 4, 4, 4, 4, 4, 4, 0, 0], [3, 3, 3, 3, 3, 3, 0, 0, 0, 0]]
    ),
    (
[[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 6, 6, 6, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 6, 6, 6, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 6, 6, 6, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]],
[[6, 6, 6, 6, 6, 6, 6, 6, 6, 0, 0, 0, 0, 0, 0, 0], [7, 7, 7, 7, 7, 7, 7, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
    ),
]

for input_grid, output_grid in examples:
    analyze_example(input_grid, output_grid)
    print("-" * 30)
