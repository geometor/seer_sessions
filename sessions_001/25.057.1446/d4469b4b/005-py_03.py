def analyze_results(task):
    print(f"Task: {task['name']}")
    correct_count = 0
    total_count = 0

    for example in task['train']:
        input_grid = example['input']
        expected_output_grid = example['output']
        predicted_output_grid = transform(input_grid)
        total_count += 1

        if predicted_output_grid == expected_output_grid:
            correct_count += 1
            print(f"  Example {total_count}: Correct")
        else:
            print(f"  Example {total_count}: Incorrect")
            print(f"    Input:\n{np.array(input_grid)}")
            print(f"    Expected Output:\n{np.array(expected_output_grid)}")
            print(f"    Predicted Output:\n{np.array(predicted_output_grid)}")


    print(f"  Accuracy: {correct_count}/{total_count} = {correct_count / total_count:.2f}\n")

task = {
    "name": "Example Task",
    "train": [
       {
            "input": [[0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 2, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0]],
            "output": [[0, 0, 0, 0], [0, 0, 5, 0], [0, 0, 0, 0]]
        },
        {
            "input": [[0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 2, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0]],
            "output": [[0, 0, 0, 0, 0, 0], [0, 0, 5, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0]]
        },
        {
            "input": [[0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 2, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0]],
            "output": [[0, 0, 0, 0, 0, 0], [0, 0, 5, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0]]
        },
        {
            "input": [[0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 2, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0]],
            "output": [[0, 0, 0, 0], [5, 0, 0, 0], [0, 0, 0, 0]]
        },
		{
            "input":  [[1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1], [1, 1, 1, 2, 1, 1], [1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1]],
            "output": [[1, 1, 1, 1], [1, 1, 5, 1], [1, 1, 1, 1]]
        }
    ]
}
analyze_results(task)