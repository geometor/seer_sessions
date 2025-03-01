import numpy as np

def find_object_by_color(grid, color):
    """Finds the coordinates of all pixels of a specific color."""
    return np.argwhere(grid == color)

def analyze_example(input_grid, output_grid, example_number):
    """Analyzes a single input-output pair and prints relevant information."""

    print(f"--- Example {example_number} ---")
    print(f"Input grid shape: {input_grid.shape}")
    print(f"Output grid shape: {output_grid.shape}")

    # Find azure pixels
    azure_pixels_in = find_object_by_color(input_grid, 8)
    azure_pixels_out = find_object_by_color(output_grid, 8)
    if azure_pixels_in.size > 0:
        print(f"Azure pixel (input) positions: {azure_pixels_in}")
    else:
      print("No azure pixels in input")
    if azure_pixels_out.size > 0:
      print(f"Azure pixel (output) positions: {azure_pixels_out}")
    else:
      print("No azure pixels in output")
        

    # Find red pixels
    red_pixels_in = find_object_by_color(input_grid, 2)
    if red_pixels_in.size > 0:
      print(f"Red pixel (input) positions: {red_pixels_in}")
    else:
      print("No red pixels in input")

    # Find green pixels in output
    green_pixels_out = find_object_by_color(output_grid, 3)
    if green_pixels_out.size > 0:
        print(f"Green pixel (output) positions: {green_pixels_out}")
        # Find top-most and bottom-most green pixel
        top_green = green_pixels_out[0]
        bottom_green = green_pixels_out[-1]
        print(f"Top-most green pixel: {top_green}")
        print(f"Bottom-most green pixel: {bottom_green}")
    else:
      print("No green pixels in output")
    print()

# Assuming 'train' is a list of dictionaries, each with 'input' and 'output'
for i in range(len(train)):
    analyze_example(np.array(train[i]['input']), np.array(train[i]['output']), i + 1)