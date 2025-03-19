import numpy as np

# Example data (replace with actual data from the task)
examples = [
    {
        "input": np.array([[8, 8, 8], [8, 2, 8], [8, 8, 8]]),
        "output": np.array([[5, 5, 5], [5, 2, 5], [5, 5, 5]]),
    },
    {
        "input": np.array([[8, 8, 8, 8, 8], [8, 2, 8, 2, 8], [8, 8, 8, 8, 8], [8, 2, 8, 2, 8], [8, 8, 8, 8, 8]]),
        "output": np.array([[5, 5, 5, 5, 5], [5, 2, 5, 2, 5], [5, 5, 5, 5, 5], [5, 2, 5, 2, 5], [5, 5, 5, 5, 5]]),
    },
    {
        "input": np.array([[8, 8, 8, 8, 8, 8, 8], [8, 2, 8, 8, 8, 2, 8], [8, 8, 8, 2, 8, 8, 8], [8, 8, 2, 8, 2, 8, 8], [8, 8, 8, 2, 8, 8, 8], [8, 2, 8, 8, 8, 2, 8],[8, 8, 8, 8, 8, 8, 8]]),
        "output": np.array([[5, 5, 5, 5, 5, 5, 5], [5, 2, 5, 5, 5, 2, 5], [5, 5, 5, 2, 5, 5, 5], [5, 5, 2, 5, 2, 5, 5], [5, 5, 5, 2, 5, 5, 5], [5, 2, 5, 5, 5, 2, 5],[5, 5, 5, 5, 5, 5, 5]]),
    },
]

for i, example in enumerate(examples):
    input_grid = example["input"]
    output_grid = example["output"]

    # Check if the grid structure is the same
    assert input_grid.shape == output_grid.shape

    # Count azure pixels in the input
    azure_in_input = np.sum(input_grid == 8)

    # Count gray pixels in the output that correspond to azure in input
    gray_in_output_at_azure = np.sum(output_grid[input_grid == 8] == 5)
    
    # Count red pixels
    red_in_input = np.sum(input_grid == 2)
    red_in_output = np.sum(output_grid == 2)

    print(f"Example {i+1}:")
    print(f"  Input grid shape: {input_grid.shape}")
    print(f"  Azure (8) pixels in input: {azure_in_input}")
    print(f"  Gray (5) pixels replacing azure in output: {gray_in_output_at_azure}")
    print(f"  Red pixels in input: {red_in_input}")
    print(f"  Red pixels in output: {red_in_output}")
    print(f"  Result: {'Correct' if azure_in_input == gray_in_output_at_azure and red_in_input == red_in_output else 'Incorrect'}")
