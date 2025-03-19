import numpy as np

def analyze_results(task_data):
    results = []
    for example in task_data['train']:
        input_grid = np.array(example['input'])
        output_grid = np.array(example['output'])
        predicted_output = transform(input_grid)

        input_height, input_width = input_grid.shape
        output_height, output_width = output_grid.shape
        predicted_output_height, predicted_output_width = predicted_output.shape

        top_left, top_right, bottom_left, bottom_right = get_corner_colors(input_grid)

        results.append({
            'input_shape': (input_height, input_width),
            'output_shape': (output_height, output_width),
            'predicted_output_shape': (predicted_output_height, predicted_output_width),
            'top_left_color': top_left,
            'top_right_color': top_right,
            'bottom_left_color': bottom_left,
            'bottom_right_color': bottom_right,
            'output_correct': np.array_equal(output_grid, predicted_output)
        })
    return results

# the current task data, copy and paste from notebook
task_data = {
  "train": [
    {
      "input": [
        [8, 5, 5, 8],
        [5, 5, 5, 5],
        [5, 5, 5, 5],
        [8, 5, 5, 3]
      ],
      "output": [
        [8, 8, 8, 8],
        [8, 8, 8, 8],
        [8, 8, 3, 3],
        [8, 8, 3, 3]
      ]
    },
    {
      "input": [
        [6, 1, 1, 1, 1, 2],
        [1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1],
        [4, 1, 1, 1, 1, 7]
      ],
      "output": [
        [6, 6, 1, 1, 2, 2],
        [6, 6, 1, 1, 2, 2],
        [4, 4, 1, 1, 7, 7],
        [4, 4, 1, 1, 7, 7]
      ]
    },
    {
      "input": [
        [7, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 5]
      ],
      "output": [
        [7, 7, 0, 0, 0, 0, 0, 0],
        [7, 7, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 5, 5],
        [0, 0, 0, 0, 0, 0, 5, 5]
      ]
    }
  ],
    "test": [
        {
            "input": [
                [2, 0, 0, 0, 0, 4],
                [0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0],
                [3, 0, 0, 0, 0, 1]
            ],
            "output": [
                [2, 2, 0, 0, 4, 4],
                [2, 2, 0, 0, 4, 4],
                [3, 3, 0, 0, 1, 1],
                [3, 3, 0, 0, 1, 1]
            ]
        }
    ]
}

analysis = analyze_results(task_data)
for result in analysis:
    print(result)
