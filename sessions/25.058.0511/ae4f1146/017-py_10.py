def analyze_grid_pair(input_grid, output_grid):
    """
    Analyzes an input-output grid pair and returns a report.
    """
    input_grid = np.array(input_grid)
    output_grid = np.array(output_grid)

    input_dims = input_grid.shape
    output_dims = output_grid.shape

    input_colors = np.unique(input_grid)
    output_colors = np.unique(output_grid)

    return {
        "input_dimensions": input_dims,
        "output_dimensions": output_dims,
        "input_colors": input_colors.tolist(),
        "output_colors": output_colors.tolist(),
        "output_height": output_dims[0] if len(output_dims) >0 else 0,
        "output_width": output_dims[1] if len(output_dims) > 1 else 0

    }

# define the training examples
examples = [
    ([
      [0, 0, 8, 0, 0, 0, 0, 8, 0],
      [0, 0, 0, 0, 0, 0, 0, 0, 0],
      [0, 8, 0, 0, 0, 0, 0, 8, 0],
      [0, 0, 0, 0, 0, 0, 0, 0, 0],
      [0, 0, 8, 0, 0, 0, 0, 0, 0]
    ],
     [[8], [0], [8], [8]]),
    ([
       [0, 0, 0, 0, 0, 0, 0, 0, 0],
       [0, 0, 0, 0, 8, 0, 0, 0, 0],
       [0, 0, 0, 8, 0, 8, 0, 0, 0],
       [0, 0, 0, 0, 8, 0, 0, 0, 0],
       [0, 0, 0, 0, 0, 0, 0, 0, 0]
    ],
    [[8], [8], [8]]),
    ([
      [0, 0, 0, 0, 0, 0, 0, 0, 0],
      [0, 0, 3, 0, 8, 0, 4, 0, 0],
      [0, 0, 1, 8, 0, 8, 7, 0, 0],
      [0, 0, 6, 0, 8, 0, 2, 0, 0],
      [0, 0, 0, 0, 0, 0, 0, 0, 0]
    ],
     [[8],
      [8],
      [8]])
]

# get reports from each example and predicted output
reports = []
for input_grid, output_grid in examples:
  report = analyze_grid_pair(input_grid, output_grid)
  report['predicted_output'] = transform(input_grid)
  reports.append(report)

print(reports)