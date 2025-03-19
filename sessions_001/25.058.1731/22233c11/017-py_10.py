import numpy as np

def analyze_example(input_grid, output_grid, predicted_grid):
    input_grid = np.array(input_grid)
    output_grid = np.array(output_grid)
    predicted_grid = np.array(predicted_grid)

    green_pixels_input = np.sum(input_grid == 3)
    azure_pixels_output = np.sum(output_grid == 8)
    green_pixels_predicted = np.sum(predicted_grid == 3)
    azure_pixels_predicted = np.sum(predicted_grid == 8)

    correct_green = np.sum((input_grid == 3) & (predicted_grid == 3))
    correct_azure = np.sum((output_grid == 8) & (predicted_grid == 8))
    incorrect_green = np.sum((input_grid != 3) & (predicted_grid == 3)) # predicted but should not
    incorrect_azure = np.sum((output_grid != 8) & (predicted_grid == 8)) # predicted but should not
    missing_green = np.sum((input_grid == 3) & (predicted_grid != 3))   # should, but not predicted
    missing_azure = np.sum((output_grid == 8) & (predicted_grid != 8)) # should, but not predicted

    print(f"Input Green Pixels: {green_pixels_input}")
    print(f"Output Azure Pixels: {azure_pixels_output}")
    print(f"Predicted Green Pixels: {green_pixels_predicted}")
    print(f"Predicted Azure Pixels: {azure_pixels_predicted}")
    print(f"Correct Green: {correct_green}")
    print(f"Correct Azure: {correct_azure}")
    print(f"Incorrect Green: {incorrect_green}")    
    print(f"Incorrect Azure: {incorrect_azure}")
    print(f"Missing Green: {missing_green}")    
    print(f"Missing Azure: {missing_azure}")    

    print("Input Grid:")
    print(input_grid)
    print("Output Grid:")
    print(output_grid)
    print("Predicted Grid:")
    print(predicted_grid)

examples = [
    (
        [[0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 3, 0], [0, 0, 0, 0, 3, 0], [0, 0, 0, 0, 3, 0], [0, 0, 0, 0, 0, 0]],
        [[0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 3, 8], [0, 0, 0, 0, 3, 0], [0, 0, 0, 0, 3, 8], [0, 0, 0, 0, 0, 0]],
        [[0, 0, 0, 0, 0, 8], [0, 0, 0, 0, 3, 0], [0, 0, 0, 0, 3, 0], [0, 0, 0, 0, 3, 0], [0, 0, 0, 0, 0, 8]]
    ),
    (
        [[0, 0, 0, 0, 0, 0, 0], [0, 0, 3, 3, 3, 0, 0], [0, 0, 0, 0, 0, 0, 0]],
        [[0, 0, 3, 3, 3, 0, 0], [0, 8, 0, 0, 0, 8, 0], [0, 0, 0, 0, 0, 0, 0]],
        [[0, 0, 3, 3, 3, 8, 0], [0, 0, 8, 0, 8, 0, 0], [0, 0, 0, 0, 0, 0, 0]]
    ),
    (
        [[0, 0, 0, 0, 0], [0, 3, 3, 3, 0], [0, 3, 0, 3, 0], [0, 3, 3, 3, 0], [0, 0, 0, 0, 0]],
        [[0, 3, 3, 3, 0], [0, 3, 0, 3, 0], [0, 3, 0, 3, 0], [0, 3, 3, 3, 0], [0, 0, 0, 0, 0]],
        [[0, 3, 3, 3, 8], [0, 3, 8, 3, 0], [0, 3, 0, 3, 8], [8, 3, 3, 3, 0], [0, 8, 0, 8, 0]]

    )
]

for i, (input_grid, output_grid, predicted_grid) in enumerate(examples):
    print(f"--- Example {i+1} ---")
    analyze_example(input_grid, output_grid, predicted_grid)