def analyze_example(input_grid, output_grid):
    """Analyzes an example and identifies swapped pixels."""

    input_grid = np.array(input_grid)
    output_grid = np.array(output_grid)

    diff = input_grid != output_grid
    changed_indices = np.where(diff)

    # verify that the transform creates the output
    result = "Correct" if np.array_equal(transform(input_grid), output_grid) else "Incorrect"
    #print(result)

    if len(changed_indices[0]) == 2:  # Expecting two changed pixels
        coords1 = (changed_indices[0][0], changed_indices[1][0])
        coords2 = (changed_indices[0][1], changed_indices[1][1])
        color1_before = input_grid[coords1]
        color1_after = output_grid[coords1]
        color2_before = input_grid[coords2]
        color2_after = output_grid[coords2]

        return {
            'result': result,
            'changed_pixels': [
                {'coords': coords1, 'before': int(color1_before), 'after': int(color1_after)},
                {'coords': coords2, 'before': int(color2_before), 'after': int(color2_after)},
            ],
            'row_diff': coords2[0] - coords1[0],
            'col_diff': coords2[1] - coords1[1],
        }
    else:
        return {
            'result': result,
            'changed_pixels': [],
            'row_diff': None,
            'col_diff': None,
        }

# Example usage (replace with actual task data):
task_id = '6f8cd795'
train_examples = [
  {
    "input": [
      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
      [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
      [0, 0, 0, 0, 5, 0, 0, 0, 0, 0],
      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    ],
    "output": [
      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
      [0, 0, 0, 0, 5, 0, 0, 0, 0, 0],
      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
      [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    ]
  },
  {
    "input": [
      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
      [0, 0, 0, 0, 2, 0, 0, 0, 0, 0],
      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
      [0, 0, 0, 0, 5, 0, 0, 0, 0, 0],
      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    ],
    "output": [
      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
      [0, 0, 0, 0, 5, 0, 0, 0, 0, 0],
      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
      [0, 0, 0, 0, 2, 0, 0, 0, 0, 0],
      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    ]
  },
  {
    "input": [
      [0, 0, 0, 0, 0, 0, 0, 0],
      [0, 0, 3, 0, 0, 0, 0, 0],
      [0, 0, 0, 0, 0, 0, 0, 0],
      [0, 0, 0, 0, 0, 0, 0, 0],
      [0, 0, 5, 0, 0, 0, 0, 0],
      [0, 0, 0, 0, 0, 0, 0, 0]
    ],
    "output": [
      [0, 0, 0, 0, 0, 0, 0, 0],
      [0, 0, 5, 0, 0, 0, 0, 0],
      [0, 0, 0, 0, 0, 0, 0, 0],
      [0, 0, 0, 0, 0, 0, 0, 0],
      [0, 0, 3, 0, 0, 0, 0, 0],
      [0, 0, 0, 0, 0, 0, 0, 0]
    ]
  }
]
results = [analyze_example(ex['input'], ex['output']) for ex in train_examples]
print(results)