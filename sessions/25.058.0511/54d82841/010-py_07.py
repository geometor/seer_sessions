import numpy as np

def examine_examples(task_data):
    results = []
    for example in task_data['train']:
        input_grid = np.array(example['input'])
        output_grid = np.array(example['output'])

        # Find the row,col of the white pixel in input
        white_pixels_input = np.where(input_grid == 0)

        #check to make sure there is only 1 white pixel
        if len(white_pixels_input[0]) != 1:
          results.append({'valid':False, 'message':'more than one white pixel'})
          continue

        #convert to a tuple
        white_pixel_input_position = (white_pixels_input[0][0], white_pixels_input[1][0])

        #verify output is the same color, except at the white pixel
        output_comparison = (input_grid == output_grid)

        #except at the white pixel
        output_comparison[white_pixel_input_position] = True

        if not np.all(output_comparison):
            results.append({'valid':False, 'message':'other pixels changed colors'})
            continue

        #make sure color at white pixel is now yellow
        if output_grid[white_pixel_input_position] != 4:
          results.append({'valid':False, 'message':'white pixel not changed to yellow'})
          continue

        results.append({
            'valid': True,
            'input_grid_shape': input_grid.shape,
            'output_grid_shape': output_grid.shape,
            'white_pixel_input_position': white_pixel_input_position,
            'output_value_at_white_pixel_position': output_grid[white_pixel_input_position]
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