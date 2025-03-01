import numpy as np

def transform(input_grid):
    """
    Transforms the input grid according to the specified rule.
    """
    # Count the number of gray pixels.
    gray_count = np.sum(input_grid == 5)

    # Create the output grid based on the count.
    if gray_count > 0 and gray_count % 2 != 0:
        output_grid = np.array([[1]])
    else:
        output_grid = np.array([[0]]) # or some other default, like an empty grid

    return output_grid

# Task examples - use the same names expected by ARC-AGI system
task = {
  "train": [
    {
      "input": [[5, 0, 5], [0, 0, 0], [5, 0, 5]],
      "output": [[1]]
    },
    {
      "input": [[5, 0, 0, 5], [0, 0, 0, 0], [0, 0, 0, 0], [5, 0, 0, 5]],
      "output": [[1]]
    },
    {
      "input": [[0, 0, 0], [0, 5, 0], [0, 0, 0]],
      "output": [[0]]
    },
    {
      "input": [[0, 0], [0, 0]],
      "output": [[0]]
    },
    {
      "input": [[0]],
      "output": [[0]]
    }
  ],
  "test": [
    {
      "input": [[5, 0, 5, 5], [0, 0, 0, 0], [5, 5, 5, 0], [0, 0, 0, 0]],
      "output": [[1]]
    }
  ]
}

# Store results for analysis
results = []

for example in task["train"]:
  input_grid = np.array(example["input"])
  output_grid = np.array(example["output"])
  predicted_output = transform(input_grid)

  results.append(
      {
          "input": example["input"],
          "output": example["output"],
          "predicted": predicted_output.tolist(),
          "correct": np.array_equal(output_grid, predicted_output),
          "gray_count": np.sum(input_grid == 5),
      }
  )

# print as a list of python dicts
print(results)
