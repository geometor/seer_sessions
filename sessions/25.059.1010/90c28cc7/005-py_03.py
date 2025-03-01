#Example - not actual execution
def analyze_example(input_grid, output_grid, predicted_output):
    input_height, input_width = input_grid.shape
    output_height, output_width = output_grid.shape
    predicted_height, predicted_width = predicted_output.shape
    
    input_bands = get_color_bands(input_grid)
    num_input_bands = len(input_bands)
    
    correct = np.array_equal(output_grid, predicted_output)

    print(f"  Input Dimensions: {input_height}x{input_width}")
    print(f"  Output Dimensions: {output_height}x{output_width}")
    print(f"  Predicted Dimensions: {predicted_height}x{predicted_width}")
    print(f"  Number of Input Bands: {num_input_bands}")
    print(f"  Correct Prediction: {correct}")
    print(f"  input bands: {input_bands}")
    print(f"  output: {output_grid.flatten()}")    
    print(f"  predicted: {predicted_output.flatten()}")

#mock data to test the analyzer - real values would come from arc framework
input_grid1 = np.array([[0,0,0],[1,1,1],[0,0,0],[2,2,2]])
output_grid1 = np.array([[1,2]])
predicted_output1 = np.array([[1,2]])

input_grid2 = np.array([[0,0,0],[3,3,3],[0,0,0],[4,4,4],[0,0,0],[5,5,5]])
output_grid2 = np.array([[3,4,5]])
predicted_output2 = np.array([[3,4,5]])

input_grid3 = np.array([[0,0,0],[6,6,6],[7,7,7],[8,8,8]])
output_grid3 = np.array([[6,7,8]])
predicted_output3 = np.array([[6,7,8]])

examples = [
    (input_grid1, output_grid1, predicted_output1),
    (input_grid2, output_grid2, predicted_output2),
    (input_grid3, output_grid3, predicted_output3)
]

for i, (input_grid, output_grid, predicted_output) in enumerate(examples):
    print(f"Example {i+1}:")
    analyze_example(input_grid, output_grid, predicted_output)