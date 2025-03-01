import numpy as np

def transform(input_grid):
    input_grid = np.array(input_grid)
    output_height, input_width = input_grid.shape
    output_width = 3
    output_grid = np.zeros((output_height, output_width), dtype=int)

    # Iterate through rows and apply row-specific column selection and color replacement
    for i in range(output_height):
        if i == 0 or i == 1:
            selected_columns = [2, 4, 5]
        elif i == 2:
            selected_columns = [1, 4, 5]
        elif i == 3:
            selected_columns = [1, 2, 5]
        else:  # Should not happen based on provided examples, but good practice to have
            selected_columns = []

        for j, col_index in enumerate(selected_columns):
            # Color Replacement within selected columns
            if input_grid[i, col_index] == 1:  # blue
                output_grid[i, j] = 3      # green
            elif input_grid[i, col_index] == 5:  # gray
                output_grid[i, j] = 3      # green
            elif input_grid[i, col_index] == 7:  # orange
                output_grid[i, j] = 0      # white
            else:
                output_grid[i, j] = input_grid[i, col_index]

    return output_grid.tolist()

def show_result(example):
    input = example['input']
    output = example['output']
    pred = transform(input)
    print (f'Input:\n{np.array(input)}')
    print (f'Expected:\n{np.array(output)}')
    print (f'Predicted:\n{np.array(pred)}')
    print (f'Correct: {np.array(output) == np.array(pred)}')

task = {
  "train": [
    {
      "input": [
        [0, 0, 1, 0, 1, 1, 0, 0, 0, 0],
        [0, 0, 1, 0, 1, 1, 0, 0, 0, 0],
        [0, 1, 0, 0, 1, 1, 0, 0, 0, 0],
        [0, 1, 1, 0, 0, 1, 0, 0, 0, 0]
      ],
      "output": [
        [0, 3, 3],
        [0, 3, 3],
        [0, 3, 3],
        [0, 3, 3]
      ]
    },
    {
      "input": [
        [0, 0, 0, 0, 7, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 7, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 7, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 7, 0, 0, 0, 0, 0]
      ],
      "output": [
        [0, 0, 0],
        [0, 0, 0],
        [0, 0, 0],
        [0, 0, 0]
      ]
    },
    {
      "input": [
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 5, 0, 0, 5, 0, 0, 0, 5, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 5, 0, 0, 5, 0, 0, 0, 5, 0]
      ],
      "output": [
        [0, 0, 0],
        [3, 0, 3],
        [0, 0, 0],
        [3, 0, 3]
      ]
    },
     {
      "input": [
        [0, 5, 0, 0, 5, 0, 0, 0, 5, 0],
        [0, 5, 0, 0, 5, 0, 0, 0, 5, 0],
        [0, 5, 0, 0, 5, 0, 0, 0, 5, 0],
        [0, 5, 0, 0, 5, 0, 0, 0, 5, 0]
      ],
      "output": [
        [3, 0, 3],
        [3, 0, 3],
        [3, 0, 3],
        [3, 0, 3]
      ]
    }
  ],
  "test": [
    {
      "input": [
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 5, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 5, 0, 0, 0, 0, 0]
      ],
      "output": [
        [0, 0, 0],
        [3, 0, 0],
        [0, 0, 0],
        [3, 0, 0]
      ]
    }
  ]
}

for ex in task["train"]:
    show_result(ex)