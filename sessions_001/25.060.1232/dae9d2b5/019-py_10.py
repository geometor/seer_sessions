import numpy as np

def grid_properties(grid):
    dimensions = grid.shape
    unique_colors = np.unique(grid)
    num_unique_colors = len(unique_colors)
    return {
        'dimensions': dimensions,
        'unique_colors': unique_colors.tolist(),
        'num_unique_colors': num_unique_colors
    }

# Example grids from the prompt (replace with actual data)

train_examples = [
    {
        'input': np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]]),
        'output': np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
    },
     {
        'input': np.array([[5, 1], [8, 9]]),
        'output': np.array([[5, 1, 6], [8, 9, 6], [6, 6, 6]])
    },
    {
        'input': np.array([[8, 8, 8, 8, 8], [8, 8, 8, 8, 8], [8, 8, 8, 8, 8], [8, 8, 8, 8, 8]]),
        'output': np.array([[8, 8, 8], [8, 8, 8], [8, 8, 8]])
    },
    {
        'input': np.array([[5, 0, 5, 0, 5], [0, 5, 0, 5, 0], [5, 0, 5, 0, 5], [0, 5, 0, 5, 0]]),
        'output': np.array([[5, 0, 5], [0, 5, 0], [5, 0, 5]])
    },
    {
        'input': np.array([[1, 0, 0, 0, 0], [0, 1, 0, 0, 0], [0, 0, 1, 0, 0], [0, 0, 0, 1, 0],[0, 0, 0, 0, 1]]),
        'output': np.array([[1, 0, 0], [0, 1, 0], [0, 0, 1]])
    }
]
# Collect properties for inputs and outputs

results = []
for i, example in enumerate(train_examples):
  input_props = grid_properties(example['input'])
  output_props = grid_properties(example['output'])
  results.append({
      'example': i + 1,
      'input': input_props,
      'output': output_props
  })

# Print the results
for result in results:
    print(result)
