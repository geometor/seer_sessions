import numpy as np

def analyze_example(input_grid, output_grid):
    input_shape = input_grid.shape
    output_shape = output_grid.shape
    input_unique_colors = np.unique(input_grid)
    output_unique_colors = np.unique(output_grid)
    print(f"  Input Shape: {input_shape}")
    print(f"  Output Shape: {output_shape}")
    print(f"  Input Unique Colors: {input_unique_colors}")
    print(f"  Output Unique Colors: {output_unique_colors}")

task_data = {
    "train": [
        {
            "input": [[8, 8, 8], [8, 8, 8]],
            "output": [[0, 8, 8, 8, 0], [0, 8, 8, 8, 0], [0, 8, 8, 8, 0], [0, 8, 8, 8, 0]],
        },
        {
            "input": [[6, 6, 8, 8, 6, 6], [6, 6, 8, 8, 6, 6]],
            "output": [
                [0, 6, 6, 8, 8, 6, 6, 0],
                [0, 6, 6, 8, 8, 6, 6, 0],
                [0, 6, 6, 8, 8, 6, 6, 0],
                [0, 6, 6, 8, 8, 6, 6, 0],
            ],
        },
        {
            "input": [[7, 7, 7], [7, 7, 7], [7, 7, 7]],
            "output": [
                [0, 7, 7, 7, 0],
                [0, 7, 7, 7, 0],
                [0, 7, 7, 7, 0],
                [0, 7, 7, 7, 0],
                [0, 7, 7, 7, 0],
            ],
        },
        {
            "input": [[4, 4], [4, 4], [4, 4], [4, 4]],
            "output": [
                [0, 4, 4, 0],
                [0, 4, 4, 0],
                [0, 4, 4, 0],
                [0, 4, 4, 0],
                [0, 4, 4, 0],
                [0, 4, 4, 0],
            ],
        },
    ]
}

for i, example in enumerate(task_data["train"]):
    print(f"Example {i+1}:")
    analyze_example(np.array(example["input"]), np.array(example["output"]))
