import numpy as np

def describe_grid(grid):
    rows, cols = grid.shape
    unique_colors = np.unique(grid)
    color_counts = {color: np.sum(grid == color) for color in unique_colors}
    return {
        'dimensions': (rows, cols),
        'unique_colors': unique_colors.tolist(),
        'color_counts': color_counts
    }

def find_vertical_line(grid, color):
    rows, cols = grid.shape
    for c in range(cols):
        for r in range(rows):
            if grid[r, c] == color:
                # Check if it's a vertical line
                line_length = 0
                for r2 in range(r, rows):
                    if grid[r2, c] == color:
                        line_length += 1
                    else:
                        break
                if line_length > 0:
                  return r, c, line_length
    return None, None, 0

def analyze_examples(task):
    results = []
    for example in task['train']:
        input_grid = np.array(example['input'])
        output_grid = np.array(example['output'])
        predicted_output = transform(input_grid) #using the transform function defined previously

        input_desc = describe_grid(input_grid)
        output_desc = describe_grid(output_grid)
        predicted_output_desc = describe_grid(predicted_output)

        start_row, start_col, line_length = find_vertical_line(input_grid, 7)
        vertical_line_info = {
          'start_row': start_row,
          'start_col': start_col,
          'line_length': line_length
        }


        results.append({
            'input': input_desc,
            'output': output_desc,
            'predicted_output': predicted_output_desc,
            'vertical_line': vertical_line_info,
            'match': np.array_equal(output_grid, predicted_output)
        })
    return results

task = {
  "train": [
    {
      "input": [
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 7, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 7, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 7, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
      ],
      "output": [
        [7, 8, 7, 8, 7, 0, 0, 0, 0, 0, 0, 0],
        [7, 8, 7, 8, 7, 0, 0, 0, 0, 0, 0, 0],
        [7, 8, 7, 8, 7, 0, 0, 0, 0, 0, 0, 0],
        [0, 8, 7, 8, 7, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 7, 8, 7, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
      ]
    },
    {
      "input": [
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 7, 0, 0, 0],
        [0, 0, 0, 0, 0, 7, 0, 0, 0],
        [0, 0, 0, 0, 0, 7, 0, 0, 0],
        [0, 0, 0, 0, 0, 7, 0, 0, 0]
      ],
      "output": [
        [7, 8, 7, 8, 7, 0, 0, 0, 0],
        [7, 8, 7, 8, 7, 0, 0, 0, 0],
        [7, 8, 7, 8, 7, 0, 0, 0, 0],
        [0, 8, 7, 8, 7, 0, 0, 0, 0],
        [0, 0, 7, 8, 7, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0]
      ]
    },
      {
      "input": [
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 7, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 7, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 7, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 7, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 7, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
      ],
      "output": [
        [7, 8, 7, 8, 7, 0, 0, 0, 0, 0, 0, 0],
        [7, 8, 7, 8, 7, 0, 0, 0, 0, 0, 0, 0],
        [7, 8, 7, 8, 7, 0, 0, 0, 0, 0, 0, 0],
        [0, 8, 7, 8, 7, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 7, 8, 7, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
      ]
    }
  ]
}

analysis_results = analyze_examples(task)
print(analysis_results)
