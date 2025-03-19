import numpy as np

def analyze_example(input_grid, output_grid):
    metrics = {}
    metrics['input_dims'] = input_grid.shape
    metrics['output_dims'] = output_grid.shape
    metrics['azure_coords_input'] = np.argwhere(input_grid == 8).tolist()
    metrics['red_coords_output'] = np.argwhere(output_grid == 2).tolist()
    if len(metrics['azure_coords_input']) > 0:
      metrics['leftmost_azure_col'] = min(c for r, c in metrics['azure_coords_input'])

    return metrics

def show_grid(grid, title):
    display(grid)

examples = task["train"]

for i, example in enumerate(examples):
    input_grid = np.array(example['input'])
    output_grid = np.array(example['output'])
    predicted_output = transform(input_grid) # from the previous turn
    print(f"--- Example {i+1} ---")
    metrics = analyze_example(input_grid, output_grid)
    print("Metrics:")
    print(metrics)
    print("Input:")
    show_grid(input_grid, "Input Grid")
    print("Expected Output:")
    show_grid(output_grid, "Output Grid")
    print("Predicted Output:")
    show_grid(predicted_output, "Predicted Output Grid")