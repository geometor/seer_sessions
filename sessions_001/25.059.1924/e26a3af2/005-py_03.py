import numpy as np

def analyze_results(task):
    results = []
    for example in task["train"]:
        input_grid = np.array(example['input'])
        output_grid = np.array(example['output'])
        predicted_output = transform(input_grid)  # Assuming 'transform' from previous code is available
        correct = np.array_equal(predicted_output, output_grid)
        
        # Get columns of interest in the *actual* output
        actual_cols_of_interest = []
        for j in range(output_grid.shape[1]):
          if not np.all(output_grid[:,j] == 1):
            actual_cols_of_interest.append(j)

        # Get colors in the columns of interest in input
        input_colors_in_cols = []
        for j in actual_cols_of_interest:
          input_colors_in_cols.append(np.unique(input_grid[:,j]))

        # Get colors in the columns of interest in output
        output_colors_in_cols = []
        for j in actual_cols_of_interest:
          output_colors_in_cols.append(np.unique(output_grid[:,j]))          

        results.append({
            'input_shape': input_grid.shape,
            'output_shape': output_grid.shape,
            'predicted_output_correct': correct,
            'actual_cols_of_interest': actual_cols_of_interest,
            'input_colors_in_cols' : input_colors_in_cols,
            'output_colors_in_cols': output_colors_in_cols
        })
    return results

# Mock task data (replace with your actual task data)
task = {
  "train": [
    {
      "input": [[8, 1, 1, 1, 1, 1], [8, 1, 1, 1, 1, 1], [8, 1, 1, 1, 1, 1]],
      "output": [[8, 1, 1, 1, 1, 1], [8, 1, 1, 1, 1, 1], [8, 1, 1, 1, 1, 1]]
    },
    {
      "input": [[1, 3, 1, 1, 1], [1, 3, 1, 1, 1], [1, 3, 1, 1, 1]],
      "output": [[1, 3, 1, 1, 1], [1, 3, 1, 1, 1], [1, 3, 1, 1, 1]]
    },
    {
      "input": [[1, 1, 1, 2, 1], [1, 1, 1, 2, 1], [1, 1, 1, 2, 1]],
      "output": [[1, 1, 1, 2, 1], [1, 1, 1, 2, 1], [1, 1, 1, 2, 1]]
    },
      {
      "input": [[1, 1, 8, 2, 1, 3, 1], [1, 1, 8, 2, 1, 3, 1], [1, 1, 8, 2, 1, 3, 1], [1,1,1,1,1,1,1]],
      "output": [[1, 1, 8, 2, 1, 3, 1], [1, 1, 8, 2, 1, 3, 1], [1, 1, 8, 2, 1, 3, 1], [1,1,1,1,1,1,1]]
    },
    {
      "input": [[0, 8, 1, 1, 1, 6, 1], [0, 8, 1, 7, 1, 6, 1], [1, 8, 1, 1, 1, 1, 1]],
      "output": [[1, 8, 1, 1, 1, 1, 1], [1, 8, 1, 1, 1, 1, 1], [1, 8, 1, 1, 1, 1, 1]]
    }
  ]
}

results = analyze_results(task)

for i, res in enumerate(results):
    print(f"Example {i+1}:")
    print(f"  Input Shape: {res['input_shape']}")
    print(f"  Output Shape: {res['output_shape']}")
    print(f"  Predicted Output Correct: {res['predicted_output_correct']}")
    print(f"  Actual Columns of Interest: {res['actual_cols_of_interest']}")
    print(f"  Input colors in output columns: {res['input_colors_in_cols']}")
    print(f"  Output colors in output columns: {res['output_colors_in_cols']}")
    print("-" * 20)