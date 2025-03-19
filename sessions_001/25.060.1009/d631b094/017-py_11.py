import numpy as np

def analyze_example(input_grid, output_grid):
    input_array = np.array(input_grid)
    output_array = np.array(output_grid)

    non_zero_indices = np.nonzero(input_array)
    num_non_zero = len(non_zero_indices[0])
    non_zero_values = input_array[non_zero_indices].tolist()

    input_dims = input_array.shape
    output_dims = output_array.shape
    
    return {
        "input_dims": input_dims,
        "num_non_zero": num_non_zero,
        "non_zero_values": non_zero_values,
        "output_dims": output_dims,
        "output_values": output_array.flatten().tolist()
    }
    

examples = [
    (
        [[0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 7, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0]],
        [[7]]
    ),
    (
        [[0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 5, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 3, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0]],
        [[5, 3]]
    ),
    (
        [[0, 0, 0, 0, 0, 0, 0], [0, 0, 6, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0]],
        [[6]]
    ),
    (
        [[0, 0, 0, 0, 0], [0, 5, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 2, 0], [0, 0, 0, 0, 0]],
        [[5, 2]]
    )
]
analysis_results = [analyze_example(inp, out) for inp, out in examples]
print(analysis_results)
