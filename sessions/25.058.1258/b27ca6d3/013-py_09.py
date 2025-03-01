import numpy as np

def code_execution(input_grid, output_grid, transformed_grid):
    """Analyzes the results and provides metrics."""
    correct = np.array_equal(output_grid, transformed_grid)
    changes_expected = np.sum(input_grid != output_grid)
    changes_made = np.sum(input_grid != transformed_grid)
    correct_changes = np.sum((input_grid != output_grid) & (output_grid == transformed_grid))
    incorrect_changes = np.sum((input_grid == output_grid) & (output_grid != transformed_grid))
    missed_changes = np.sum((input_grid != output_grid) & (output_grid != transformed_grid))

    print(f"Correct Transformation: {correct}")
    print(f"Expected Changes: {changes_expected}")
    print(f"Changes Made: {changes_made}")
    print(f"Correct Changes: {correct_changes}")
    print(f"Incorrect Changes: {incorrect_changes}")
    print(f"Missed Changes: {missed_changes}")
    print("-" * 20)
    return correct, changes_expected, changes_made, correct_changes, incorrect_changes, missed_changes



def test_transform_on_examples(transform, examples):
  results = []
  for task_name, example_set in examples.items():
    print(f"Testing: {task_name}")
    for i, example in enumerate(example_set):
      input_grid = np.array(example['input'])
      output_grid = np.array(example['output'])
      transformed_grid = transform(input_grid)
      print(f"Example {i + 1}:")
      results.append(code_execution(input_grid, output_grid, transformed_grid))
  return results

# Example Data (replace with actual data)
examples = {
  "Task1": [
        {
            "input": [[0, 0, 0, 0, 0],
                      [0, 2, 2, 2, 0],
                      [0, 0, 0, 0, 0]],
            "output": [[0, 0, 0, 0, 0],
                       [0, 3, 3, 3, 0],
                       [0, 0, 0, 0, 0]]
        },
        {
            "input": [[0, 0, 0, 0, 0],
                      [0, 2, 0, 2, 0],
                      [0, 0, 0, 0, 0]],
            "output": [[0, 0, 0, 0, 0],
                       [0, 2, 0, 2, 0],
                       [0, 0, 0, 0, 0]]
        },
        {
            "input": [[0, 0, 0, 0, 0],
                      [0, 2, 0, 0, 0],
                      [0, 0, 2, 0, 0]],
            "output": [[0, 0, 0, 0, 0],
                       [0, 3, 0, 0, 0],
                       [0, 0, 3, 0, 0]]
        },
        {
            "input": [[2, 0, 0, 0, 0, 2],
                      [0, 0, 0, 0, 0, 0],
                      [0, 0, 2, 2, 0, 0],
                      [0, 2, 0, 0, 2, 0],
                      [0, 0, 0, 0, 0, 0],
                      [2, 0, 0, 0, 0, 2]],
            "output": [[3, 0, 0, 0, 0, 3],
                       [0, 0, 0, 0, 0, 0],
                       [0, 0, 3, 3, 0, 0],
                       [0, 3, 0, 0, 3, 0],
                       [0, 0, 0, 0, 0, 0],
                       [3, 0, 0, 0, 0, 3]]
        },
        {
             "input": [[2, 0, 0, 0, 0, 0, 2, 0],
                       [0, 0, 0, 0, 0, 0, 0, 0],
                       [0, 0, 2, 0, 2, 0, 0, 0],
                       [0, 0, 0, 2, 0, 0, 0, 0],
                       [0, 0, 2, 0, 2, 0, 0, 2]],
             "output": [[3, 0, 0, 0, 0, 0, 3, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 3, 0, 3, 0, 0, 0],
                        [0, 0, 0, 3, 0, 0, 0, 0],
                        [0, 0, 3, 0, 3, 0, 0, 3]]
        }

    ]
}


test_transform_on_examples(transform, examples)
