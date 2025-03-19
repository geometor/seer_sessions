import numpy as np

def transform(input_grid):
    """
    Transforms the input grid based on observed patterns.
    The transformation can be identity or 90-degree clockwise rotation, seemingly dependent on object uniformity.
    """
    input_array = np.array(input_grid)
    rows, cols = input_array.shape

    # Check if the grid is uniform (all pixels have the same color)
    unique_colors = np.unique(input_array)
    if len(unique_colors) == 1:
        return input_grid.tolist()  # Identity transformation

    # If not uniform, perform 90-degree clockwise rotation
    output_grid = np.zeros((cols, rows), dtype=int)
    for i in range(rows):
        for j in range(cols):
            output_grid[j, rows - 1 - i] = input_array[i, j]

    return output_grid.tolist()

# Example Data (replace with your actual task data)
train_examples = [
    {
        "input": [[0, 0, 0], [0, 0, 0], [0, 0, 0]],
        "output": [[0, 0, 0], [0, 0, 0], [0, 0, 0]],
    },
    {
        "input": [[5, 5, 5], [5, 5, 5], [5, 5, 5]],
        "output": [[5, 5, 5], [5, 5, 5], [5, 5, 5]],
    },
    {
        "input": [[1, 0, 0], [0, 0, 0], [0, 0, 0]],
        "output": [[0, 0, 1], [0, 0, 0], [0, 0, 0]],
    },
    {
        "input": [[0, 0, 0, 0], [0, 2, 2, 0], [0, 0, 0, 0]],
        "output": [[0, 0, 0], [0, 2, 0], [0, 2, 0], [0, 0, 0]]
    },
    {
        "input":  [[0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 7, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]],
        "output": [[0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 7, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]]
    },
]

for i, example in enumerate(train_examples):
    input_grid = example["input"]
    expected_output = example["output"]
    predicted_output = transform(input_grid)
    print(f"Example {i+1}:")
    print(f"  Input:\n{np.array(input_grid)}")
    print(f"  Expected Output:\n{np.array(expected_output)}")
    print(f"  Predicted Output:\n{np.array(predicted_output)}")
    print(f"  Match: {np.array_equal(np.array(predicted_output), np.array(expected_output))}")
    print("-" * 20)