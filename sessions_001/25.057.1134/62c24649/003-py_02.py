import numpy as np

def compare_grids(grid1, grid2):
    """Compares two grids and returns a diff and a match score."""
    if grid1.shape != grid2.shape:
        return "Shapes differ", 0
    diff = grid1 != grid2
    match_score = np.sum(~diff) / diff.size
    return diff, match_score

# Example usage (assuming you have 'output_grid' and 'expected_output')
# Make sure these are defined from your actual task execution.
task_data = {
    "3ed85e60": {
        "train": [
            {
                "input": np.array([[5, 0, 5], [0, 8, 0], [5, 0, 5]]),
                "output": np.array([[5, 0, 5, 5, 0, 5], [0, 8, 8, 8, 8, 0], [5, 8, 8, 8, 8, 5], [5, 8, 8, 8, 8, 5], [0, 8, 8, 8, 8, 0], [5, 0, 5, 5, 0, 5]])
            },
             {
                "input": np.array([[0, 5, 0], [6, 0, 6], [0, 5, 0]]),
                "output": np.array([[0, 5, 0, 0, 5, 0], [6, 5, 5, 5, 5, 6], [6, 5, 5, 5, 5, 6], [0, 0, 0, 0, 0, 0], [6, 0, 0, 0, 0, 6], [0, 5, 0, 0, 5, 0]])
            },
            {
                "input": np.array([[8, 8, 8, 8, 8], [8, 5, 5, 5, 8], [8, 8, 8, 8, 8]]),
                "output": np.array([[8, 8, 8, 8, 8, 8, 8, 8, 8, 8], [8, 5, 5, 5, 5, 5, 5, 5, 5, 8], [8, 5, 5, 5, 5, 5, 5, 5, 5, 8], [8, 5, 5, 5, 5, 5, 5, 5, 5, 8], [8, 5, 5, 5, 5, 5, 5, 5, 5, 8], [8, 8, 8, 8, 8, 8, 8, 8, 8, 8]])
            }
        ]
    }
}

task_id = "3ed85e60"

results = []
for i, example in enumerate(task_data[task_id]["train"]):
  input_grid = example["input"]
  expected_output = example["output"]
  output_grid = transform(input_grid)
  diff, match_score = compare_grids(output_grid, expected_output)
  results.append(
        {
            "example": i,
            "match_score": match_score,
            "diff": diff,
        }
    )
print(results)