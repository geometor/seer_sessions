def code_execution(input_grid, output_grid, predicted_output):
    import numpy as np

    def get_objects(grid):
        objects = {}
        for color in np.unique(grid):
            coords = np.argwhere(grid == color)
            if coords.size > 0:
                min_row, max_row = np.min(coords[:, 0]), np.max(coords[:, 0])
                min_col, max_col = np.min(coords[:, 1]), np.max(coords[:, 1])
                objects[color] = {
                    'coords': coords.tolist(),
                    'bounding_box': (min_row, max_row, min_col, max_col),
                    'size': (max_row - min_row + 1, max_col - min_col + 1)
                }
        return objects
    
    input_grid = np.array(input_grid)
    output_grid = np.array(output_grid)
    predicted_output = np.array(predicted_output)

    input_objects = get_objects(input_grid)
    output_objects = get_objects(output_grid)
    predicted_objects = get_objects(predicted_output)

    print("Input Objects:")
    for color, data in input_objects.items():
        print(f"  Color {color}:")
        print(f"    Bounding Box: {data['bounding_box']}")
        print(f"    Size: {data['size']}")

    print("\nOutput Objects:")
    for color, data in output_objects.items():
        print(f"  Color {color}:")
        print(f"    Bounding Box: {data['bounding_box']}")
        print(f"    Size: {data['size']}")

    print("\nPredicted Objects:")
    for color, data in predicted_objects.items():
      print(f"  Color {color}:")
      print(f"    Bounding Box: {data['bounding_box']}")
      print(f"    Size: {data['size']}")
    print("-" * 30)

# Example data (replace with actual data from the task)

example_data = [
  ([
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 3, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
  ],
  [
    [3],
    [1]
  ],
  [
    [3, 0, 0],
    [1, 0, 0],
    [0, 0, 0]
  ]),
  ([
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
  ],
  [
    [3],
    [1]
  ],
  [
    [0, 3, 0, 0, 0, 0],
    [0, 1, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0]
  ]),
  ([
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 3, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    ],
  [
    [3],
    [1],
    [1],
    [1]
  ],
  [
    [3, 0, 0],
    [1, 1, 1],
    [0, 0, 0]
  ]),
  ([
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 3, 3, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
  ],
  [
    [3, 3],
    [1, 1]
  ],
  [
    [3, 3, 0, 0],
    [1, 1, 0, 0],
    [0, 0, 0, 0]
  ])
]

for input_grid, output_grid, predicted in example_data:
  code_execution(input_grid, output_grid, predicted)
