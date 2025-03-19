def collect_example_data(task):
    example_data = []
    for example in task['train']:
        input_grid = np.array(example['input'])
        output_grid = np.array(example['output'])
        
        green_pixel_coords = find_pixel(input_grid, 3)
        zero_rows_input = np.where(~input_grid.any(axis=1))[0]
        zero_rows_output = np.where(~output_grid.any(axis=1))[0]

        input_height = input_grid.shape[0]
        output_height = output_grid.shape[0]
        
        result_grid = transform(input_grid) # execute our transform
        result_correct = np.array_equal(result_grid,output_grid)


        example_info = {
            'input_height': input_height,
            'output_height': output_height,
            'green_pixel': green_pixel_coords is not None,
            'green_pixel_coords': green_pixel_coords,
            'zero_rows_input': zero_rows_input.tolist(),
            'zero_rows_output': zero_rows_output.tolist(),
            'result_correct': result_correct
        }
        example_data.append(example_info)
    return example_data

import json
task = json.loads("""
{
  "train": [
    {
      "input": [
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 3, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0],
        [1, 1, 1, 1, 1, 1, 1],
        [2, 2, 2, 2, 2, 2, 2]
      ],
      "output": [
        [0, 0, 0, 3, 0, 0, 0],
        [1, 1, 1, 1, 1, 1, 1],
        [2, 2, 2, 2, 2, 2, 2]
      ]
    },
    {
      "input": [
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 3, 0, 0, 0],
        [1, 1, 1, 1, 1, 1, 1],
        [2, 2, 2, 2, 2, 2, 2]
      ],
      "output": [
        [0, 0, 0, 3, 0, 0, 0],
        [1, 1, 1, 1, 1, 1, 1],
        [2, 2, 2, 2, 2, 2, 2]
      ]
    },
    {
      "input": [
        [1, 1, 1, 1, 1, 1, 1],
        [0, 0, 0, 0, 0, 0, 0],
        [2, 2, 2, 2, 2, 2, 2],
        [3, 3, 3, 3, 3, 3, 3],
        [4, 4, 4, 4, 4, 4, 4]
      ],
      "output": [
        [1, 1, 1, 1, 1, 1, 1],
        [2, 2, 2, 2, 2, 2, 2],
        [3, 3, 3, 3, 3, 3, 3],
        [4, 4, 4, 4, 4, 4, 4]
      ]
    },
    {
      "input": [
        [1, 1, 1, 1, 1, 1, 1],
        [2, 2, 2, 2, 2, 2, 2],
        [0, 0, 0, 0, 0, 0, 0],
        [3, 3, 3, 3, 3, 3, 3],
        [4, 4, 4, 4, 4, 4, 4]
      ],
      "output": [
        [1, 1, 1, 1, 1, 1, 1],
        [2, 2, 2, 2, 2, 2, 2],
        [3, 3, 3, 3, 3, 3, 3],
        [4, 4, 4, 4, 4, 4, 4]
      ]
    }
  ],
  "test": [
    {
      "input": [
        [0, 0, 0, 0, 0, 0, 0],
        [1, 1, 1, 1, 1, 1, 1],
        [2, 2, 2, 2, 2, 2, 2],
        [3, 3, 3, 3, 3, 3, 3],
        [4, 4, 4, 4, 4, 4, 4]
      ],
      "output": [
        [1, 1, 1, 1, 1, 1, 1],
        [2, 2, 2, 2, 2, 2, 2],
        [3, 3, 3, 3, 3, 3, 3],
        [4, 4, 4, 4, 4, 4, 4]
      ]
    }
  ]
}
""")
example_data = collect_example_data(task)
for d in example_data:
  print(d)