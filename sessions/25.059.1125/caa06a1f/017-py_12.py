def analyze_example(input_grid, output_grid):
    input_colors, input_counts = np.unique(input_grid, return_counts=True)
    output_colors, output_counts = np.unique(output_grid, return_counts=True)

    print(f"Input Colors: {input_colors}, Counts: {input_counts}")
    print(f"Output Colors: {output_colors}, Counts: {output_counts}")

    #check for size changes
    if input_grid.shape != output_grid.shape:
        print(f"Input Shape: {input_grid.shape}, Output Shape: {output_grid.shape}")

    # simple color swap check
    color_changes = {}
    for color in input_colors:
        if color not in output_colors:
            print(f"color {color} not in output")
            
    for color in output_colors:
        if color not in input_colors:
            print(f"color {color} not in input")

import numpy as np
example_grids = task_data['train']
for i, example in enumerate(example_grids):
    print(f"--- Example {i+1} ---")
    analyze_example(np.array(example['input']), np.array(example['output']))
