import numpy as np

def calculate_metrics(input_grid, output_grid, predicted_grid):
    """Calculates metrics comparing the predicted output to the actual output."""
    correct_pixels = np.sum(predicted_grid == output_grid)
    incorrect_pixels = np.sum(predicted_grid != output_grid)
    total_pixels = predicted_grid.size
    accuracy = correct_pixels / total_pixels if total_pixels > 0 else 0.0

    input_green_count = np.sum(input_grid == 3)
    output_green_count = np.sum(output_grid == 3)
    predicted_green_count = np.sum(predicted_grid == 3)

    return {
        "accuracy": accuracy,
        "correct_pixels": correct_pixels,
        "incorrect_pixels": incorrect_pixels,
        "total_pixels": total_pixels,
        "input_green_count": input_green_count,
        "output_green_count": output_green_count,
        "predicted_green_count": predicted_green_count,
    }
def print_grid(grid, title="Grid"):
    """Prints a grid with a title."""
    print(f"\n--- {title} ---")
    for row in grid:
        print("".join(map(str, row)))


# example grids, replacing '...' with actual grid data.
example_grids = [
  {
    'input': np.array([[0, 0, 0, 0, 0, 0, 0],
                       [0, 0, 0, 0, 3, 0, 0],
                       [0, 0, 0, 0, 0, 0, 0],
                       [0, 3, 0, 0, 0, 0, 0],
                       [0, 0, 0, 0, 0, 0, 0],
                       [0, 0, 0, 0, 0, 0, 0]]),
    'output': np.array([[0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 3, 0, 0],
                        [0, 0, 0, 0, 3, 0, 0],
                        [0, 3, 3, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0]])
    },
     {
    'input': np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0],
                       [0, 0, 0, 0, 0, 0, 3, 0, 0],
                       [0, 0, 0, 0, 0, 0, 0, 0, 0],
                       [0, 0, 0, 0, 0, 0, 0, 0, 0],
                       [0, 0, 0, 3, 0, 0, 0, 0, 0],
                       [0, 0, 0, 0, 0, 0, 0, 0, 0],
                       [0, 0, 0, 0, 0, 0, 0, 0, 0]]),
    'output': np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 3, 0, 0],
                        [0, 0, 0, 0, 0, 0, 3, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 3, 3, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0, 0]])
    },
    {
    'input': np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                       [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3],
                       [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                       [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                       [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                       [0, 0, 0, 3, 0, 0, 0, 0, 0, 0, 0],
                       [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]),
    'output': np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3],
                        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3],
                        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 3, 3, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]])
    },
    {
    'input': np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0],
                       [0, 0, 0, 0, 0, 0, 0, 0, 0],
                       [0, 0, 0, 0, 0, 0, 0, 0, 3],
                       [0, 0, 0, 0, 0, 0, 0, 0, 0],
                       [0, 0, 0, 0, 3, 0, 0, 0, 0],
                       [0, 0, 0, 0, 0, 0, 0, 0, 0],
                       [0, 3, 0, 0, 0, 0, 0, 0, 0]]),
    'output': np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0, 3],
                        [0, 0, 0, 0, 0, 0, 0, 0, 3],
                        [0, 0, 0, 0, 3, 3, 0, 0, 0],
                        [0, 3, 3, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0, 0]])
    }

]

for i, grids in enumerate(example_grids):
    input_grid = grids['input']
    output_grid = grids['output']
    predicted_grid = transform(input_grid)  # Use the provided transform function
    metrics = calculate_metrics(input_grid, output_grid, predicted_grid)
    print(f"Example {i+1}:")
    print(metrics)
    print_grid(input_grid, "Input")
    print_grid(output_grid, "Expected Output")
    print_grid(predicted_grid, "Predicted Output")

