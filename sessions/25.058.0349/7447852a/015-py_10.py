import numpy as np
from collections import Counter

def analyze_result(input, output, prediction):
    results = {}
    results['input_color_count'] =  dict(Counter(input.flatten()))
    results['output_color_count'] = dict(Counter(output.flatten()))
    results['prediction_color_count'] = dict(Counter(prediction.flatten()))
    results['correct'] = np.array_equal(output, prediction)
    return results

#dummy data for demonstration
input_grid = np.array([[0, 2, 0], [2, 0, 5], [0, 0, 2]])
expected_output = np.array([[0, 2, 4], [2, 4, 5], [0, 0, 2]])
predicted_output = transform(input_grid)

analysis_results = analyze_result(input_grid, expected_output, predicted_output)
print(analysis_results)


task_data = {
    'train': [
        {
            'input': np.array([[8, 0, 8, 0, 8, 0, 8, 0],
       [0, 5, 0, 5, 0, 5, 0, 5],
       [8, 0, 8, 0, 8, 0, 8, 0],
       [0, 5, 0, 5, 0, 5, 0, 5],
       [8, 0, 8, 0, 8, 0, 8, 0],
       [0, 5, 0, 5, 0, 5, 0, 5],
       [8, 0, 8, 0, 8, 0, 8, 0],
       [0, 5, 0, 5, 0, 5, 0, 5]]),
            'output': np.array([[8, 0, 8, 0, 8, 0, 8, 0],
       [0, 5, 0, 5, 0, 5, 0, 5],
       [8, 0, 8, 0, 8, 0, 8, 0],
       [0, 5, 0, 5, 0, 5, 0, 5],
       [8, 0, 8, 0, 8, 0, 8, 0],
       [0, 5, 0, 5, 0, 5, 0, 5],
       [8, 0, 8, 0, 8, 0, 8, 0],
       [0, 5, 0, 5, 0, 5, 0, 5]])
        },
        {
            'input': np.array([[8, 0, 8, 0, 8, 0, 8, 0, 8],
       [0, 2, 0, 5, 0, 5, 0, 5, 0],
       [8, 0, 8, 0, 8, 0, 8, 0, 8],
       [0, 5, 0, 2, 0, 5, 0, 5, 0],
       [8, 0, 8, 0, 8, 0, 8, 0, 8],
       [0, 5, 0, 5, 0, 2, 0, 5, 0],
       [8, 0, 8, 0, 8, 0, 8, 0, 8],
       [0, 5, 0, 5, 0, 5, 0, 2, 0],
       [8, 0, 8, 0, 8, 0, 8, 0, 8]]),
            'output': np.array([[8, 0, 8, 0, 8, 0, 8, 0, 8],
       [0, 2, 4, 5, 0, 5, 0, 5, 0],
       [8, 4, 8, 0, 8, 0, 8, 0, 8],
       [0, 5, 0, 2, 4, 5, 0, 5, 0],
       [8, 0, 8, 4, 8, 0, 8, 0, 8],
       [0, 5, 0, 5, 0, 2, 4, 5, 0],
       [8, 0, 8, 0, 8, 4, 8, 0, 8],
       [0, 5, 0, 5, 0, 5, 0, 2, 4],
       [8, 0, 8, 0, 8, 0, 8, 4, 8]])
        },
		{
            'input': np.array([[8, 0, 8, 0, 8, 0, 8, 0, 8],
       [0, 5, 0, 5, 0, 5, 0, 2, 0],
       [8, 0, 8, 0, 8, 0, 8, 0, 8],
       [0, 2, 0, 5, 0, 5, 0, 5, 0],
       [8, 0, 8, 0, 8, 0, 8, 0, 8],
       [0, 5, 0, 2, 0, 5, 0, 5, 0],
       [8, 0, 8, 0, 8, 0, 8, 0, 8],
       [0, 5, 0, 5, 0, 2, 0, 5, 0],
       [8, 0, 8, 0, 8, 0, 8, 0, 8]]),
            'output': np.array([[8, 0, 8, 0, 8, 0, 8, 0, 8],
       [0, 5, 0, 5, 0, 5, 0, 2, 4],
       [8, 0, 8, 0, 8, 0, 8, 4, 8],
       [0, 2, 4, 5, 0, 5, 0, 5, 0],
       [8, 4, 8, 0, 8, 0, 8, 0, 8],
       [0, 5, 0, 2, 4, 5, 0, 5, 0],
       [8, 0, 8, 4, 8, 0, 8, 0, 8],
       [0, 5, 0, 5, 0, 2, 4, 5, 0],
       [8, 0, 8, 0, 8, 4, 8, 0, 8]])
        },
        {
            'input': np.array([[2, 0, 2, 0, 2, 0, 2, 0],
                [0, 5, 0, 5, 0, 5, 0, 5],
                [2, 0, 2, 0, 2, 0, 2, 0],
                [0, 5, 0, 5, 0, 5, 0, 5],
                [2, 0, 2, 0, 2, 0, 2, 0],
                [0, 5, 0, 5, 0, 5, 0, 5],
                [2, 0, 2, 0, 2, 0, 2, 0],
                [0, 5, 0, 5, 0, 5, 0, 5]]),
            'output': np.array([[2, 4, 2, 4, 2, 4, 2, 4],
                [4, 5, 4, 5, 4, 5, 4, 5],
                [2, 4, 2, 4, 2, 4, 2, 4],
                [4, 5, 4, 5, 4, 5, 4, 5],
                [2, 4, 2, 4, 2, 4, 2, 4],
                [4, 5, 4, 5, 4, 5, 4, 5],
                [2, 4, 2, 4, 2, 4, 2, 4],
                [4, 5, 4, 5, 4, 5, 4, 5]])
        }

    ]
}
results = []
for example in task_data['train']:
    input_grid = example['input']
    expected_output = example['output']
    predicted_output = transform(input_grid)
    analysis_results = analyze_result(input_grid, expected_output, predicted_output)
    results.append(analysis_results)
print(results)
