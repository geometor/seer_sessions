def code_execution(input_grid, output_grid):
    input_grid = np.array(input_grid)
    output_grid = np.array(output_grid)
    
    # Find the first occurence of each color.
    input_color_positions = {}
    for color in range(10):
      pos = np.where(input_grid == color)
      if len(pos[0]) > 0:
        input_color_positions[color] = (pos[0][0],pos[1][0])

    # Look for a 3x3 region
    regions = []
    for r in range(input_grid.shape[0] - 2):
        for c in range(input_grid.shape[1] - 2):
            region = input_grid[r:r+3, c:c+3]
            regions.append((region, (r,c)))

    # Check region properties
    valid_regions = []
    for region, coords in regions:
      colors_present = np.unique(region)
      if len(colors_present) > 1: #more than one non-zero color
            valid_regions.append((region, coords))

    print(f"First occurrences of colors: {input_color_positions}")
    print(f"Number of 3x3 regions: {len(regions)}")
    print(f"Number of interesting 3x3 regions (multiple non-zero colors): {len(valid_regions)}")
    #print(f"Regions: {regions}")
    print("---")

task = {
    "train": [
        {
            "input": [
                [0, 0, 0, 4, 4, 4, 0, 0, 0],
                [0, 0, 0, 4, 4, 4, 0, 0, 0],
                [0, 0, 0, 4, 4, 4, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0],
            ],
            "output": [[4, 4, 4], [4, 4, 4], [4, 4, 4]],
        },
        {
            "input": [
                [0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 4, 4, 4, 0, 0, 0],
                [0, 0, 0, 4, 4, 4, 0, 0, 0],
                [0, 0, 0, 4, 4, 4, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0],
            ],
            "output": [[4, 4, 4], [4, 4, 4], [4, 4, 4]],
        },
        {
            "input": [
                [0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 3, 3, 3, 0, 0, 0],
                [0, 0, 0, 3, 3, 3, 0, 0, 0],
                [0, 0, 0, 3, 3, 3, 0, 0, 0],
            ],
            "output": [[3, 3, 3], [3, 3, 3], [3, 3, 3]],
        },
    ]
}

for i, example in enumerate(task["train"]):
    print(f"Example {i+1}:")
    code_execution(example["input"], example["output"])
