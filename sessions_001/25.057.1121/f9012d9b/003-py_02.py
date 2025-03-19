def analyze_example(example):
    input_grid = example['input']
    expected_output_grid = example['output']
    predicted_output_grid = transform(input_grid)

    input_np = np.array(input_grid)
    expected_output_np = np.array(expected_output_grid)
    predicted_output_np = np.array(predicted_output_grid)

    input_shapes = input_np.shape
    output_shapes = expected_output_np.shape

    match = np.array_equal(expected_output_np, predicted_output_np)

    input_colors = np.unique(input_np)
    expected_output_colors = np.unique(expected_output_np)

    print(f"  Input: {input_shapes}, Colors: {input_colors}")
    print(f"  Output: {output_shapes}, Colors: {expected_output_colors}")
    print(f"  Prediction Matches Expected: {match}")

task_data = task
print(f"Task: {task_data['name']}")
for i, example in enumerate(task_data['train']):
    print(f"Example {i + 1}:")
    analyze_example(example)
