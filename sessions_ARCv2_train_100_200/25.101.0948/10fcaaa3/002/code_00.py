import numpy as np

def analyze_example(input_grid, expected_output, transformed_output):
    input_shape = np.array(input_grid).shape if input_grid else (0,0)
    expected_shape = np.array(expected_output).shape if expected_output else (0,0)
    transformed_shape = np.array(transformed_output).shape if transformed_output else (0,0)

    if not expected_output or not transformed_output:
        match = False
        pixels_off = -1 # Indicate N/A
        size_correct = (expected_shape == transformed_shape)

    elif expected_shape != transformed_shape:
        match = False
        pixels_off = -1 # Indicate N/A due to size mismatch
        size_correct = False
    else:
        expected_np = np.array(expected_output)
        transformed_np = np.array(transformed_output)
        diff = expected_np != transformed_np
        match = not np.any(diff)
        pixels_off = np.sum(diff)
        size_correct = True

    # Derive expected base tile
    exp_h, exp_w = expected_shape
    in_h, in_w = input_shape
    expected_base_tile = None
    if size_correct and exp_h == 2 * in_h and exp_w == 2 * in_w and in_h > 0 and in_w > 0:
         expected_base_tile = [row[:in_w] for row in expected_output[:in_h]]

    # Derive transformed base tile (based on the code's logic)
    transformed_base_tile = None
    if transformed_output and in_h > 0 and in_w > 0 and transformed_shape == (2*in_h, 2*in_w):
         transformed_base_tile = [row[:in_w] for row in transformed_output[:in_h]]


    return {
        "input_shape": input_shape,
        "expected_output_shape": expected_shape,
        "transformed_output_shape": transformed_shape,
        "match": match,
        "pixels_off": pixels_off,
        "size_correct": size_correct,
        "expected_base_tile": expected_base_tile,
        "transformed_base_tile": transformed_base_tile
    }

# Data from the prompt
train_1_in = [[0,0,0],[0,4,0],[0,0,0],[0,0,0],[4,0,0]]
train_1_exp = [[8,0,8,8,0,8],[0,4,0,0,4,0],[8,0,8,8,0,8],[0,8,8,0,8,0],[4,0,0,4,0,0],[8,8,8,8,8,8],[0,4,0,0,4,0],[8,0,8,8,0,8],[0,8,8,0,8,0],[4,0,0,4,0,0]]
train_1_trans = [[8,0,8,8,0,8],[0,4,0,0,4,0],[8,0,8,8,0,8],[0,8,0,0,8,0],[4,0,8,4,0,8],[8,0,8,8,0,8],[0,4,0,0,4,0],[8,0,8,8,0,8],[0,8,0,0,8,0],[4,0,8,4,0,8]]

train_2_in = [[0,0,6,0],[0,0,0,0],[0,6,0,0]]
train_2_exp = [[0,0,6,0,0,0,6,0],[8,8,8,8,8,8,8,8],[0,6,0,8,0,6,0,8],[8,0,6,0,8,0,6,0],[8,8,8,8,8,8,8,8],[0,6,0,0,0,6,0,0]]
train_2_trans = [[8,0,6,0,8,0,6,0],[0,8,0,8,0,8,0,8],[8,6,8,0,8,6,8,0],[8,0,6,0,8,0,6,0],[0,8,0,8,0,8,0,8],[8,6,8,0,8,6,8,0]]

train_3_in = [[0,0,0,0],[0,2,0,0],[0,0,0,0],[0,0,0,0]]
train_3_exp = [[8,0,8,0,8,0,8,0],[0,2,0,0,0,2,0,0],[8,0,8,0,8,0,8,0],[0,0,0,0,0,0,0,0],[8,0,8,0,8,0,8,0],[0,2,0,0,0,2,0,0],[8,0,8,0,8,0,8,0],[0,0,0,0,0,0,0,0]]
train_3_trans = [[8,0,8,0,8,0,8,0],[0,2,0,8,0,2,0,8],[8,0,8,0,8,0,8,0],[0,8,0,8,0,8,0,8],[8,0,8,0,8,0,8,0],[0,2,0,8,0,2,0,8],[8,0,8,0,8,0,8,0],[0,8,0,8,0,8,0,8]]

train_4_in = [[0,0,0,0],[0,5,0,0]]
train_4_exp = [[8,0,8,0,8,0,8,0],[0,5,0,0,0,5,0,0],[8,0,8,0,8,0,8,0],[0,5,0,0,0,5,0,0]]
train_4_trans = [[8,0,8,0,8,0,8,0],[0,5,0,8,0,5,0,8],[8,0,8,0,8,0,8,0],[0,5,0,8,0,5,0,8]]

results = {}
results["train_1"] = analyze_example(train_1_in, train_1_exp, train_1_trans)
results["train_2"] = analyze_example(train_2_in, train_2_exp, train_2_trans)
results["train_3"] = analyze_example(train_3_in, train_3_exp, train_3_trans)
results["train_4"] = analyze_example(train_4_in, train_4_exp, train_4_trans)

# Format base tiles for printing
for key in results:
    if results[key]["expected_base_tile"]:
        results[key]["expected_base_tile_str"] = [" ".join(map(str, row)) for row in results[key]["expected_base_tile"]]
    if results[key]["transformed_base_tile"]:
        results[key]["transformed_base_tile_str"] = [" ".join(map(str, row)) for row in results[key]["transformed_base_tile"]]

print(results)
