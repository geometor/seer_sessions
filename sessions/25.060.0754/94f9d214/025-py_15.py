import numpy as np

def analyze_grids(input_grid, output_grid):
    """
    Analyzes the input and output grids and returns a dictionary of observations.
    """
    input_grid = np.array(input_grid)
    output_grid = np.array(output_grid)

    analysis = {
        "input_shape": input_grid.shape,
        "output_shape": output_grid.shape,
        "input_unique_colors": np.unique(input_grid).tolist(),
        "output_unique_colors": np.unique(output_grid).tolist(),
        "grids_equal": np.array_equal(input_grid, output_grid),
        "input_has_blue" : 1 in input_grid,
    }

    return analysis
examples = [
    {
        "input": [[5, 5, 5, 5, 5, 5, 5, 5, 5], [5, 5, 5, 5, 5, 5, 5, 5, 5], [5, 5, 5, 5, 5, 5, 5, 5, 5], [5, 5, 5, 1, 5, 5, 5, 5, 5], [5, 5, 5, 5, 5, 5, 5, 5, 5], [5, 5, 5, 5, 5, 5, 5, 5, 5], [5, 5, 5, 5, 5, 5, 5, 5, 5], [5, 5, 5, 5, 5, 5, 5, 5, 5], [5, 5, 5, 5, 5, 5, 5, 5, 5]],
        "output": [[5, 5, 5, 5], [5, 5, 5, 5], [5, 5, 5, 5], [5, 5, 5, 0]],
    },
    {
        "input": [[5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5], [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5], [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5], [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5], [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5], [5, 5, 5, 1, 1, 1, 5, 5, 5, 5, 5], [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5], [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5], [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5], [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5], [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5]],
        "output": [[5, 5, 5, 5], [5, 5, 5, 5], [5, 5, 5, 5], [5, 5, 5, 5]],
    },
    {
        "input": [[8, 5, 5, 5, 5, 5, 8, 5, 5], [5, 8, 5, 5, 5, 5, 5, 8, 5], [5, 5, 8, 5, 5, 5, 5, 5, 8], [5, 5, 5, 8, 5, 5, 5, 5, 5], [5, 5, 5, 5, 8, 5, 5, 5, 5], [5, 5, 5, 5, 5, 8, 5, 5, 5], [5, 5, 5, 5, 5, 5, 8, 5, 5], [5, 5, 5, 5, 5, 5, 5, 8, 5], [5, 5, 5, 5, 5, 5, 5, 5, 8]],
        "output": [[8, 5, 5, 5, 5, 5, 8, 5, 5], [5, 8, 5, 5, 5, 5, 5, 8, 5], [5, 5, 8, 5, 5, 5, 5, 5, 8], [5, 5, 5, 8, 5, 5, 5, 5, 5], [5, 5, 5, 5, 8, 5, 5, 5, 5], [5, 5, 5, 5, 5, 8, 5, 5, 5], [5, 5, 5, 5, 5, 5, 8, 5, 5], [5, 5, 5, 5, 5, 5, 5, 8, 5], [5, 5, 5, 5, 5, 5, 5, 5, 8]],
    },
    {
        "input": [[3, 3, 3, 3, 3, 3, 3, 3], [3, 3, 3, 3, 3, 3, 3, 3], [3, 3, 3, 3, 3, 3, 3, 3], [3, 3, 3, 3, 3, 3, 3, 3], [3, 3, 3, 3, 3, 3, 1, 3], [3, 3, 3, 3, 3, 3, 3, 3], [3, 3, 3, 3, 3, 3, 3, 3], [3, 3, 3, 3, 3, 3, 3, 3]],
        "output": [[3, 3, 3, 3], [3, 3, 3, 3], [3, 3, 3, 3], [3, 3, 3, 3]],
    },
]

for i, example in enumerate(examples):
    analysis = analyze_grids(example["input"], example["output"])
    print(f"Example {i+1}:")
    for key, value in analysis.items():
        print(f"  {key}: {value}")
    print("-" * 20)