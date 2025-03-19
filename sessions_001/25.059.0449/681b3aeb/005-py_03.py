def check_transform(task):
    print(f"Task: {task['name']}")
    correct_count = 0
    for example in task['train']:
        input_grid = np.array(example['input'])
        expected_output = np.array(example['output'])
        predicted_output = transform(input_grid)
        
        objects = get_objects(input_grid)
        print(f"  Example:")
        print(f"    Input:\n{input_grid}")
        print(f"    Objects: {objects}")
        print(f"    Expected Output:\n{expected_output}")
        print(f"    Predicted Output:\n{predicted_output}")

        if np.array_equal(predicted_output, expected_output):
            correct_count += 1
            print("    Correct")
        else:
            print("    Incorrect")

    print(f"  Correct: {correct_count}/{len(task['train'])}")
    print("-" * 20)

# Assuming 'task' variable holds the current ARC task data
check_transform(task)