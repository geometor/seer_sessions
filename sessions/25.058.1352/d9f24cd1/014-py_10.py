import numpy as np

def analyze_examples(examples):
    results = []
    for i, example in enumerate(examples):
        input_grid = example["input"]
        output_grid = example["output"]
        
        # Find gray pixels
        gray_pixels_input = np.where(input_grid == 5)
        gray_pixels_output = np.where(output_grid == 5)
        
        # Find red pixels
        red_pixels_input = np.where(input_grid == 2)
        red_pixels_output = np.where(output_grid == 2)
        
        # Find white pixels (important for checking for error)
        white_pixels_input = np.where(input_grid == 0)
        white_pixels_output = np.where(output_grid == 0)

        # Find red pixels on last row of input
        bottom_row_red = np.where(input_grid[-1] == 2)

        results.append(
            {
                "example_number": i + 1,
                "input_shape": input_grid.shape,
                "output_shape": output_grid.shape,
                "gray_pixels_input": list(zip(gray_pixels_input[0], gray_pixels_input[1])),
                "gray_pixels_output": list(zip(gray_pixels_output[0], gray_pixels_output[1])),
                "red_pixels_input": list(zip(red_pixels_input[0], red_pixels_input[1])),
                "red_pixels_output": list(zip(red_pixels_output[0], red_pixels_output[1])),
                "white_pixels_input": list(zip(white_pixels_input[0], white_pixels_input[1])),
                "white_pixels_output": list(zip(white_pixels_output[0], white_pixels_output[1])),
                "bottom_row_red_pixels": list(bottom_row_red[0])
            }
        )
    return results


examples = [
    {
        "input": np.array([[0, 0, 0, 0, 0, 0],
                           [0, 0, 5, 0, 0, 0],
                           [0, 0, 5, 0, 0, 0],
                           [0, 0, 5, 0, 0, 0],
                           [0, 0, 2, 0, 0, 0]]),
        "output": np.array([[2, 2, 5, 2, 2, 2],
                            [2, 2, 5, 2, 2, 2],
                            [2, 2, 5, 2, 2, 2],
                            [2, 2, 5, 2, 2, 2],
                            [2, 2, 2, 2, 2, 2]]),
    },
        {
        "input": np.array([[0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 5, 0, 0, 5, 0],
                           [0, 0, 5, 0, 0, 5, 0],
                           [0, 0, 5, 0, 0, 5, 0],
                           [0, 0, 2, 0, 0, 2, 0]]),
        "output": np.array([[2, 2, 5, 2, 2, 5, 2],
                            [2, 2, 5, 2, 2, 5, 2],
                            [2, 2, 5, 2, 2, 5, 2],
                            [2, 2, 5, 2, 2, 5, 2],
                            [2, 2, 2, 2, 2, 2, 2]]),
    },
        {
        "input": np.array([[0, 0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 5, 0, 0, 0, 5, 0],
                           [0, 0, 5, 0, 0, 0, 5, 0],
                           [0, 0, 5, 0, 0, 0, 5, 0],
                           [0, 0, 2, 0, 0, 0, 2, 0]]),
        "output": np.array([[2, 2, 5, 2, 2, 2, 5, 2],
                            [2, 2, 5, 2, 2, 2, 5, 2],
                            [2, 2, 5, 2, 2, 2, 5, 2],
                            [2, 2, 5, 2, 2, 2, 5, 2],
                            [2, 2, 5, 2, 2, 2, 5, 2],
                            [2, 2, 2, 2, 2, 2, 2, 2]]),
    },
]

analysis = analyze_examples(examples)
for item in analysis:
    print(item)