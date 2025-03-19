import numpy as np

def transform(input_grid):
    output_grid = np.copy(input_grid)
    for row_index, row in enumerate(input_grid):
        for col_index, pixel_value in enumerate(row):
            if pixel_value == 1 or pixel_value == 8:
                output_grid[row_index, col_index] = 5
    return output_grid

# Dummy data for demonstration - replace with actual task data
train_examples = [
    {
        "input": np.array([[1, 0, 2], [3, 8, 4], [1, 2, 8]]),
        "output": np.array([[5, 0, 2], [3, 5, 4], [5, 2, 5]]),
    },
    {
        "input": np.array([[8, 1, 8], [1, 8, 1], [8, 1, 8]]),
        "output": np.array([[5, 5, 5], [5, 5, 5], [5, 5, 5]]),
    },
    {
        "input": np.array([[2, 2, 2], [2, 2, 2], [2, 2, 2]]),
        "output": np.array([[2, 2, 2], [2, 2, 2], [2, 2, 2]]),
    },
]

for i, example in enumerate(train_examples):
    predicted_output = transform(example["input"])
    print(f"Example {i+1}:")
    print(f"  Input:\n{example['input']}")
    print(f"  Expected Output:\n{example['output']}")
    print(f"  Predicted Output:\n{predicted_output}")
    print(f"  Match: {np.array_equal(example['output'], predicted_output)}")
    print("-" * 20)
