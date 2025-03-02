import numpy as np

def transform(input_grid):
    output_grid = np.copy(input_grid)
    rows, cols = output_grid.shape

    # Iterate through rows
    for i in range(rows):
        # Magenta Replacement (Corners): First and Third Rows
        if i == 0 or i == rows -1:
            if output_grid[i, 0] == 4:
                output_grid[i, 0] = 6
            if output_grid[i, cols - 1] == 4:
                output_grid[i, cols - 1] = 6

            # Magenta Replacement (Pattern):  Every other yellow, starting from the second yellow if present
            yellow_indices = np.where(output_grid[i] == 4)[0]
            for j in range(1, len(yellow_indices), 2):
                 output_grid[i, yellow_indices[j]] = 6

        # Magenta Replacement (Middle Row)
        elif i == 1:
            for j in range(1, cols - 1):
                if output_grid[i, j] == 4 and output_grid[i, j-1] == 4 and output_grid[i, j+1] == 4:
                    output_grid[i, j] = 6

    return output_grid

def assess_transform(task):
    """
    Assesses the transform function against a set of input/output pairs.

    Args:
        task: A dictionary containing 'train' and 'test' lists of input/output examples.

    Returns:
        A dictionary containing results for each example, indicating 'correct' (boolean)
        and providing the transformed output.
    """
    results = {}
    for example_set in ['train', 'test']:
        results[example_set] = []
        for i, example in enumerate(task[example_set]):
            input_grid = np.array(example['input'])
            expected_output = np.array(example['output'])
            transformed_output = transform(input_grid)
            correct = np.array_equal(transformed_output, expected_output)
            results[example_set].append({
                'index': i,
                'correct': correct,
                'transformed_output': transformed_output.tolist()
            })
    return results

# Example usage (assuming 'task' variable holds the ARC task data):
# Replace with the actual ARC task data structure
task = {
    'train': [
        {'input': [[0, 0, 0, 0, 0, 0], [0, 4, 4, 4, 0, 0], [0, 0, 0, 0, 0, 0]], 'output': [[0, 0, 0, 0, 0, 0], [0, 4, 6, 4, 0, 0], [0, 0, 0, 0, 0, 0]]},
        {'input': [[0, 0, 4, 0, 0, 0], [0, 4, 4, 4, 0, 0], [0, 0, 4, 0, 0, 0]], 'output': [[0, 0, 6, 0, 0, 0], [0, 4, 6, 4, 0, 0], [0, 0, 6, 0, 0, 0]]},
        {'input': [[4, 0, 0, 0, 0, 4], [0, 0, 0, 0, 0, 0], [4, 0, 0, 0, 0, 4]], 'output': [[6, 0, 0, 0, 0, 6], [0, 0, 0, 0, 0, 0], [6, 0, 0, 0, 0, 6]]},
        {'input': [[0, 0, 0, 0, 0, 0], [0, 4, 0, 4, 0, 0], [0, 0, 0, 0, 0, 0]], 'output': [[0, 0, 0, 0, 0, 0], [0, 4, 0, 4, 0, 0], [0, 0, 0, 0, 0, 0]]}
    ],
    'test': [
        {'input': [[0, 4, 0, 0, 0, 4, 0], [0, 0, 0, 0, 0, 0, 0], [0, 4, 0, 0, 0, 4, 0]], 'output': [[0, 6, 0, 0, 0, 6, 0], [0, 0, 0, 0, 0, 0, 0], [0, 6, 0, 0, 0, 6, 0]]}
    ]
}

results = assess_transform(task)

# Create the report
report = ""
for set_name, set_results in results.items():
    report += f"Set: {set_name}\n"
    for example_result in set_results:
        report += f"  Example {example_result['index'] + 1}: {'Correct' if example_result['correct'] else 'Incorrect'}\n"

print(report)