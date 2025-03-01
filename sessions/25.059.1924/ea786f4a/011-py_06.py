import numpy as np

def analyze_example(input_grid, output_grid, example_number):
    print(f"--- Example {example_number} ---")
    print(f"Input Grid Shape: {input_grid.shape}")
    print(f"Output Grid Shape: {output_grid.shape}")

    # Find the white pixel in the input grid
    input_white_pixels = np.where(input_grid == 0)
    print(f"Input White Pixel Coordinates: {list(zip(input_white_pixels[0], input_white_pixels[1]))}")

    # Find the white pixels in the output grid
    output_white_pixels = np.where(output_grid == 0)
    print(f"Output White Pixel Coordinates: {list(zip(output_white_pixels[0], output_white_pixels[1]))}")

    # Check if shapes are the same
    print(f"Input and Output Shapes Match: {input_grid.shape == output_grid.shape}")
    
    # compare that all non-white pixels are red in both input and output
    input_red_pixels = np.where(input_grid == 2)
    output_red_pixels = np.where(output_grid == 2)
    print(f"Input and Output Red Pixels are identical except center: {np.array_equal(input_grid[input_red_pixels], output_grid[output_red_pixels])}")
    


# Provided examples (replace with actual data)
examples = [
    (np.array([[2, 2, 2], [2, 0, 2], [2, 2, 2]]), np.array([[2, 0, 2], [0, 0, 0], [2, 0, 2]])),
    (np.array([[2, 2, 2, 2, 2], [2, 2, 2, 2, 2], [2, 2, 0, 2, 2], [2, 2, 2, 2, 2], [2, 2, 2, 2, 2]]), np.array([[2, 2, 2, 2, 2], [2, 2, 0, 2, 2], [2, 0, 0, 0, 2], [2, 2, 0, 2, 2], [2, 2, 2, 2, 2]])),
    (np.array([[2, 2, 2, 2, 2, 2, 2], [2, 2, 2, 2, 2, 2, 2], [2, 2, 2, 2, 2, 2, 2], [2, 2, 2, 0, 2, 2, 2], [2, 2, 2, 2, 2, 2, 2], [2, 2, 2, 2, 2, 2, 2], [2, 2, 2, 2, 2, 2, 2]]), np.array([[2, 2, 2, 2, 2, 2, 2], [2, 2, 2, 2, 2, 2, 2], [2, 2, 2, 2, 2, 2, 2], [2, 2, 0, 0, 0, 2, 2], [2, 2, 2, 2, 2, 2, 2], [2, 2, 2, 2, 2, 2, 2], [2, 2, 2, 2, 2, 2, 2]])),
]

for i, (input_grid, output_grid) in enumerate(examples):
    analyze_example(input_grid, output_grid, i + 1)
