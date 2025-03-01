import numpy as np

def describe_grid(grid):
    """Provides a basic description of the grid: dimensions and unique colors."""
    dimensions = grid.shape
    unique_colors = np.unique(grid)
    return f"Dimensions: {dimensions}, Unique Colors: {unique_colors}"

def compare_grids(input_grid, output_grid):
    """Compares two grids and reports differences."""
    if input_grid.shape != output_grid.shape:
        return "Different dimensions!"
    else:
        diff = input_grid != output_grid
        num_diff = np.sum(diff)
        diff_indices = np.where(diff)
        
        # are all output pixels the same value
        output_values = output_grid[diff_indices]
        all_same_output_value = np.all(output_values == output_values[0]) if len(output_values) >0 else "no difference"
        return f"Number of different pixels: {num_diff}, All changed pixels are same value: {all_same_output_value}"

# Example data (replace with the actual data)

train_examples = [
    {
        "input": np.array([[6, 6, 6], [6, 6, 6], [6, 6, 6]]),
        "output": np.array([[0, 0, 0], [0, 0, 0], [0, 0, 0]]),
         "test_result": np.array([[0, 0, 0], [0, 0, 0], [0, 0, 0]])
    },
    {
        "input": np.array([[5, 5, 5, 5], [5, 5, 5, 5], [5, 5, 5, 5], [5, 5, 5, 5]]),
        "output": np.array([[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]),
        "test_result": np.array([[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]])
    },
    {
        "input": np.array([[8, 8, 8, 8, 8, 8], [8, 8, 8, 8, 8, 8], [8, 8, 8, 8, 8, 8]]),
        "output": np.array([[0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0]]),
        "test_result": np.array([[0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0]])
    },
    {
        "input": np.array([[7, 7], [7, 7], [7, 7]]),
        "output": np.array([[0, 0], [0, 0], [0, 0]]),
         "test_result": np.array([[0, 0], [0, 0], [0, 0]])
    },
        {
        "input": np.array([[4, 4]]),
        "output": np.array([[0, 0]]),
         "test_result": np.array([[0, 0]])
    },

]


for i, example in enumerate(train_examples):
    print(f"Example {i+1}:")
    print("Input Grid Description:", describe_grid(example["input"]))
    print("Output Grid Description:", describe_grid(example["output"]))
    print("Comparison:", compare_grids(example["input"], example["output"]))
    print("Comparison with Test Result:", compare_grids(example["input"], example["test_result"]))
    print("-" * 20)