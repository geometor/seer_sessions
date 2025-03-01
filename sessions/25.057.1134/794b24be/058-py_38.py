import numpy as np

def get_grid_info(grid):
    """Extracts relevant information from a grid."""
    info = {}
    info["shape"] = grid.shape
    info["colors"] = np.unique(grid).tolist()
    # Find top-most row with blue (1)
    top_blue_row = -1
    for i, row in enumerate(grid):
        if 1 in row:
            top_blue_row = i
            break
    info["top_blue_row"] = top_blue_row
    if top_blue_row != -1:
      info["top_blue_row_colors"] = np.unique(grid[top_blue_row]).tolist()
    return info

def analyze_examples(task_data):
    """Analyzes input and expected output grids."""
    analysis = {}
    for i, example in enumerate(task_data["train"]):
        input_info = get_grid_info(np.array(example["input"]))
        output_info = get_grid_info(np.array(example["output"]))
        analysis[f"example_{i+1}"] = {
            "input": input_info,
            "expected_output": output_info,
        }
    return analysis

# Assuming 'task' is defined elsewhere and contains the ARC task data
# task = ... # Your ARC task loading logic here
# For demonstration purposes, let's create a mock 'task'
task = {
  "train": [
    {"input": [[0, 0, 0], [0, 1, 0], [0, 0, 0]], "output": [[2, 2, 2], [0, 0, 0], [0, 0, 0]]},
    {"input": [[0, 0, 0], [0, 1, 0], [0, 1, 0]], "output": [[2, 2, 2], [0, 0, 0], [0, 0, 0]]},
    {"input": [[0, 1, 0], [0, 0, 0], [0, 1, 0]], "output": [[2, 2, 2], [0, 0, 0], [0, 0, 0]]},
    {"input": [[1, 0, 0], [0, 0, 0], [0, 0, 0]], "output": [[2, 0, 0], [0, 0, 0], [0, 0, 0]]}
  ]
}

analysis = analyze_examples(task)
print(analysis)