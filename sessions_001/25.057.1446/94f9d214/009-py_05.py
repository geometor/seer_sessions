import numpy as np

def code_execution(input_grid, output_grid, predicted_output):
    """
    Executes code and provides information about the grids
    """

    input_grid = np.array(input_grid)
    output_grid = np.array(output_grid)
    predicted_output = np.array(predicted_output)

    input_shape = input_grid.shape
    output_shape = output_grid.shape
    predicted_shape = predicted_output.shape

    input_non_white_pixels = np.argwhere(input_grid != 0)
    output_non_white_pixels = np.argwhere(output_grid != 0)

    print(f"Input shape: {input_shape}")
    print(f"Output shape: {output_shape}")
    print(f"Predicted Output Shape: {predicted_shape}")
    print(f"Input non-white pixel locations: {input_non_white_pixels}")
    print(f"Output non-white pixel locations: {output_non_white_pixels}")
    print(f"Correct Prediction: {np.array_equal(output_grid, predicted_output)}")

# Example data (replace with your actual data)
examples = [
  (
        [[0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 1, 0]],

        [[0, 0],
        [0, 2]]
    ),
    (
        [[0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 4, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0]],

        [[0, 0],
        [2, 0]]
    ),
     (
        [[0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 3, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0]],

        [[0, 2],
        [0, 0]]
    ),
    (
      [[0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 5, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0]],
        [[0,2],
         [0,0]]

    )
]

for input_grid, output_grid in examples:
    # Get predicted output using your transform function
    predicted_output = transform(input_grid)
    code_execution(input_grid, output_grid, predicted_output)
