import numpy as np

def analyze_grid(grid):
    """Analyzes a single grid and returns relevant metrics."""
    grid = np.array(grid)  # Ensure it's a NumPy array
    unique_colors = np.unique(grid)
    num_unique_colors = len(unique_colors)
    rows, cols = grid.shape
    return {
        'shape': (rows, cols),
        'unique_colors': unique_colors.tolist(),
        'num_unique_colors': num_unique_colors,
        'color_counts': {color: np.sum(grid == color) for color in unique_colors}
    }

def compare_io(input_grid, output_grid):
    """Compares input and output grids."""
    input_analysis = analyze_grid(input_grid)
    output_analysis = analyze_grid(output_grid)

    return {
        'input': input_analysis,
        'output': output_analysis,
    }
task = {
    "train": [
        {
            "input": [[0, 0, 0, 0], [0, 3, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]],
            "output": [[2, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]],
        },
        {
            "input": [[0, 0, 0, 0], [0, 0, 0, 0], [0, 3, 0, 0], [0, 0, 0, 0]],
            "output": [[0, 0, 0, 0], [2, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]],
        },
		{
            "input": [[0, 3, 0, 0, 0], [0, 3, 0, 0, 0], [0, 3, 0, 0, 0], [0, 0, 0, 0, 0]],
            "output": [[2, 0, 0, 0, 0], [2, 0, 0, 0, 0], [2, 0, 0, 0, 0], [0, 0, 0, 0, 0]],
        },
        {
            "input": [[0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 3, 0, 0, 0], [0, 3, 0, 0, 0]],
            "output": [[0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [2, 0, 0, 0, 0], [2, 0, 0, 0, 0]],
        }
    ],
    "test": [
        {
            "input": [[0, 0, 0, 0, 0], [0, 3, 0, 0, 0], [0, 3, 0, 0, 0], [0, 3, 0, 0, 0]],
            "output": [[0, 0, 0, 0, 0], [2, 0, 0, 0, 0], [2, 0, 0, 0, 0], [2, 0, 0, 0, 0]],
        }
    ],
}

results = []
for example in task["train"]:
  results.append(compare_io(example["input"],example["output"]))

print(results)