def analyze_example(example):
    input_grid = np.array(example['input'])
    output_grid = np.array(example['output'])
    blue_pixel_coords_input = find_pixel_by_color(input_grid, 1)
    
    input_shape = input_grid.shape
    output_shape = output_grid.shape
    
    print(f"  Input shape: {input_shape}")
    print(f"  Output shape: {output_shape}")
    print(f"  Blue pixel coordinates in input: {blue_pixel_coords_input}")
    print(f"  Output grid is equal to input grid: {np.array_equal(input_grid,output_grid)}")

print("Example 0:")
analyze_example(task["train"][0])
print("\nExample 1:")
analyze_example(task["train"][1])
print("\nExample 2:")
analyze_example(task["train"][2])
print("\nExample 3:")
analyze_example(task["train"][3])
