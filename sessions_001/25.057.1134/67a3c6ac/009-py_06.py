import numpy as np

def get_grid_dimensions(grid):
    return len(grid), len(grid[0]) if grid else (0, 0)

task_data = {
    "train": [
        {
            "input": [
                [5, 0, 5, 0, 5],
                [0, 5, 0, 5, 0],
                [5, 0, 5, 0, 5],
                [0, 5, 0, 5, 0]
            ],
            "output": [
                [5, 0, 5, 0],
                [0, 5, 0, 5],
                [5, 0, 5, 0],
                [0, 5, 0, 5],
                [5, 0, 5, 0]
            ]
        },
                        {
            "input": [
                [8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8],
            ],
            "output": [
                [8], [8], [8], [8], [8], [8], [8], [8], [8], [8], [8], [8]
            ]
        },

        {
            "input": [
                [7, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [7, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [7, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [7, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [7, 0, 0, 0, 0, 0, 0, 0, 0, 0],

            ],
            "output": [
                [7, 7, 7, 7, 7],
                [0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0],
            ]
        }
    ],
    "test": [
        {
            "input": [
                [1, 1, 1, 1, 1, 1, 1, 1],
                [1, 1, 1, 1, 1, 1, 1, 8],
            ],
            "output": [
                [1, 1],
                [1, 1],
                [1, 1],
                [1, 1],
                [1, 1],
                [1, 1],
                [1, 1],
                [1, 8],
            ]
        }
    ]
}
results = {}
for phase in ["train", "test"]:
    results[phase] = []
    for example in task_data[phase]:
        input_dims = get_grid_dimensions(example["input"])
        output_dims = get_grid_dimensions(example["output"])
        results[phase].append({"input_dims": input_dims, "output_dims": output_dims})

print(results)
