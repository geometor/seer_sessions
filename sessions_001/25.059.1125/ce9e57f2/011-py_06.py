def report(grid, title="Grid"):
    rows, cols = grid.shape
    unique_colors = np.unique(grid)
    color_counts = {color: np.count_nonzero(grid == color) for color in unique_colors}

    print(f"--- {title} ---")
    print(f"Dimensions: {rows}x{cols}")
    print(f"Unique Colors: {unique_colors}")
    print(f"Color Counts: {color_counts}")
    red_stacks = find_red_stacks(grid)

    total_red_stack_height = sum(len(stack) for stack in red_stacks)
    print(f"Number of Red Stacks: {len(red_stacks)}")
    print(f"Red Stack Heights: {[len(stack) for stack in red_stacks]}")
    print(f"Total Red Stack Height (pixels): {total_red_stack_height}")
    print()

# display all example results
for idx, example in enumerate(task["train"]):
  input_grid = np.array(example["input"])
  output_grid = np.array(example["output"])

  report(input_grid, title=f"Input {idx}")
  report(output_grid, title=f"Output {idx}")
  
  transformed_grid = transform(input_grid)
  report(transformed_grid, title=f"Predicted {idx}")
  
  print(f"Correct: {np.array_equal(transformed_grid, output_grid)}")