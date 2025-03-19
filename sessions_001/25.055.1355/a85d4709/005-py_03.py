# Hypothetical Code - this is what I would execute if I could.
import numpy as np

def analyze_examples(examples):
    results = []
    for example in examples:
        input_grid = np.array(example['input'])
        output_grid = np.array(example['output'])
        
        # find diff of grids
        diff = output_grid - input_grid

        results.append({
            'input_shape': input_grid.shape,
            'output_shape': output_grid.shape,
            'value_changes': np.unique(diff, return_counts=True),
            'input_values' : np.unique(input_grid, return_counts=True),
            'output_values' : np.unique(output_grid, return_counts=True),
        })
    return results

# Assume 'examples' is a list of dictionaries like:
# examples = [
#     {'input': [[0, 1], [5, 2]], 'output': [[3, 1], [4, 2]]},
#     {'input': [[5,5,5],[0,0,0]], 'output': [[4,4,4],[3,3,3]]},
#     ... more examples ...
# ]

# results = analyze_examples(examples)
# for result in results:
#     print(result)