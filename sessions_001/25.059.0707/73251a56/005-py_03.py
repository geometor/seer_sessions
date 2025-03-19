def analyze_results(task_data):
    results = {}
    for task_type in ['train', 'test']:
        results[task_type] = []
        for i, example in enumerate(task_data[task_type]):
            input_grid = example['input']
            expected_output = example['output']
            
            # Predict output using the transform function (from the problem description)
            predicted_output = transform(np.array(input_grid))

            # convert to list for comparison
            predicted_output = predicted_output.tolist()

            # Compare predicted and expected outputs
            is_correct = (predicted_output == expected_output)
            mismatched_pixels = []
            if not is_correct:
                for row_idx, (pred_row, exp_row) in enumerate(zip(predicted_output, expected_output)):
                    for col_idx, (pred_pixel, exp_pixel) in enumerate(zip(pred_row, exp_row)):
                        if pred_pixel != exp_pixel:
                            mismatched_pixels.append(((row_idx, col_idx), pred_pixel, exp_pixel))

            results[task_type].append({
                'example_index': i,
                'is_correct': is_correct,
                'mismatched_pixels': mismatched_pixels,
            })

    return results
task_data_str = """
{'train': [{'input': [[0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0]], 'output': [[6, 6, 6, 6, 6, 6, 6, 6, 6], [6, 6, 6, 6, 6, 6, 6, 6, 6], [6, 6, 6, 6, 6, 6, 6, 6, 6], [6, 6, 6, 6, 6, 6, 6, 6, 6], [6, 6, 6, 6, 6, 6, 6, 6, 6], [6, 6, 6, 6, 6, 6, 6, 6, 6]]}, {'input': [[0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 4, 4, 4, 4, 4, 4, 4, 0], [0, 4, 0, 0, 0, 0, 0, 4, 0], [0, 4, 0, 0, 0, 0, 0, 4, 0], [0, 4, 4, 4, 4, 0, 4, 4, 0], [0, 4, 0, 0, 0, 0, 0, 4, 0], [0, 4, 0, 0, 0, 0, 0, 4, 0], [0, 4, 4, 4, 4, 4, 4, 4, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0]], 'output': [[6, 6, 6, 6, 6, 6, 6, 6, 6], [6, 4, 4, 4, 4, 4, 4, 4, 6], [6, 4, 6, 6, 6, 6, 6, 4, 6], [6, 4, 6, 6, 6, 6, 6, 4, 6], [6, 4, 4, 4, 4, 6, 4, 4, 6], [6, 4, 6, 6, 6, 6, 6, 4, 6], [6, 4, 6, 6, 6, 6, 6, 4, 6], [6, 4, 4, 4, 4, 4, 4, 4, 6], [6, 6, 6, 6, 6, 6, 6, 6, 6]]}, {'input': [[0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 5, 5, 0, 0, 0], [0, 0, 5, 5, 5, 5, 0, 0], [0, 0, 5, 5, 5, 5, 0, 0], [0, 0, 0, 5, 5, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0]], 'output': [[6, 6, 6, 6, 6, 6, 6, 6], [6, 6, 6, 5, 5, 6, 6, 6], [6, 6, 5, 5, 5, 5, 6, 6], [6, 6, 5, 5, 5, 5, 6, 6], [6, 6, 6, 5, 5, 6, 6, 6], [6, 6, 6, 6, 6, 6, 6, 6]]}, {'input': [[0, 0, 0, 0, 0, 0, 0], [0, 3, 3, 3, 3, 3, 0], [0, 3, 3, 3, 3, 3, 0], [0, 3, 3, 3, 3, 3, 0], [0, 3, 3, 3, 3, 3, 0], [0, 0, 0, 0, 0, 0, 0]], 'output': [[6, 6, 6, 6, 6, 6, 6], [6, 3, 3, 3, 3, 3, 6], [6, 3, 3, 3, 3, 3, 6], [6, 3, 3, 3, 3, 3, 6], [6, 3, 3, 3, 3, 3, 6], [6, 6, 6, 6, 6, 6, 6]]}], 'test': [{'input': [[0, 0, 0, 0, 0, 0], [0, 0, 1, 1, 0, 0], [0, 1, 1, 1, 1, 0], [0, 1, 1, 1, 1, 0], [0, 0, 1, 1, 0, 0], [0, 0, 0, 0, 0, 0]], 'output': [[6, 6, 6, 6, 6, 6], [6, 6, 1, 1, 6, 6], [6, 1, 1, 1, 1, 6], [6, 1, 1, 1, 1, 6], [6, 6, 1, 1, 6, 6], [6, 6, 6, 6, 6, 6]]}]}
"""
import json
task_data = json.loads(task_data_str)
analysis = analyze_results(task_data)
print(json.dumps(analysis, indent=2))