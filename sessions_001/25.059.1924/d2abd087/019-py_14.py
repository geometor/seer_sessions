import numpy as np
from scipy.ndimage import label

def analyze_example_red(input_grid, output_grid):
    """
    Analyzes a single input-output pair, focusing on which regions becomes red.
    """

    # Find gray regions in input
    gray_pixels_input = (input_grid == 5)
    labeled_input, num_features_input = label(gray_pixels_input)
      # Find gray regions in input
    red_pixels_output = (output_grid == 2)
    labeled_red_output, num_red_features = label(red_pixels_output)

    red_region_properties = []

    if num_features_input > 0 and num_red_features > 0:

        for i in range(1, num_red_features + 1):
              red_region = labeled_red_output == i
              # Find corresponding pixels coordinates
              coords = np.where(red_region)
              min_row, min_col = np.min(coords, axis=1)

              # Check to which region corresponds in input image
              input_label_value = labeled_input[min_row, min_col]

              if input_label_value != 0:  # Ensure there's a corresponding input region
                 #get the centroid for the input regions
                 region_pixels = labeled_input == input_label_value
                 coords_input = np.where(region_pixels)

                 center_of_mass_row = np.mean(coords_input[0])
                 center_of_mass_col = np.mean(coords_input[1])

                 red_region_properties.append({
                    "input_region_index": input_label_value,
                     "min_row": min_row,
                     "min_col": min_col,
                     "center_of_mass_row":center_of_mass_row,
                     "center_of_mass_col":center_of_mass_col
                     })


    print(f"Red Region Properties: {red_region_properties}")
    return red_region_properties

# Load the task data (assuming task is loaded as 'task')

for i, (train_input, train_output) in enumerate(zip(task['train_inputs'], task['train_outputs'])):
    print(f"--- Example {i+1} ---")
    analyze_example_red(np.array(train_input), np.array(train_output))