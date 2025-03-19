import numpy as np

def analyze_transformation(input_grid, output_grid):
    """
    Analyzes the transformation between input and output grids.

    Args:
        input_grid: The input grid as a NumPy array.
        output_grid: The output grid as a NumPy array.

    Returns:
        A dictionary containing analysis results.
    """

    changed_pixels = []
    unchanged_red_pixels = []
    total_red_pixels_in = 0
    total_red_pixels_out = 0

    for r in range(input_grid.shape[0]):
        for c in range(input_grid.shape[1]):
            if input_grid[r, c] == 2:
                total_red_pixels_in += 1
            if output_grid[r,c] == 2:
                total_red_pixels_out += 1
            if input_grid[r, c] != output_grid[r, c]:
                changed_pixels.append({
                    "row": r,
                    "col": c,
                    "from": int(input_grid[r, c]),
                    "to": int(output_grid[r, c])
                })
            elif input_grid[r,c] == 2 and output_grid[r,c] == 2:
                unchanged_red_pixels.append({
                    "row": r,
                    "col": c,
                    "from": int(input_grid[r, c]),
                    "to": int(output_grid[r, c])
                })
    return {
        "changed_pixels": changed_pixels,
        "unchanged_red_pixels": unchanged_red_pixels,
      "total_red_pixels_input": total_red_pixels_in,
        "total_red_pixels_output": total_red_pixels_out
    }

# Example Usage (replace with actual grids)
task_id = '7b6016b9'
examples = [
  {
    "input": [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 4, 4, 4, 4, 4, 0, 0], [0, 0, 0, 4, 2, 2, 2, 4, 0, 0], [0, 0, 0, 4, 2, 2, 2, 4, 0, 0], [0, 0, 0, 4, 2, 2, 2, 4, 0, 0], [0, 0, 0, 4, 4, 4, 4, 4, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]],
    "output": [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 4, 4, 4, 4, 4, 0, 0], [0, 0, 0, 4, 4, 4, 4, 4, 0, 0], [0, 0, 0, 4, 4, 4, 4, 4, 0, 0], [0, 0, 0, 4, 4, 4, 4, 4, 0, 0], [0, 0, 0, 4, 4, 4, 4, 4, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]],
  },
  {
    "input": [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 4, 4, 4, 0, 0, 0], [0, 0, 0, 4, 2, 2, 4, 0, 0, 0], [0, 0, 0, 4, 2, 4, 4, 0, 0, 0], [0, 0, 0, 4, 4, 4, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]],
    "output": [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 4, 4, 4, 0, 0, 0], [0, 0, 0, 4, 4, 4, 4, 0, 0, 0], [0, 0, 0, 4, 4, 4, 4, 0, 0, 0], [0, 0, 0, 4, 4, 4, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]],
  },
  {
    "input": [[0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 4, 4, 4, 4, 0, 0], [0, 0, 4, 2, 2, 2, 4, 0, 0], [0, 0, 4, 2, 4, 2, 4, 0, 0], [0, 0, 4, 2, 2, 2, 4, 0, 0], [0, 0, 0, 4, 4, 4, 4, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0]],
    "output": [[0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 4, 4, 4, 4, 0, 0], [0, 0, 4, 4, 4, 4, 4, 0, 0], [0, 0, 4, 4, 4, 4, 4, 0, 0], [0, 0, 4, 4, 4, 4, 4, 0, 0], [0, 0, 0, 4, 4, 4, 4, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0]],
  },
]

results = []
for example in examples:
  analysis = analyze_transformation(np.array(example["input"]), np.array(example["output"]))
  results.append(analysis)

for i, result in enumerate(results):
    print(f"Example {i+1}:")
    print(f"  Changed Pixels: {result['changed_pixels']}")
    print(f"  Unchanged Red Pixels: {result['unchanged_red_pixels']}")
    print(f"  Total Red Pixels in Input: {result['total_red_pixels_input']}")
    print(f"  Total Red Pixels in Output: {result['total_red_pixels_output']}")
    print("-" * 20)