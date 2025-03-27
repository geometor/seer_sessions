import numpy as np

def transform(input_grid: np.ndarray) -> np.ndarray:
    """
    Creates an output grid by selecting pixels from the input grid where both the
    row and column indices are even. The selected pixel at input coordinates
    (r_in, c_in) is placed at output coordinates (r_in / 2, c_in / 2).
    The output grid dimensions are half the input grid dimensions.
    """

    # Get input grid dimensions
    input_height, input_width = input_grid.shape

    # Calculate output grid dimensions
    output_height = input_height // 2
    output_width = input_width // 2

    # Initialize the output grid with white (0)
    output_grid = np.zeros((output_height, output_width), dtype=input_grid.dtype)

    # Iterate through the input grid
    for r_in in range(input_height):
        for c_in in range(input_width):
            # Check if both row and column indices are even
            if r_in % 2 == 0 and c_in % 2 == 0:
                # Calculate corresponding output coordinates
                r_out = r_in // 2
                c_out = c_in // 2
                
                # Check if output coordinates are within bounds (should always be true given the logic)
                if 0 <= r_out < output_height and 0 <= c_out < output_width:
                    # Copy the pixel value from input to output
                    output_grid[r_out, c_out] = input_grid[r_in, c_in]

    return output_grid