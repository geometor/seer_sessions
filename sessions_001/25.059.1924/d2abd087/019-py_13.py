import numpy as np
from scipy.ndimage import label

def analyze_example(input_grid, output_grid):
    """
    Analyzes a single input-output pair.
    Identifies and counts distinct gray regions in the input and output grids.
    """

    # Find gray regions in input
    gray_pixels_input = (input_grid == 5)
    labeled_input, num_features_input = label(gray_pixels_input)

    # Find gray regions in output
    gray_pixels_output = (output_grid == 5)
    labeled_output, num_features_output = label(gray_pixels_output)

    # Analyze how colors change
    color_changes = {}
    if num_features_input > 0:
        for i in range(1, num_features_input + 1):
            region_pixels = labeled_input == i
            # Find corresponding pixels output color
            output_colors = output_grid[region_pixels]
            unique_colors = np.unique(output_colors)
            color_changes[f"Input Region {i}"] = unique_colors.tolist()


    print(f"Input: {num_features_input} gray regions")
    print(f"Output: {num_features_output} gray regions")
    print(f"Color Changes: {color_changes}")
    return num_features_input, num_features_output

# Load the task data (assuming task is loaded as 'task')

for i, (train_input, train_output) in enumerate(zip(task['train_inputs'], task['train_outputs'])):
    print(f"--- Example {i+1} ---")
    analyze_example(np.array(train_input), np.array(train_output))
