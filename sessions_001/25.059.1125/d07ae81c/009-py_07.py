import numpy as np

def analyze_pixel_counts(input_grid, output_grid):
    """
    Compares pixel counts for each color in the input and output grids.
    """
    input_grid = np.array(input_grid)
    output_grid = np.array(output_grid)
    
    input_counts = {color: np.sum(input_grid == color) for color in range(10)}
    output_counts = {color: np.sum(output_grid == color) for color in range(10)}

    print("Pixel Count Comparison:")
    for color in range(10):
        diff = output_counts[color] - input_counts[color]
        print(f"  Color {color}: Input={input_counts[color]}, Output={output_counts[color]}, Diff={diff}")
    return input_counts, output_counts

# --- Example Usage (replace with actual data) ---
# You'd loop through your examples and call this function for each pair
# input_grid, output_grid = example_data  # This would come from the ARC task data
# input_counts, output_counts = analyze_pixel_counts(input_grid, output_grid)