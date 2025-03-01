import numpy as np

def count_color_blocks(row):
    """Counts the number of contiguous color blocks in a row."""
    blocks = 0
    current_color = None
    for cell in row:
        if cell != current_color:
            blocks += 1
            current_color = cell
    return blocks

def analyze_example(input_grid, output_grid):
    """Analyzes a single input-output pair."""
    input_grid = np.array(input_grid)
    output_grid = np.array(output_grid)

    # Check for vertical green line
    green_line_present = False
    for j in range(input_grid.shape[1]):
        if all(input_grid[:, j] == 3):
            green_line_present = True
            break

    # Analyze rows
    input_row_blocks = [count_color_blocks(row) for row in input_grid]
    output_row_blocks = [count_color_blocks(row) for row in output_grid] if output_grid.size > 0 else []

    return {
        "green_line": green_line_present,
        "input_row_blocks": input_row_blocks,
        "output_row_blocks": output_row_blocks,
        "input_shape": input_grid.shape,
        "output_shape": output_grid.shape,

    }

# The examples and results
examples = [
  ([
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 3, 0, 0, 0, 0],
    [0, 0, 0, 0, 3, 0, 0, 2, 0],
    [0, 0, 0, 0, 3, 2, 2, 2, 2],
    [0, 0, 0, 0, 3, 0, 0, 0, 0],
    [0, 0, 0, 0, 3, 0, 2, 2, 0],
    ],
    [
      [3, 2],
      [3, 2],
      [3, 2]
    ]),
  ([
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 8, 0, 0, 0, 0],
    [0, 0, 0, 0, 8, 0, 0, 2, 0],
    [0, 0, 0, 0, 8, 2, 2, 2, 2],
    [0, 0, 0, 0, 8, 0, 0, 0, 0],
    [0, 0, 0, 0, 8, 0, 2, 2, 0],
    ],
    [
      [8, 2],
      [8, 2],
      [8, 2]
    ]),
    ([
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 5, 6, 6, 6, 6, 6, 6, 0, 0, 2, 2, 2],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
  ],
  [
    [1, 4, 1],
    [4, 4, 1],
    [5, 6, 4, 2]
  ]),
  ([
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1],
    [0, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3],
    [0, 0, 0, 5, 6, 6, 6, 6, 6, 6, 0, 0, 2, 2, 2],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
  ],
  [
    [1, 4, 1],
    [4, 4, 1],
    [3,3,3,3,3,3,3,3,3,3,3,3,3,3,3],
    [5, 6, 4, 2]
  ])
]

results = [transform(ex[0]).tolist() for ex in examples]

analysis_results = [analyze_example(examples[i][0], examples[i][1]) for i in range(len(examples))]

for i, res in enumerate(analysis_results):
    print(f"Example {i+1}:")
    print(f"  Green Line Present: {res['green_line']}")
    print(f"  Input Row Blocks: {res['input_row_blocks']}")
    print(f"  Output Row Blocks: {res['output_row_blocks']}")
    print(f"  Input Shape: {res['input_shape']}")
    print(f"  Output Shape: {res['output_shape']}")
    print(f"  Expected output:\n  {np.array(examples[i][1])}")
    print(f"  Actual output:\n  {np.array(results[i])}")
    print("-" * 20)