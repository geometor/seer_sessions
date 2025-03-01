def analyze_example(example):
    input_grid = example['input']
    expected_output_grid = example['output']
    predicted_output_grid = transform(input_grid)

    input_shape = (len(input_grid), len(input_grid[0]) if input_grid else 0)
    expected_output_shape = (len(expected_output_grid), len(expected_output_grid[0]) if expected_output_grid else 0)
    predicted_output_shape = (len(predicted_output_grid), len(predicted_output_grid[0]) if predicted_output_grid else 0 )

    correct_pixels = 0
    total_pixels = 0

    if predicted_output_shape == expected_output_shape:
      total_pixels = expected_output_shape[0] * expected_output_shape[1]
      for r in range(expected_output_shape[0]):
          for c in range(expected_output_shape[1]):
              if predicted_output_grid[r][c] == expected_output_grid[r][c]:
                  correct_pixels += 1
    
    accuracy = (correct_pixels / total_pixels) * 100 if total_pixels > 0 else 0

    print(f"Input Shape: {input_shape}")
    print(f"Expected Output Shape: {expected_output_shape}")
    print(f"Predicted Output Shape: {predicted_output_shape}")
    print(f"Pixel Accuracy: {accuracy:.2f}% ({correct_pixels}/{total_pixels})\n")
    print(f"Input grid: {input_grid}")
    print(f"Predicted output: {predicted_output_grid}")
    print(f"Expected output: {expected_output_grid}\n")
    print("---")

examples = task["train"]

for i, example in enumerate(examples):
    print(f"Example {i+1}:")
    analyze_example(example)
