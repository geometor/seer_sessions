# --- Simulated Code Execution ---
# (I'm simulating what the coder role would do based on the given examples)
# Assume the transform function from the previous prompt is available.

import numpy as np

def analyze_results(task_examples):
    results = []
    for i, example in enumerate(task_examples):
        input_grid = example['input']
        expected_output = example['output']
        predicted_output = transform(input_grid)
        
        input_np = np.array(input_grid)
        output_np = np.array(expected_output)
        objects = find_objects(input_np)
        
        #calculate subgrid for objects - this matches what transform does
        all_coords = []
        for obj in objects:
          for coord in obj:
            all_coords.append(coord)
        rows = sorted(list(set([r for r, c in all_coords])))
        cols = sorted(list(set([c for r, c in all_coords])))

        subgrid = extract_subgrid(input_np, objects)
        
        results.append({
            'example_index': i,
            'input_shape': input_np.shape,
            'output_shape': output_np.shape,
            'predicted_output_shape': np.array(predicted_output).shape,
            'objects': objects,
            'object_colors': [input_np[obj[0]] for obj in objects],
            'subgrid_shape': subgrid.shape,
            'predicted_output': predicted_output,
            'expected_output': expected_output,
            'correct': predicted_output == expected_output
        })
    return results
#Simulated execution results:

task_examples = [
    {
        "input": [
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 8, 8, 8, 8, 8, 8, 8, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 8, 5, 5, 5, 5, 5, 8, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 8, 5, 5, 5, 5, 5, 8, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 8, 5, 5, 5, 5, 5, 8, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 8, 5, 5, 5, 5, 5, 8, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 8, 5, 5, 5, 5, 5, 8, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 8, 8, 8, 8, 8, 8, 8, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        ],
        "output": [
            [8, 8, 8, 8, 8, 8, 8],
            [8, 5, 5, 5, 5, 5, 8],
            [8, 5, 5, 5, 5, 5, 8],
            [8, 5, 5, 5, 5, 5, 8],
            [8, 5, 5, 5, 5, 5, 8],
            [8, 5, 5, 5, 5, 5, 8],
            [8, 8, 8, 8, 8, 8, 8],
        ],
    },
    {
        "input": [
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 8, 0],
            [0, 0, 0, 0, 0, 0, 0, 8, 8, 0],
            [0, 0, 0, 0, 0, 0, 8, 5, 8, 0],
            [0, 0, 0, 0, 0, 8, 5, 5, 8, 0],
            [0, 0, 0, 0, 8, 5, 5, 5, 8, 0],
            [0, 0, 0, 8, 5, 5, 5, 5, 8, 0],
            [0, 0, 8, 5, 5, 5, 5, 5, 8, 0],
            [0, 8, 8, 8, 8, 8, 8, 8, 8, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        ],
        "output": [
            [8, 8, 8],
            [8, 5, 8],
            [8, 5, 5],
            [5, 5, 5],
            [5, 5, 5],
            [5, 5, 5],
            [8, 8, 8],
        ],
    },
    {
        "input": [
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 8, 8, 8, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 8, 5, 8, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 8, 5, 8, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 8, 5, 8, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 8, 5, 8, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 8, 5, 8, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 8, 8, 8, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        ],
        "output": [
            [8, 8, 8],
            [8, 5, 8],
            [8, 5, 8],
            [8, 5, 8],
            [8, 5, 8],
            [8, 5, 8],
            [8, 8, 8],
        ],
    },
]

results = analyze_results(task_examples)
print(results)