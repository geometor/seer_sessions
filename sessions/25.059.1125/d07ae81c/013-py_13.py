import numpy as np

def analyze_results(task):
    print(f"Task: {task['name']}")
    correct_count = 0
    for i, example in enumerate(task['train']):
        input_grid = np.array(example['input'])
        expected_output = np.array(example['output'])
        predicted_output = transform(input_grid)  # Assuming 'transform' function is available
        is_correct = np.array_equal(predicted_output, expected_output)
        correct_count += is_correct
        print(f"  Example {i + 1}: {'Correct' if is_correct else 'Incorrect'}")
        if not is_correct:
          print(f"expected:\n{expected_output}\npredicted:\n{predicted_output}")

    print(f"Correct Examples: {correct_count} / {len(task['train'])} \n--------")

# Example Usage (replace with actual task data)
task1 = {
    'name': 'Example Task 1',
    'train': [
       {'input': [[0, 1, 0, 0, 0, 0, 0, 0, 0, 0], [1, 1, 1, 1, 1, 1, 1, 1, 8, 0], [0, 1, 0, 0, 0, 0, 0, 0, 0, 0], [0, 1, 1, 1, 1, 1, 1, 1, 0, 0], [0, 1, 0, 0, 0, 0, 1, 0, 0, 0], [0, 2, 0, 0, 0, 0, 1, 0, 0, 0], [0, 1, 0, 0, 0, 0, 1, 0, 0, 0], [0, 1, 1, 1, 1, 1, 1, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]], 'output': [[0, 1, 0, 0, 0, 0, 0, 0, 0, 0], [1, 1, 1, 1, 1, 1, 1, 8, 8, 0], [0, 1, 0, 0, 0, 0, 0, 0, 0, 0], [0, 1, 1, 1, 1, 1, 1, 1, 0, 0], [0, 2, 0, 0, 0, 0, 1, 0, 0, 0], [2, 2, 2, 0, 0, 0, 1, 0, 0, 0], [0, 2, 0, 0, 0, 0, 1, 0, 0, 0], [0, 1, 1, 1, 1, 1, 1, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]},
       {'input': [[0, 0, 0, 0, 1, 0, 0, 0, 0, 0], [0, 0, 0, 1, 1, 1, 0, 0, 0, 0], [0, 0, 1, 1, 1, 1, 1, 0, 0, 0], [0, 1, 1, 1, 1, 1, 1, 1, 0, 0], [0, 0, 1, 1, 2, 1, 1, 0, 0, 0], [0, 0, 0, 1, 1, 1, 0, 0, 0, 0], [0, 0, 0, 0, 1, 0, 0, 0, 8, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]], 'output': [[0, 0, 0, 0, 1, 0, 0, 0, 0, 0], [0, 0, 0, 1, 1, 1, 0, 0, 0, 0], [0, 0, 1, 1, 1, 1, 1, 0, 0, 0], [0, 1, 1, 1, 2, 1, 1, 1, 0, 0], [0, 0, 1, 2, 2, 2, 1, 0, 0, 0], [0, 0, 0, 1, 2, 1, 0, 0, 0, 0], [0, 0, 0, 0, 1, 0, 0, 0, 8, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]},
       {'input': [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 8, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 1, 1, 0, 0, 0, 0], [0, 0, 0, 1, 1, 1, 1, 0, 0, 0], [0, 0, 1, 1, 1, 1, 1, 1, 0, 0], [0, 0, 0, 1, 2, 1, 1, 0, 0, 0], [0, 0, 0, 0, 1, 1, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]], 'output': [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 8, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 1, 1, 0, 0, 0, 0], [0, 0, 0, 1, 1, 1, 1, 0, 0, 0], [0, 0, 1, 1, 2, 1, 1, 1, 0, 0], [0, 0, 0, 1, 2, 2, 1, 0, 0, 0], [0, 0, 0, 0, 1, 1, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]}
    ]
}

analyze_results(task1)
