def code_execution(input_grid, output_grid, transformed_grid):
    print(f"Input:\n{input_grid}")
    print(f"Expected Output:\n{output_grid}")
    print(f"Transformed:\n{transformed_grid}")
    print(f"Matches Expected: {np.array_equal(output_grid, transformed_grid)}")
    #find diff
    diff = np.where(input_grid != output_grid)
    print(f"Difference Location: {diff}")
    if (len(diff) > 0 and len(diff[0])>0):
        print(f"Input Value: {input_grid[diff]}")
        print(f"Output Value: {output_grid[diff]}")

    #find blue
    blue_pixels_input = np.where(input_grid == 1)
    print(f"Blue Pixels input: {blue_pixels_input}")
    blue_pixels_output = np.where(output_grid == 1)
    print(f"Blue Pixels output: {blue_pixels_output}")
    #find green
    green_pixels_input = np.where(input_grid == 3)
    print(f"green Pixels input: {green_pixels_input}")
    green_pixels_output = np.where(output_grid == 3)
    print(f"green Pixels output: {green_pixels_output}")

    # Check if the transform function modifies the input grid in place
    print(f"Input grid modified: {not np.array_equal(input_grid, transformed_grid)}")

example_data = [
  ([
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 1, 0, 0, 0, 0, 0],
    [0, 0, 1, 1, 1, 0, 0, 0, 0],
    [0, 0, 0, 1, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 1, 0, 0, 0, 0, 0],
    [0, 0, 0, 1, 0, 0, 0, 0, 0],
    [0, 0, 0, 1, 0, 0, 0, 0, 0]
  ],
  [
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 3, 0, 0, 0, 0, 0],
    [0, 0, 3, 3, 3, 0, 0, 0, 0],
    [0, 0, 0, 3, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 1, 0, 0, 0, 0, 0],
    [0, 0, 0, 1, 0, 0, 0, 0, 0],
    [0, 0, 0, 1, 0, 0, 0, 0, 0]
  ]),
  ([
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 1, 0, 0, 0, 0, 0, 0],
    [0, 1, 0, 0, 0, 0, 0, 0],
    [0, 1, 0, 0, 0, 0, 0, 0],
    [0, 1, 0, 0, 0, 0, 0, 0]
  ],
  [
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 3, 0, 0, 0, 0, 0, 0],
    [0, 3, 0, 0, 0, 0, 0, 0],
    [0, 3, 0, 0, 0, 0, 0, 0],
    [0, 3, 0, 0, 0, 0, 0, 0]
  ]),
  ([
      [0,0,0,0,0],
      [0,0,1,0,0],
      [0,0,1,0,0],
      [0,0,0,0,0],
  ],
  [
      [0,0,0,0,0],
      [0,0,3,0,0],
      [0,0,3,0,0],
      [0,0,0,0,0],
  ]),
    ([
      [0,0,0,0,0,0],
      [0,0,1,0,0,0],
      [0,0,1,0,0,0],
      [0,0,0,0,0,0],
  ],
  [
      [0,0,0,0,0,0],
      [0,0,3,0,0,0],
      [0,0,3,0,0,0],
      [0,0,0,0,0,0],
  ])
]

for i in range(0, len(example_data), 2):
    input_grid = np.array(example_data[i])
    output_grid = np.array(example_data[i+1])
    transformed_grid = transform(input_grid)
    print(f"Example {i//2 + 1}:")
    code_execution(input_grid, output_grid, transformed_grid)
    print("-" * 40)