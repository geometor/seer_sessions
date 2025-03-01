import numpy as np

task = {
    "train": [
        {
            "input": [[0, 1, 0, 1, 0],
                      [1, 0, 1, 0, 1],
                      [0, 1, 0, 1, 0]],
            "output": [[0, 2, 0, 2, 0],
                       [0, 0, 0, 0, 0],
                       [2, 0, 2, 0, 2]]
        },
        {
            "input": [[0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 1, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0],
                      [1, 0, 0, 0, 1, 0, 0]],
            "output": [[0, 0, 0, 0, 0, 0, 0],
                       [0, 0, 2, 0, 0, 0, 0],
                       [0, 0, 0, 0, 0, 0, 0],
                       [0, 0, 0, 0, 0, 0, 0],
                       [2, 0, 0, 0, 2, 0, 0]]
        },
        {
            "input": [[0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 1, 0, 0],
                      [0, 0, 1, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0]],
            "output": [[0, 0, 0, 0, 0, 0],
                       [0, 0, 0, 2, 0, 0],
                       [0, 0, 0, 0, 0, 0],
                       [0, 0, 2, 0, 0, 0]]
        }
    ],
    "test": [
        {
            "input": [[1, 0, 0, 0, 1, 0],
                      [0, 0, 0, 0, 0, 0],
                      [0, 1, 0, 0, 0, 0]],
            "output": [[2, 0, 0, 0, 2, 0],
                       [0, 0, 0, 0, 0, 0],
                       [0, 0, 0, 0, 0, 0],
                       [0, 2, 0, 0, 0, 0]]
        }
    ]
}

for i, example in enumerate(task["train"]):
    input_grid = np.array(example["input"])
    output_grid = np.array(example["output"])
    input_height, input_width = input_grid.shape
    output_height, output_width = output_grid.shape

    print(f"Example {i+1}:")
    print(f"  Input Shape: {input_grid.shape}")
    print(f"  Output Shape: {output_grid.shape}")
    print(f"  Height Ratio: {output_height / input_height}")
    print(f"  Width Ratio: {output_width / input_width}")

    # Find blue pixel locations and corresponding output pixel locations
    blue_pixels = np.where(input_grid == 1)
    print(f"  Blue Pixel Coordinates (Input): {list(zip(blue_pixels[0], blue_pixels[1]))}")

    for r, c in zip(blue_pixels[0], blue_pixels[1]):
        # this logic won't work, just shows my intent.
        #output_r, output_c = find_corresponding_output_pixel(r, c, input_grid.shape, output_grid.shape)
        #print(f"    Input ({r}, {c}) -> Output ({output_r}, {output_c})")
        pass
