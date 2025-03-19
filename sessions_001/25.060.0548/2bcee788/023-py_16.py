def code_execution(input_grid, output_grid, caption):
    # uses input_grid and output_grid from the example
    # original_grid is the result of the current transform() function
    original_grid = transform(input_grid.copy())

    # compare pixel counts for colors
    print(f"--- {caption} ---")
    print(f"Input  : azure={np.sum(input_grid == 8)}, red={np.sum(input_grid == 2)}, white={np.sum(input_grid == 0)}")
    print(f"Output : azure={np.sum(output_grid == 8)}, red={np.sum(output_grid == 2)}, white={np.sum(output_grid == 0)}")
    print(f"Original: azure={np.sum(original_grid == 8)}, red={np.sum(original_grid == 2)}, white={np.sum(original_grid == 0)}")

    # compare dimensions
    print(f"Input  : shape={input_grid.shape}")
    print(f"Output : shape={output_grid.shape}")
    print(f"Original: shape={original_grid.shape}")
    
    # check for equivalence in output and result from transform()
    print(f"   Identical to Output: {np.array_equal(original_grid,output_grid)}")    