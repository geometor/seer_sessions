def analyze_example(input_grid, output_grid, predicted_output):
    import numpy as np

    input_grid = np.array(input_grid)
    output_grid = np.array(output_grid)
    predicted_output = np.array(predicted_output)

    orange_pixels = np.argwhere(input_grid == 7)
    if orange_pixels.size > 0:
        min_row, min_col = np.min(orange_pixels, axis=0)
        max_row, max_col = np.max(orange_pixels, axis=0)
        orange_bounding_box = (min_row, min_col, max_row + 1, max_col + 1)  # +1 for inclusive
        orange_shape_size = (max_row - min_row + 1, max_col - min_col + 1)
    else:
        orange_bounding_box = (0, 0, 0, 0)
        orange_shape_size = (0, 0)

    green_pixels_output = np.argwhere(output_grid == 3)

    comparison = output_grid == predicted_output
    all_match = np.all(comparison)


    report = {
        "input_dimensions": input_grid.shape,
        "orange_pixels": orange_pixels.tolist(),
        "orange_bounding_box": orange_bounding_box,
        "orange_shape_size": orange_shape_size,
        "output_dimensions": output_grid.shape,
        "green_pixels_output": green_pixels_output.tolist(),
        "all_match": all_match

    }
    return report

# Example Usage (assuming you have the input_grid, output_grid, and predicted_output)
# Replace with actual data from the examples
results = []
for i in range(len(train_input_output_list)):
    predicted_output = transform(train_input_output_list[i][0])
    analysis = analyze_example(train_input_output_list[i][0], train_input_output_list[i][1], predicted_output)
    results.append(analysis)


for i,res in enumerate(results):
    print (f"Example {i}:")
    print (res)
