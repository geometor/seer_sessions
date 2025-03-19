def code_execution(input_grid, output_grid, predicted_output, example_id):
    input_grid = np.array(input_grid)
    output_grid = np.array(output_grid)
    predicted_output = np.array(predicted_output)

    input_dims = input_grid.shape
    output_dims = output_grid.shape
    predicted_dims = predicted_output.shape

    correct = np.array_equal(output_grid, predicted_output)

    print(f"Example {example_id}:")
    print(f"  Input Dimensions: {input_dims}")
    print(f"  Output Dimensions: {output_dims}")
    print(f"  Predicted Dimensions: {predicted_dims}")
    print(f"  Correct Prediction: {correct}")
    print(f"  Input: \n{input_grid}")
    print(f"  Output: \n{output_grid}")
    print(f"  Predicted: \n{predicted_output}")

# Assuming 'train' contains the training examples
for i, example in enumerate(train):
     predicted_output = transform(example['input'])
     code_execution(example['input'], example['output'], predicted_output, i + 1)
