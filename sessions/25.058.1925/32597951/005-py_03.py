import numpy as np

def calculate_diff(grid1, grid2):
    """Calculates the difference between two grids."""
    if grid1.shape != grid2.shape:
        return "Grids have different shapes"
    diff = (grid1 != grid2).astype(int)
    return diff

def analyze_results(examples):
    results = []
    for i, example in enumerate(examples):
        input_grid = np.array(example['input'])
        expected_output = np.array(example['output'])
        actual_output = transform(input_grid)
        diff = calculate_diff(expected_output, actual_output)
        num_diff_pixels = np.sum(diff) if isinstance(diff, np.ndarray) else 0

        results.append({
            'example_index': i,
            'input_shape': input_grid.shape,
            'output_shape': expected_output.shape,
            'diff_pixels': num_diff_pixels,
            'diff_grid': diff.tolist() if isinstance(diff, np.ndarray) else diff
        })
    return results

# Assuming 'train' is a list of dictionaries as provided in ARC data
# Example: train = [{'input': [[...]], 'output': [[...]]}, ...]

#Dummy data representing the structure. Replace with actual train examples
train = [
    {'input': [[0, 0, 0, 0, 0, 0, 0],
               [0, 8, 8, 8, 8, 8, 0],
               [0, 0, 0, 8, 0, 0, 0],
               [0, 0, 0, 8, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0]],
     'output': [[0, 0, 0, 0, 0, 0, 0],
                [0, 8, 8, 3, 8, 8, 0],
                [0, 0, 0, 3, 0, 0, 0],
                [0, 0, 0, 3, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0]]},
    {'input': [[0, 0, 0, 0, 0, 0],
               [0, 8, 8, 8, 8, 0],
               [0, 0, 0, 8, 0, 0],
               [0, 0, 0, 0, 0, 0]],
     'output': [[0, 0, 0, 0, 0, 0],
                [0, 8, 8, 3, 8, 0],
                [0, 0, 0, 3, 0, 0],
                [0, 0, 0, 0, 0, 0]]},
    {'input': [[8, 8, 8, 8],
               [8, 8, 8, 8],
               [8, 8, 8, 8],
               [8, 8, 8, 8]],
     'output': [[8, 8, 3, 8],
                [8, 8, 3, 8],
                [3, 3, 3, 3],
                [8, 8, 3, 8]]}
]

analysis = analyze_results(train)
print(analysis)

