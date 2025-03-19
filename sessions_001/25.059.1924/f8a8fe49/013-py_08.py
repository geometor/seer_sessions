def analyze_results(task):
    results = []
    for i, (train_input, train_output) in enumerate(task['train']):
        input_grid = np.array(train_input['input'])
        expected_output_grid = np.array(train_output['output'])
        predicted_output_grid = transform(input_grid)
        is_correct = np.array_equal(predicted_output_grid, expected_output_grid)
        results.append({
            'example': i + 1,
            'input_shape': input_grid.shape,
            'output_shape': expected_output_grid.shape,
            'predicted_shape': predicted_output_grid.shape,
            'correct': is_correct
        })

        if not is_correct:
          print(f"Example {i+1} errors:")
          diff = predicted_output_grid - expected_output_grid
          print(np.argwhere(diff != 0))

    return results
import json
task = json.load(open('272f9755.json'))
analysis = analyze_results(task)
for item in analysis:
  print(item)