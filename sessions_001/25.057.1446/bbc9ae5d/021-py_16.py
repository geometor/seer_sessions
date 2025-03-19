def report(input_grid, expected_output, actual_output):
    diff = expected_output != actual_output
    print(f"Input:\n{input_grid}\n")
    print(f"Expected Output:\n{expected_output}\n")
    print(f"Actual Output:\n{actual_output}\n")
    print(f"Differences (Expected != Actual):\n{diff}\n")
    input_height, input_width = input_grid.shape
    output_height, output_width = expected_output.shape
    print(f"input size: {input_height}, {input_width}")
    print(f"output size: {output_height}, {output_width}")


# Example usage with the provided data (assuming 'task' variable holds the task data)
# for example in task['train']:
#  report(np.array(example['input']), np.array(example['output']), transform(np.array(example['input'])))