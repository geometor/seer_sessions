def analyze_rows(input_grid, output_grid):
    """Analyzes the changes between input and output grids row by row."""
    rows = input_grid.shape[0]
    results = []
    for i in range(rows):
        input_row = input_grid[i, :]
        output_row = output_grid[i, :]
        if np.array_equal(input_row, output_row):
            change = "No Change"
        else:
            change = f"Changed: {np.unique(input_row)} -> {np.unique(output_row)}"
        results.append(f"Row {i+1}: {change}")
    return results

def run_analysis(task):
    for i, example in enumerate(task['train']):
        input_grid = np.array(example['input'])
        output_grid = np.array(example['output'])
        analysis = analyze_rows(input_grid, output_grid)
        print(f"Example {i+1}:")
        for row_result in analysis:
            print(row_result)
        print("-" * 20)

# Provide the task data.  I do not have access to the task variable from previous turn.
task = {
  "train": [
    {
      "input": [
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
      ],
      "output": [
        [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
      ]
    },
    {
      "input": [
        [2, 2, 2, 2, 2, 2, 2, 2],
        [2, 2, 2, 2, 2, 2, 2, 2],
        [2, 2, 2, 2, 2, 2, 2, 2],
        [2, 2, 2, 2, 2, 2, 2, 2],
        [2, 2, 2, 2, 2, 2, 2, 2]
      ],
      "output": [
        [5, 5, 5, 5, 5, 5, 5, 5],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0]
      ]
    },
      {
      "input": [
        [3, 3, 3, 3, 3, 3, 3, 3, 3, 3],
        [3, 3, 3, 3, 3, 3, 3, 3, 3, 3],
        [3, 3, 3, 3, 3, 3, 3, 3, 3, 3],
        [3, 3, 3, 3, 3, 3, 3, 3, 3, 3]
      ],
      "output": [
        [5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
      ]
    },
      {
      "input": [
        [4, 4, 4, 4],
        [4, 4, 4, 4],
        [4, 4, 4, 4]
      ],
      "output": [
        [5, 5, 5, 5],
        [0, 0, 0, 0],
        [0, 0, 0, 0]
      ]
    }
  ]
}
run_analysis(task)
