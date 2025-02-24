def check_results(task_examples):
    for i, example in enumerate(task_examples):
        input_grid = example["input"]
        expected_output = example["output"]

        print(f"Example {i+1}:")
        print(f"  Input Dimensions: {input_grid.shape}")
        print(f"  Expected Output Dimensions: {expected_output.shape}")

        series = get_series(input_grid)
        print(f"  Identified Series: {series}")

        transformed_output = transform(input_grid)
        print(f"  Transformed Output Dimensions: {transformed_output.shape}")
         # Check series color in tranformed output
        for s in series:
          start, end, direction, color = s
          if direction == 'horizontal':
            for j in range(start[1],min(start[1]+2, transformed_output.shape[1])):
              if transformed_output[start[0],j] != color:
                print(f"  Color mismatch in series {s}")
          if direction == 'vertical':
            for j in range(start[0],min(start[0]+2, transformed_output.shape[0])):
              if transformed_output[j,start[1]] != color:
                print(f"  Color mismatch in series {s}")
        # Pixel-by-pixel comparison
        diff = (transformed_output != expected_output)
        if np.any(diff):
            diff_coords = np.where(diff)
            print(f"  Pixel Differences (Transformed vs Expected):")
            for r, c in zip(*diff_coords):
                print(
                    f"    - ({r}, {c}): Transformed={transformed_output[r, c]}, Expected={expected_output[r, c]}"
                )
        else:
            print("  Transformed output matches expected output.")
        print("-" * 40)

# Assuming 'train' contains the training examples
check_results(train)