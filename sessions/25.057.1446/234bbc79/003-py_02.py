import numpy as np

def analyze_example(input_grid, output_grid, predicted_grid):
    gray_positions = np.argwhere(input_grid == 5)
    input_dims = input_grid.shape
    output_dims = output_grid.shape
    predicted_dims = predicted_grid.shape
    correct = np.array_equal(output_grid,predicted_grid)

    print(f"  Input Dimensions: {input_dims}")
    print(f"  Output Dimensions: {output_dims}")
    print(f"  Predicted Dimensions: {predicted_dims}")
    print(f"  Gray Pixel Positions: {gray_positions}")
    print(f"  Correct: {correct}")
    print(f"  Difference: {np.where(output_grid != predicted_grid)}")


task_data = {
    "train": [
        {
            "input": [[0, 0, 0, 5, 1, 0, 2, 0], [0, 0, 0, 5, 1, 0, 0, 0], [0, 0, 0, 5, 1, 0, 0, 0]],
            "output": [[0, 0, 0, 1, 0, 2, 0], [0, 0, 0, 1, 0, 0, 0], [0, 0, 0, 1, 0, 0, 0]],
        },
        {
            "input": [[5, 1, 5, 2, 5, 3], [0, 5, 1, 0, 5, 6]],
            "output": [[1, 2, 3], [0, 1, 6]],
        },
        {
            "input": [[5, 1, 5, 5, 5, 2, 5, 5, 3, 5, 4, 5, 5]],
            "output": [[1, 2, 3, 4]],
        },
        {
            "input": [[1, 5, 5, 2, 5, 3, 5, 5, 4, 5, 5, 5, 6]],
            "output": [[1, 2, 3, 4, 6]],
        },
    ]
}

for i, example in enumerate(task_data["train"]):
  print(f"Example {i+1}:")
  input_grid = np.array(example["input"])
  output_grid = np.array(example["output"])

  #use existing transform function
  predicted_grid = transform(input_grid)

  analyze_example(input_grid, output_grid, predicted_grid)
  print("---")