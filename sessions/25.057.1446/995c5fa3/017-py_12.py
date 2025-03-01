import numpy as np

def report(grid, title="Grid Report"):
    grid = np.array(grid)
    print(f"--- {title} ---")
    print(f"Dimensions: {grid.shape}")
    unique, counts = np.unique(grid, return_counts=True)
    color_counts = dict(zip(unique, counts))
    print(f"Color Counts: {color_counts}")    
    #detect multiple rows
    if (len(grid.shape) > 1):
      print(f"Rows: {grid.shape[0]}")
    else:
      print("Rows: 1")

def get_blocks(grid):
    blocks = []
    start = 0
    in_block = False
    block_widths = []

    for j in range(grid.shape[1]):
        # Check for a vertical separator (e.g., a black column). Assuming black is not used in the input, we can use any color that contrasts. Here we check if *all* are not the dominant.
        column = grid[:, j]

        # Find the dominant color in the entire grid (excluding white - 0)
        unique, counts = np.unique(grid, return_counts=True)
        color_counts = dict(zip(unique, counts))
        if 0 in color_counts:
          del color_counts[0] # remove white

        if len(color_counts) > 0:
          dominant_color = max(color_counts, key=color_counts.get)
        else:
          dominant_color = 0 #default

        #if all the column has the same color, we are in a boundary
        is_separator = all(column == column[0]) and column[0] != dominant_color
        if is_separator:
            if in_block:
                block = grid[:, start:j]
                blocks.append(block)
                block_widths.append(j-start)
                in_block = False
        elif not in_block:
            start = j
            in_block = True

    # Add the last block if the input ends with a block
    if in_block:
        block = grid[:, start:]
        blocks.append(block)
        block_widths.append(grid.shape[1] - start)

    return blocks

def analyze_block(block):
    # If a row exists filled with only gray (5), encode 8.
    for row in block:
        if np.all(row == 5):
            return 8
    # If a row exists in which the second and third pixel is white (0), encode 2.
    for row in block:
        if row.shape[0] > 2 and row[1] == 0 and row[2] == 0:
            return 2
    # If the entire block does not satisfy any condition above, encode 4.
    return 4

def transform(input_grid):
    input_grid = np.array(input_grid)
    blocks = get_blocks(input_grid)
    output_rows = []

    # Process blocks and collect encodings
    row_encodings = []
    for block in blocks:
        block_code = analyze_block(block)
        row_encodings.append(block_code)

    output_rows.append(row_encodings)

    # Determine maximum row length for padding
    max_row_length = 0
    if len(output_rows) > 0:
       max_row_length = max(len(row) for row in output_rows)

    # Pad rows with zeros and create the output grid. Here padding with 0.
    padded_rows = []

    if len(output_rows) > 0: #ensure not empty
      for row in output_rows:
          padding_length = max_row_length - len(row)
          padded_row = np.pad(row, (0, padding_length), mode='constant', constant_values=0)
          padded_rows.append(padded_row)

      output_grid = np.array(padded_rows)

    else: #return empty grid
      output_grid = np.array([])


    return output_grid.tolist()

task = {
  "train": [
    {
      "input": [
        [5, 5, 5, 0, 0, 0, 1, 1, 1, 1, 1, 5, 5, 5, 0, 0, 0, 1, 1, 1, 1, 1, 5, 5, 5, 5, 5, 5],
        [5, 5, 5, 0, 0, 0, 1, 1, 1, 1, 1, 5, 5, 5, 0, 0, 0, 1, 1, 1, 1, 1, 5, 5, 5, 0, 0, 0],
        [5, 5, 5, 0, 0, 0, 1, 1, 1, 1, 1, 5, 5, 5, 0, 0, 0, 1, 1, 1, 1, 1, 5, 5, 5, 0, 0, 0],
        [5, 5, 5, 0, 0, 0, 1, 1, 1, 1, 1, 5, 5, 5, 0, 0, 0, 1, 1, 1, 1, 1, 5, 5, 5, 5, 5, 5],
        [5, 5, 5, 0, 0, 0, 1, 1, 1, 1, 1, 5, 5, 5, 0, 0, 0, 1, 1, 1, 1, 1, 5, 5, 5, 0, 0, 0]
      ],
      "output": [[8, 4, 8, 4, 8, 4]]
    },
    {
      "input": [
        [5, 5, 5, 5, 5, 5, 1, 1, 1, 1, 5, 5, 5, 5, 5, 5, 5, 5, 1, 1, 1, 5, 5, 5, 5, 5, 5, 5],
        [5, 5, 5, 0, 0, 0, 1, 1, 1, 1, 5, 5, 5, 0, 0, 0, 0, 0, 1, 1, 1, 5, 5, 5, 5, 5, 5, 5],
        [5, 5, 5, 0, 0, 0, 1, 1, 1, 1, 5, 5, 5, 0, 0, 0, 0, 0, 1, 1, 1, 5, 5, 5, 5, 5, 5, 5],
        [5, 5, 5, 5, 5, 5, 1, 1, 1, 1, 5, 5, 5, 5, 5, 5, 5, 5, 1, 1, 1, 5, 5, 5, 5, 5, 5, 5],
        [5, 5, 5, 0, 0, 0, 1, 1, 1, 1, 5, 5, 5, 0, 0, 0, 0, 0, 1, 1, 1, 5, 5, 5, 5, 5, 5, 5]
      ],
      "output": [[8, 4, 8, 8, 8, 4]]
    },
    {
      "input": [
        [5, 5, 5, 1, 1, 5, 5, 5, 0, 0, 0, 5, 5, 1, 1, 1, 5, 5, 5, 1, 5, 5, 5, 5, 5, 5, 5, 5],
        [5, 5, 5, 1, 1, 5, 5, 5, 0, 0, 0, 5, 5, 1, 1, 1, 5, 5, 5, 1, 5, 5, 5, 5, 5, 5, 5, 5],
        [5, 5, 5, 1, 1, 5, 5, 5, 0, 0, 0, 5, 5, 1, 1, 1, 5, 5, 5, 1, 5, 5, 5, 5, 5, 5, 5, 5],
        [5, 5, 5, 1, 1, 5, 5, 5, 0, 0, 0, 5, 5, 1, 1, 1, 5, 5, 5, 1, 5, 5, 5, 5, 5, 5, 5, 5],
        [5, 5, 5, 1, 1, 5, 5, 5, 0, 0, 0, 5, 5, 1, 1, 1, 5, 5, 5, 1, 5, 5, 5, 5, 5, 5, 5, 5]
      ],
      "output": [[4, 4, 4, 4, 4, 1]]
    },
    {
      "input": [
        [5, 5, 5, 5, 5, 5, 1, 1, 1, 1, 5, 5, 5, 5, 5, 5, 5, 5, 1, 1, 1, 1, 5, 5, 5, 5, 5, 5],
        [5, 5, 5, 0, 0, 0, 1, 1, 1, 1, 5, 5, 5, 0, 0, 0, 0, 0, 1, 1, 1, 1, 5, 5, 5, 5, 5, 5],
        [5, 5, 5, 0, 0, 0, 1, 1, 1, 1, 5, 5, 5, 0, 0, 0, 0, 0, 1, 1, 1, 1, 5, 5, 5, 5, 5, 5],
        [5, 5, 5, 5, 5, 5, 1, 1, 1, 1, 5, 5, 5, 5, 5, 5, 5, 5, 1, 1, 1, 1, 5, 5, 5, 5, 5, 5],
        [5, 5, 5, 0, 0, 0, 1, 1, 1, 1, 5, 5, 5, 0, 0, 0, 0, 0, 1, 1, 1, 1, 5, 5, 5, 5, 5, 5]
      ],
      "output": [[8, 4, 8, 8, 8, 4]]
    }
  ],
  "test": [
    {
      "input": [
        [5, 5, 5, 1, 1, 1, 5, 5, 5, 1, 1, 1, 1, 5, 5, 5, 1, 1, 1, 1, 1, 1, 5, 5, 5, 5, 5, 5],
        [5, 5, 5, 1, 1, 1, 5, 5, 5, 1, 1, 1, 1, 5, 5, 5, 1, 1, 1, 1, 1, 1, 5, 5, 5, 0, 0, 0],
        [5, 5, 5, 1, 1, 1, 5, 5, 5, 1, 1, 1, 1, 5, 5, 5, 1, 1, 1, 1, 1, 1, 5, 5, 5, 0, 0, 0],
        [5, 5, 5, 1, 1, 1, 5, 5, 5, 1, 1, 1, 1, 5, 5, 5, 1, 1, 1, 1, 1, 1, 5, 5, 5, 5, 5, 5],
        [5, 5, 5, 1, 1, 1, 5, 5, 5, 1, 1, 1, 1, 5, 5, 5, 1, 1, 1, 1, 1, 1, 5, 5, 5, 0, 0, 0]
      ],
      "output": [[4, 4, 4, 4, 4, 4]]
    }
  ]
}

for ex_num, ex in enumerate(task["train"]):
  input_grid = ex["input"]
  expected_output = ex["output"]
  actual_output = transform(input_grid)

  report(input_grid, f"Train Input {ex_num + 1}")
  report(np.array(actual_output), f"Actual Output {ex_num + 1}")
  report(np.array(expected_output), f"Expected Output {ex_num + 1}")
  print(f"Correct: {actual_output == expected_output}")
  print("\n")

input_grid = task["test"][0]["input"]
actual_output = transform(input_grid)
report(input_grid, f"Test Input")
report(np.array(actual_output), f"Actual Output")
