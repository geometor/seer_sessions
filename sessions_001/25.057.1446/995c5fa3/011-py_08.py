# Assuming 'train' is a list of dictionaries, each with 'input' and 'output'
for example_number, example in enumerate(train):
    input_grid = example['input']
    output_grid = example['output']
    predicted_output = transform(input_grid)

    print(f"Example {example_number + 1}:")
    print(f"  Input Dimensions: {np.array(input_grid).shape}")
    print(f"  Output Dimensions: {np.array(output_grid).shape}")
    print(f"  Predicted Dimensions: {np.array(predicted_output).shape}")
    print(f"  Match: {output_grid == predicted_output}")

