import numpy as np

def analyze_results(task_index, input_grid, output_grid, expected_output_grid):
    """Analyzes the results and provides a report."""

    print(f"--- Task {task_index} ---")
    print(f"Input Grid:\n{input_grid}")
    print(f"Output Grid:\n{output_grid}")
    print(f"Expected Output Grid:\n{expected_output_grid}")

    correct = np.array_equal(output_grid, expected_output_grid)
    print(f"Correct: {correct}")

    input_colors = np.unique(input_grid)
    output_colors = np.unique(output_grid)
    expected_output_colors = np.unique(expected_output_grid)

    print(f"Input Colors: {input_colors}")
    print(f"Output Colors: {output_colors}")
    print(f"Expected Output Colors: {expected_output_colors}")

    if not correct:
        diff = output_grid == expected_output_grid
        print(f"Difference Matrix (True if correct):\n{diff}")
        print(f"Number of incorrect pixels: {diff.size - np.sum(diff)}")

# Example usage (assuming you have loaded the grids from the JSON)
# For demonstration, let's simulate the data from the prompt. You'd replace these with actual data.

# the grids are already loaded in the environment
# task_data['train'][0]['input']
# task_data['train'][0]['output']

for i in range(len(task_data['train'])):
  transformed_grid = transform(np.array(task_data['train'][i]['input']))
  analyze_results(i+1, np.array(task_data['train'][i]['input']), transformed_grid, np.array(task_data['train'][i]['output']))