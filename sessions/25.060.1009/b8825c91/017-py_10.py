import numpy as np

# Example Data (replace with actual data from the task)
examples = [
    {'input': [[1, 2], [3, 4]], 'output': [[4, 3], [2, 1]]},
    {'input': [[1, 2, 3], [4, 5, 6]], 'output': [[6, 5, 4], [3, 2, 1]]},
    {'input': [[1,1,1],[2,2,2],[3,3,3]], 'output': [[3,3,3], [2,2,2],[1,1,1]]},
]

for i, example in enumerate(examples):
    input_grid = np.array(example['input'])
    output_grid = np.array(example['output'])
    print(f"Example {i+1}:")
    print(f"  Input Shape: {input_grid.shape}")
    print(f"  Output Shape: {output_grid.shape}")
