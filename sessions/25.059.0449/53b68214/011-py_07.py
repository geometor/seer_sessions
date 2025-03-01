def analyze_results(task):
    print(f"Task: {task['name']}")
    correct_count = 0
    for i, example in enumerate(task['train']):
        input_grid = np.array(example['input'])
        expected_output = np.array(example['output'])
        predicted_output = transform(input_grid)
        
        is_correct = np.array_equal(predicted_output, expected_output)
        if is_correct: correct_count += 1

        print(f"  Example {i + 1}: {'Correct' if is_correct else 'Incorrect'}")
        if not is_correct:
            print(f"    Input grid shape: {input_grid.shape}")
            print(f"    Expected output shape: {expected_output.shape}")
            print(f"    Predicted output shape: {predicted_output.shape}")

            # check differences between individual values
            diff = predicted_output == expected_output
            print(f"    Differences: {np.sum(~diff)} cells differ")
            if not np.array_equal(predicted_output.shape, expected_output.shape):
                print("Shapes are different, not printing differences")
            else:
                for row in range(expected_output.shape[0]):
                    for col in range(expected_output.shape[1]):
                        if not diff[row,col]:
                            print(f"      [{row},{col}] expected: {expected_output[row,col]}, got: {predicted_output[row,col]}")

    print(f"Correct examples: {correct_count}/{len(task['train'])}")

task = {
    "name": "Example Task",
    "train": [
        {
            "input": [[0, 0, 3, 0, 0, 0, 0, 0, 0], [0, 0, 3, 0, 0, 0, 0, 0, 0], [0, 0, 3, 0, 0, 0, 0, 0, 0]],
            "output": [[0, 0, 3, 0, 0, 0, 0, 0, 0], [0, 0, 3, 0, 0, 0, 0, 0, 0], [0, 0, 3, 0, 0, 0, 0, 0, 0], [0, 0, 3, 0, 0, 0, 0, 0, 0], [0, 0, 3, 0, 0, 0, 0, 0, 0], [0, 0, 3, 0, 0, 0, 0, 0, 0]],
        },
        {
            "input": [[0, 0, 3, 0, 0, 0], [0, 0, 3, 0, 0, 0], [0, 0, 3, 0, 0, 0], [0, 0, 3, 0, 0, 0]],
            "output": [[0, 0, 3, 0, 0, 0], [0, 0, 3, 0, 0, 0], [0, 0, 3, 0, 0, 0], [0, 0, 3, 0, 0, 0], [0, 0, 3, 0, 0, 0], [0, 0, 3, 0, 0, 0], [0, 0, 3, 0, 0, 0], [0, 0, 3, 0, 0, 0]],
        },
        {
            "input": [[0, 0, 3, 0, 0], [0, 0, 3, 0, 0], [0, 0, 3, 0, 0], [0, 0, 3, 0, 0], [0, 0, 3, 0, 0]],
            "output": [[0, 0, 3, 0, 0], [0, 0, 3, 0, 0], [0, 0, 3, 0, 0], [0, 0, 3, 0, 0], [0, 0, 3, 0, 0], [0, 0, 3, 0, 0], [0, 0, 3, 0, 0], [0, 0, 3, 0, 0], [0, 0, 3, 0, 0], [0, 0, 3, 0, 0]],
        },
    ],
        "test": [
        {
            "input": [[0, 0, 3, 0], [0, 0, 3, 0], [0, 0, 3, 0]],
            "output": [[0, 0, 3, 0], [0, 0, 3, 0], [0, 0, 3, 0], [0, 0, 3, 0], [0, 0, 3, 0], [0, 0, 3, 0]]
        }
    ]

}
analyze_results(task)
import numpy as np
