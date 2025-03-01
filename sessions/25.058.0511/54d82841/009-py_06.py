import numpy as np

def examine_examples(task_data):
    results = []
    for example in task_data['train']:
        input_grid = np.array(example['input'])
        output_grid = np.array(example['output'])
        # find the row,col of the white pixel
        white_pixels_input = np.where(input_grid == 0)
        white_pixels_output = np.where(output_grid == 0)

        yellow_pixels_input = np.where(input_grid == 4)
        yellow_pixels_output = np.where(output_grid == 4)

        results.append({
            'input_grid_shape': input_grid.shape,
            'output_grid_shape': output_grid.shape,
            'white_pixels_input_count': len(white_pixels_input[0]),
            'white_pixels_input_positions': list(zip(white_pixels_input[0].tolist(), white_pixels_input[1].tolist())),
            'white_pixels_output_count': len(white_pixels_output[0]),
            'white_pixels_output_positions': list(zip(white_pixels_output[0].tolist(), white_pixels_output[1].tolist())),
            'yellow_pixels_input_count': len(yellow_pixels_input[0]),
            'yellow_pixels_input_positions': list(zip(yellow_pixels_input[0].tolist(), yellow_pixels_input[1].tolist())),
            'yellow_pixels_output_count': len(yellow_pixels_output[0]),
            'yellow_pixels_output_positions': list(zip(yellow_pixels_output[0].tolist(), yellow_pixels_output[1].tolist())),

        })
    return results

# Hypothetical task data - this would be replaced with the actual data in the coder phase
task_data = {
  "train": [
    {
      "input": [[5, 5, 5, 5, 5, 5],
               [5, 5, 5, 5, 5, 5],
               [5, 5, 5, 5, 5, 5],
               [5, 5, 5, 5, 5, 5],
               [5, 5, 5, 5, 5, 5],
               [5, 5, 5, 5, 5, 5],
               [5, 5, 5, 5, 5, 5],
               [5, 5, 5, 5, 5, 5],
               [5, 5, 5, 5, 5, 5],
                [5, 5, 5, 0, 5, 5]],
      "output": [[5, 5, 5, 5, 5, 5],
               [5, 5, 5, 5, 5, 5],
               [5, 5, 5, 5, 5, 5],
               [5, 5, 5, 5, 5, 5],
               [5, 5, 5, 5, 5, 5],
               [5, 5, 5, 5, 5, 5],
               [5, 5, 5, 5, 5, 5],
               [5, 5, 5, 5, 5, 5],
               [5, 5, 5, 5, 5, 5],
                [5, 5, 5, 4, 5, 5]],
    },
    {
      "input": [[5, 5, 5, 5, 5, 5],
               [5, 5, 5, 5, 5, 5],
               [5, 5, 5, 5, 5, 5],
               [5, 5, 5, 5, 5, 5],
               [5, 5, 5, 5, 5, 5],
               [5, 5, 5, 5, 5, 5],
               [5, 5, 5, 5, 5, 5],
               [5, 5, 5, 5, 5, 5],
               [5, 5, 5, 5, 5, 5],
                [5, 5, 0, 5, 5, 5]],
      "output": [[5, 5, 5, 5, 5, 5],
               [5, 5, 5, 5, 5, 5],
               [5, 5, 5, 5, 5, 5],
               [5, 5, 5, 5, 5, 5],
               [5, 5, 5, 5, 5, 5],
               [5, 5, 5, 5, 5, 5],
               [5, 5, 5, 5, 5, 5],
               [5, 5, 5, 5, 5, 5],
               [5, 5, 5, 5, 5, 5],
                [5, 5, 4, 5, 5, 5]],
    },
    {
      "input": [[5, 5, 5, 5, 5, 5],
               [5, 5, 5, 5, 5, 5],
               [5, 5, 5, 5, 5, 5],
               [5, 5, 5, 5, 5, 5],
               [5, 5, 5, 5, 5, 5],
               [5, 5, 5, 5, 5, 5],
               [5, 5, 5, 5, 5, 5],
               [5, 5, 5, 5, 5, 5],
               [5, 5, 5, 5, 5, 5],
                [0, 5, 5, 5, 5, 5]],
      "output": [[5, 5, 5, 5, 5, 5],
               [5, 5, 5, 5, 5, 5],
               [5, 5, 5, 5, 5, 5],
               [5, 5, 5, 5, 5, 5],
               [5, 5, 5, 5, 5, 5],
               [5, 5, 5, 5, 5, 5],
               [5, 5, 5, 5, 5, 5],
               [5, 5, 5, 5, 5, 5],
               [5, 5, 5, 5, 5, 5],
                [4, 5, 5, 5, 5, 5]],
    }
  ]
}

results = examine_examples(task_data)
print(results)
