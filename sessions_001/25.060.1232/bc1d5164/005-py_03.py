import numpy as np

def analyze_examples(task_data):
    results = []
    for example in task_data['train']:
        input_grid = np.array(example['input'])
        output_grid = np.array(example['output'])

        input_colors = np.unique(input_grid)
        output_colors = np.unique(output_grid)

        input_shapes = {}
        output_shapes = {}

        for color in input_colors:
            coords = np.where(input_grid == color)
            min_row, max_row = np.min(coords[0]), np.max(coords[0])
            min_col, max_col = np.min(coords[1]), np.max(coords[1])
            height = max_row - min_row + 1
            width = max_col - min_col + 1

            if height == width:
                input_shapes[color] = "Square"
            elif height == 1 or width == 1:
                input_shapes[color] = "Line" #can be horizontal or vertical
            else:
                input_shapes[color] = "Rectangle"

        for color in output_colors:
            coords = np.where(output_grid == color)
            min_row, max_row = np.min(coords[0]), np.max(coords[0])
            min_col, max_col = np.min(coords[1]), np.max(coords[1])
            height = max_row - min_row + 1
            width = max_col - min_col + 1
            if height == width:
                output_shapes[color] = "Square"
            elif height == 1 or width == 1:
                output_shapes[color] = "Line" #can be horizontal or vertical
            else:
                output_shapes[color] = "Rectangle"

        results.append({
            'input_colors': input_colors.tolist(),
            'output_colors': output_colors.tolist(),
            'input_shapes': input_shapes,
            'output_shapes': output_shapes,
        })

    return results

# Assuming 'task' is your task dictionary loaded from JSON
# Example usage with dummy data:
task = {
    "train": [
        {
            "input": [[0, 0, 0, 0, 0, 0, 8, 0, 0],
                      [0, 0, 0, 0, 0, 0, 8, 0, 0],
                      [0, 0, 0, 0, 0, 0, 8, 0, 0],
                      [0, 0, 0, 0, 0, 0, 8, 0, 0]],
            "output": [[8],
                       [8],
                       [8],
                       [8]]
        },
        {
           "input":  [[0, 0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0, 2]],
            "output": [[2]]

        },
        {
            "input":  [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 4, 4, 4, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0]],
            "output": [[4, 4, 4],
                       [2, 0, 0]],
        }
    ]
}
analysis_results = analyze_examples(task)
for i, result in enumerate(analysis_results):
    print(f"Example {i+1}:")
    print(f"  Input Colors: {result['input_colors']}")
    print(f"  Output Colors: {result['output_colors']}")
    print(f"  Input Shapes: {result['input_shapes']}")
    print(f"  Output Shapes: {result['output_shapes']}")
    print("-" * 20)
