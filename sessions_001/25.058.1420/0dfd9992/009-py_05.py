import numpy as np

def analyze_grid(grid):
    shape = grid.shape
    white_pixels = np.sum(grid == 0)
    non_white_pixels = np.sum(grid != 0)
    return shape, white_pixels, non_white_pixels

def analyze_example(example):
    input_grid = np.array(example['input'])
    output_grid = np.array(example['output'])
    actual_output_grid = transform(input_grid)
    
    input_shape, input_white, input_non_white = analyze_grid(input_grid)
    output_shape, output_white, output_non_white = analyze_grid(output_grid)
    actual_output_shape, actual_output_white, actual_output_non_white = analyze_grid(actual_output_grid)

    return {
        'input': {
            'shape': input_shape,
            'white_pixels': input_white,
            'non_white_pixels': input_non_white
        },
        'output': {
            'shape': output_shape,
            'white_pixels': output_white,
            'non_white_pixels': output_non_white
        },
        'actual_output': {
            'shape': actual_output_shape,
            'white_pixels': actual_output_white,
            'non_white_pixels': actual_output_non_white,
            'match': np.array_equal(output_grid,actual_output_grid)
        }

    }

examples = [
    {
        "input": [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 3]],
        "output": [[3]]
    },
    {
        "input": [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 2], [0, 0, 0, 0, 0, 0, 0, 0, 0, 3]],
        "output": [[2], [3]]
    },
    {
        "input": [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 2], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 2], [0, 0, 0, 0, 0, 0, 0, 0, 0, 3]],
        "output": [[2], [2], [3]]
    },
    {
        "input" : [[0, 0, 0, 0, 0, 0, 0, 0, 0, 2], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 2], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 2], [0, 0, 0, 0, 0, 0, 0, 0, 0, 3]],
        "output": [[2], [2], [2], [3]]
    }
]

results = [analyze_example(example) for example in examples]
for i, result in enumerate(results):
    print(f"Example {i+1}:")
    print(f"  Input: Shape={result['input']['shape']}, White={result['input']['white_pixels']}, Non-White={result['input']['non_white_pixels']}")
    print(f"  Output: Shape={result['output']['shape']}, White={result['output']['white_pixels']}, Non-White={result['output']['non_white_pixels']}")
    print(f"  Actual Output: Shape={result['actual_output']['shape']}, White={result['actual_output']['white_pixels']}, Non-White={result['actual_output']['non_white_pixels']}, Match={result['actual_output']['match']}")