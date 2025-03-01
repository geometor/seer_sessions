import numpy as np

def analyze_example(input_grid, output_grid):
    input_grid = np.array(input_grid)
    output_grid = np.array(output_grid)

    input_objects = {}
    output_objects = {}

    for color in range(10):  # Check all colors
        input_coords = np.argwhere(input_grid == color)
        output_coords = np.argwhere(output_grid == color)

        if input_coords.size > 0:
            input_objects[color] = {
                'count': input_coords.shape[0],
                'min_row': np.min(input_coords[:, 0]),
                'max_row': np.max(input_coords[:, 0]),
                'min_col': np.min(input_coords[:, 1]),
                'max_col': np.max(input_coords[:, 1]),
            }
        if output_coords.size > 0:
            output_objects[color] = {
                'count': output_coords.shape[0],
                'min_row': np.min(output_coords[:, 0]),
                'max_row': np.max(output_coords[:, 0]),
                'min_col': np.min(output_coords[:, 1]),
                'max_col': np.max(output_coords[:, 1]),
            }
    return input_objects, output_objects

examples = [
    ([
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 8, 8, 8, 0, 0, 0],
        [0, 0, 0, 0, 8, 3, 8, 0, 0, 0],
        [0, 0, 0, 0, 8, 8, 8, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    ],
    [
        [8, 8, 8],
        [8, 3, 8],
        [8, 8, 8]
    ]),
    ([
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 8, 8, 8, 0, 0],
        [0, 0, 0, 8, 5, 8, 0, 0],
        [0, 0, 0, 8, 8, 8, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0]
    ],
    [
        [8, 8, 8],
        [8, 5, 8],
        [8, 8, 8]
    ]),
    ([
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 8, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 8, 8, 8, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 8, 1, 8, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 8, 8, 8, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 8, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    ],
    [
        [8, 8, 8],
        [8, 1, 8],
        [8, 8, 8]
    ]),
    ([
       [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
       [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
       [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
       [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
       [0, 0, 0, 0, 0, 0, 8, 8, 8, 0, 0, 0],
       [0, 0, 0, 0, 0, 0, 8, 2, 8, 0, 0, 0],
       [0, 0, 0, 0, 0, 0, 8, 8, 8, 0, 0, 0],
       [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
       [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
       [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    ],
    [
        [8, 8, 8],
        [8, 2, 8],
        [8, 8, 8]
    ]),
        ([
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 8, 8, 8, 0, 0, 0],
        [0, 0, 0, 0, 8, 4, 8, 0, 0, 0],
        [0, 0, 0, 0, 8, 8, 8, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    ],
    [
        [8, 8, 8],
        [8, 4, 8],
        [8, 8, 8]
    ]),
]

for i, (input_grid, output_grid) in enumerate(examples):
    input_objects, output_objects = analyze_example(input_grid, output_grid)
    print(f"Example {i+1}:")
    print("Input Objects:", input_objects)
    print("Output Objects:", output_objects)
    print("-" * 30)