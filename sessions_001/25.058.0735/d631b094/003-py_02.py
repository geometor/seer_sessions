import numpy as np

def analyze_examples(task):
    print(f"Task: {task['name']}")
    for i, example in enumerate(task['train']):
        input_grid = np.array(example['input'])
        output_grid = np.array(example['output'])
        predicted_output = transform(input_grid)  # Use the original transform function

        print(f"  Example {i+1}:")
        print(f"    Input shape: {input_grid.shape}")
        print(f"    Output shape: {output_grid.shape}")
        print(f"    Predicted output shape: {predicted_output.shape}")
        print(f"    Input blue count: {np.count_nonzero(input_grid == 1)}")
        print(f"    Output blue count: {np.count_nonzero(output_grid == 1)}")
        print(f"    Predicted output blue count: {np.count_nonzero(predicted_output == 1)}")
        print(f"    Input non-zero count: {np.count_nonzero(input_grid)}")
        print(f"    Output non-zero count: {np.count_nonzero(output_grid)}")

        # Check if the prediction is correct
        is_correct = np.array_equal(output_grid, predicted_output)
        print(f"    Prediction correct: {is_correct}")
        if not is_correct:
          print(f"    Differences: {np.where(output_grid != predicted_output)}")

# Example dummy task data (replace with actual task data)
example_task = {
    'name': 'Example Task',
    'train': [
        {'input': [[0, 1, 0], [0, 1, 0], [0, 1, 0]], 'output': [[1, 1, 1]]},
        {'input': [[0, 0, 0], [1, 1, 1], [0, 0, 0]], 'output': [[1, 1, 1]]},
        {'input': [[0, 0, 0], [0, 0, 0], [0, 0, 0]], 'output': [[0]]},
        {'input': [[1, 0, 0], [0, 1, 0], [0, 0, 1]], 'output' : [[1,1,1]]},
    ]
}

analyze_examples(example_task)