import numpy as np
from collections import Counter

def analyze_results(task):
    print(f"Task: {task['name']}")
    for i, example in enumerate(task['train']):
        input_grid = np.array(example['input'])
        expected_output = np.array(example['output'])
        predicted_output = transform(input_grid)  # Using the provided transform function
        
        if not np.array_equal(predicted_output, expected_output):
            print(f"  Example {i+1} - Mismatch:")
            
            # Color frequencies in input
            input_colors = Counter(input_grid.flatten())
            print(f"    Input Colors: {input_colors}")

            # Color frequencies in expected output
            expected_output_colors = Counter(expected_output.flatten())
            print(f"    Expected Output Colors: {expected_output_colors}")

            # Color frequencies in predicted output
            predicted_output_colors = Counter(predicted_output.flatten())
            print(f"   Predicted Output Colors: {predicted_output_colors}")
            
            diff = predicted_output != expected_output
            print(f"  Differences at (row, col): {np.transpose(np.where(diff))}")

        else:
            print(f"  Example {i+1} - Match")
    print("-" * 20)

# Mock task data for demonstration (replace with actual task data)
mock_task = {
    'name': 'Mock Task',
    'train': [
      {'input': [[0, 1, 2], [0, 2, 1], [0, 1, 2]], 'output': [[0, 2, 1], [0, 1, 2], [0, 2, 1]]},  # Example 1 (swap 1 and 2)
      {'input': [[5, 5, 5, 5], [5, 1, 1, 5], [5, 1, 3, 5], [5, 5, 5, 5]], 'output': [[5, 5, 5, 5], [5, 3, 3, 5], [5, 3, 1, 5], [5, 5, 5, 5]]}, # Example 2 (swap 1 and 3, bg=5)
      {'input': [[1, 1, 1, 1], [1, 0, 0, 1], [1, 0, 0, 1], [1, 1, 1, 1]], 'output': [[1, 1, 1, 1], [1, 0, 0, 1], [1, 0, 0, 1], [1, 1, 1, 1]]},  # Example 3 (no change, only 0 and 1)
    ]
}

analyze_results(mock_task)