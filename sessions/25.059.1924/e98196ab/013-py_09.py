def grid_to_string(grid):
    return '\n'.join(''.join(str(cell) for cell in row) for row in grid)

task_data = {
    "train": [
        {
            "input": [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 8, 0, 0, 0, 0, 0], [0, 0, 0, 0, 5, 0, 0, 0, 0, 0], [0, 0, 0, 0, 1, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]],
            "output": [[0, 0, 0, 0, 8, 0, 0, 0, 0, 0], [0, 0, 0, 0, 1, 0, 0, 0, 0, 0]]
        },
        {
            "input": [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 5, 5, 5, 5, 5, 5, 5, 5, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [1, 0, 0, 0, 0, 0, 0, 0, 0, 6], [0, 0, 0, 0, 0, 0, 0, 0, 0, 6], [0, 0, 0, 0, 0, 0, 0, 0, 0, 6], [5, 5, 5, 5, 5, 5, 5, 5, 5, 5], [3, 3, 3, 3, 3, 3, 3, 3, 3, 3]],
            "output": [[1, 0, 0, 0, 0, 0, 0, 0, 0, 6], [0, 0, 0, 0, 0, 0, 0, 0, 0, 6], [0, 0, 0, 0, 0, 0, 0, 0, 0, 6], [3, 3, 3, 3, 3, 3, 3, 3, 3, 3]]
        },
        {
            "input": [[5, 5, 5, 5, 5, 5, 5, 5, 5, 5], [5, 5, 5, 5, 5, 5, 5, 5, 5, 5], [5, 5, 5, 5, 5, 5, 5, 5, 5, 5], [0, 0, 0, 5, 5, 5, 5, 0, 0, 0], [0, 0, 0, 5, 5, 5, 5, 0, 0, 0], [0, 0, 0, 5, 5, 5, 5, 0, 0, 0], [0, 0, 0, 5, 5, 5, 5, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 2, 0, 0, 0, 0, 0], [0, 0, 4, 0, 2, 0, 0, 4, 0, 0], [0, 4, 0, 0, 2, 0, 0, 0, 4, 0], [4, 0, 0, 0, 2, 0, 0, 0, 0, 4]],
            "output": [[0, 0, 0, 0, 2, 0, 0, 0, 0, 0], [0, 0, 4, 0, 2, 0, 0, 4, 0, 0], [0, 4, 0, 0, 2, 0, 0, 0, 4, 0], [4, 0, 0, 0, 2, 0, 0, 0, 0, 4]]
        }
    ]
}

def get_result_string(example):
  input_grid = np.array(example["input"])
  expected_output_grid = np.array(example["output"])
  expected_output = grid_to_string(expected_output_grid)
  actual_output_grid = transform(input_grid)
  actual_output = grid_to_string(actual_output_grid)
  return f"""
Input:
{grid_to_string(input_grid)}

Expected Output:
{expected_output}

Actual Output:
{actual_output}

Correct: {np.array_equal(actual_output_grid, expected_output_grid)}
"""


for i, example in enumerate(task_data["train"]):
  print(f"Example {i+1}:")
  print(get_result_string(example))
