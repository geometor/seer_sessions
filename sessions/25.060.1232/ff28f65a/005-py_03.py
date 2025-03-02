import numpy as np

def analyze_grid(grid):
    """Analyzes a grid and returns relevant properties."""
    unique_colors = np.unique(grid)
    shapes = {}
    for color in unique_colors:
        coords = np.argwhere(grid == color)
        min_row, min_col = np.min(coords, axis=0)
        max_row, max_col = np.max(coords, axis=0)
        width = max_col - min_col + 1
        height = max_row - min_row + 1
        shapes[color] = (width, height)
    return {
        "shape": grid.shape,
        "unique_colors": unique_colors.tolist(),
        "color_shapes": shapes
    }

def analyze_example(example):
    """Analyzes an input-output pair."""
    input_analysis = analyze_grid(np.array(example["input"]))
    output_analysis = analyze_grid(np.array(example["output"]))
    return {
        "input": input_analysis,
        "output": output_analysis,
    }

# Example data (replace with your actual task data)
task = {
  "train": [
    {
      "input": [[0, 0, 0, 0, 0], [0, 2, 2, 0, 0], [0, 2, 2, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]],
      "output": [[1, 0, 0], [0, 0, 0], [0, 0, 0]]
    },
    {
      "input": [[0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 2, 2, 2, 0, 0, 0], [0, 0, 0, 2, 2, 2, 0, 0, 0], [0, 0, 0, 2, 2, 2, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0]],
      "output": [[0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 1, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0]]
    },
    {
      "input": [[0, 0, 0, 0, 0, 0, 0], [0, 2, 2, 2, 2, 0, 0], [0, 2, 2, 2, 2, 0, 0], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0]],
      "output": [[0, 1, 0], [0, 0, 0], [0, 0, 0]]
    },
  ],
  "test": [
    {
      "input": [[0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 2, 2, 2, 2, 0], [0, 0, 0, 2, 2, 2, 2, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0]],
      "output": [[0, 0, 0, 0], [0, 1, 0, 0], [0, 0, 0, 0]]
    }
  ]
}
results = [analyze_example(ex) for ex in task["train"]]

for i, analysis in enumerate(results):
  print(f"Example {i+1}:")
  print(f"  Input:  Shape: {analysis['input']['shape']}, Colors: {analysis['input']['unique_colors']}, Color Shapes: {analysis['input']['color_shapes']}")
  print(f"  Output: Shape: {analysis['output']['shape']}, Colors: {analysis['output']['unique_colors']}, Color Shapes: {analysis['output']['color_shapes']}")
  print("-" * 20)