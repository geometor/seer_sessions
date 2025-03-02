import numpy as np

def transform(input_grid):
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    for r in range(rows):
        gray_count = 0
        for c in range(cols):
            if input_grid[r, c] == 5:
                gray_count += 1
                if r == 0 or r == 2:  # First and third rows
                    if gray_count == 2 or gray_count == 4:
                        output_grid[r, c] = 3
                elif r == 1:  # Second row
                    if gray_count == 3:
                        output_grid[r, c] = 3
    return output_grid

# Example data (replace with actual data from the task)
train_examples = [
    {
        "input": np.array([[0, 5, 0, 5, 0, 5, 0, 5, 0],
                           [5, 0, 5, 0, 5, 0, 0, 0, 0],
                           [0, 5, 0, 5, 0, 5, 0, 5, 0]]),
        "output": np.array([[0, 3, 0, 3, 0, 5, 0, 5, 0],
                            [5, 0, 3, 0, 5, 0, 0, 0, 0],
                            [0, 3, 0, 3, 0, 5, 0, 5, 0]]),
    },
        {
        "input": np.array([[0, 5, 0, 5, 0, 0, 5, 0, 5],
                           [0, 0, 5, 0, 5, 0, 5, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0, 0, 0],
                           [5, 0, 5, 0, 5, 0, 5, 0, 5]]),
        "output": np.array([[0, 3, 0, 3, 0, 0, 3, 0, 3],
                            [0, 0, 3, 0, 3, 0, 3, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0, 0],
                            [3, 0, 3, 0, 3, 0, 3, 0, 3]]),
    },
    {
        "input": np.array([[5, 0, 5, 5, 0, 5, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                           [5, 0, 5, 5, 0, 5, 0, 5, 5, 0, 5, 5]]),
        "output": np.array([[3, 0, 3, 3, 0, 3, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                            [3, 0, 3, 3, 0, 3, 0, 3, 3, 0, 3, 3]]),
    }
]

for i, example in enumerate(train_examples):
    input_grid = example["input"]
    expected_output = example["output"]
    actual_output = transform(input_grid)
    comparison = np.array_equal(expected_output, actual_output)
    print(f"Example {i + 1}:")
    print(f"  Input:\n{input_grid}")
    print(f"  Expected Output:\n{expected_output}")
    print(f"  Actual Output:\n{actual_output}")
    print(f"  Match: {comparison}")
    print("-" * 20)