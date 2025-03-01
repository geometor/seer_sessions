import numpy as np

def analyze_examples(task_data):
    results = []
    for example in task_data['train']:
        input_grid = np.array(example['input'])
        output_grid = np.array(example['output'])
        predicted_output = transform(input_grid)  # Assuming 'transform' function is defined elsewhere
        correct = np.array_equal(predicted_output, output_grid)

        metrics = {
            'example_id': example.get('id', 'N/A'), #use id if it is available
            'correct': correct,
            'input_shape': input_grid.shape,
            'output_shape': output_grid.shape,
            'contains_magenta_input': np.any(input_grid == 6),
            'contains_azure_input': np.any(input_grid == 8),
            'contains_magenta_output': np.any(output_grid == 6),
            'contains_azure_output': np.any(output_grid == 8),
             'predicted_eq_output': np.array_equal(predicted_output,output_grid)
        }
        results.append(metrics)
    return results
from arc import ArcTask
task = ArcTask(task_id='6b6b767a')
task_data = task.task_data
analysis_results = analyze_examples(task_data)

for result in analysis_results:
    print(result)
