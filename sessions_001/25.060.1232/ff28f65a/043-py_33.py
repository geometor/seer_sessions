import numpy as np

def analyze_example(input_grid, output_grid):
    input_height, input_width = input_grid.shape
    output_height, output_width = output_grid.shape

    row_ratio = input_height / output_height
    col_ratio = input_width / output_width

    # Count of red pixels in the input
    red_pixels_input = np.sum(input_grid == 2)

    # Count of blue pixels in the output.
    blue_pixels_output = np.sum(output_grid == 1)

    print(f"  Input Dimensions: {input_height}x{input_width}")
    print(f"  Output Dimensions: {output_height}x{output_width}")
    print(f"  Row Ratio: {row_ratio}")
    print(f"  Column Ratio: {col_ratio}")
    print(f"  Red Pixels (Input): {red_pixels_input}")
    print(f"  Blue Pixels (Output): {blue_pixels_output}")

# Example Usage:
input_grid_ex1 = np.array([[0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0],
                           [0, 0, 2, 2, 0, 0],
                           [0, 0, 2, 2, 0, 0],
                           [0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0]])

output_grid_ex1 = np.array([[0, 0],
                            [0, 1]])

analyze_example(input_grid_ex1, output_grid_ex1)


input_grid_ex2 = np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 2, 2, 2, 0, 0, 0, 0],
                           [0, 0, 0, 2, 2, 2, 0, 0, 0, 0],
                           [0, 0, 0, 2, 2, 2, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]])
output_grid_ex2 = np.array([[0, 0, 0],
                            [0, 1, 0],
                            [0, 0, 0]])
analyze_example(input_grid_ex2, output_grid_ex2)

input_grid_ex3 = np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0, 2, 2, 2, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0, 2, 2, 2, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0, 2, 2, 2, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]])
output_grid_ex3 = np.array([[0,0,0,0,0],
                            [0,0,1,0,0],
                            [0,0,0,0,0]])
analyze_example(input_grid_ex3, output_grid_ex3)
