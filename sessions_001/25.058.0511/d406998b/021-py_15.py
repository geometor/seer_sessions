import numpy as np

def analyze_grids(input_grid, output_grid, code_output_grid):
    """Analyzes input and output grids and returns a dictionary of metrics."""

    input_gray_count = np.sum(input_grid == 5)
    output_gray_count = np.sum(output_grid == 5)
    input_green_count = np.sum(input_grid == 3)
    output_green_count = np.sum(output_grid == 3)
    code_output_gray_count = np.sum(code_output_grid == 5)
    code_output_green_count = np.sum(code_output_grid == 3)
    results_match = np.array_equal(output_grid, code_output_grid)

    metrics = {
        "input_dims": input_grid.shape,
        "output_dims": output_grid.shape,
        "input_gray": int(input_gray_count),
        "output_gray": int(output_gray_count),
        "input_green": int(input_green_count),
        "output_green": int(output_green_count),
        "code_output_gray": int(code_output_gray_count),
        "code_output_green": int(code_output_green_count),
        "match": bool(results_match)
    }
    return metrics

# Example Usage (replace with actual data from the task)
task_data = [
  ([
    [5, 0, 0, 0, 5, 0, 0, 0, 5, 0, 0, 0, 5],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 5, 0, 0, 0, 5, 0, 0, 0, 5, 0, 0],
  ],
  [
    [5, 0, 0, 0, 5, 0, 0, 0, 5, 0, 0, 0, 3],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 3, 0, 0, 0, 5, 0, 0, 0, 5, 0, 0],
  ]),
  ([
    [0, 0, 0, 0, 0, 5, 5, 5, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 5, 5, 5, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 5, 5, 5, 0, 0, 0, 0, 0],
  ],
  [
    [0, 0, 0, 0, 0, 5, 5, 5, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 5, 5, 5, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 5, 5, 5, 0, 0, 0, 0, 0],
  ]),
  ([
    [0, 0, 0, 0, 0, 5, 5, 5, 0, 0, 0, 0, 0],
    [0, 5, 5, 5, 0, 5, 5, 5, 0, 5, 5, 5, 0],
    [0, 0, 0, 0, 0, 5, 5, 5, 0, 0, 0, 0, 0],
    ],
  [
    [0, 0, 0, 0, 0, 5, 5, 3, 0, 0, 0, 0, 0],
    [0, 3, 5, 5, 0, 5, 5, 5, 0, 5, 5, 3, 0],
    [0, 0, 0, 0, 0, 3, 5, 5, 0, 0, 0, 0, 0],
    ])
]

input_grids = [np.array(inp) for inp, _ in task_data]
output_grids = [np.array(outp) for _, outp in task_data]

results = []
for i in range(len(input_grids)):
    code_output = transform(input_grids[i])
    metrics = analyze_grids(input_grids[i], output_grids[i], code_output)
    results.append(metrics)

for i, res in enumerate(results):
  print (f"Example {i}: {res}")