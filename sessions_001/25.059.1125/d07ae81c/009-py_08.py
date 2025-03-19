def analyze_pixel_displacement(input_grid, output_grid):
    """
    Analyzes the displacement of each pixel from input to output.
    """
    input_grid = np.array(input_grid)
    output_grid = np.array(output_grid)
    rows, cols = input_grid.shape

    print("Pixel Displacement Analysis:")
    for r in range(rows):
        for c in range(cols):
            input_color = input_grid[r, c]
            # Find where this pixel moved to in the output
            output_locations = np.argwhere(output_grid == input_color)
            print(f"Pixel at ({r}, {c}) - Color {input_color}:")
            if output_locations.size > 0:
                for out_r, out_c in output_locations:
                    print(f"  Moved to: ({out_r}, {out_c})")
            else:
                print("  Disappeared!") #or it might change color

# --- Example Usage ---
# input_grid, output_grid = example_data
# analyze_pixel_displacement(input_grid, output_grid)
