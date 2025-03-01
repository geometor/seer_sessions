import numpy as np

def analyze_example(input_grid, output_grid, expected_output_grid):
    results = {}

    results["input_shape"] = input_grid.shape
    results["output_shape"] = output_grid.shape
    results["expected_output_shape"] = expected_output_grid.shape

    results["input_unique_colors"] = np.unique(input_grid).tolist()
    results["output_unique_colors"] = np.unique(output_grid).tolist()
    results["expected_output_unique_colors"] = np.unique(expected_output_grid).tolist()

    results["input_color_counts"] = {color: int(count) for color, count in zip(*np.unique(input_grid, return_counts=True))}
    results["output_color_counts"] = {color: int(count) for color, count in zip(*np.unique(output_grid, return_counts=True))}
    results["expected_output_color_counts"] = {color: int(count) for color, count in zip(*np.unique(expected_output_grid, return_counts=True))}

    results["grids_match"] = np.array_equal(output_grid, expected_output_grid)

    return results

# Example usage (replace with actual grids from the task)
task_id = '868de0fa'
task = ARC_DATA[task_id]

for i, example in enumerate(task['train']):

    input_grid = np.array(example['input'])
    expected_output_grid = np.array(example['output'])
    output_grid = transform(input_grid) # Use existing transform function
    analysis = analyze_example(input_grid, output_grid, expected_output_grid)

    print(f"Example {i+1}:")
    print(f"  Input Shape: {analysis['input_shape']}")
    print(f"  Output Shape: {analysis['output_shape']}")
    print(f"  Input Colors: {analysis['input_unique_colors']}")
    print(f"  Output Colors: {analysis['output_unique_colors']}")
    print(f"  Expected Output Colors: {analysis['expected_output_unique_colors']}")
    print(f"  Input Color Counts: {analysis['input_color_counts']}")
    print(f"  Output Color Counts: {analysis['output_color_counts']}")
    print(f"  Expected Output Color Counts: {analysis['expected_output_color_counts']}")
    print(f"  Grids Match: {analysis['grids_match']}")
    print("-" * 20)
