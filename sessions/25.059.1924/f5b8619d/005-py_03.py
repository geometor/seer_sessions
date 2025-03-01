import numpy as np

def code_execution(input_grid, output_grid):
    """Executes code and reports on the grids."""
    input_shape = input_grid.shape
    output_shape = output_grid.shape
    unique_input_colors = np.unique(input_grid)
    unique_output_colors = np.unique(output_grid)
    print(f"Input shape: {input_shape}, Output shape: {output_shape}")
    print(f"Unique input colors: {unique_input_colors}, Unique output colors: {unique_output_colors}")

task = {
    "train": [
        {
            "input": [[5, 5, 5], [5, 5, 5], [5, 5, 5]],
            "output": [[5, 0, 8, 5, 0, 8, 5, 0, 8], [0, 0, 0, 0, 0, 0, 0, 0, 0], [8, 0, 8, 8, 0, 8, 8, 0, 8], [5, 0, 8, 5, 0, 8, 5, 0, 8], [0, 0, 0, 0, 0, 0, 0, 0, 0], [8, 0, 8, 8, 0, 8, 8, 0, 8], [5, 0, 8, 5, 0, 8, 5, 0, 8]],
        },
        {
            "input": [[6, 6, 5], [6, 6, 5], [5, 5, 5]],
            "output": [[6, 0, 8, 6, 0, 8, 5, 0, 8], [0, 0, 0, 0, 0, 0, 0, 0, 0], [8, 0, 8, 8, 0, 8, 8, 0, 8], [6, 0, 8, 6, 0, 8, 5, 0, 8], [0, 0, 0, 0, 0, 0, 0, 0, 0], [8, 0, 8, 8, 0, 8, 8, 0, 8], [5, 0, 8, 5, 0, 8, 5, 0, 8]],
        },
		{
            "input": [[6, 6, 6], [5, 6, 5], [5, 5, 5]],
            "output": [[6, 0, 8, 6, 0, 8, 6, 0, 8], [0, 0, 0, 0, 0, 0, 0, 0, 0], [8, 0, 8, 8, 0, 8, 8, 0, 8], [5, 0, 8, 6, 0, 8, 5, 0, 8], [0, 0, 0, 0, 0, 0, 0, 0, 0], [8, 0, 8, 8, 0, 8, 8, 0, 8], [5, 0, 8, 5, 0, 8, 5, 0, 8]],
        },
       {
            "input": [[5, 5, 6], [6, 6, 6], [5, 5, 5]],
            "output" : [[5, 0, 8, 5, 0, 8, 6, 0, 8], [0, 0, 0, 0, 0, 0, 0, 0, 0], [8, 0, 8, 8, 0, 8, 8, 0, 8], [6, 0, 8, 6, 0, 8, 6, 0, 8], [0, 0, 0, 0, 0, 0, 0, 0, 0], [8, 0, 8, 8, 0, 8, 8, 0, 8], [5, 0, 8, 5, 0, 8, 5, 0, 8]]
        }
    ],
    "test": [
        {"input": [[5, 5, 5], [6, 6, 6], [5, 5, 5]], "output": [[5, 0, 8, 5, 0, 8, 5, 0, 8], [0, 0, 0, 0, 0, 0, 0, 0, 0], [8, 0, 8, 8, 0, 8, 8, 0, 8], [6, 0, 8, 6, 0, 8, 6, 0, 8], [0, 0, 0, 0, 0, 0, 0, 0, 0], [8, 0, 8, 8, 0, 8, 8, 0, 8], [5, 0, 8, 5, 0, 8, 5, 0, 8]]},
    ],
}

for i, example in enumerate(task["train"]):
    print(f"Example {i+1}:")
    code_execution(np.array(example["input"]), np.array(example["output"]))