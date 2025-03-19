import numpy as np

def analyze_example(input_grid, expected_output_grid, current_code_output):
    input_grid = np.array(input_grid)
    expected_output_grid = np.array(expected_output_grid)
    current_code_output = np.array(current_code_output)

    input_red_count = np.sum(input_grid == 2)
    expected_output_blue_count = np.sum(expected_output_grid == 1)
    current_output_blue_count = np.sum(current_code_output == 1)

    dimensions_match = input_grid.shape == expected_output_grid.shape
    correct_pixels = np.sum(current_code_output == expected_output_grid)
    total_pixels_expected = expected_output_grid.size
    accuracy = correct_pixels / total_pixels_expected if total_pixels_expected > 0 else 0


    print(f"Input Red Pixel Count: {input_red_count}")
    print(f"Expected Output Blue Pixel Count: {expected_output_blue_count}")
    print(f"Current Output Blue Pixel Count: {current_output_blue_count}")
    print(f"Dimensions Match (Input vs. Expected Output): {dimensions_match}")
    print(f"Accuracy (Correct Pixels / Total Expected Pixels): {accuracy:.2f}")
    print(f"Input Shape: {input_grid.shape}")
    print(f"Expected Output Shape: {expected_output_grid.shape}")
    print(f"Current Code Output Shape: {current_code_output.shape}")


# Example Usage (using the hypothetical data above)
input_grid = [[0, 0, 2, 2], [0, 0, 2, 2], [0, 0, 0, 0]]
expected_output = [[1, 1], [1, 1]]
current_output = [[0, 0, 1, 1], [0, 0, 1, 1], [0, 0, 0, 0]]

analyze_example(input_grid, expected_output, current_output)
