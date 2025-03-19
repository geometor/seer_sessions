import numpy as np

# Mock-up of the input and output grids for each training example.  Replace with actual data.
train_examples = [
    {
        "input": [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                  [8, 1, 0, 0, 0, 0, 0, 0, 0, 0],
                  [8, 8, 1, 0, 0, 0, 0, 0, 0, 0],
                  [1, 8, 1, 0, 0, 0, 0, 0, 0, 0]],
        "output": [[8, 1, 0],
                   [8, 8, 1],
                   [1, 8, 1]],
        "result": [[8, 1, 0],
                   [8, 8, 1],
                   [1, 8, 1]],
        "passed": True
    },
      {
        "input": [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                  [1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                  [8, 1, 0, 0, 0, 0, 0, 0, 0, 0],
                  [8, 8, 0, 0, 0, 0, 0, 0, 0, 0]],
        "output": [[1, 0],
                   [8, 1],
                   [8, 8]],
        "result": [[8, 1, 0],
                    [8, 8, 0],
                    [0, 0, 0]],
        "passed": False
    },
    {
        "input": [[0, 0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 8, 0],
                  [0, 0, 0, 0, 0, 0, 8, 1],
                  [0, 0, 0, 0, 0, 0, 1, 1]],
        "output": [[8, 0],
                   [8, 1],
                   [1, 1]],
        "result": [[0, 0, 0],
                   [0, 0, 8],
                   [0, 0, 0]],
        "passed": False
    },
    {
       "input": [[0, 0, 0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0, 8, 0],
                 [0, 0, 0, 0, 0, 0, 1, 8, 0],
                 [0, 0, 0, 0, 0, 0, 0, 1, 1]],
        "output": [[8, 0],
                   [1, 8],
                   [1, 1]],
        "result": [[0, 0, 0],
                   [0, 0, 1],
                   [0, 0, 0]],
        "passed": False

    }
]

def analyze_grids(examples):
    results = []
    for i, example in enumerate(examples):
        input_grid = np.array(example['input'])
        output_grid = np.array(example['output'])
        result_grid = np.array(example['result'])

        # Find bounding box for colors 1 and 8
        rows, cols = np.where((input_grid == 1) | (input_grid == 8))
        if rows.size > 0:  # Check if any 1s or 8s were found
          min_row, max_row = np.min(rows), np.max(rows)
          min_col, max_col = np.min(cols), np.max(cols)
        else:
          min_row, max_row, min_col, max_col = 0,0,0,0
        
        # calculate rows and cols in output
        output_rows, output_cols = output_grid.shape
        
        results.append({
            "example": i + 1,
            "bounding_box": (min_row, max_row, min_col, max_col),
            "output_shape": (output_rows, output_cols),
            "passed": example['passed']
        })
    return results

analysis_results = analyze_grids(train_examples)
for result in analysis_results:
    print(result)