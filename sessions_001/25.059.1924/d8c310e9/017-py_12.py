import numpy as np

def compare_grids(input_grid, output_grid):
    """Compares two grids and returns a dictionary of changes."""
    changes = []
    for r in range(max(input_grid.shape[0], output_grid.shape[0])):
        for c in range(max(input_grid.shape[1], output_grid.shape[1])):
            in_val = input_grid[r, c] if r < input_grid.shape[0] and c < input_grid.shape[1] else None
            out_val = output_grid[r, c] if r < output_grid.shape[0] and c < output_grid.shape[1] else None
            if in_val != out_val:
                changes.append({
                    'row': r,
                    'col': c,
                    'input_value': in_val,
                    'output_value': out_val
                })
    return changes

def analyze_task(task):
    results = []
    for example in task['train']:
        input_grid = np.array(example['input'])
        output_grid = np.array(example['output'])
        changes = compare_grids(input_grid, output_grid)
        results.append({
            'input_shape': input_grid.shape,
            'output_shape': output_grid.shape,
            'changes': changes
        })
    return results

task = {
  "train": [
    {
      "input": [[0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 5, 5, 5, 0, 0, 0], [0, 0, 0, 5, 5, 5, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0]],
      "output": [[0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 5, 5, 5, 5, 5, 5], [0, 0, 0, 5, 5, 5, 5, 5, 5], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0]],
    },
    {
      "input": [[0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 4, 4, 4, 0, 0, 0], [0, 0, 0, 4, 4, 4, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0]],
      "output": [[0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 4, 4, 4, 4, 4, 4], [0, 0, 0, 4, 4, 4, 4, 4, 4], [0, 0, 0, 0, 0, 0, 0, 0, 0]],
    },
    {
      "input": [[0, 0, 0, 0, 0, 0], [0, 6, 6, 6, 6, 0], [0, 6, 6, 6, 6, 0], [0, 6, 6, 6, 6, 0], [0, 0, 0, 0, 0, 0]],
      "output": [[0, 0, 0, 0, 0, 0], [0, 6, 6, 6, 6, 6, 6, 6, 6, 0], [0, 6, 6, 6, 6, 6, 6, 6, 6, 0], [0, 6, 6, 6, 6, 6, 6, 6, 6, 0], [0, 0, 0, 0, 0, 0]],
    },
      {
      "input": [[0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 8, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0]],
      "output": [[0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 8, 8, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0]],
    }
  ],
  "test": [
    {
      "input": [[0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 3, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0]],
      "output": [[0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 3, 3, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0]],
    }
  ]
}

results = analyze_task(task)
for i, res in enumerate(results):
    print(f"Example {i+1}:")
    print(f"  Input Shape: {res['input_shape']}")
    print(f"  Output Shape: {res['output_shape']}")
    print(f"  Changes: {res['changes']}")