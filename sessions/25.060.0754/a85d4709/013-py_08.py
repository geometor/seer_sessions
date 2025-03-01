import numpy as np

def analyze_examples(examples):
    results = []
    for i, example in enumerate(examples):
        input_grid = np.array(example['input'])
        expected_output_grid = np.array(example['output'])
        target_color = find_target_color(input_grid, expected_output_grid)

        #basic grid comparisons
        same_dimensions = input_grid.shape == expected_output_grid.shape
        input_pixels = input_grid.size
        output_pixels = expected_output_grid.size

        results.append({
            'example_index': i,
            'input_shape': input_grid.shape,
            'output_shape': expected_output_grid.shape,
            'same_dimensions': same_dimensions,
            'input_pixels': input_pixels,
            'output_pixels': output_pixels,
            'target_color': target_color
        })
    return results
#provided examples (from the prompt)
examples = [
    {'input': [[5, 5, 5, 5], [5, 5, 5, 5], [5, 5, 5, 5], [5, 5, 5, 5]],
     'output': [[3, 3, 3, 3], [3, 3, 3, 3], [3, 3, 3, 3], [3, 3, 3, 3]]},
    {'input': [[5, 5, 5, 5], [5, 5, 5, 5], [5, 5, 5, 5], [5, 5, 5, 5]],
     'output': [[3, 5, 5, 5], [3, 5, 5, 5], [3, 5, 5, 5], [3, 5, 5, 5]]},     
    {'input': [[1, 1, 1, 1], [1, 1, 1, 1], [1, 1, 1, 1], [1, 1, 1, 1]],
     'output': [[3, 1, 1, 1], [3, 1, 1, 1], [3, 1, 1, 1], [3, 1, 1, 1]]},
    {'input': [[8, 8, 8, 8], [8, 8, 8, 8], [8, 8, 8, 8], [8, 8, 8, 8]],
     'output': [[3, 8, 8, 8], [3, 8, 8, 8], [3, 8, 8, 8], [3, 8, 8, 8]]}
]

analysis_results = analyze_examples(examples)

#print each result on a new line
for result in analysis_results:
    print(result)
