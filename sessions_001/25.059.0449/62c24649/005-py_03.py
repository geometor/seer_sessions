def analyze_example(input_grid, expected_output_grid):
    input_height, input_width = input_grid.shape
    output_height, output_width = expected_output_grid.shape
    input_colors = np.unique(input_grid)
    output_colors = np.unique(expected_output_grid)
    top_left_input = input_grid[0,0]
    top_left_output = expected_output_grid[0,0]

    print(f"  Input Dimensions: {input_height}x{input_width}")
    print(f"  Output Dimensions: {output_height}x{output_width}")
    print(f"  Input Colors: {input_colors}")
    print(f"  Output Colors: {output_colors}")
    print(f"  Input Top-Left Pixel: {top_left_input}")
    print(f"  Output Top-Left Pixel: {top_left_output}")
    # Check if input grid appears in output grid and at what offsets.
    input_in_output = False
    offsets = []
    for y_offset in range(output_height - input_height + 1):
        for x_offset in range(output_width - input_width + 1):
            if np.array_equal(expected_output_grid[y_offset:y_offset+input_height, x_offset:x_offset+input_width], input_grid):
                input_in_output = True
                offsets.append((y_offset, x_offset))
    print(f"  Input in Output: {input_in_output}")
    print(f"  Offsets: {offsets}")

task_data = {
    "train": [
        {
            "input": [
                [8, 8, 8],
                [8, 8, 8]
            ],
            "output": [
                [8, 8, 8, 8, 8, 8],
                [8, 8, 8, 8, 8, 8],
                [8, 8, 8, 8, 8, 8],
                [8, 8, 8, 8, 8, 8]
            ]
        },
        {
            "input": [
                [1, 0, 1],
                [0, 1, 0],
                [1, 0, 1]
            ],
            "output": [
                [1, 0, 1, 1, 0, 1],
                [0, 1, 0, 0, 1, 0],
                [1, 0, 1, 1, 0, 1]
            ]
        },
       {
            "input": [
                [6, 0, 6, 0, 6, 0],
                [0, 8, 0, 8, 0, 0],
                [6, 0, 6, 0, 6, 0]
            ],
            "output": [
                [6, 0, 6, 0, 6, 0, 6, 0, 6, 0, 6, 0],
                [0, 8, 0, 8, 0, 0, 0, 8, 0, 8, 0, 0],
                [6, 0, 6, 0, 6, 0, 6, 0, 6, 0, 6, 0]
            ]
       },
        {
            "input": [
                [1, 1, 1, 1, 1, 1, 1],
                [1, 1, 1, 1, 1, 1, 1],
                [1, 1, 1, 1, 1, 1, 1],
                [1, 1, 1, 1, 1, 1, 1]
            ],
            "output": [
                [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
            ]
       }
    ]
}

for i, example in enumerate(task_data["train"]):
  print(f"Example {i+1}:")
  analyze_example(np.array(example["input"]), np.array(example["output"]))