import numpy as np

def get_grid_stats(grid):
    """Returns grid shape, unique values, and value counts."""
    shape = grid.shape
    unique_values = np.unique(grid)
    value_counts = {val: np.count_nonzero(grid == val) for val in unique_values}
    return shape, unique_values, value_counts

# Example usage with provided training data (assuming they are loaded as numpy arrays):
# Replace these with the actual input/output grids.
train_examples = [
    {
        "input": np.array([[1, 1, 1], [1, 1, 1], [1, 1, 1]]),
        "output": np.array([[9, 9, 9], [9, 9, 9], [9, 9, 9]])
    },
    {
        "input": np.array([[5, 5, 5, 5], [5, 5, 5, 5], [5, 5, 5, 5], [5, 5, 5, 5]]),
        "output": np.array([[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]])
    }

]


for i, example in enumerate(train_examples):
    input_shape, input_unique, input_counts = get_grid_stats(example["input"])
    output_shape, output_unique, output_counts = get_grid_stats(example["output"])
    print(f"Example {i+1}:")
    print(f"  Input: Shape={input_shape}, Unique={input_unique}, Counts={input_counts}")
    print(f"  Output: Shape={output_shape}, Unique={output_unique}, Counts={output_counts}")
