def get_task_examples_and_predictions(task_data, transform_func):
    """
    Applies the transformation function to each input grid in the training set of a task and zips it together with input, output, predicted output

    Args:
        task_data (dict): The task data loaded from the JSON file.
        transform_func (function): The transformation function to apply.

    Returns:
        list: A list of dictionaries, where each dictionary contains the 'input', 'output', and 'predicted' grids.
    """
    results = []
    for example in task_data['train']:
        input_grid = np.array(example['input'])
        output_grid = np.array(example['output'])
        predicted_grid = transform_func(input_grid)
        results.append({
            'input': input_grid,
            'output': output_grid,
            'predicted': predicted_grid
        })
    return results

# import the json
import json
with open('data/training/d515c40f.json', 'r') as f:
    task_data = json.load(f)
results = get_task_examples_and_predictions(task_data, transform)

for i,result in enumerate(results):
  print(f"Example {i+1}:")
  print(f"Input:\n{result['input']}")
  print(f"Expected Output:\n{result['output']}")
  print(f"Predicted Output:\n{result['predicted']}")
  print(f"Matches Expected: {np.array_equal(result['output'], result['predicted'])}\n")