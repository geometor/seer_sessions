def report(task):
    correct_count = 0
    for example in task['train']:
        input_grid = example['input']
        expected_output = example['output']
        actual_output = transform(input_grid)
        if actual_output.tolist() == expected_output:
            correct_count += 1
            print(f"Example: Correct")
        else:
            print(f"Example: Incorrect")
            print(f"  Input: {input_grid}")
            print(f"  Expected Output: {expected_output}")
            print(f"  Actual Output: {actual_output.tolist()}")  # Convert to list for easy comparison
    print ("\nSummary of Results:")
    print (f"{correct_count} of {len(task['train'])} example transformations are correct")
report(task)
