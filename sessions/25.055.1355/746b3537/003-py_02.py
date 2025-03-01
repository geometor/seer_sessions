import numpy as np

# Define the transform function (as provided)
def transform(input_grid):
    # Get the dimensions of the input grid.
    rows = len(input_grid)
    cols = len(input_grid[0])

    # Initialize the output grid as a list of lists (to build it dynamically)
    output_grid = []
    
    # Iterate each row in input
    for i in range(rows):
        # Append each complete row array to the output list.
        output_grid.append([input_grid[i][0]])

    return output_grid

# Example data (replace with actual data from the task)
examples = [
    {
        "input": [[5, 5, 5], [5, 5, 5], [5, 5, 5]],
        "output": [[5], [5], [5]],
    },
    {
        "input": [[1, 1, 1], [1, 1, 1]],
        "output": [[1], [1]],
    },
    {
         "input": [[3, 3, 3, 3], [3, 3, 3, 3], [3, 3, 3, 3], [3, 3, 3, 3]],
         "output": [[3], [3], [3], [3]]
    },
    {
        "input": [[4, 4], [4, 4], [4, 4], [4, 4], [4, 4]],
        "output": [[4], [4], [4], [4], [4]],
    },
    {
        "input": [[7],[7],[7]],
        "output": [[7],[7],[7]]
    }

]

results = []
for i, example in enumerate(examples):
    input_grid = example["input"]
    expected_output = example["output"]
    actual_output = transform(input_grid)
    correct = actual_output == expected_output
    results.append(
        {
            "example_index": i,
            "input_shape": np.array(input_grid).shape,
            "output_shape": np.array(expected_output).shape,
            "actual_output_shape": np.array(actual_output).shape,
            "correct": correct,
        }
    )
print(results)
