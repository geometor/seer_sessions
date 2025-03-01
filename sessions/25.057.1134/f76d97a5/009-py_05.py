import numpy as np

def analyze_transform(input_grid, expected_output_grid, transform_function):
    """
    Analyzes the transformation performed by the provided function.

    Args:
        input_grid: The input grid (NumPy array).
        expected_output_grid: The expected output grid (NumPy array).
        transform_function: The function to apply to the input_grid.

    Returns:
        A dictionary containing analysis results:
        - "correct": Boolean indicating if the transformation is correct.
        - "input_colors": Dictionary of colors and their counts in the input.
        - "expected_output_colors": Dictionary of colors and their counts in the expected output.
        - "actual_output_colors": Dictionary of colors and their counts in the actual output.
        - "comparison_matrix":  A character matrix to make comparison easy.
            - '.' if input and output match
            - 'X' if they differ
            - 'I' if the pixel was and should be unchanged
            - 'C' if the pixel was correctly changed
    """
    actual_output_grid = transform_function(input_grid)
    correct = np.array_equal(actual_output_grid, expected_output_grid)

    def count_colors(grid):
        unique, counts = np.unique(grid, return_counts=True)
        return dict(zip(unique, counts))
    
    comparison_matrix = np.full(input_grid.shape, '.', dtype='U1')
    for r in range(input_grid.shape[0]):
        for c in range(input_grid.shape[1]):
          if input_grid[r,c] == expected_output_grid[r,c]:
              comparison_matrix[r,c] = 'I' if input_grid[r,c] == actual_output_grid[r,c] else '.'
          else:
              comparison_matrix[r,c] = 'C' if expected_output_grid[r,c] == actual_output_grid[r,c] else 'X'
    
    return {
        "correct": correct,
        "input_colors": count_colors(input_grid),
        "expected_output_colors": count_colors(expected_output_grid),
        "actual_output_colors": count_colors(actual_output_grid),
        "comparison_matrix": comparison_matrix,
    }

def summarize_results(task, transform_function):
  print(f"TASK: {task['id']}")
  for i in range(len(task['train'])):
        analysis = analyze_transform(np.array(task['train'][i]['input']), np.array(task['train'][i]['output']), transform_function)
        print(f"\nExample {i+1}:")
        print(f"  Correct: {analysis['correct']}")
        print(f"  Input Colors: {analysis['input_colors']}")
        print(f"  Expected Output Colors: {analysis['expected_output_colors']}")
        print(f"  Actual Output Colors: {analysis['actual_output_colors']}")
        print("Comparison Matrix:")
        print(analysis["comparison_matrix"])

# Mock task and previous transform function for demonstration - replace with the real task
mock_task = {
  'id': 'mock_task',
  'train': [
      {'input': [[5, 5, 5], [5, 6, 5], [5, 5, 5]], 'output': [[0, 0, 0], [0, 6, 0], [0, 0, 0]]},
      {'input': [[5, 5, 6], [5, 5, 5], [6, 5, 5]], 'output': [[0, 0, 6], [0, 0, 0], [6, 0, 0]]},
      {'input': [[5, 6, 5], [6, 5, 6], [5, 6, 5]], 'output': [[5, 6, 5], [6, 5, 6], [5, 6, 5]]},
      {'input': [[1, 5, 1], [5, 6, 5], [1, 5, 1]], 'output': [[1, 0, 1], [0, 6, 0], [1, 0, 1]]}
  ]
}
def previous_transform(input_grid):
    output_grid = np.copy(input_grid)
    rows, cols = output_grid.shape
    for i in range(rows):
        for j in range(cols):
            if output_grid[i, j] == 5:
                output_grid[i, j] = 0
    return output_grid
summarize_results(mock_task, previous_transform)