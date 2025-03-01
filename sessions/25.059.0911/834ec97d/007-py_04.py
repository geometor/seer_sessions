import numpy as np

def find_pixel_by_color(grid, color_value):
    # Find the coordinates of a pixel with the specified color value.
    coords = np.where(grid == color_value)
    if len(coords[0]) > 0:
        return [coords[0][0], coords[1][0]]  # return first occurance
    return None

def find_all_pixels_by_color(grid, color_value):
    # Find the coordinates of all pixels with the specified color value.
    rows, cols = np.where(grid == color_value)
    return list(zip(rows, cols))

def analyze_example(input_grid, expected_output_grid, predicted_output_grid):
    input_red_pixels = find_all_pixels_by_color(input_grid, 2)
    input_yellow_pixels = find_all_pixels_by_color(input_grid, 4)
    expected_red_pixels = find_all_pixels_by_color(expected_output_grid, 2)
    expected_yellow_pixels = find_all_pixels_by_color(expected_output_grid, 4)
    predicted_red_pixels = find_all_pixels_by_color(predicted_output_grid, 2)
    predicted_yellow_pixels = find_all_pixels_by_color(predicted_output_grid, 4)


    print(f"  Input Red Pixels: {input_red_pixels}")
    print(f"  Input Yellow Pixels: {input_yellow_pixels}")
    print(f"  Expected Output Red Pixels: {expected_red_pixels}")
    print(f"  Expected Output Yellow Pixels: {expected_yellow_pixels}")
    print(f"  Predicted Output Red Pixels: {predicted_red_pixels}")
    print(f"  Predicted Output Yellow Pixels: {predicted_yellow_pixels}")
    print("-" * 20)

# Assuming 'task' is loaded with training examples
for i, example in enumerate(task["train"]):
    print(f"Example {i+1}:")
    predicted_output = transform(np.array(example["input"]))
    analyze_example(np.array(example["input"]), np.array(example["output"]), predicted_output)
