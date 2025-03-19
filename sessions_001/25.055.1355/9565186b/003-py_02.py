# Simulated execution and analysis
import numpy as np

# Mockup of the provided example data (replace with actual data)
train_examples = [
    {
        "input": np.array([[1, 1, 2], [1, 1, 2], [8, 8, 2]]),
        "output": np.array([[5, 5, 2], [5, 5, 2], [5, 5, 2]])
    },
    {
        "input": np.array([[0, 1, 2, 3], [4, 5, 6, 7], [8, 9, 1, 2]]),
        "output": np.array([[0, 5, 2, 3], [4, 5, 6, 7], [5, 9, 5, 2]])
    },
    {
        "input": np.array([[3, 3, 3], [3, 3, 3], [3, 3, 3]]),
        "output": np.array([[3, 3, 3], [3, 3, 3], [3, 3, 3]])
    }
]

def transform(input_grid):
    # initialize output_grid as a copy of the input grid
    output_grid = np.copy(input_grid)

    # Iterate through each pixel of the grid
    for i in range(output_grid.shape[0]):
        for j in range(output_grid.shape[1]):
            # change output pixels based on color rules
            if output_grid[i, j] == 1 or output_grid[i, j] == 8:
                output_grid[i, j] = 5
            elif output_grid[i, j] == 2:
                output_grid[i, j] = 2  # Red remains unchanged (though redundant, it clarifies the logic)

    return output_grid

results = []
for i, example in enumerate(train_examples):
  predicted = transform(example["input"])
  correct = np.array_equal(predicted, example["output"])
  results.append({
      "example": i+1,
      "correct": correct,
      "input_colors": np.unique(example["input"]).tolist(),
      "output_colors": np.unique(example["output"]).tolist(),
      "predicted_colors": np.unique(predicted).tolist()
  })


print(results)
