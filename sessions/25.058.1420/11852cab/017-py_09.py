import numpy as np

def calculate_diff(grid1, grid2):
    # Ensure both grids have the same shape
    if grid1.shape != grid2.shape:
        return "Grids have different shapes"

    # Calculate the absolute difference
    diff = np.abs(grid1 - grid2)
    return diff

def show_grid(grid, title):
    print(title)
    rows = len(grid)
    cols = len(grid[0]) if rows > 0 else 0
    print(f"rows: {rows}")
    print(f"cols: {cols}")
    print(grid)

def process_examples(examples):
    results = []
    for i, example in enumerate(examples):
        input_grid = np.array(example['input'])
        expected_output_grid = np.array(example['output'])
        predicted_output_grid = transform(input_grid)
        diff_grid = calculate_diff(expected_output_grid, predicted_output_grid)

        example_info = {
            'example_index': i,
            'input': input_grid.tolist(),
            'expected_output': expected_output_grid.tolist(),
            'predicted_output': predicted_output_grid.tolist(),
            'diff': diff_grid.tolist() if isinstance(diff_grid, np.ndarray) else diff_grid
        }
        results.append(example_info)

     # Print details of each example
    for example_result in results:
        print(f"\nExample {example_result['example_index'] + 1}:")
        show_grid(np.array(example_result['input']), "Input Grid")
        show_grid(np.array(example_result['expected_output']), "Expected Output Grid")
        show_grid(np.array(example_result['predicted_output']), "Predicted Output Grid")
        show_grid(np.array(example_result['diff']), "Difference Grid")
        print(f"diff sum: {np.sum(example_result['diff'])}")

# assuming the train set is provided via prompt history
process_examples(train)