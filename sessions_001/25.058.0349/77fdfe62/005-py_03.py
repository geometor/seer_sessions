import numpy as np

def compare_grids(grid1, grid2):
    return np.array_equal(grid1, grid2)

def array_to_string(arr):
    return '\n'.join([' '.join(map(str, row)) for row in arr])

def test_transform(transform, task):
  for i, example in enumerate(task['train']):
     input_grid = example['input']
     expected_output = example['output']
     actual_output = transform(input_grid)
     print(f"Example {i + 1}:")
     print(f"Input:\n{array_to_string(input_grid)}")
     print(f"Expected Output:\n{array_to_string(expected_output)}")
     print(f"Actual Output:\n{array_to_string(actual_output)}")
     print(f"Match: {compare_grids(actual_output, expected_output)}")
     print("-" * 20)