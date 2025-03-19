import numpy as np

# Example data (replace with actual data from the task)
examples = [
    {
        "input": np.array([[8, 0, 8, 0], [0, 8, 0, 2], [8, 0, 8, 0], [0, 8, 0, 8]]),
        "output": np.array([[8, 0, 8, 0, 8, 0, 8, 0], [0, 8, 0, 8, 0, 8, 0, 8], [8, 0, 8, 0, 8, 0, 8, 0], [0, 8, 0, 2, 0, 8, 0, 8], [8, 0, 8, 0, 8, 0, 8, 0], [0, 8, 0, 8, 0, 8, 0, 8], [8, 0, 8, 0, 8, 0, 8, 0], [0, 8, 0, 8, 0, 8, 0, 8]])
    },
    {
        "input": np.array([[0, 8, 0, 8], [8, 0, 8, 0], [0, 8, 2, 8], [8, 0, 8, 0]]),
        "output": np.array([[8, 0, 8, 0, 8, 0, 8, 0], [0, 8, 0, 8, 0, 8, 0, 8], [8, 0, 8, 0, 8, 0, 8, 0], [0, 8, 0, 8, 0, 8, 0, 8], [8, 0, 8, 0, 8, 0, 8, 2], [0, 8, 0, 8, 0, 8, 0, 8], [8, 0, 8, 0, 8, 0, 8, 0], [0, 8, 0, 8, 0, 8, 0, 8]])
    },
    {
        "input": np.array([[8, 0, 8, 0, 8], [0, 8, 0, 8, 0], [8, 0, 8, 0, 8], [0, 8, 0, 2, 0], [8, 0, 8, 0, 8]]),
        "output": np.array([[8, 0, 8, 0, 8, 0, 8, 0, 8, 0], [0, 8, 0, 8, 0, 8, 0, 8, 0, 8], [8, 0, 8, 0, 8, 0, 8, 0, 8, 0], [0, 8, 0, 8, 0, 8, 0, 8, 0, 8], [8, 0, 8, 0, 8, 0, 8, 0, 8, 0], [0, 8, 0, 8, 0, 8, 0, 8, 0, 8], [8, 0, 8, 0, 8, 0, 8, 0, 8, 0], [0, 8, 0, 8, 0, 2, 0, 8, 0, 8], [8, 0, 8, 0, 8, 0, 8, 0, 8, 0], [0, 8, 0, 8, 0, 8, 0, 8, 0, 8]])
    }
]

for i, example in enumerate(examples):
    input_grid = example['input']
    output_grid = example['output']

    red_pixels_input = np.argwhere(input_grid == 2)
    red_pixels_output = np.argwhere(output_grid == 2)

    print(f"Example {i+1}:")
    print(f"  Input grid size: {input_grid.shape}")
    print(f"  Output grid size: {output_grid.shape}")

    if len(red_pixels_input) > 0:
        print(f"  Red pixel input coordinates: {red_pixels_input}")
        print(f"  Red pixel output coordinates: {red_pixels_output}")
    else:
        print("  No red pixel found in input.")