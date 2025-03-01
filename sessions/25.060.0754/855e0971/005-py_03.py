import numpy as np

def describe_grid(grid):
    """Provides a basic description of a grid."""
    return {
        "shape": grid.shape,
        "unique_colors": np.unique(grid).tolist(),
        "has_white": 0 in np.unique(grid)
    }

def analyze_examples(task):
    """Analyzes input-output pairs in a task."""
    analysis = {}
    for i, example in enumerate(task["train"]):
        input_grid = np.array(example["input"])
        output_grid = np.array(example["output"])
        analysis[f"example_{i+1}"] = {
            "input": describe_grid(input_grid),
            "output": describe_grid(output_grid),
            "same_shape": input_grid.shape == output_grid.shape
        }
    return analysis

task = {
  "train": [
    {
      "input": [[0, 1, 0], [0, 1, 0], [0, 1, 0]],
      "output": [[0, 1, 0], [0, 1, 0], [0, 1, 0], [0, 1, 0], [0, 1, 0]]
    },
    {
      "input": [[8, 0, 8], [8, 0, 8], [8, 0, 8], [8, 0, 8], [8, 8, 8]],
      "output": [[8, 0, 8], [8, 0, 8], [8, 0, 8], [8, 0, 8], [8, 8, 8], [8, 0, 8], [8, 0, 8], [8, 0, 8]]
    },
     {
      "input": [[8, 0, 8], [8, 5, 8], [8, 0, 8], [8, 0, 8], [8, 8, 8]],
      "output": [[8, 0, 8], [8, 5, 8], [8, 0, 8], [8, 0, 8], [8, 8, 8], [8, 0, 8],[8, 0, 8],[8,5,8]]
    }
  ]
}
analysis_results = analyze_examples(task)
print(analysis_results)