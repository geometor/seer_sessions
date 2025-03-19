import numpy as np

def analyze_example(input_grid, output_grid, transform_func):
    """Analyzes a single input-output pair and the result of the transformation."""
    input_grid = np.array(input_grid)
    output_grid = np.array(output_grid)
    transformed_grid = transform_func(input_grid)
    result = np.array_equal(transformed_grid, output_grid)

    metrics = {
        "Input Shape": input_grid.shape,
        "Output Shape": output_grid.shape,
        "Non-White Pixels (Input)": np.count_nonzero(input_grid),
        "Non-White Pixels (Output)": np.count_nonzero(output_grid),
        "Transformation Result": result,
        "Generated vs Expected": not result,
    }
    if not result:
      metrics["Generated Output"] = transformed_grid.tolist()
      metrics["Expected Output"] = output_grid.tolist()


    return metrics

def pretty_print_analysis(task_data, transform_func):
    """Analyzes all examples in the task data and prints the results."""
    all_metrics = []
    for example in task_data['train']:
        input_grid = example['input']
        output_grid = example['output']
        metrics = analyze_example(input_grid, output_grid, transform_func)
        all_metrics.append(metrics)

    for i, metrics in enumerate(all_metrics):
        print(f"--- Example {i+1} ---")
        for key, value in metrics.items():
            print(f"{key}: {value}")
        print()

# The provided task data and the transform function from previous turn
task_data = {
  "train": [
    {
      "input": [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 1], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]],
      "output": [[0, 0, 0], [0, 0, 0], [0, 0, 1]]
    },
    {
      "input": [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 7], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]],
      "output": [[0, 0, 0], [0, 0, 0], [0, 0, 7]]
    },
    {
      "input": [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 4], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]],
      "output": [[0, 0, 0], [0, 0, 0], [0, 0, 4]]
    },
    {
      "input": [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 5], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]],
      "output": [[0, 0, 0], [0, 0, 0], [0, 0, 5]]
    }
  ]
}
import numpy as np

def transform(input_grid):
    """
    Transforms the input grid by extracting all non-white pixels and
    placing them into a 3x3 output grid.

    Args:
        input_grid: A 2D numpy array representing the input grid.

    Returns:
        A 3x3 numpy array containing the non-white pixels from the input grid.
    """
    # Initialize a 3x3 output grid filled with zeros (white).
    output_grid = np.zeros((3, 3), dtype=int)

    # Find all non-zero pixels and their coordinates
    non_zero_pixels = []
    rows, cols = input_grid.shape
    for r in range(rows):
        for c in range(cols):
            if input_grid[r, c] != 0:
                non_zero_pixels.append(input_grid[r, c])

    # Populate the output grid with the non-zero pixels
    count = 0
    for r in range(3):
        for c in range(3):
            if count < len(non_zero_pixels):
                output_grid[r, c] = non_zero_pixels[count]
                count += 1

    return output_grid
pretty_print_analysis(task_data, transform)