import numpy as np

def code_execution(input_grid, expected_output, transform_func):
    try:
        actual_output = transform_func(input_grid)
        correct = np.array_equal(np.array(actual_output), np.array(expected_output))
        print(f"  Success: {correct}")
        print(f"  Input:\n{np.array(input_grid)}")
        print(f"  Expected Output:\n{np.array(expected_output)}")
        print(f"  Actual Output:\n{np.array(actual_output)}")

        # analyze colors
        input_colors = sorted(list(set(np.array(input_grid).flatten())))
        output_colors = sorted(list(set(np.array(expected_output).flatten())))
        input_colors = [c for c in input_colors if c != 0]
        output_colors = [c for c in output_colors if c!= 0]

        print(f"  Input  Colors: {input_colors}")
        print(f"  Output Colors: {output_colors}")

        # analyze size
        input_grid = np.array(input_grid)
        expected_output = np.array(expected_output)
        print(f"  Input  Shape: {input_grid.shape}")
        print(f"  Output Shape: {expected_output.shape}")

        return correct
    except Exception as e:
        print(f"Error during execution: {e}")
        return False

task = {
  "train": [
    {
      "input": [[0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 3], [0, 0, 0, 0, 0, 0, 0, 3, 3], [0, 0, 0, 0, 0, 0, 0, 3, 3], [0, 0, 0, 0, 0, 2, 2, 2, 2], [0, 0, 0, 0, 0, 2, 2, 2, 2], [0, 0, 0, 0, 0, 2, 2, 2, 2]],
      "output": [[3, 2], [3, 2], [3, 2]]
    },
    {
      "input": [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 3], [0, 0, 0, 0, 0, 0, 0, 0, 3, 3], [0, 0, 0, 0, 0, 0, 3, 3, 3, 3], [0, 0, 0, 0, 0, 0, 3, 3, 3, 3], [0, 0, 0, 0, 0, 2, 2, 2, 2, 2], [0, 0, 0, 0, 0, 2, 2, 2, 2, 2]],
      "output": [[3, 2], [3, 2], [3, 2], [3, 2]]
    },
    {
      "input": [[0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 3, 0, 0], [0, 0, 0, 0, 3, 3, 0, 0], [0, 0, 0, 0, 3, 3, 0, 0], [0, 0, 0, 2, 2, 2, 2, 0], [0, 0, 0, 2, 2, 2, 2, 0], [0, 0, 0, 2, 2, 2, 2, 0]],
      "output": [[3, 2], [3, 2], [3, 2]]
    },
      {
      "input": [[1, 0, 0, 0, 0, 0, 0, 0], [1, 0, 0, 0, 0, 0, 0, 0], [1, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 3, 0, 0], [0, 0, 0, 0, 3, 3, 0, 0], [0, 0, 0, 0, 3, 3, 0, 0], [0, 0, 0, 2, 2, 2, 2, 0], [0, 0, 0, 2, 2, 2, 2, 0], [0, 0, 0, 2, 2, 2, 2, 0]],
      "output": [[1, 0, 0], [1, 0, 0], [1, 3, 2], [0, 3, 2], [0, 3, 2]]
    },
    {
      "input": [[0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 5], [0, 0, 0, 0, 0, 0, 0, 5, 5], [0, 0, 0, 0, 0, 0, 0, 5, 5], [0, 0, 0, 0, 0, 2, 2, 2, 2], [0, 0, 0, 0, 0, 2, 2, 2, 2], [0, 0, 0, 0, 0, 2, 2, 2, 2]],
      "output": [[5, 2], [5, 2], [5, 2]]
    }
  ],
  "test": [
    {
      "input": [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 7], [0, 0, 0, 0, 0, 0, 0, 0, 7, 7], [0, 0, 0, 0, 0, 0, 0, 7, 7, 7], [0, 0, 0, 0, 0, 0, 7, 7, 7, 7], [0, 0, 0, 0, 0, 2, 2, 2, 2, 2], [0, 0, 0, 0, 0, 2, 2, 2, 2, 2]],
      "output": [[7,2], [7,2], [7,2],[7,2]]
    }
  ]
}

from previous_code import transform # Assuming your transform function is in 'previous_code.py'

print("Train Set Results:")
for i, example in enumerate(task["train"]):
    print(f"Example {i+1}:")
    code_execution(example["input"], example["output"], transform)