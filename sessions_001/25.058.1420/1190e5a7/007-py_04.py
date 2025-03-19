import numpy as np

def analyze_grid(grid, grid_type):
    """Analyzes a single grid and returns relevant properties."""
    unique_values = np.unique(grid)
    shape = grid.shape
    return {
        f"{grid_type}_colors": unique_values.tolist(),
        f"{grid_type}_shape": shape,
    }

def analyze_example(example):
  input_grid = np.array(example['input'])
  output_grid = np.array(example['output'])
  results = analyze_grid(input_grid, 'input')
  results.update(analyze_grid(output_grid, 'output'))
  return results
  

def analyze_task(task):
    """Analyzes all examples in a task and the test input."""
    example_results = [analyze_example(eg) for eg in task['train']]
    return example_results

task = {
    "train": [
        {
            "input": [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 7, 7, 7, 7, 7, 7, 0, 0],
                      [0, 0, 0, 0, 7, 0, 0, 0, 0, 7, 0, 0],
                      [0, 0, 0, 0, 7, 0, 3, 3, 0, 7, 0, 0],
                      [0, 0, 0, 0, 7, 0, 3, 3, 0, 7, 0, 0],
                      [0, 0, 0, 0, 7, 0, 0, 0, 0, 7, 0, 0],
                      [0, 0, 0, 0, 7, 7, 7, 7, 7, 7, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]],
            "output": [[3, 3],
                       [3, 3]]
        },
        {
            "input": [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 7, 7, 7, 7, 7, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 7, 0, 0, 0, 7, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 7, 0, 1, 0, 7, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 7, 7, 7, 7, 7, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]],
            "output": [[1]]
        },
        {
           "input": [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 7, 7, 7, 7, 7, 7, 7, 7, 7, 0],
                      [0, 7, 0, 0, 0, 0, 0, 0, 0, 7, 0],
                      [0, 7, 0, 0, 5, 5, 0, 0, 0, 7, 0],
                      [0, 7, 0, 0, 5, 5, 0, 0, 0, 7, 0],
                      [0, 7, 0, 0, 0, 0, 0, 0, 0, 7, 0],
                      [0, 7, 7, 7, 7, 7, 7, 7, 7, 7, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]],
            "output": [[5,5],
                       [5,5]]
        },
        {
            "input": [[7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7],
                      [7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7],
                      [7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7],
                      [7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7],
                      [7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7],
                      [7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7],
                      [7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 7],
                      [7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7],
                      [7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7]],
            "output": [[2]]
        }
    ],
    "test": [
        {
            "input": [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 7, 7, 7, 7, 7, 7, 7, 7, 0],
                      [0, 7, 0, 0, 0, 0, 0, 0, 7, 0],
                      [0, 7, 0, 4, 4, 0, 0, 0, 7, 0],
                      [0, 7, 0, 4, 4, 0, 0, 0, 7, 0],
                      [0, 7, 0, 0, 0, 0, 0, 0, 7, 0],
                      [0, 7, 7, 7, 7, 7, 7, 7, 7, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]],
            "output": [[4, 4],
                       [4, 4]]
        }
    ]
}

results = analyze_task(task)
for i, r in enumerate(results):
    print(f"Example {i+1}:")
    for k, v in r.items():
        print(f"  {k}: {v}")