import numpy as np

def analyze_example(input_grid, output_grid):
    print("Input Grid:")
    print(input_grid)
    print("Output Grid:")
    print(output_grid)
    print("Input shape:", input_grid.shape)
    print("Output shape:", output_grid.shape)
    print("Input unique values:", np.unique(input_grid))
    print("Output unique values:", np.unique(output_grid))
    print("-" * 20)

task_data = [
    {
        "input": [[0, 0, 0, 0, 0, 0, 0],
                  [0, 2, 2, 2, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0]],
        "output": [[2, 2, 2]]
    },
   {
        "input": [[0, 0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 2, 2, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0, 0]],
        "output": [[2, 2]]
    },
    {
        "input": [[0, 0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 2, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0, 0]],
        "output": [[2]]
    },
    {
        "input": [[0, 0, 0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 2, 2, 2, 2],
                  [0, 0, 0, 0, 0, 0, 0, 0, 0]],
        "output": [[2, 2, 2, 2]]
    },
    {
        "input":  [[0, 0, 0, 0, 7, 0, 0, 0, 0],
                   [0, 0, 0, 0, 7, 0, 0, 0, 0],
                   [0, 0, 0, 0, 7, 0, 0, 0, 0],
                   [0, 0, 0, 0, 7, 0, 0, 0, 0],
                   [0, 0, 0, 0, 7, 0, 0, 0, 0],
                   [0, 0, 0, 0, 7, 0, 0, 0, 0]],
        "output": [[7, 7, 7, 7, 7, 7]]
    }

]

for example in task_data:
    analyze_example(np.array(example["input"]), np.array(example["output"]))