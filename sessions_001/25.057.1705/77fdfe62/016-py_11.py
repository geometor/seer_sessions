import numpy as np

def get_corner_colors(grid):
    height, width = grid.shape
    top_left = grid[0, 0]
    top_right = grid[0, width - 1]
    bottom_left = grid[height - 1, 0]
    bottom_right = grid[height - 1, width - 1]
    return top_left, top_right, bottom_left, bottom_right

def find_colored_pixels(grid):
    """Finds positions and colors of non-background pixels."""
    height, width = grid.shape
    colored_pixels = []
    for r in range(height):
        for c in range(width):
            if grid[r, c] != 0 and grid[r,c] != 5:  # Consider 0 as background and grey (5)
                colored_pixels.append(((r, c), grid[r, c]))
    return colored_pixels

def analyze_results(task_data):
    results = []
    for example in task_data['train'] + task_data['test']: #include test
        input_grid = np.array(example['input'])
        output_grid = np.array(example['output'])
        #predicted_output = transform(input_grid) #remove prediction

        input_height, input_width = input_grid.shape
        output_height, output_width = output_grid.shape
        #predicted_output_height, predicted_output_width = predicted_output.shape

        top_left, top_right, bottom_left, bottom_right = get_corner_colors(input_grid)
        colored_pixels = find_colored_pixels(input_grid)
        output_colored_pixels = find_colored_pixels(output_grid)


        results.append({
            'input_shape': (input_height, input_width),
            'output_shape': (output_height, output_width),
            #'predicted_output_shape': (predicted_output_height, predicted_output_width),
            'top_left_color': top_left,
            'top_right_color': top_right,
            'bottom_left_color': bottom_left,
            'bottom_right_color': bottom_right,
            'colored_pixels': colored_pixels,
            'output_colored_pixels': output_colored_pixels,
            #'output_correct': np.array_equal(output_grid, predicted_output) #remove prediction
            'output_correct': "not calculated"
        })
    return results

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