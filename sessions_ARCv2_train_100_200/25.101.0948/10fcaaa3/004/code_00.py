import numpy as np

# Helper function to check adjacency
def is_adjacent(r, c, non_white_coords, H, W):
    for nr, nc in non_white_coords:
        if abs(r - nr) <= 1 and abs(c - nc) <= 1:
            # Check if it's the non-white pixel itself
            if r == nr and c == nc:
                continue
            return True
    return False

# Function implementing the revised hypothesis
def transform_revised(input_grid: list[list[int]]) -> list[list[int]]:
    input_height = len(input_grid)
    if input_height == 0: return []
    input_width = len(input_grid[0])
    if input_width == 0: return [[] for _ in range(input_height * 2)]

    # Find coordinates of non-white pixels
    non_white_coords = []
    for r in range(input_height):
        for c in range(input_width):
            if input_grid[r][c] != 0:
                non_white_coords.append((r, c))

    # Create base tile based on revised hypothesis
    base_tile = [[0 for _ in range(input_width)] for _ in range(input_height)]
    for r in range(input_height):
        for c in range(input_width):
            input_value = input_grid[r][c]
            if input_value != 0:
                base_tile[r][c] = input_value
            else:
                # Check adjacency to any non-white input pixel
                if is_adjacent(r, c, non_white_coords, input_height, input_width):
                    # Apply checkerboard
                    if (r + c) % 2 == 0:
                        base_tile[r][c] = 8
                    else:
                        base_tile[r][c] = 0
                else:
                    # Not adjacent, set to 0
                    base_tile[r][c] = 0

    # Tile the base tile 2x2
    output_height = input_height * 2
    output_width = input_width * 2
    output_grid = [[0 for _ in range(output_width)] for _ in range(output_height)]
    for r_out in range(output_height):
        for c_out in range(output_width):
            r_base = r_out % input_height
            c_base = c_out % input_width
            output_grid[r_out][c_out] = base_tile[r_base][c_base]

    return output_grid

# Function to analyze differences
def analyze_example(input_grid, expected_output):
    input_shape = np.array(input_grid).shape if input_grid else (0,0)
    expected_shape = np.array(expected_output).shape if expected_output else (0,0)

    transformed_output = transform_revised(input_grid) # Use revised transform
    transformed_shape = np.array(transformed_output).shape if transformed_output else (0,0)

    pixels_off = -1
    match = False
    size_correct = (expected_shape == transformed_shape)
    base_tile_match = False
    base_tile_pixels_off = -1

    if size_correct and expected_output and transformed_output:
        expected_np = np.array(expected_output)
        transformed_np = np.array(transformed_output)
        diff = expected_np != transformed_np
        match = not np.any(diff)
        pixels_off = int(np.sum(diff)) # Cast to int for JSON

        # Compare base tiles
        in_h, in_w = input_shape
        if in_h > 0 and in_w > 0:
             expected_base_tile = np.array([row[:in_w] for row in expected_output[:in_h]])
             transformed_base_tile = np.array([row[:in_w] for row in transformed_output[:in_h]])
             base_diff = expected_base_tile != transformed_base_tile
             base_tile_match = not np.any(base_diff)
             base_tile_pixels_off = int(np.sum(base_diff)) # Cast to int

    return {
        "input_shape": input_shape,
        "expected_output_shape": expected_shape,
        "transformed_output_shape": transformed_shape,
        "output_match": match,
        "output_pixels_off": pixels_off,
        "base_tile_match": base_tile_match,
        "base_tile_pixels_off": base_tile_pixels_off,
        "size_correct": size_correct,
    }

# --- Data ---
train_1_in = [[0,0,0],[0,4,0],[0,0,0],[0,0,0],[4,0,0]]
train_1_exp = [[8,0,8,8,0,8],[0,4,0,0,4,0],[8,0,8,8,0,8],[0,8,8,0,8,0],[4,0,0,4,0,0],[8,8,8,8,8,8],[0,4,0,0,4,0],[8,0,8,8,0,8],[0,8,8,0,8,0],[4,0,0,4,0,0]]
train_2_in = [[0,0,6,0],[0,0,0,0],[0,6,0,0]]
train_2_exp = [[0,0,6,0,0,0,6,0],[8,8,8,8,8,8,8,8],[0,6,0,8,0,6,0,8],[8,0,6,0,8,0,6,0],[8,8,8,8,8,8,8,8],[0,6,0,0,0,6,0,0]]
train_3_in = [[0,0,0,0],[0,2,0,0],[0,0,0,0],[0,0,0,0]]
train_3_exp = [[8,0,8,0,8,0,8,0],[0,2,0,0,0,2,0,0],[8,0,8,0,8,0,8,0],[0,0,0,0,0,0,0,0],[8,0,8,0,8,0,8,0],[0,2,0,0,0,2,0,0],[8,0,8,0,8,0,8,0],[0,0,0,0,0,0,0,0]]
train_4_in = [[0,0,0,0],[0,5,0,0]]
train_4_exp = [[8,0,8,0,8,0,8,0],[0,5,0,0,0,5,0,0],[8,0,8,0,8,0,8,0],[0,5,0,0,0,5,0,0]]

# --- Analysis ---
results = {}
results["train_1"] = analyze_example(train_1_in, train_1_exp)
results["train_2"] = analyze_example(train_2_in, train_2_exp)
results["train_3"] = analyze_example(train_3_in, train_3_exp)
results["train_4"] = analyze_example(train_4_in, train_4_exp)

# --- Output ---
import json
# Convert numpy shapes tuples to lists for JSON serialization
for key in results:
    results[key]["input_shape"] = list(results[key]["input_shape"])
    results[key]["expected_output_shape"] = list(results[key]["expected_output_shape"])
    results[key]["transformed_output_shape"] = list(results[key]["transformed_output_shape"])

print(json.dumps(results, indent=2))