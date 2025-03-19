import numpy as np

def analyze_results(task):
    results = []
    for example in task['train']:
        input_grid = np.array(example['input'])
        output_grid = np.array(example['output'])
        predicted_output = transform(input_grid)  # Assuming 'transform' is defined
        
        start_col, structure_rows = find_vertical_structure(input_grid)
        
        # calculate structure height and color based on the FIRST connected pixels
        input_rows, input_cols = input_grid.shape
        first_color = 0
        structure_height = 0
        for r in range(input_rows):
          if input_grid[r,0] != 0:
              if structure_height == 0:
                  first_color = input_grid[r,0]
              structure_height += 1
          elif structure_height > 0:
              break

        is_correct = np.array_equal(predicted_output, output_grid)
        results.append({
            'input_shape': input_grid.shape,
            'output_shape': output_grid.shape,
            'predicted_output_shape': predicted_output.shape,
            'is_correct': is_correct,
            'structure_start_col': start_col,
            'structure_rows': structure_rows,
            'first_color' : first_color,
            'structure_height' : structure_height
        })
    return results

# Assuming 'task' is defined elsewhere, containing the train/test examples.
# Replace this with your actual task data.
task = {
  "train": [
    {
      "input": [[0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [1, 0, 0, 0, 0, 0, 0, 0, 0], [6, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 8, 0]],
      "output": [[0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [1, 1, 1, 1, 1, 1, 1, 1, 0], [6, 6, 6, 6, 6, 6, 6, 6, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0]]
    },
    {
      "input": [[0, 0, 0, 0, 0, 0, 0], [1, 0, 0, 0, 0, 0, 0], [6, 0, 0, 0, 0, 0, 0], [6, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0]],
      "output": [[0, 0, 0, 0, 0, 0, 0], [1, 1, 1, 1, 1, 1, 0], [6, 6, 6, 6, 6, 6, 0], [6, 6, 6, 6, 6, 6, 0], [0, 0, 0, 0, 0, 0, 0]]
    },
    {
      "input": [[3, 0, 0, 0, 0, 0, 0, 0], [3, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0]],
      "output": [[3, 3, 3, 3, 3, 3, 3, 0], [3, 3, 3, 3, 3, 3, 3, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0]]
    }
  ]
}
analysis = analyze_results(task)
print(analysis)
