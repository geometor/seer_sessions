def get_grid_dimensions_and_colors(grid):
    """Returns the dimensions and unique colors of a grid."""
    import numpy as np
    grid_array = np.array(grid)
    dimensions = grid_array.shape
    unique_colors = np.unique(grid_array)
    return dimensions, unique_colors

# Example Data (Assuming this is defined elsewhere in the notebook)
examples = [
    {
        "input": [[5, 5, 5, 5, 5, 5], [5, 1, 5, 5, 5, 5], [5, 5, 5, 3, 5, 5], [5, 5, 5, 5, 5, 2]],
        "output": [[3]]
    },
    {
        "input": [[0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 4, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0]],
        "output": [[1]]
    },
    {
        "input": [[1, 1, 1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1, 2, 1], [1, 1, 1, 1, 1, 1, 1, 1, 1]],
        "output": [[2]]
    },
     {
        "input": [[7,7,7],[7,7,7],[7,7,0]],
        "output": [[2]]
    }
]

for i, example in enumerate(examples):
    input_grid = example['input']
    expected_output = example['output']
    actual_output = transform(input_grid)  # Assuming 'transform' function is defined
    input_dimensions, input_colors = get_grid_dimensions_and_colors(input_grid)
    output_dimensions, output_colors = get_grid_dimensions_and_colors(expected_output)
    print(f"Example {i+1}:")
    print(f"  Input Dimensions: {input_dimensions}, Unique Colors: {input_colors}")
    print(f"  Expected Output Dimensions: {output_dimensions}, Unique Colors: {output_colors}")
    print(f"  Actual Output: {actual_output}")
    print(f"  Correct: {np.array_equal(actual_output, np.array(expected_output))}")
    print("-" * 20)