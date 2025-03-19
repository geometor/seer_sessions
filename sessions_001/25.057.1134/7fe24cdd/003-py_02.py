import numpy as np

def describe_grid(grid):
    """Provides a description of the grid's properties."""
    rows, cols = grid.shape
    unique_colors = np.unique(grid)
    color_counts = {color: np.sum(grid == color) for color in unique_colors}
    return {
        "dimensions": (rows, cols),
        "unique_colors": unique_colors.tolist(),
        "color_counts": color_counts,
    }

#Example Usage (replace with actual grids from prompt)
#example usage using the first set of the provided examples
examples = [
    {
        "input": np.array([[5, 5, 5], [5, 5, 5], [5, 5, 5]]),
        "output": np.array([[5, 5, 5, 5, 5, 5], [5, 5, 5, 5, 5, 5], [5, 5, 5, 5, 5, 5], [5, 5, 5, 5, 5, 5], [5, 5, 5, 5, 5, 5], [5, 5, 5, 5, 5, 5]]),
    },
     {
        "input": np.array([[8, 8, 8, 8, 8, 8, 8, 8, 8], [8, 8, 8, 8, 8, 8, 8, 8, 8],[8, 8, 8, 8, 8, 8, 8, 8, 8]]),
        "output": np.array([[8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8],[8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8],[8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8]]),
    },
    {
        "input": np.array([[8, 8, 8, 8, 8, 8, 8, 8, 8], [8, 8, 8, 8, 8, 8, 8, 8, 8],[8, 8, 8, 8, 8, 8, 8, 8, 8],[8, 8, 8, 8, 8, 8, 8, 8, 8],[8, 8, 8, 8, 8, 8, 8, 8, 8]]),
        "output": np.array([[8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8],[8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8],[8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8],[8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8],[8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8]]),
    },
    {
        "input": np.array([[6, 6, 6], [6, 0, 6], [6, 6, 6]]),
        "output": np.array([[6, 6, 6, 6, 6, 6], [6, 0, 6, 6, 0, 6], [6, 6, 6, 6, 6, 6], [6, 6, 6, 6, 6, 6], [6, 0, 6, 6, 0, 6],[6, 6, 6, 6, 6, 6]]),
    },
]

results = []
for example in examples:
    input_description = describe_grid(example["input"])
    output_description = describe_grid(example["output"])
    results.append({
        "input": input_description,
        "output": output_description,
    })

for i, result in enumerate(results):
    print(f"Example {i+1}:")
    print(f"  Input: {result['input']}")
    print(f"  Output: {result['output']}")