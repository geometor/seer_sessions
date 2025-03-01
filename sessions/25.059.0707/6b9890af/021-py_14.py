import numpy as np

def analyze_example(input_grid, output_grid):
    input_shape = input_grid.shape
    output_shape = output_grid.shape
    input_colors = np.unique(input_grid)
    output_colors = np.unique(output_grid)

    # use find objects defined in previous turn
    input_objects = find_objects(input_grid)
    output_objects = find_objects(output_grid)
    return {
        "input_shape": input_shape,
        "output_shape": output_shape,
        "input_colors": input_colors.tolist(),
        "output_colors": output_colors.tolist(),
        "input_objects": {k: len(v) for k, v in input_objects.items()},
        "output_objects": {k: len(v) for k, v in output_objects.items()},
    }

def pretty_print_analysis(analysis_results):
  for ex_num, analysis in analysis_results.items():
      print(f"Example: {ex_num}")
      print(f"  Input Shape: {analysis['input_shape']}")
      print(f"  Output Shape: {analysis['output_shape']}")
      print(f"  Input Colors: {analysis['input_colors']}")
      print(f"  Output Colors: {analysis['output_colors']}")
      print(f"  Input Objects: {analysis['input_objects']}")
      print(f"  Output Objects: {analysis['output_objects']}")

# provided in the prompt - pasted here for easy execution
train = [
  [
    np.array([
      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
      [0, 0, 0, 0, 0, 0, 2, 2, 2, 2, 2, 2, 2, 0, 0, 0, 0, 0],
      [0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0],
      [0, 0, 0, 0, 0, 0, 2, 0, 4, 4, 4, 0, 2, 0, 0, 0, 0, 0],
      [0, 0, 0, 0, 0, 0, 2, 0, 4, 4, 4, 0, 2, 0, 0, 0, 0, 0],
      [0, 0, 0, 0, 0, 0, 2, 0, 4, 4, 4, 0, 2, 0, 0, 0, 0, 0],
      [0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0],
      [0, 0, 0, 0, 0, 0, 2, 2, 2, 2, 2, 2, 2, 0, 0, 0, 0, 0],
      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    ]),
    np.array([
      [2, 2, 2, 2, 2, 2, 2],
      [2, 0, 0, 0, 0, 0, 2],
      [2, 0, 4, 4, 4, 0, 2],
      [2, 0, 4, 4, 4, 0, 2],
      [2, 0, 4, 4, 4, 0, 2],
      [2, 0, 0, 0, 0, 0, 2],
      [2, 2, 2, 2, 2, 2, 2],
    ])
  ],
  [
    np.array([
      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
      [0, 0, 0, 0, 0, 3, 3, 0, 0, 0, 0],
      [0, 0, 0, 0, 0, 3, 3, 0, 0, 0, 0],
      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    ]),
    np.array([
      [2, 2, 2, 2],
      [2, 3, 3, 2],
      [2, 3, 3, 2],
      [2, 2, 2, 2],
    ])
  ],
  [
    np.array([
      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 6, 6, 0, 0],
      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 6, 6, 0, 0],
    ]),
    np.array([
      [2, 2, 2, 2],
      [2, 6, 6, 2],
      [2, 6, 6, 2],
      [2, 2, 2, 2],
    ])
  ],
]

analysis_results = {}
for i in range(len(train)):
    analysis_results[i+1] = analyze_example(train[i][0], train[i][1])
pretty_print_analysis(analysis_results)