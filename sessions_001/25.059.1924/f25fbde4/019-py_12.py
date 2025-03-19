def code_execution(input_grid, expected_output, generated_output):
    """Executes the transform function and compares the output.
      Also provides metrics and simple descriptions.
    """
    input_grid_np = np.array(input_grid)
    expected_output_np = np.array(expected_output)
    generated_output_np = np.array(generated_output)
    
    input_shape = input_grid_np.shape
    output_shape = expected_output_np.shape
    generated_shape = generated_output_np.shape
    
    correct = np.array_equal(expected_output_np, generated_output_np)

    print(f"  Input shape: {input_shape}")
    print(f"  Expected output shape: {output_shape}")
    print(f"  Generated output shape: {generated_shape}")    
    print(f"  Correctly generated: {correct}")

# Example usage (assuming 'train' contains the examples)
# Example usage
for i, example in enumerate(train):
  print (f"Example: {i +1}")
  generated_output = transform(example['input'])
  code_execution(example['input'], example['output'], generated_output)