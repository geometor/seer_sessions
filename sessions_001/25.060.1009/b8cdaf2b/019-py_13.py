def describe_grid(grid):
    rows, cols = grid.shape
    first_three_rows_colors = []
    for i in range(min(3, rows)):
        row_colors = []
        for j in range(cols):
            row_colors.append(grid[i, j])
        first_three_rows_colors.append(row_colors)

    other_rows = []
    for i in range(min(3, rows),rows):
        row_colors = []
        for j in range(cols):
           row_colors.append(grid[i, j])
        other_rows.append(row_colors)

    return {
        'rows': rows,
        'cols': cols,
        'first_three_rows_colors': first_three_rows_colors,
        'other_rows': other_rows
    }

task_data = {
    'train': [
        {
            'input': [
                [0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 5, 0, 0, 4, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0],
            ],
            'output': [
                [0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0],
                [1, 0, 0, 0, 0, 0, 0, 0, 1],
                [0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 5, 0, 0, 4, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0],
            ]
        },
       {
            'input': [
                [0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 5, 0, 0, 4, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0]

            ],
            'output': [
                [0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0],
                [1, 0, 0, 0, 0, 0, 0, 0, 1],
                [0, 0, 0, 5, 0, 0, 4, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0]
            ]
        },
        {
            'input': [
                [0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0]
            ],
            'output': [
                [0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0],
                [1, 0, 0, 0, 0, 0, 0, 0, 1]
            ]
        },
        {
            'input': [
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
            ],
            'output': [
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1]
            ]
        }
    ]
}

import numpy as np
for i, example in enumerate(task_data['train']):
    input_grid = np.array(example['input'])
    output_grid = np.array(example['output'])
    input_desc = describe_grid(input_grid)
    output_desc = describe_grid(output_grid)
    print(f"Example {i + 1}:")
    print(f"  Input Grid Description: {input_desc}")
    print(f"  Output Grid Description: {output_desc}")