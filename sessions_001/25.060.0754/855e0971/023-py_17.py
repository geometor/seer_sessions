import numpy as np

def analyze_example(input_grid, output_grid):
    """
    Analyzes a single input-output pair and gathers relevant metrics.
    """
    input_grid = np.array(input_grid)
    output_grid = np.array(output_grid)

    def get_regions(grid):
      rows, cols = grid.shape
      red_region = []
      grey_region = []
      yellow_region = []
      for r in range(rows):
        for c in range(cols):
          if grid[r,c] == 2:
            red_region.append((r,c))
          if grid[r,c] == 5:
            grey_region.append((r,c))
          if grid[r,c] == 4:
              yellow_region.append((r,c))
      return red_region, grey_region, yellow_region

    red_region_in, grey_region_in, yellow_region_in = get_regions(input_grid)
    red_region_out, grey_region_out, yellow_region_out = get_regions(output_grid)

    input_dims = input_grid.shape
    output_dims = output_grid.shape

    print(f"  Input Dimensions: {input_dims}")
    print(f"  Output Dimensions: {output_dims}")
    print(f"  Red Region (Input): {red_region_in}")
    print(f"  Grey Region (Input): {grey_region_in}")
    print(f"  Yellow region (Input): {yellow_region_in}")
    print(f"  Red Region (Output): {red_region_out}")
    print(f"  Grey Region (Output): {grey_region_out}")
    print(f" Yellow Region (Output): {yellow_region_out}")



    # Check for white pixels in the grey region of the input
    white_pixels_grey_input = [(r, c) for r, c in grey_region_in if input_grid[r, c] == 0]
    print(f"  White Pixels in Grey Region (Input): {white_pixels_grey_input}")

    # find the boundary between grey/red in both input and output, verify they are the same
    def find_boundary(region1, region2):
        boundary = []
        for r1, c1 in region1:
            for r2, c2 in region2:
                if abs(r1 - r2) + abs(c1 - c2) == 1:
                    boundary.append(((r1, c1), (r2, c2)))
        return boundary

    grey_red_boundary_in = find_boundary(grey_region_in, red_region_in)
    grey_red_boundary_out = find_boundary(grey_region_out, red_region_out)

    print(f" Grey-Red Boundary In:{grey_red_boundary_in}")
    print(f" Grey-Red Boundary Out:{grey_red_boundary_out}")
    #assert grey_red_boundary_in == grey_red_boundary_out, "Boundary changed"

task = {
    "train": [
        {
            "input": [[5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2], [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2], [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2], [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 2], [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 2], [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 2], [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2], [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2], [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2], [4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5], [4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5], [4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5], [4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 0, 0, 0, 0, 0, 0, 0, 5, 5, 5, 5], [4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 0, 0, 0, 0, 0, 0, 0, 5, 5, 5, 5], [4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 0, 0, 0, 0, 0, 0, 0, 5, 5, 5, 5], [4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5], [4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5], [4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5]],
            "output": [[5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2], [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2], [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2], [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 2], [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 2], [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 2], [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2], [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2], [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2], [4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5], [4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5], [4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5], [4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 0, 0, 0, 0, 0, 0, 0, 5, 5, 5, 5], [4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 0, 0, 0, 0, 0, 0, 0, 5, 5, 5, 5], [4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 0, 0, 0, 0, 0, 0, 0, 5, 5, 5, 5], [4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5], [4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5], [4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5]],
        },
        {
            "input": [[5, 5, 5, 5, 2, 2, 2, 2, 4, 4, 4, 4], [5, 5, 5, 5, 2, 2, 2, 2, 4, 4, 4, 4], [5, 5, 5, 5, 0, 0, 2, 2, 4, 4, 4, 4], [5, 5, 5, 5, 0, 0, 2, 2, 4, 4, 4, 4], [5, 5, 5, 5, 2, 2, 2, 2, 0, 0, 4, 4], [5, 5, 5, 5, 2, 2, 2, 2, 0, 0, 4, 4]],
            "output": [[5, 5, 5, 5, 2, 2, 2, 2, 4, 4, 4, 4], [5, 5, 5, 5, 2, 2, 2, 2, 4, 4, 4, 4], [5, 5, 5, 5, 0, 0, 2, 2, 4, 4, 4, 4], [5, 5, 5, 5, 0, 0, 2, 2, 4, 4, 4, 4], [5, 5, 5, 5, 2, 2, 2, 2, 0, 0, 4, 4], [5, 5, 5, 5, 2, 2, 2, 2, 0, 0, 4, 4]],
        },
        {
            "input": [[5, 5, 2, 2, 4, 4], [5, 5, 0, 0, 4, 4], [5, 5, 2, 2, 4, 4]],
            "output": [[5, 5, 2, 2, 4, 4], [5, 5, 0, 0, 4, 4], [5, 5, 2, 2, 4, 4]],
        },
        {
            "input": [[5, 5, 5, 2, 4, 4, 4], [5, 5, 5, 0, 4, 4, 4], [5, 5, 5, 2, 4, 4, 4]],
            "output": [[5, 5, 5, 2, 4, 4, 4], [5, 5, 5, 0, 4, 4, 4], [5, 5, 5, 2, 4, 4, 4]],
        },
        {
            "input": [[4, 5, 5, 5, 5, 2, 2], [4, 5, 5, 5, 5, 2, 2], [4, 5, 5, 5, 5, 0, 0], [4, 5, 5, 5, 5, 2, 2], [4, 5, 5, 5, 5, 2, 2]],
            "output": [[4, 5, 5, 5, 5, 2, 2], [4, 5, 5, 5, 5, 2, 2], [4, 5, 5, 5, 5, 0, 0], [4, 5, 5, 5, 5, 2, 2], [4, 5, 5, 5, 5, 2, 2]],
        }
    ],
    "test": [
        {
            "input": [[5, 2, 2, 4], [5, 0, 2, 4], [5, 2, 2, 4]],
            "output": [[5, 2, 2, 4], [5, 0, 2, 4], [5, 2, 2, 4]],
        }
    ],
}

for i, example in enumerate(task["train"]):
  print(f"Example {i+1}:")
  analyze_example(example["input"], example["output"])