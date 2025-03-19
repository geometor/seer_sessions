import numpy as np

def calculate_metrics(input_grid, output_grid, predicted_output_grid):
    correct_pixels = np.sum(output_grid == predicted_output_grid)
    total_pixels = output_grid.size
    accuracy = correct_pixels / total_pixels if total_pixels > 0 else 0.0

    input_white_pixels = np.sum(input_grid == 0)
    input_magenta_pixels = np.sum(input_grid == 6)
    input_yellow_pixels = np.sum(input_grid == 4)
    output_yellow_pixels = np.sum(output_grid == 4)

    return {
        'accuracy': accuracy,
        'input_white_pixels': int(input_white_pixels),
        'input_magenta_pixels': int(input_magenta_pixels),
        'input_yellow_pixels': int(input_yellow_pixels),
        'output_yellow_pixels': int(output_yellow_pixels),
        'rows': int(input_grid.shape[0]),
        'cols': int(input_grid.shape[1])
    }

def pretty_print_grid(grid):
    """Prints the grid in a more readable format with brackets."""
    print("[")
    for row in grid:
        print("  " + str(list(row)) + ",")  # Convert NumPy array to list
    print("]")

task = {
    "train": [
        {
            "input": [[0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 6, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0]],
            "output": [[4, 4, 4, 4, 4, 4, 4, 4, 4], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 6, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [4, 4, 4, 4, 4, 4, 4, 4, 4]],
        },
        {
            "input": [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 6, 0, 0, 0, 0, 0, 0, 0, 0, 0]],
            "output": [[4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 6, 0, 0, 0, 0, 0, 0, 0, 0, 0]],
        },
		{
            "input": [[0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 6, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0]],
            "output": [[4, 4, 4, 4, 4, 4, 4, 4], [0, 0, 0, 0, 0, 0, 6, 0], [4, 4, 4, 4, 4, 4, 4, 4], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0]]
        },
        {
            "input": [[6, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]],
            "output": [[6, 4, 4, 4, 4], [4, 4, 4, 4, 4], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]]
        }
    ],
    "test": [
        {"input": [[0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0], [0, 0, 6, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0]], "output": [[4, 4, 4, 4, 4, 4, 4], [0, 0, 0, 0, 0, 0, 0], [0, 0, 6, 0, 0, 0, 0], [4, 4, 4, 4, 4, 4, 4]]}
    ],
}

for i, example in enumerate(task["train"]):
    input_grid = np.array(example['input'])
    output_grid = np.array(example['output'])
    predicted_output_grid = transform(input_grid)  # Use the current transform function
    metrics = calculate_metrics(input_grid, output_grid, predicted_output_grid)
    print(f"Example {i+1}:")
    print("Input Grid:")
    pretty_print_grid(input_grid)
    print("Output Grid:")
    pretty_print_grid(output_grid)
    print("Predicted Output Grid:")
    pretty_print_grid(predicted_output_grid)
    print("Metrics:", metrics)
    print("-" * 30)