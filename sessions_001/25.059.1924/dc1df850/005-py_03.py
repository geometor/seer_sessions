import numpy as np

def analyze_examples(examples):
    results = []
    for i, example in enumerate(examples):
        input_grid = np.array(example['input'])
        expected_output_grid = np.array(example['output'])

        # Find rightmost red pixel
        red_pixels = np.argwhere(input_grid == 2)
        rightmost_red_col = np.max(red_pixels[:, 1]) if len(red_pixels) > 0 else -1

        # Find magenta pixel
        magenta_pixels = np.argwhere(input_grid == 6)
        magenta_row = magenta_pixels[0][0] if len(magenta_pixels) > 0 else -1
        magenta_col = magenta_pixels[0][1] if len(magenta_pixels) > 0 else -1

        # Find blue pixels in the expected output
        blue_pixels_output = np.argwhere(expected_output_grid == 1)
        
        # derive predicted output
        predicted_output = transform(input_grid)
        
        # Find if blue is filled and its boundaries in expected
        blue_filled_expected = len(blue_pixels_output) > 0
        blue_top_expected = np.min(blue_pixels_output[:, 0]) if blue_filled_expected else -1
        blue_left_expected = np.min(blue_pixels_output[:, 1]) if blue_filled_expected else -1
        blue_right_expected = np.max(blue_pixels_output[:, 1]) if blue_filled_expected else -1
        blue_bottom_expected = np.max(blue_pixels_output[:, 0]) if blue_filled_expected else -1

        #check if the transform function worked
        correct = np.array_equal(expected_output_grid,predicted_output)

        results.append({
            'example_index': i,
            'rightmost_red_col': rightmost_red_col,
            'magenta_row': magenta_row,
            'magenta_col': magenta_col,
            'blue_filled_expected': blue_filled_expected,
            'blue_top_expected': blue_top_expected,
            'blue_left_expected': blue_left_expected,
            'blue_right_expected' : blue_right_expected,
            'blue_bottom_expected': blue_bottom_expected,
            'transform_correct': correct
        })

    return results

# Assuming 'train' contains the training examples
examples_data = analyze_examples(train)

for result in examples_data:
    print(result)
