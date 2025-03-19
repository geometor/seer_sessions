import numpy as np

def calculate_metrics(input_grid, output_grid, predicted_output_grid):
    metrics = {}

    # Count of azure and red pixels in input
    metrics['input_azure_count'] = np.sum(input_grid == 8)
    metrics['input_red_count'] = np.sum(input_grid == 2)

    # Count of azure and red pixels in output
    metrics['output_azure_count'] = np.sum(output_grid == 8)
    metrics['output_red_count'] = np.sum(output_grid == 2)
    
    # difference map
    metrics['difference_map'] = (output_grid != predicted_output_grid).astype(int)
    metrics['error_count'] = np.sum(metrics['difference_map'])

    return metrics

def transform(input_grid):
    """Transforms the input grid according to the described rule."""

    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # Iterate through each row
    for r in range(rows):
        row_has_red = False
        for c in range(cols):
            if input_grid[r, c] == 2:
                row_has_red = True
                break

        if row_has_red:
            # Extend all azure pixels in this row downwards
            for c in range(cols):
                if input_grid[r, c] == 8:
                    for r_below in range(r + 1, rows):
                        output_grid[r_below, c] = 8
        else:
            # Extend only the lowest azure pixel in each column downwards
            for c in range(cols):
                azure_indices = [row_index for row_index in range(r, rows) if input_grid[row_index, c] == 8]
                if azure_indices:
                    lowest_azure = max(azure_indices)
                    for r_below in range(lowest_azure + 1, rows):
                        output_grid[r_below, c] = 8
    return output_grid

# Provided training examples (replace with actual data loading)
train_examples = [
  ([
    [0, 8, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 8, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 8, 0, 0, 0, 0, 0, 0, 2, 0],
    [0, 8, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    ],
   [
    [0, 8, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 8, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 8, 0, 0, 0, 0, 0, 0, 2, 0],
    [0, 8, 0, 0, 0, 0, 0, 0, 8, 0],
    [0, 8, 0, 0, 0, 0, 0, 0, 8, 0],
    ]),
  ([
    [0, 8, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 8, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 8, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 8, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 2, 0, 0, 0, 0, 0, 0, 0, 0],
    ],
   [
    [0, 8, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 8, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 8, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 8, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 2, 0, 0, 0, 0, 0, 0, 0, 0],
    ]),
    ([
    [0, 8, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2],
    [0, 8, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 8, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 8],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 8],
   ],
   [
    [0, 8, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2],
    [0, 8, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 8],
    [0, 8, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 8],
    [0, 8, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 8],
    ]),
    ([
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 8],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 8],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 8],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 2],
   ],
   [
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 8],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 8],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 8],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 2],
    ]),
    ([
    [0, 8, 0, 0, 2],
    [0, 8, 0, 0, 0],
    [0, 8, 0, 0, 8],
    [0, 0, 0, 0, 8],
   ],
   [
    [0, 8, 0, 0, 2],
    [0, 8, 0, 0, 8],
    [0, 8, 0, 0, 8],
    [0, 8, 0, 0, 8],
    ])

]

results = []
for i, (input_grid, output_grid) in enumerate(train_examples):
    input_grid = np.array(input_grid)
    output_grid = np.array(output_grid)
    predicted_output_grid = transform(input_grid)
    metrics = calculate_metrics(input_grid, output_grid, predicted_output_grid)
    results.append((i, metrics))
    print(f"Example {i}:")
    print(metrics)
    print("Difference map:")
    print(metrics['difference_map'])
