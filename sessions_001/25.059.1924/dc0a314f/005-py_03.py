def analyze_results(examples, transform_function):
    results = []
    for i, example in enumerate(examples):
        input_grid = example["input"]
        expected_output = example["output"]
        predicted_output = transform_function(input_grid)
        
        # Convert to numpy arrays for easier comparison
        expected_output_np = np.array(expected_output) if expected_output is not None else None
        predicted_output_np = np.array(predicted_output) if predicted_output is not None else None

        # Check if prediction matches expected output
        match = np.array_equal(expected_output_np, predicted_output_np)
        
        results.append({
            "example_index": i,
            "input_shape": np.array(input_grid).shape,
            "expected_output_shape": expected_output_np.shape if expected_output_np is not None else None,
            "predicted_output_shape": predicted_output_np.shape if predicted_output_np is not None else None,
            "match": match
        })
    return results

# Assuming 'train' variable holds the training examples
# and 'transform' is the function defined above

import json
#load the json file
with open('data/training/e9afcf61.json', 'r') as f:
  task = json.load(f)
train = task['train']
test = task['test']

analysis = analyze_results(train, transform)
print(json.dumps(analysis, indent=2))