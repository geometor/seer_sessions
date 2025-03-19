def analyze_results(task):
    correct_count = 0
    print(f"Task: {task['name']}")
    for example in task['train']:
        input_grid = example['input']
        expected_output = example['output']
        predicted_output = transform(input_grid)

        if np.array_equal(predicted_output, expected_output):
            correct_count += 1
            print(f"  Example {example['index']} - PASS")
        else:
            print(f"  Example {example['index']} - FAIL")
            print(f"    Input: {np.array(input_grid).shape} - {input_grid}")
            print(f"    Expected Output: {np.array(expected_output).shape} - {expected_output}")
            print(f"    Predicted Output: {np.array(predicted_output).shape} - {predicted_output}")
    print(f"  Passed {correct_count} of {len(task['train'])} examples")

# Assuming 'task' variable is loaded with the current task data
analyze_results(task)

