import numpy as np

task_data = {
  "train": [
    {
      "input": [[3, 1, 3], [3, 2, 1], [1, 3, 3]],
      "output": [[4, 5, 4], [4, 6, 5], [5, 4, 4]]
    },
    {
      "input": [[2, 2, 3], [3, 1, 1], [1, 1, 3]],
      "output": [[6, 6, 4], [4, 5, 5], [5, 5, 4]]
    },
     {
      "input": [[3, 1, 2], [1, 2, 2], [3, 3, 1]],
      "output": [[4, 5, 6], [5, 6, 6], [4, 4, 5]]
    },
  ],
  "test": [
    {
      "input": [[1, 3, 3], [2, 2, 1], [3, 1, 2]],
      "output": [[5, 4, 4], [6, 6, 5], [4, 5, 6]]
    }
  ]
}

def get_color_counts(grid):
    unique, counts = np.unique(grid, return_counts=True)
    return dict(zip(unique, counts))

for example_type in ["train", "test"]:
    print(f"--- {example_type.upper()} EXAMPLES ---")
    for i, example in enumerate(task_data[example_type]):
        input_grid = np.array(example["input"])
        output_grid = np.array(example["output"])
        print(f"Example {i+1}:")
        print("Input Color Counts:", get_color_counts(input_grid))
        print("Output Color Counts:", get_color_counts(output_grid))