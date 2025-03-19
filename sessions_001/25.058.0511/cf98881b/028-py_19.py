import numpy as np

def analyze_results(task_data):
    analysis = []
    for i, example in enumerate(task_data['train']):
        input_grid = np.array(example['input'])
        output_grid = np.array(example['output'])

        input_height, input_width = input_grid.shape
        output_height, output_width = output_grid.shape

        # Find the color in the last row, middle of the input grid
        middle_col = input_width // 2
        bottom_middle_color = input_grid[-1, middle_col]
        
        # Find the actual middle color of the last row (important if input width is even)
        actual_middle_color = None
        for x in range(input_width):
            if input_grid[-1,x] != input_grid[-1,0]:
                actual_middle_color = input_grid[-1,x]
                break;
        if actual_middle_color == None:
          actual_middle_color = input_grid[-1,middle_col]

        # Determine which columns in the output correspond to which in the input, based on color
        output_cols_kept = []
        input_cols_kept = []
        for output_col_index in range(output_width):
           for input_col_index in range(input_width):
              if (output_grid[:,output_col_index] == input_grid[1:-1,input_col_index]).all():
                output_cols_kept.append(output_col_index)
                input_cols_kept.append(input_col_index)
                break;

        analysis.append({
            "example": i,
            "input_shape": (input_height, input_width),
            "output_shape": (output_height, output_width),
            "bottom_middle_color": bottom_middle_color.item(),
            "actual_middle_color": actual_middle_color.item(),
            "output_cols_kept": output_cols_kept,
            "input_cols_kept": input_cols_kept,
        })
    return analysis

task_data = {
  "train": [
    {
      "input": [[8, 8, 8, 8, 8, 8, 8, 8], [8, 1, 1, 1, 1, 1, 1, 8], [8, 1, 1, 1, 4, 1, 1, 8], [8, 1, 1, 1, 1, 1, 1, 8], [8, 8, 8, 8, 8, 8, 8, 8]],
      "output": [[8, 8, 8, 8], [8, 1, 1, 8], [8, 1, 4, 8], [8, 1, 1, 8], [8, 8, 8, 8]]
    },
    {
      "input": [[8, 8, 8, 8, 8, 8, 8, 8, 8, 8], [8, 8, 8, 8, 8, 8, 8, 8, 8, 8], [8, 8, 1, 1, 1, 1, 1, 8, 8, 8], [8, 8, 1, 1, 1, 1, 1, 8, 8, 8], [8, 8, 1, 1, 1, 4, 1, 8, 8, 8], [8, 8, 1, 1, 1, 1, 1, 8, 8, 8], [8, 8, 8, 8, 8, 8, 8, 8, 8, 8], [8, 8, 8, 8, 8, 8, 8, 8, 8, 8]],
      "output": [[8, 8, 8, 8, 8, 6], [8, 8, 1, 1, 8, 8], [8, 8, 1, 1, 8, 8], [8, 8, 1, 4, 8, 8], [8, 8, 1, 1, 8, 8], [8, 8, 8, 8, 8, 8]]
    },
    {
      "input": [[6, 6, 6, 6, 6, 6, 6, 6, 6], [6, 6, 6, 6, 6, 6, 0, 0, 6], [6, 6, 0, 0, 6, 6, 0, 0, 6], [6, 6, 0, 0, 6, 6, 6, 6, 6], [6, 6, 0, 0, 6, 6, 6, 4, 6], [6, 6, 6, 6, 6, 6, 6, 6, 6]],
      "output": [[6, 6, 6, 6, 6, 6, 6], [6, 6, 6, 6, 0, 0, 6], [6, 6, 0, 0, 6, 6, 6], [6, 6, 0, 0, 6, 4, 6], [6, 6, 6, 6, 6, 6, 6]]
    },
    {
      "input": [[0, 3, 0, 0, 0, 0, 0, 0, 0], [0, 3, 0, 0, 0, 0, 0, 3, 0], [0, 3, 0, 0, 0, 0, 0, 3, 0], [0, 3, 0, 0, 0, 0, 0, 3, 0], [0, 3, 0, 0, 0, 0, 0, 3, 0], [0, 3, 0, 0, 0, 0, 0, 3, 0], [0, 3, 0, 0, 0, 0, 0, 3, 0], [0, 3, 0, 0, 0, 0, 0, 3, 0], [0, 0, 0, 4, 0, 0, 0, 3, 0]],
      "output": [[0, 3, 0, 0, 0, 0, 0], [0, 3, 0, 0, 0, 0, 0], [0, 3, 0, 0, 0, 0, 0], [0, 3, 0, 0, 0, 0, 0], [0, 3, 0, 0, 0, 0, 0], [0, 3, 0, 0, 0, 0, 0], [0, 0, 0, 4, 0, 0, 0]]
    }
  ]
}

analysis = analyze_results(task_data)
for item in analysis:
    print(item)