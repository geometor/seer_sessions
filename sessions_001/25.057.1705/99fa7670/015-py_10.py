import numpy as np

def analyze_results(task_data):
    results = []
    for example in task_data['train']:
        input_grid = np.array(example['input'])
        output_grid = np.array(example['output'])
        predicted_output = transform(input_grid)  # Using the provided transform function
        
        # Get objects before the transform
        input_objects = get_objects(input_grid)
        
        # Get object after the transform
        output_objects = get_objects(output_grid)
        
        # Get object of the prediction
        predicted_objects = get_objects(predicted_output)

        results.append({
            'input_objects': input_objects,
            'output_objects': output_objects,
            'predicted_objects' : predicted_objects,
            'correct': np.array_equal(output_grid, predicted_output),
            'output_last_col': output_grid[:, -1].tolist(),
            'predicted_last_col': predicted_output[:, -1].tolist(),
        })
    return results