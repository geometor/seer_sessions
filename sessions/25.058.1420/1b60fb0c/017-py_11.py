import numpy as np

def analyze_results(task_data):
    results = []
    for example in task_data['train']:
        input_grid = np.array(example['input'])
        output_grid = np.array(example['output'])
        predicted_output = transform(input_grid)  # using previous transform function

        correct_pixels = np.sum(predicted_output == output_grid)
        total_pixels = output_grid.size
        accuracy = correct_pixels / total_pixels

        diff = predicted_output - output_grid
        false_positives = np.sum(diff > 0)  # Predicted red where it shouldn't be
        false_negatives = np.sum(diff < 0)  # Didn't predict red where it should have
        results.append({
            'input_shape': input_grid.shape,
            'output_shape': output_grid.shape,
            'accuracy': accuracy,
            'false_positives': false_positives,
            'false_negatives': false_negatives,
            'predicted_output' : predicted_output.tolist(),
            'diff' : diff.tolist()
        })
    return results

# dummy task data for demonstration and to avoid errors in the report
# real task data will be inserted during actual processing of the notebook
dummy_task_data = {
'train': [
    {
        'input': [[0, 0, 0, 1], [0, 0, 0, 1]],
        'output': [[2, 0, 0, 1], [2, 0, 0, 1]]
    },
    {
        'input': [[0, 0, 1, 0, 0, 0], [0, 1, 0, 0, 0, 0]],
        'output': [[2, 0, 1, 0, 0, 0], [2, 1, 0, 0, 0, 0]]
    },
    {
       'input' : [[0,1,0,0,0,0,1],[0,0,0,0,0,0,0]],
       'output': [[2,1,0,0,0,2,1],[0,0,0,0,0,0,0]]
    }
]
}
analysis = analyze_results(dummy_task_data)

#display_analysis(analysis) # for notebook display

# build string output for report
report_str = ""
i = 1
for a in analysis:
    report_str += f"Example {i}:\n"
    report_str += f"  Input Shape: {a['input_shape']}\n"
    report_str += f"  Output Shape: {a['output_shape']}\n"
    report_str += f"  Accuracy: {a['accuracy']:.2f}\n"
    report_str += f"  False Positives: {a['false_positives']}\n"
    report_str += f"  False Negatives: {a['false_negatives']}\n"
    report_str += f"  Predicted Output:\n"
    for row in a['predicted_output']:
        report_str += f"  {row}\n"
    report_str += f"  Diff:\n"
    for row in a['diff']:
        report_str += f"  {row}\n"        
    i+=1

print(report_str)