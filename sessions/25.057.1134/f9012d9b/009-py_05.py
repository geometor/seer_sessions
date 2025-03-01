def analyze_example(input_grid, expected_output, actual_output):
    unique_values, counts = np.unique(input_grid, return_counts=True)
    value_counts = dict(zip(unique_values, counts))
    expected_value = expected_output.item() if expected_output.size == 1 else None
    actual_value = actual_output.item() if actual_output.size == 1 else None
    match = np.array_equal(expected_output, actual_output)

    print(f"  Unique Values: {unique_values}")
    print(f"  Value Counts: {value_counts}")
    print(f"  Expected Output: {expected_value}, Actual Output: {actual_value}, Match: {match}")

task_data = task.get("train")
for i, example in enumerate(task_data):
    input_grid = example.get('input')
    output_grid = example.get('output')
    print(f"Example {i+1}:")
    input_np = np.array(input_grid)
    output_np = np.array(output_grid)

    
    actual_output_np = transform(input_np) #your previous transform function
    analyze_example(input_np, output_np, actual_output_np)