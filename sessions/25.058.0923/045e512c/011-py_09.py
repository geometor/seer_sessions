import numpy as np

def analyze_grid(grid, grid_name):
    blue_pixels = np.argwhere(grid == 1)
    red_pixels = np.argwhere(grid == 2)
    yellow_pixels = np.argwhere(grid == 4)

    print(f"Analysis of {grid_name}:")
    if blue_pixels.size > 0:
        print(f"  Blue pixel(s) at: {blue_pixels}")
    else:
        print("  No blue pixels found.")
    print(f"  Red pixel(s) at: {red_pixels}, Count: {red_pixels.shape[0]}")
    print(f"  Yellow pixel(s) at: {yellow_pixels}, Count: {yellow_pixels.shape[0]}")

# Provided training examples and outputs (replace with the actual data)
train = [
    [
        [
            [0, 0, 0, 4, 0, 0, 0],
            [0, 0, 0, 4, 0, 0, 0],
            [0, 0, 0, 4, 0, 0, 0],
            [2, 2, 2, 1, 4, 4, 4],
            [0, 0, 0, 4, 0, 0, 0],
            [0, 0, 0, 4, 0, 0, 0],
            [0, 0, 0, 4, 0, 0, 0],
        ],
        [
            [2, 2, 2, 4, 2, 2, 2],
            [2, 2, 2, 4, 2, 2, 2],
            [2, 2, 2, 4, 2, 2, 2],
            [4, 4, 4, 1, 4, 4, 4],
            [2, 2, 2, 4, 2, 2, 2],
            [2, 2, 2, 4, 2, 2, 2],
            [2, 2, 2, 4, 2, 2, 2],
        ]
    ],
        [
        [
            [0, 0, 4, 0, 0, 0, 0],
            [0, 0, 4, 0, 0, 0, 0],
            [0, 0, 4, 0, 0, 0, 0],
            [0, 0, 4, 0, 0, 0, 0],
            [2, 2, 1, 4, 0, 0, 0],
            [0, 0, 4, 0, 0, 0, 0],
        ],
        [
            [2, 2, 4, 2, 2, 2, 2],
            [2, 2, 4, 2, 2, 2, 2],
            [2, 2, 4, 2, 2, 2, 2],
            [2, 2, 4, 2, 2, 2, 2],
            [2, 2, 1, 4, 2, 2, 2],
            [2, 2, 4, 2, 2, 2, 2],
        ],
    ],
        [
        [
            [4, 0, 0, 0, 0, 0],
            [0, 4, 0, 0, 0, 0],
            [0, 0, 4, 0, 0, 0],
            [0, 0, 2, 1, 0, 0],
            [0, 0, 0, 0, 0, 0],
        ],
        [
            [4, 2, 2, 2, 2, 2],
            [4, 4, 2, 2, 2, 2],
            [4, 4, 4, 2, 2, 2],
            [4, 4, 4, 1, 2, 2],
            [4, 4, 4, 4, 4, 2],
        ],
    ]

]

for i, (input_grid, output_grid) in enumerate(train):
    analyze_grid(np.array(input_grid), f"train[{i}] input")
    analyze_grid(np.array(output_grid), f"train[{i}] output")
    print("-" * 30)