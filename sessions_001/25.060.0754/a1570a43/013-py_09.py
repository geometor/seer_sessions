import numpy as np

def get_red_block(grid):
    return np.argwhere(grid == 2)

def get_green_pixels(grid):
    return np.argwhere(grid == 3)

def is_horizontal(coords):
    return all([coords[0][0] == c[0] for c in coords])

def is_vertical(coords):
    return all([coords[0][1] == c[1] for c in coords])

def calculate_center(coords):
    min_x = min(coords[:, 0])
    max_x = max(coords[:, 0])
    min_y = min(coords[:, 1])
    max_y = max(coords[:, 1])
    return np.array([(min_x + max_x) / 2.0, (min_y + max_y) / 2.0])

def analyze_example(input_grid, output_grid):
    red_block = get_red_block(input_grid)
    green_pixels = get_green_pixels(input_grid)

    red_shape = "horizontal" if is_horizontal(red_block) else "vertical" if is_vertical(red_block) else "other"
    red_center = calculate_center(red_block) if len(red_block) >0 else None
    num_green = len(green_pixels)

    #very simple transformation detection
    transformed_red_block = get_red_block(output_grid)
    transformation = "none"

    if(len(red_block) != len(transformed_red_block)):
        transformation = "unknown"
    elif (len(red_block) > 0 and len(transformed_red_block) > 0):
        if(not np.array_equal(red_block, transformed_red_block)):
            if(is_horizontal(red_block) and is_vertical(transformed_red_block)):
                transformation = "rotation"
            elif(is_vertical(red_block) and is_vertical(transformed_red_block)):
                transformation = "translation"

    return {
        "red_shape": red_shape,
        "red_center": red_center.tolist() if red_center is not None else None,
        "num_green": num_green,
        "transformation": transformation,
    }

task = 'd511f180'
train_data = [
    [
        [[0, 3, 0, 0, 0, 0, 0, 0, 0], [3, 3, 3, 0, 0, 0, 0, 0, 0], [0, 3, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 2, 2, 2, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0]],
        [[0, 3, 0, 0, 0, 0, 0, 0, 0], [3, 3, 3, 0, 0, 0, 0, 0, 0], [0, 3, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 2, 0, 0, 0, 0], [0, 0, 0, 0, 2, 0, 0, 0, 0], [0, 0, 0, 0, 2, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0]],
    ],
    [
        [[0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 2, 0, 0, 0, 0, 0], [0, 0, 0, 2, 0, 0, 0, 0, 0], [0, 0, 0, 2, 0, 0, 0, 0, 0], [0, 0, 0, 3, 3, 3, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0]],
        [[0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 2, 0, 0, 0, 0, 0], [0, 0, 0, 2, 0, 0, 0, 0, 0], [0, 0, 0, 2, 0, 0, 0, 0, 0], [0, 0, 0, 3, 3, 3, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0]],
    ],
    [
        [[0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 2, 0, 0, 0, 0, 0], [0, 0, 0, 2, 0, 0, 0, 0, 0], [0, 0, 0, 2, 0, 0, 0, 0, 0], [0, 0, 0, 3, 3, 3, 3, 3, 3], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0]],
        [[0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 2, 0, 0, 0, 0, 0], [0, 0, 0, 2, 0, 0, 0, 0, 0], [0, 0, 0, 3, 3, 3, 3, 3, 3], [0, 0, 0, 2, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0]],
    ],
]

results = [analyze_example(np.array(inp), np.array(out)) for inp, out in train_data]

print(results)
