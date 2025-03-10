import numpy as np

def analyze_transformation(input_grid, output_grid, predicted_grid):
    """Analyzes the input, output, and predicted grids to identify transformation patterns and errors."""

    def get_nonzero_cells(grid):
        """Finds and returns non-zero cells with their original row and column indices."""
        nonzero_cells = []
        for r in range(grid.shape[0]):
            for c in range(grid.shape[1]):
                if grid[r, c] != 0:
                    nonzero_cells.append((r, c, grid[r, c]))
        return nonzero_cells

    input_nonzero = get_nonzero_cells(input_grid)
    output_nonzero = get_nonzero_cells(output_grid)
    predicted_nonzero = get_nonzero_cells(predicted_grid)

    analysis = {
        'input_nonzero_count': len(input_nonzero),
        'output_nonzero_count': len(output_nonzero),
        'predicted_nonzero_count': len(predicted_nonzero),
        'column_wise_comparison': {},
        'errors': []
    }

    # Column-wise comparison
    for c in range(input_grid.shape[1]):
        input_col = [cell for cell in input_nonzero if cell[1] == c]
        output_col = [cell for cell in output_nonzero if cell[1] == c]
        predicted_col = [cell for cell in predicted_nonzero if cell[1] == c]

        analysis['column_wise_comparison'][c] = {
            'input': input_col,
            'output': output_col,
            'predicted': predicted_col
        }

    # Find differences between expected and predicted.
    diff = output_grid - predicted_grid
    for r in range(diff.shape[0]):
      for c in range(diff.shape[1]):
        if diff[r,c] != 0:
          analysis['errors'].append(
              {'row':r,
               'col':c,
               'output_val': output_grid[r,c],
               'predicted_val': predicted_grid[r,c]})

    return analysis
# get the previous code
previous_code = """
import numpy as np

def get_nonzero_cells(grid):
    "Finds and returns non-zero cells with their original row and column indices."
    nonzero_cells = []
    for r in range(grid.shape[0]):
        for c in range(grid.shape[1]):
            if grid[r, c] != 0:
                nonzero_cells.append((r, c, grid[r, c]))
    return nonzero_cells

def transform(input_grid):
    "Transforms the input grid by shifting non-zero cells down."
    # Initialize output grid with zeros (white)
    output_grid = np.zeros_like(input_grid)

    # Get non-zero cells from input, keeping initial locations.
    nonzero_cells = get_nonzero_cells(input_grid)

    # sort by row, then column
    nonzero_cells.sort(key=lambda x: (x[0], x[1]))

    # compute new locations, starting at bottom
    num_rows = input_grid.shape[0]
    current_row = num_rows-len(nonzero_cells)

    for _, col, value in nonzero_cells:
        output_grid[current_row,col] = value
        current_row += 1

    return output_grid
"""

exec(previous_code)

def get_task_data(task):
    """Extracts input-output pairs from a task dictionary, handling both train and test sets."""
    data = []
    for set_type in ['train', 'test']:
        if set_type in task:
            for pair in task[set_type]:
                input_grid = np.array(pair['input'])
                output_grid = np.array(pair['output'])
                data.append((input_grid, output_grid))
    return data

# Example Usage with Dummy Data (replace with your actual task data)

task = {
  "train": [
    {
      "input": [
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 8, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 8, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 8, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 8, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 8, 0, 0, 0, 0, 0, 0, 0, 0]
      ],
      "output": [
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 8, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 8, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 8, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 8, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 8, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 8, 0, 0, 0, 0, 0, 0, 0, 0]
      ]
    },
     {
      "input": [
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 8, 0, 0, 0, 0, 0, 0, 2, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 8, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 8, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 8, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 8, 0, 0, 0, 0, 0, 0, 2, 0]
      ],
      "output": [
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 8, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 8, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 8, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 8, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 8, 0, 0, 0, 0, 0, 0, 2, 0],
        [0, 8, 0, 0, 0, 0, 0, 0, 2, 0]
      ]
    },
    {
      "input": [
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 8, 0, 0, 0, 0, 0, 0, 2, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 8, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 8, 0, 0, 4, 0, 0, 0, 0, 0],
        [0, 8, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 8, 0, 0, 0, 0, 0, 0, 2, 0]
      ],
      "output": [
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 8, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 8, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 8, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 8, 0, 0, 4, 0, 0, 0, 0, 0],
        [0, 8, 0, 0, 0, 0, 0, 0, 2, 0],
        [0, 8, 0, 0, 0, 0, 0, 0, 2, 0]
      ]
    },
        {
      "input": [
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 8, 0, 7, 0, 0, 0, 0, 2, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 8, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 8, 0, 0, 4, 0, 0, 0, 0, 0],
        [0, 8, 0, 0, 0, 0, 1, 0, 0, 0],
        [0, 8, 0, 0, 0, 0, 0, 0, 2, 0]
      ],
      "output": [
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 8, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 8, 0, 7, 0, 0, 0, 0, 0, 0],
        [0, 8, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 8, 0, 0, 4, 0, 0, 0, 0, 0],
        [0, 8, 0, 0, 0, 0, 1, 0, 2, 0],
        [0, 8, 0, 0, 0, 0, 0, 0, 2, 0]
      ]
    }
  ]
}

task_data = get_task_data(task)

for input_grid, output_grid in task_data:
    predicted_grid = transform(input_grid)
    analysis = analyze_transformation(input_grid, output_grid, predicted_grid)
    print(f"Analysis:\n{analysis}\n")
    #print(f"Input:\n{input_grid}\nOutput:\n{output_grid}\nPredicted:\n{predicted_grid}")
