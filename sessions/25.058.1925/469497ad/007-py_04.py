import numpy as np

def analyze_examples(task_data):
    results = []
    for example in task_data['train']:
        input_grid = np.array(example['input'])
        output_grid = np.array(example['output'])

        input_height, input_width = input_grid.shape
        output_height, output_width = output_grid.shape

        # Find Azure objects and determine their size
        azure_objects = np.array(np.where(output_grid == 8)).T
        if azure_objects.size > 0:  # Check if the array is not empty
           azure_height = np.max(azure_objects[:, 0]) - np.min(azure_objects[:, 0]) + 1
           azure_width = np.max(azure_objects[:, 1]) - np.min(azure_objects[:, 1]) + 1
        else:
          azure_height = 0
          azure_width = 0

        # Find Green objects and determine "border" size
        green_objects = np.array(np.where(output_grid == 3)).T
        if green_objects.size > 0:
            green_height = np.max(green_objects[:, 0]) - np.min(green_objects[:, 0]) + 1
            green_width = np.max(green_objects[:, 1]) - np.min(green_objects[:, 1]) + 1
        else:
            green_height = 0
            green_width = 0

        results.append({
            'input_shape': (input_height, input_width),
            'output_shape': (output_height, output_width),
            'azure_shape': (azure_height, azure_width),
            'green_shape':(green_height, green_width)
        })
    return results

# Assuming 'task' is a dictionary containing the ARC task data
# For demonstration purposes, let's create a sample 'task'
task = {
    'train': [
        {'input': [[0, 0], [0, 0]], 'output': [[2, 0, 0, 2], [0, 3, 3, 0], [0, 3, 3, 0], [2, 0, 0, 2]]},
        {'input': [[0, 0, 0]], 'output': [[2, 0, 0, 0, 2], [0, 3, 3, 3, 0], [0, 3, 8, 3, 0], [0, 3, 3, 3, 0], [2, 0, 0, 0, 2]]},
        {'input': [[0], [0], [0]], 'output': [[2, 0, 2], [0, 3, 0], [0, 8, 0], [0, 3, 0], [2, 0, 2]]}
    ]
}

analysis_results = analyze_examples(task)
print(analysis_results)
