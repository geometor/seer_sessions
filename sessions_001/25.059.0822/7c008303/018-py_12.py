import numpy as np

train = [
    {
        "input": np.array([
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 8, 0, 0, 0, 0, 0, 0],
            [0, 0, 8, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 3, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 3, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 2, 2],
            [0, 0, 0, 0, 0, 0, 0, 2, 2],
            [0, 0, 8, 0, 0, 0, 0, 0, 8]
        ]),
        "output": np.array([
            [2, 0, 0, 0, 0, 4],
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [0, 0, 5, 0, 0, 0],
            [0, 0, 0, 0, 6, 0],
            [0, 0, 0, 0, 0, 0]
        ]),
    },
    {
        "input": np.array([
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 8, 0, 0, 0, 0, 0, 0],
            [0, 0, 8, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 3, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [4, 4, 0, 0, 0, 0, 0, 0, 0],
            [4, 4, 8, 0, 0, 0, 0, 0, 8]
        ]),
        "output": np.array([
            [2, 0, 0, 0, 0, 4],
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 5, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
        ]),
    },
    {
        "input": np.array([
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 8, 0, 0, 0, 0, 0, 0],
            [0, 0, 8, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [1, 0, 0, 0, 0, 0, 0, 0, 0],
            [1, 1, 0, 3, 0, 0, 0, 0, 0],
            [1, 1, 8, 0, 0, 0, 0, 0, 8],
        ]),
        "output": np.array([
            [2, 0, 0, 0, 0, 4],
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
        ]),
    },
]

def get_positions(grid, color):
    return [(row, col) for row in range(grid.shape[0]) for col in range(grid.shape[1]) if grid[row, col] == color]

def analyze_examples(examples):
    results = []
    for i, example in enumerate(examples):
        input_grid = example["input"]
        output_grid = example["output"]
        input_colors = np.unique(input_grid)
        output_colors = np.unique(output_grid)
        input_color_positions = {color: get_positions(input_grid, color) for color in input_colors if color != 0}
        output_color_positions = {color: get_positions(output_grid, color) for color in output_colors if color != 0}

        results.append({
            "example": i + 1,
            "input_shape": input_grid.shape,
            "output_shape": output_grid.shape,
            "input_colors": input_colors.tolist(),
            "output_colors": output_colors.tolist(),
            "input_color_positions": input_color_positions,
            "output_color_positions": output_color_positions,
        })
    return results

analysis = analyze_examples(train)

for result in analysis:
    print(f"Example {result['example']}:")
    print(f"  Input shape: {result['input_shape']}")
    print(f"  Output shape: {result['output_shape']}")
    print(f"  Input colors: {result['input_colors']}")
    print(f"  Output colors: {result['output_colors']}")
    print(f"  Input color positions: {result['input_color_positions']}")
    print(f"  Output color positions: {result['output_color_positions']}")
    print("-" * 20)