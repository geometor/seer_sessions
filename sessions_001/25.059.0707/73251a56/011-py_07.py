import numpy as np

def analyze_example(input_grid, output_grid):
    """Analyzes a single input-output pair and returns relevant metrics."""

    input_grid = np.array(input_grid)
    output_grid = np.array(output_grid)

    input_colors = {}
    output_colors = {}

    for i in range(10):  # Colors 0-9
        input_colors[i] = np.sum(input_grid == i)
        output_colors[i] = np.sum(output_grid == i)
    
    input_shape = input_grid.shape
    output_shape = output_grid.shape
    
    color_changes = {}
    for color in input_colors:
        if input_colors[color] != output_colors[color]:
            color_changes[color] = (input_colors[color], output_colors[color])
            

    return {
        "input_shape": input_shape,
        "output_shape": output_shape,
        "input_colors": input_colors,
        "output_colors": output_colors,
        "color_changes": color_changes,
    }

# Example usage (assuming train_in, train_out are defined from the task data)
examples = [
    {
        "input": [[0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 1, 1, 1, 0, 0, 0], [0, 0, 0, 1, 1, 1, 0, 0, 0], [0, 0, 0, 1, 1, 1, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0]],
        "output": [[1, 1, 1], [1, 1, 1], [1, 1, 1]]
    },
    {
        "input": [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 8, 8, 8, 0, 0, 0], [0, 0, 0, 0, 8, 8, 8, 0, 0, 0], [0, 0, 0, 0, 8, 8, 8, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]],
        "output": [[8, 8, 8], [8, 8, 8], [8, 8, 8]]
    },
    {
       "input": [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 5, 5, 5, 0, 0, 0], [0, 0, 0, 0, 5, 5, 5, 0, 0, 0], [0, 0, 0, 0, 5, 5, 5, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]],
        "output": [[5, 5, 5], [5, 5, 5], [5, 5, 5]]
    }
]
results = [analyze_example(ex["input"], ex["output"]) for ex in examples]
for i, result in enumerate(results):
    print(f"Example {i+1}:")
    print(f"  Input Shape: {result['input_shape']}")
    print(f"  Output Shape: {result['output_shape']}")
    print(f"  Input Colors: {result['input_colors']}")
    print(f"  Output Colors: {result['output_colors']}")
    print(f"  Color Changes: {result['color_changes']}")
    print("-" * 20)