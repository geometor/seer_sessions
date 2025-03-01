# Example of Analysis (Conceptual - can't directly execute)
import numpy as np

def analyze_results(input_grid, expected_output, predicted_output):
    input_gray_objects = count_connected_components(input_grid, 5)
    output_gray_objects = count_connected_components(expected_output, 5)
    predicted_gray_objects = count_connected_components(predicted_output, 5)

    input_gray_pixels = np.sum(input_grid == 5)
    output_gray_pixels = np.sum(expected_output == 5)
    predicted_gray_pixels = np.sum(predicted_output == 5)
    
    diff_grid = (expected_output != predicted_output).astype(int)
    num_errors = np.sum(diff_grid)
    error_positions = np.where(diff_grid !=0)

    return {
        "input_gray_objects": input_gray_objects,
        "output_gray_objects": output_gray_objects,
        "predicted_gray_objects": predicted_gray_objects,
        "input_gray_pixels" : input_gray_pixels,
        "output_gray_pixels" : output_gray_pixels,
        "predicted_gray_pixels" : predicted_gray_pixels,
        "num_errors": num_errors,
        "error_positions": error_positions
    }

def count_connected_components(grid, color):
  # Placeholder for connected component analysis (e.g., using scipy.ndimage)
  # returns the number of connected components
  pass

# results = []
# for i in range(len(train_input)):
#   results.append( analyze_results(train_input[i],train_output[i], transform(train_input[i])) )
# print(results)