import numpy as np

def analyze_example(input_grid, output_grid):
    input_grid = np.array(input_grid)
    output_grid = np.array(output_grid)
    num_rows_in = input_grid.shape[0]
    num_cols_in = input_grid.shape[1]
    num_rows_out = output_grid.shape[0]
    num_cols_out = output_grid.shape[1]
    white_positions_in = []
    output_values = []

    for r in range(num_rows_in):
        for c in range(num_cols_in):
            if input_grid[r, c] == 0:
                white_positions_in.append((r, c))
    for r in range(num_rows_out):
        for c in range(num_cols_out):
           output_values.append((r, c, output_grid[r,c]))
    
    return {
        "input_dims": (num_rows_in, num_cols_in),
        "output_dims": (num_rows_out, num_cols_out),
        "white_positions_input": white_positions_in,
        "output_values": output_values,
        "row_counts": [np.count_nonzero(input_grid[r,:] == 0) for r in range(num_rows_in)]
    }

task_examples = [
    {
        "input": [[5, 0, 5, 0, 5, 0, 5]],
        "output": [[6, 6, 6]]
    },
    {
        "input": [[0, 5, 0, 5, 0, 5, 0]],
        "output": [[1, 1, 1]]
    },
     {
        "input": [[5, 5, 5, 5, 5],[0, 0, 0, 0, 0],[5, 5, 5, 5, 5]],
        "output": [[0, 0, 0],[2, 2, 2],[0, 0, 0]]
    },
    {
        "input": [[5, 5, 5, 5, 5],[5, 5, 5, 5, 5],[0, 0, 0, 0, 0]],
        "output": [[0, 0, 0],[0, 0, 0],[2, 2, 2]]
    },
    {
        "input": [[0, 0, 0, 0, 0],[5, 5, 5, 5, 5],[5, 5, 5, 5, 5]],
        "output": [[2, 2, 2],[0, 0, 0],[0, 0, 0]]
    }
]

for i, example in enumerate(task_examples):
  analysis = analyze_example(example["input"], example["output"])
  print(f"Example {i+1}:")
  print(analysis)