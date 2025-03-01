import numpy as np

def describe_grid(grid):
    """
    Identifies objects (non-zero pixels) in a grid and their properties.
    Returns a list of dictionaries, each describing an object.
    """
    grid = np.array(grid)
    objects = []
    for color in np.unique(grid):
        if color != 0:  # Ignore background
            rows, cols = np.where(grid == color)
            min_row, max_row = np.min(rows), np.max(rows)
            min_col, max_col = np.min(cols), np.max(cols)
            objects.append({
                'color': int(color),
                'min_row': int(min_row),
                'max_row': int(max_row),
                'min_col': int(min_col),
                'max_col': int(max_col),
                'height': int(max_row - min_row + 1),
                'width': int(max_col - min_col + 1)
            })
    return objects
def compare_io(input_grid, output_grid):
  input_desc = describe_grid(input_grid)
  output_desc = describe_grid(output_grid)
  print("--- INPUT ---")
  for obj in input_desc: print(obj)
  print("--- OUTPUT ---")
  for obj in output_desc: print(obj)
  print("\n")

train = [
    [
        [[8, 0, 5, 0, 0, 0, 0, 0, 0], [0, 0, 5, 0, 0, 0, 0, 0, 0], [0, 0, 5, 0, 0, 0, 0, 0, 0], [0, 0, 5, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0]],
        [[8, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [5, 5, 5, 5, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0]]
    ],
    [
        [[0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 6, 0, 6], [0, 0, 0, 0, 0, 0, 6, 0, 6], [0, 0, 0, 0, 0, 0, 6, 0, 6]],
        [[0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 6, 6, 6, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 6, 6, 6, 0, 0]]
    ],
    [
        [[0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 7, 0, 0, 0, 0], [0, 0, 0, 0, 7, 0, 0, 0, 0], [0, 0, 0, 0, 7, 0, 0, 0, 0], [0, 0, 0, 0, 7, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0]],
        [[0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 7, 7, 7, 7, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0]]
    ]
]

for example in train:
  compare_io(example[0], example[1])

def check_result(grid, transform_func):
    transformed = transform_func(grid)
    return transformed

def compare_all_examples(train_data, transform_func):
    for i, (input_grid, expected_output) in enumerate(train_data):
        transformed_grid = check_result(input_grid, transform_func)
        correct = transformed_grid == expected_output
        print(f"Example {i+1}: {'Correct' if correct else 'Incorrect'}")
        if not correct:
            print("Transformed Grid:")
            print(np.array(transformed_grid))
            print("Expected Output:")
            print(np.array(expected_output))


from previous_code import transform
compare_all_examples(train, transform)
