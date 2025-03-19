import numpy as np

def get_bounding_box(grid, color):
    rows, cols = np.where(grid == color)
    if len(rows) == 0:
        return None  # No object of that color
    min_row, max_row = np.min(rows), np.max(rows)
    min_col, max_col = np.min(cols), np.max(cols)
    return (min_row, min_col), (max_row, max_col)

def analyze_example(input_grid, output_grid):
    print("Input grid:")
    print(input_grid)
    print("Output grid:")
    print(output_grid)

    rows, cols = input_grid.shape
    mid_col = cols // 2
    right_half = input_grid[:, mid_col:]
    left_half = input_grid[:, :mid_col]

    print(f"Input right half:\n{right_half}")
    print(f"Input left half:\n{left_half}")

    # Find and print bounding boxes for each color
    for color in np.unique(input_grid):
        input_bbox = get_bounding_box(input_grid, color)
        output_bbox = get_bounding_box(output_grid, color)

        print(f"Color {color}:")
        print(f"  Input Bounding Box: {input_bbox}")
        print(f"  Output Bounding Box: {output_bbox}")

    right_objects = get_objects(right_half, 8)
    left_objects = get_objects(left_half, 0) #assume background is white

    print(f"Objects in right half: {right_objects}")
    print(f"Objects in left half: {left_objects}")
    print("-" * 20)


task_data = {
    "train": [
        {
            "input": [
                [0, 0, 0, 0, 0, 0, 0, 0, 8, 8, 8, 8],
                [0, 0, 0, 0, 0, 0, 0, 0, 8, 8, 8, 8],
                [0, 0, 0, 0, 0, 0, 0, 0, 8, 8, 1, 8],
                [0, 0, 0, 0, 0, 0, 0, 0, 8, 8, 8, 8],
                [0, 0, 0, 0, 0, 0, 0, 0, 8, 8, 6, 8],
                [0, 0, 0, 0, 0, 0, 0, 0, 8, 2, 8, 8],
            ],
            "output": [
                [0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 1, 0],
                [0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 6, 0],
                [0, 0, 0, 0, 2, 0],
            ],
        },
        {
            "input": [
                [0, 0, 0, 0, 0, 0, 0, 0, 8, 8, 8, 8],
                [0, 0, 0, 0, 0, 0, 0, 0, 8, 8, 8, 8],
                [0, 0, 0, 0, 0, 0, 0, 0, 8, 8, 8, 8],
                [0, 0, 0, 0, 0, 0, 0, 0, 8, 8, 2, 8],
                [0, 0, 0, 0, 0, 0, 0, 0, 8, 8, 8, 8],
                [0, 0, 0, 0, 0, 0, 0, 0, 8, 8, 8, 8],
            ],
            "output": [
                [0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 2, 0],
                [0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0],
            ],
        },
        {
            "input": [
                [0, 0, 0, 0, 0, 0, 0, 0, 8, 8, 8, 8],
                [0, 0, 0, 0, 0, 0, 0, 0, 8, 8, 1, 8],
                [0, 0, 0, 0, 0, 0, 0, 0, 8, 8, 8, 8],
                [0, 0, 0, 0, 0, 0, 0, 0, 8, 8, 8, 8],
                [0, 0, 0, 0, 0, 0, 0, 0, 8, 8, 6, 8],
                [0, 0, 0, 0, 0, 0, 0, 0, 8, 8, 8, 8],
            ],
            "output": [
                [0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 1, 0],
                [0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 6, 0],
                [0, 0, 0, 0, 0, 0],
            ],
        },
                {
            "input": [
                [0, 0, 0, 0, 0, 0, 0, 0, 8, 8, 8, 8, 8],
                [0, 0, 0, 0, 0, 0, 0, 0, 8, 8, 8, 8, 8],
                [0, 0, 0, 0, 0, 0, 0, 0, 8, 8, 8, 2, 8],
                [0, 0, 0, 0, 0, 0, 0, 0, 8, 8, 8, 8, 8],
                [0, 0, 0, 0, 0, 0, 0, 0, 8, 8, 8, 8, 8],
                [0, 0, 0, 0, 0, 0, 0, 0, 8, 8, 8, 8, 8],
                [0, 0, 0, 0, 0, 0, 0, 0, 8, 8, 8, 8, 8],
            ],
            "output": [
                [0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 2, 0],
                [0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0],
            ],
        },
    ]
}

for example in task_data["train"]:
    analyze_example(np.array(example["input"]), np.array(example["output"]))
