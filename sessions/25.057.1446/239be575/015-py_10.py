import numpy as np

train_pairs = [
    {
        "input": [[5, 5, 5], [5, 5, 5], [5, 5, 5]],
        "output": [[5]]
    },
    {
        "input": [[5, 5, 5, 5], [5, 5, 5, 5], [5, 5, 5, 5], [5, 5, 5, 5]],
        "output": [[5]]
    },
    {
        "input": [[0, 0, 7, 7, 7], [7, 0, 7, 7, 7], [7, 7, 7, 7, 7], [7, 7, 7, 7, 7], [7, 7, 7, 7, 7]],
        "output": [[7]]
    }
]


def analyze_grid(grid):
    """Analyzes a single grid and returns relevant metrics."""
    grid = np.array(grid)
    unique, counts = np.unique(grid, return_counts=True)
    color_counts = dict(zip(unique, counts))
    dimensions = grid.shape
    return {
        "color_counts": color_counts,
        "dimensions": dimensions,
    }


def analyze_results(train_pairs, transform_function):
    """Analyzes the results of applying the transform function to the training pairs."""
    results = []
    for pair in train_pairs:
        input_grid = pair["input"]
        expected_output = pair["output"]
        actual_output = transform_function(input_grid)
        correct = np.array_equal(np.array(actual_output), np.array(expected_output))
        analysis = analyze_grid(input_grid)
        analysis["expected_output"] = expected_output[0][0]  # Extract single value
        analysis["actual_output"] = actual_output[0][0]
        analysis["correct"] = correct
        results.append(analysis)
    return results

# Current transform for this task.
def transform(input_grid):
    """
    Extracts the top-left element of the input grid.

    Args:
        input_grid (list of lists): A 2D array representing the input grid.

    Returns:
        int: The value at the top-left corner of the input grid.
    """
    # Convert input_grid to numpy array for easier manipulation
    input_array = np.array(input_grid)
    
    # Extract the top-left element (0,0)
    top_left_element = input_array[0, 0]
    
    # Create output grid, a 1x1 matrix with top_left_element
    output_grid = np.array([[top_left_element]])

    return output_grid.tolist()

analysis_results = analyze_results(train_pairs, transform)

for i, result in enumerate(analysis_results):
    print(f"--- Example {i+1} ---")
    print(f"  Dimensions: {result['dimensions']}")
    print(f"  Color Counts: {result['color_counts']}")
    print(f"  Expected Output: {result['expected_output']}")
    print(f"  Actual Output: {result['actual_output']}")
    print(f"  Correct: {result['correct']}")