import numpy as np

def analyze_results(task):
    print(f"Task: {task['name']}")
    for i, example in enumerate(task['train']):
        input_grid = np.array(example['input'])
        expected_output = np.array(example['output'])
        predicted_output = transform(input_grid)

        print(f"  Example {i + 1}:")
        print(f"    Input shape: {input_grid.shape}")
        print(f"    Expected output shape: {expected_output.shape}")
        print(f"    Predicted output shape: {predicted_output.shape}")

        if predicted_output.size > 0:  # Avoid errors if predicted output is empty
            print(f"    Correct pixels: {np.sum(predicted_output == expected_output)}")
            print(f"    Total pixels in expected: {expected_output.size}")
            print(f"    Accuracy: {np.sum(predicted_output == expected_output) / expected_output.size:.2f}" if expected_output.size>0 else "N/A")
        else:
            print("    Predicted output is empty.")

        print(f"    Expected output: {expected_output}")
        print(f"    Predicted output:\n{predicted_output}")

# assemble ARC data
task1 = {
    "name": "Task 1",
    "train": [
        {
            "input": [[5, 0, 5, 0, 5, 0, 5, 0], [0, 4, 0, 4, 0, 4, 0, 4], [5, 0, 5, 0, 5, 0, 5, 0], [0, 4, 0, 4, 0, 4, 0, 4], [5, 0, 5, 0, 5, 0, 5, 0], [0, 4, 0, 4, 0, 4, 0, 4], [5, 0, 5, 0, 5, 0, 5, 0], [0, 4, 0, 4, 0, 4, 0, 4]],
            "output": [[5, 0, 5, 0], [0, 4, 0, 4], [5, 0, 5, 0], [0, 4, 0, 4]]
        },
        {
            "input": [[5, 0, 5, 0, 5, 0, 5, 0, 5, 0, 5, 0, 5, 0, 5], [0, 4, 0, 4, 0, 4, 0, 4, 0, 4, 0, 4, 0, 4, 0], [5, 0, 5, 0, 5, 0, 5, 0, 5, 0, 5, 0, 5, 0, 5], [0, 4, 0, 4, 0, 4, 0, 4, 0, 4, 0, 4, 0, 4, 0], [5, 0, 5, 0, 5, 0, 5, 0, 5, 0, 5, 0, 5, 0, 5], [0, 4, 0, 4, 0, 4, 0, 4, 0, 4, 0, 4, 0, 4, 0]],
            "output": [[5, 0, 5, 0, 5, 0, 5], [0, 4, 0, 4, 0, 4, 0], [5, 0, 5, 0, 5, 0, 5], [0, 4, 0, 4, 0, 4, 0]]
        },
        {
            "input": [[5, 0, 5, 0, 5, 0], [0, 4, 0, 4, 0, 4], [5, 0, 5, 0, 5, 0], [0, 4, 0, 4, 0, 4]],
            "output": [[5, 0, 5], [0, 4, 0]]
        }
    ]
}

analyze_results(task1)
