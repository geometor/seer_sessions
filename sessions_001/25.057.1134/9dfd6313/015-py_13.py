import numpy as np

def calculate_accuracy(expected, actual):
    """Calculates the accuracy of the transformation."""
    if expected.shape != actual.shape:
        return 0.0  # Incompatible shapes
    return np.mean(expected == actual)

def show_diff(expected, actual):
  return np.where(expected == actual, 0, actual)

def analyze_results(task):
    print(f"Analyzing Task: {task['task_name']}")
    for i, example in enumerate(task['train']):
        input_grid = np.array(example['input'])
        expected_output = np.array(example['output'])
        actual_output = transform(input_grid)
        accuracy = calculate_accuracy(expected_output, actual_output)

        print(f"  Example {i + 1}:")
        print(f"    Input:\n{input_grid}")
        print(f"    Expected Output:\n{expected_output}")
        print(f"    Actual Output:\n{actual_output}")
        print(f"    diff:\n{show_diff(expected_output,actual_output)}")
        print(f"    Accuracy: {accuracy:.4f}")
        
# Dummy task for demonstration - replace with your actual task data

task1 = {
    'task_name': 'Example Task 1',
    'train': [
        {'input': [[0, 0, 0, 0, 0, 0, 0],
                   [0, 0, 0, 7, 0, 0, 0],
                   [0, 0, 0, 5, 0, 0, 0],
                   [0, 0, 7, 7, 7, 0, 0],
                   [0, 0, 0, 5, 0, 0, 0],
                   [0, 0, 0, 7, 0, 0, 0],
                   [0, 0, 0, 0, 0, 0, 0]],
         'output': [[0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 7, 0, 0, 0],
                    [0, 0, 0, 5, 0, 0, 0],
                    [0, 0, 7, 7, 7, 0, 0],
                    [0, 0, 0, 5, 0, 0, 0],
                    [0, 0, 0, 7, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0]]},
    ]
}
task2 = {
    'task_name': 'Example Task 2',
     'train': [
      {'input': [[0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 7, 0, 0, 0], [0, 0, 0, 5, 0, 0, 0], [0, 0, 7, 7, 7, 0, 0], [0, 0, 0, 5, 0, 0, 0], [0, 0, 0, 7, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0]], 'output': [[0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 7, 0, 0, 0], [0, 0, 0, 5, 0, 0, 0], [0, 0, 7, 7, 7, 0, 0], [0, 0, 0, 5, 0, 0, 0], [0, 0, 0, 7, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0]]},
      {'input': [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 4], [0, 0, 0, 0, 0, 5, 0, 0, 0, 0, 4, 4], [0, 0, 0, 0, 0, 5, 5, 5, 0, 0, 4, 4], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]], 'output': [[0, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 4], [0, 0, 0, 0, 0, 5, 0, 0, 0, 0, 4, 4], [0, 0, 0, 0, 0, 5, 5, 5, 0, 0, 4, 4], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]},
      {'input': [[0, 0, 0, 5, 0, 0, 0, 0, 0], [0, 0, 0, 5, 0, 0, 0, 0, 0], [0, 0, 0, 5, 2, 0, 0, 0, 0], [0, 0, 0, 5, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0]], 'output': [[0, 0, 0, 5, 0, 0, 0, 0, 0], [0, 0, 0, 5, 0, 0, 0, 0, 0], [0, 0, 0, 5, 2, 0, 0, 0, 0], [0, 0, 0, 5, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0]]},
      {'input': [[0, 0, 0, 0, 5, 0, 0, 0, 0], [0, 0, 0, 5, 5, 0, 0, 0, 0], [0, 2, 0, 0, 5, 0, 0, 0, 0], [0, 0, 0, 0, 5, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0]], 'output': [[0, 0, 0, 0, 5, 0, 0, 0, 0], [0, 0, 0, 5, 5, 0, 0, 0, 0], [0, 2, 0, 0, 5, 0, 0, 0, 0], [0, 0, 0, 0, 5, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0]]}
     ]
    }

analyze_results(task1)
analyze_results(task2)
