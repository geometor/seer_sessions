import numpy as np

def analyze_example(input_grid, expected_output_grid, predicted_output_grid):
    input_grid = np.array(input_grid)
    expected_output_grid = np.array(expected_output_grid)
    predicted_output_grid = np.array(predicted_output_grid)

    input_unique_colors = []
    rows, cols = input_grid.shape
    for i in range(rows):
        for j in range(cols):
            color = input_grid[i, j]
            if color not in input_unique_colors:
                input_unique_colors.append(color)


    expected_unique_colors = []
    rows, cols = expected_output_grid.shape
    for i in range(rows):
        for j in range(cols):
            color = expected_output_grid[i, j]
            if color not in expected_unique_colors:
                expected_unique_colors.append(color)

    predicted_unique_colors = []
    if predicted_output_grid.size > 0:  # Check if the array is not empty
        rows, cols = predicted_output_grid.shape
        for i in range(rows):
            for j in range(cols):
                color = predicted_output_grid[i, j]
                if color not in predicted_unique_colors:
                    predicted_unique_colors.append(color)

    print(f"  Input Unique Colors: {input_unique_colors}")
    print(f"  Expected Unique Colors: {expected_unique_colors}")
    print(f"  Predicted Unique Colors: {predicted_unique_colors}")
    print(f"  Input Shape: {input_grid.shape}, Output Shape: {expected_output_grid.shape}, Predicted Shape: {predicted_output_grid.shape}")
    print(f"  Match: {np.array_equal(expected_output_grid, predicted_output_grid)}")

#Example Usage (replace with your actual data for each task)
task_examples = [
    {
        "input": [[5, 4, 5], [5, 4, 5], [5, 4, 5]],
        "output": [[5], [4], [5]]
    },
    {
        "input": [[8, 8, 8, 8], [8, 0, 0, 8], [8, 8, 8, 8]],
        "output": [[8], [0], [8]]
    },
        {
        "input": [[1, 0, 2, 0, 3], [0, 1, 0, 2, 0], [3, 0, 1, 0, 2], [0, 3, 0, 1, 0], [2, 0, 3, 0, 1]],
        "output": [[1, 0, 2, 0, 3]]
    },
     {
        "input": [[1, 0, 2, 0, 3, 4], [0, 1, 0, 2, 0, 4], [3, 0, 1, 0, 2, 4], [0, 3, 0, 1, 0, 4], [2, 0, 3, 0, 1, 4]],
        "output": [[1, 0, 2, 0, 3, 4]]
     }
]

previous_code_output = [
    [[5], [4]],
    [[8], [0]],
    [[1],[0],[2],[3]],
    [[1],[0],[2],[3],[4]]
]

for i, example in enumerate(task_examples):
  print(f"Example {i+1}:")
  analyze_example(example["input"], example["output"], previous_code_output[i])