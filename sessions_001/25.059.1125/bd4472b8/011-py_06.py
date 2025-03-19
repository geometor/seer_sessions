import numpy as np

def calculate_metrics(input_grid, output_grid, generated_grid):
    input_grid = np.array(input_grid)
    output_grid = np.array(output_grid)
    generated_grid = np.array(generated_grid)

    metrics = {
        "input_shape": input_grid.shape,
        "output_shape": output_grid.shape,
        "generated_shape": generated_grid.shape,
        "output_matches_generated": np.array_equal(output_grid, generated_grid),
        "differences": []
    }
    if not metrics["output_matches_generated"]:
        diff = output_grid != generated_grid
        rows, cols = np.where(diff)
        for r, c in zip(rows, cols):
          metrics["differences"].append(
              {
                  "row": int(r),
                  "col": int(c),
                  "output_val": int(output_grid[r,c]),
                  "generated_val": int(generated_grid[r,c])
              }
          )

    return metrics

examples = [
    {
        "input": [[5, 5, 5, 5, 5, 5, 5, 5, 5, 5], [8, 8, 5, 8, 8, 5, 8, 8, 8, 5], [8, 8, 5, 8, 8, 5, 8, 8, 8, 5], [8, 8, 5, 8, 8, 5, 8, 8, 8, 5]],
        "output": [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [8, 8, 5, 8, 8, 5, 8, 8, 8, 5], [5, 5, 5, 5, 5, 5, 5, 5, 5, 5], [5, 5, 5, 5, 5, 5, 5, 5, 5, 5], [5, 5, 5, 5, 5, 5, 5, 5, 5, 5], [5, 5, 5, 5, 5, 5, 5, 5, 5, 5], [5, 5, 5, 5, 5, 5, 5, 5, 5, 5], [5, 5, 5, 5, 5, 5, 5, 5, 5, 5], [5, 5, 5, 5, 5, 5, 5, 5, 5, 5], [5, 5, 5, 5, 5, 5, 5, 5, 5, 5]],
    },
    {
        "input": [[1, 7, 8, 3, 6, 2, 7, 8, 3, 2], [7, 7, 7, 2, 2, 2, 1, 1, 1, 5], [1, 7, 8, 3, 6, 2, 7, 8, 3, 2]],
        "output": [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [7, 7, 7, 2, 2, 2, 1, 1, 1, 5], [1, 1, 1, 1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1, 1, 1, 1], [7, 7, 7, 7, 7, 7, 7, 7, 7, 7], [7, 7, 7, 7, 7, 7, 7, 7, 7, 7], [8, 8, 8, 8, 8, 8, 8, 8, 8, 8], [8, 8, 8, 8, 8, 8, 8, 8, 8, 8], [3, 3, 3, 3, 3, 3, 3, 3, 3, 3], [3, 3, 3, 3, 3, 3, 3, 3, 3, 3], [6, 6, 6, 6, 6, 6, 6, 6, 6, 6], [6, 6, 6, 6, 6, 6, 6, 6, 6, 6], [2, 2, 2, 2, 2, 2, 2, 2, 2, 2], [2, 2, 2, 2, 2, 2, 2, 2, 2, 2]],
    },
    {
      "input":  [[4, 4, 4, 4, 4, 0, 0, 0, 0, 0], [1, 2, 3, 4, 5, 6, 7, 8, 9, 0], [4, 4, 4, 4, 4, 0, 0, 0, 0, 0]],
      "output": [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [1, 2, 3, 4, 4, 4, 7, 8, 9, 0], [4, 4, 4, 4, 4, 4, 4, 4, 4, 4], [4, 4, 4, 4, 4, 4, 4, 4, 4, 4], [4, 4, 4, 4, 4, 4, 4, 4, 4, 4], [4, 4, 4, 4, 4, 4, 4, 4, 4, 4], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
    },
]
previous_code = """
import numpy as np

def transform(input_grid):
    # Initialize output grid. We know the width, and we can calculate
    # the height based on first row: 2 * len(first row) + 1 for second row
    input_grid = np.array(input_grid)
    output_height = 2 * len(input_grid[0]) + 1 +1 # + 1 because the prompt provided said len() and it's wrong
    output_grid = np.zeros((output_height, len(input_grid[0])), dtype=int)

    # Copy the second row of the input to the second row of the output
    output_grid[1, :] = input_grid[1, :]

    # Process the first row: each color generates two rows
    row_index = 2  # Start filling from the third row
    for color in input_grid[0, :]:
        output_grid[row_index, :] = color
        row_index += 1
        output_grid[row_index, :] = color
        row_index += 1


    return output_grid.tolist()
"""

for i, example in enumerate(examples):
    generated = eval(previous_code.split("def transform")[1].split("return")[0], {}, {"input_grid":example["input"], "np":np})
    metrics = calculate_metrics(example["input"], example["output"], generated)
    print(f"Example {i+1}:")
    print(f"  Input Shape: {metrics['input_shape']}")
    print(f"  Output Shape: {metrics['output_shape']}")
    print(f"  Generated Shape: {metrics['generated_shape']}")
    print(f"  Output Matches Generated: {metrics['output_matches_generated']}")
    if metrics["differences"]:
        print(f"  Differences: {metrics['differences']}")
    print("-" * 20)