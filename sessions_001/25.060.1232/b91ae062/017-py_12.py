import numpy as np

def get_grid_dims(grid):
    return len(grid), len(grid[0])

def analyze_examples(task):
    print(f"Task: {task['task_name']}")
    for i, example in enumerate(task['train']):
        input_grid = example['input']
        output_grid = example['output']
        input_dims = get_grid_dims(input_grid)
        output_dims = get_grid_dims(output_grid)
        print(f"  Example {i+1}:")
        print(f"    Input Dimensions: {input_dims}")
        print(f"    Output Dimensions: {output_dims}")

        #check that output grid cells values at (3*i,3*j) match input[i][j]
        for row in range(input_dims[0]):
            for col in range(input_dims[1]):
                i_val = input_grid[row][col]
                o_row = 3 * row
                o_col = 3 * col
                o_val = output_grid[o_row][o_col]
                if i_val != o_val:
                    print(f"    Expansion mismatch at Input Cell: ({row},{col}) - Input Value: {i_val}, Output Value: {o_val}")


# Dummy task data for demonstration - replace with actual data from prompt
# This example includes all three training examples
dummy_task_data = {
  "task_name": "dummy_task",
  "train": [
    {
      "input": [[1, 2, 3], [4, 5, 6], [7, 8, 9]],
      "output": [[1, 1, 1, 2, 2, 2, 3, 3, 3], [1, 1, 1, 2, 2, 2, 3, 3, 3], [1, 1, 1, 2, 2, 2, 3, 3, 3], [4, 4, 4, 5, 5, 5, 6, 6, 6], [4, 4, 4, 5, 5, 5, 6, 6, 6], [4, 4, 4, 5, 5, 5, 6, 6, 6], [7, 7, 7, 8, 8, 8, 9, 9, 9], [7, 7, 7, 8, 8, 8, 9, 9, 9], [7, 7, 7, 8, 8, 8, 9, 9, 9]]
    },
    {
        "input": [[0, 5, 1], [7, 5, 8], [5, 9, 5]],
        "output" : [[0, 0, 0, 5, 5, 5, 1, 1, 1], [0, 0, 0, 5, 5, 5, 1, 1, 1], [0, 0, 0, 5, 5, 5, 1, 1, 1], [7, 7, 7, 5, 5, 5, 8, 8, 8], [7, 7, 7, 5, 5, 5, 8, 8, 8], [7, 7, 7, 5, 5, 5, 8, 8, 8], [5, 5, 5, 9, 9, 9, 5, 5, 5], [5, 5, 5, 9, 9, 9, 5, 5, 5], [5, 5, 5, 9, 9, 9, 5, 5, 5]]
    },
    {
        "input": [[5, 2, 0], [6, 2, 1], [2, 2, 8]],
        "output": [[5, 5, 5, 2, 2, 2, 0, 0, 0], [5, 5, 5, 2, 2, 2, 0, 0, 0], [5, 5, 5, 2, 2, 2, 0, 0, 0], [6, 6, 6, 2, 2, 2, 1, 1, 1], [6, 6, 6, 2, 2, 2, 1, 1, 1], [6, 6, 6, 2, 2, 2, 1, 1, 1], [2, 2, 2, 2, 2, 2, 8, 8, 8], [2, 2, 2, 2, 2, 2, 8, 8, 8], [2, 2, 2, 2, 2, 2, 8, 8, 8]]
    }
  ]
}

analyze_examples(dummy_task_data)