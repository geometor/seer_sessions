def describe_grid(grid):
    """Provides a concise description of a grid."""
    grid = np.array(grid)
    unique_colors = np.unique(grid)
    shapes = {}
    for color in unique_colors:
        coords = np.argwhere(grid == color)
        if len(coords) > 0:
            min_row, min_col = coords.min(axis=0)
            max_row, max_col = coords.max(axis=0)
            height = max_row - min_row + 1
            width = max_col - min_col + 1
            shapes[color] = {
                'min_row': int(min_row), 'min_col': int(min_col),
                'max_row': int(max_row), 'max_col': int(max_col),
                'height': int(height), 'width': int(width)
            }
    return shapes

def analyze_examples(task):
    """Analyzes input/output pairs and predicted outputs."""
    results = []
    for example in task['train']:
        input_grid = example['input']
        output_grid = example['output']
        predicted_grid = transform(input_grid)  # Assuming 'transform' is defined
        results.append({
            'input': describe_grid(input_grid),
            'output': describe_grid(output_grid),
            'predicted': describe_grid(predicted_grid)
        })
    return results

# Assuming 'task' is the JSON object provided in the initial prompt
task = {
    "train": [
        {
            "input": [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 2, 2, 2, 2, 0, 0, 0], [0, 0, 0, 2, 2, 2, 2, 0, 0, 0], [0, 0, 0, 2, 2, 2, 2, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [8, 8, 8, 8, 8, 8, 8, 8, 8, 8]],
            "output": [[2, 2], [2, 2]]
        },
        {
            "input": [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 1, 1, 1, 1, 0, 0, 0], [0, 0, 0, 1, 1, 1, 1, 0, 0, 0], [0, 0, 0, 1, 1, 1, 1, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [8, 8, 8, 8, 8, 8, 8, 8, 8, 8], [8, 8, 8, 8, 8, 8, 8, 8, 8, 8]],
            "output": [[1, 1], [1, 1]]
        },
        {
            "input": [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 4, 4, 4, 4, 0, 0, 0], [0, 0, 0, 4, 4, 4, 4, 0, 0, 0], [0, 0, 0, 4, 4, 4, 4, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [8, 8, 8, 8, 8, 8, 8, 8, 8, 8], [8, 8, 8, 8, 8, 8, 8, 8, 8, 8]],
            "output": [[4, 4], [4, 4]]
        }
    ],
    "test": [
        {
            "input": [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 3, 3, 3, 3, 0, 0, 0], [0, 0, 0, 3, 3, 3, 3, 0, 0, 0], [0, 0, 0, 3, 3, 3, 3, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [8, 8, 8, 8, 8, 8, 8, 8, 8, 8]],
            "output": [[3, 3], [3, 3]]
        }
    ]
}

analysis = analyze_examples(task)
for i, result in enumerate(analysis):
    print(f"Example {i+1}:")
    print(f"  Input: {result['input']}")
    print(f"  Output: {result['output']}")
    print(f"  Predicted: {result['predicted']}")