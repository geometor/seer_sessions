import numpy as np

def analyze_examples(examples):
    results = []
    for example in examples:
        input_grid = np.array(example['input'])
        output_grid = np.array(example['output'])
        
        input_colors, input_counts = np.unique(input_grid, return_counts=True)
        output_colors, output_counts = np.unique(output_grid, return_counts=True)
        
        results.append({
            'input_shape': input_grid.shape,
            'input_color_counts': dict(zip(input_colors, input_counts)),
            'output_shape': output_grid.shape,
            'output_color_counts': dict(zip(output_colors, output_counts)),
        })
    return results

# Assuming 'train' contains the training examples
# This part needs to run in the actual environment with the 'train' data.
# results = analyze_examples(train)
# print(results)

#Dummy data to simulate the structure, replace with actual environment
dummy_train = [
    {'input': [[1, 2, 3], [4, 5, 6]], 'output': [[9, 9, 9], [9, 9, 9]]},
    {'input': [[0, 0, 0], [0, 0, 0], [0,0,0]], 'output': [[9, 9, 9], [9, 9, 9],[9,9,9]]},
    {'input': [[7, 8], [9, 1]], 'output': [[9, 9], [9, 9]]}
]

results = analyze_examples(dummy_train)
print(results)
