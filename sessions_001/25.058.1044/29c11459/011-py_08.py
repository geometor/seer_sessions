def check_solution(task, transform_func):
    """Checks the solution against all training examples and prints relevant details."""
    print(f"Task: {task['name']}")
    correct_count = 0
    for i, example in enumerate(task['train']):
        input_grid = np.array(example['input'])
        output_grid = np.array(example['output'])
        predicted_output = transform_func(input_grid)

        if np.array_equal(predicted_output, output_grid):
            correct_count += 1
            print(f"  Example {i + 1}: Correct")
        else:
            print(f"  Example {i + 1}: Incorrect")
            print(f"    Input:\n{input_grid}")
            print(f"    Expected Output:\n{output_grid}")
            print(f"    Predicted Output:\n{predicted_output}")

            # Find differences
            diff = predicted_output != output_grid
            diff_coords = np.argwhere(diff)

            # Find colors in the input at the differing coordinates in output
            input_colors = [input_grid[coord[0], coord[1]] for coord in diff_coords]

            # Find expected and predicted colors
            expected_colors = [output_grid[coord[0], coord[1]] for coord in diff_coords]
            predicted_colors = [predicted_output[coord[0], coord[1]] for coord in diff_coords]

            print(f"    Differences at coordinates: {diff_coords}")
            print(f"    Input colors at diff: {input_colors}")
            print(f"    Expected colors at diff: {expected_colors}")
            print(f"    Predicted colors at diff: {predicted_colors}")

    print(f"  Correct examples: {correct_count}/{len(task['train'])}")
    print("-" * 40)

# Assuming 'transform' function and 'task' are defined
# Example usage (replace with your actual task data):
#   check_solution(task, transform)

# Mock task to prevent execution errors
task = {
    'name': 'mock_task',
    'train': [
        {'input': [[1, 2], [3, 4]], 'output': [[1, 2], [3, 4]]},
        {'input': [[5, 6], [7, 8]], 'output': [[5, 6], [7, 8]]}
    ]

}

check_solution(task, transform)