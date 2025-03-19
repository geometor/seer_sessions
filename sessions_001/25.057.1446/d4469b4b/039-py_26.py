def describe_grid(grid, name):
    print(f"{name} Grid:")
    print(f"  Shape: {grid.shape}")
    print(f"  Values:\n{grid}")
    #find location of green pixels
    green_coords = [(i, j) for i, row in enumerate(grid) for j, val in enumerate(row) if val == 3]
    white_coords = [(i, j) for i, row in enumerate(grid) for j, val in enumerate(row) if val == 0]
    print(f"    Green Pixels: {green_coords}")    
    print(f"    White Pixels: {white_coords}")

# Accessing the examples directly
for i, example in enumerate(task_data['train']):
    print(f"\nExample {i + 1}:")
    describe_grid(np.array(example['input']), "Input")
    describe_grid(np.array(example['output']), "Output")
