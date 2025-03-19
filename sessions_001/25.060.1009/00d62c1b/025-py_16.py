import numpy as np

def analyze_example(input_grid, output_grid):
    input_green_regions = find_contiguous_regions(input_grid, 3)
    output_green_regions = find_contiguous_regions(output_grid, 3)
    input_yellow_regions = find_contiguous_regions(input_grid, 4)
    output_yellow_regions = find_contiguous_regions(output_grid, 4)
    print(f"Input Grid Size: {input_grid.shape}")
    print(f"Output Grid Size: {output_grid.shape}")
    print(f"Input Green Regions: {len(input_green_regions)}")
    print(f"Output Green Regions: {len(output_green_regions)}")
    print(f"Input Yellow Regions: {len(input_yellow_regions)}")
    print(f"Output Yellow Regions: {len(output_yellow_regions)}")    
    diff = output_grid - input_grid
    print(f"Changes from input to output:\n {diff}")
    for i,region in enumerate(input_green_regions):
      print(f"  Region {i+1}:")
      highlights = find_highlight_in_region(input_grid, region)
      print(f"     highlight by current algorithm {highlights}")

examples = [
  ( # example 1
      np.array([[0,0,0,0,0,0,0,0,0],
                [0,0,0,0,0,0,0,0,0],
                [0,0,0,0,0,0,0,0,0],
                [0,0,0,3,3,3,0,0,0],
                [0,0,0,0,3,0,0,0,0]]),
      np.array([[0,0,0,0,0,0,0,0,0],
                [0,0,0,0,0,0,0,0,0],
                [0,0,0,0,0,0,0,0,0],
                [0,0,0,3,4,3,0,0,0],
                [0,0,0,0,4,0,0,0,0]])    
  ),
    ( # example 2
      np.array([[0,0,0,0,0,0,0,0],
                [0,0,0,3,3,0,0,0],
                [0,0,0,3,0,0,0,0],
                [0,0,0,0,0,0,0,0]]),
      np.array([[0,0,0,0,0,0,0,0],
                [0,0,0,4,4,0,0,0],
                [0,0,0,4,0,0,0,0],
                [0,0,0,0,0,0,0,0]])
    ),
  ( # example 3
      np.array([[0,0,0,0,0,0,0,0,0],
                [0,3,3,3,3,3,3,3,0],
                [0,3,3,3,3,3,3,3,0],
                [0,3,3,3,3,3,3,3,0],
                [0,3,3,3,3,3,3,3,0],
                [0,0,0,0,0,0,0,0,0]]),
      np.array([[0,0,0,0,0,0,0,0,0],
                [0,4,4,4,4,4,4,4,0],
                [0,4,4,4,4,4,4,4,0],
                [0,4,4,4,4,4,4,4,0],
                [0,4,4,4,4,4,4,4,0],
                [0,0,0,0,0,0,0,0,0]])
  ),
    ( # example 4
    np.array([[0,0,0,0,0,0,0,0,0,0,0],
                [0,3,3,3,3,3,3,3,3,3,0],
                [0,3,3,3,3,3,3,3,3,3,0],
                [0,0,0,0,0,0,0,0,0,0,0]]),
    np.array([[0,0,0,0,0,0,0,0,0,0,0],
                [0,4,4,4,4,4,4,4,4,4,0],
                [0,4,4,4,4,4,4,4,4,4,0],
                [0,0,0,0,0,0,0,0,0,0,0]])
  ),
    ( # example 5
    np.array([[3,3,3,0,0,0,0,0,0],
              [3,3,3,0,0,0,0,0,0],
              [3,3,3,0,0,0,0,0,0],
              [0,0,0,0,0,0,0,0,0],
              [0,0,0,0,0,0,0,0,0]]),
    np.array([[4,4,4,0,0,0,0,0,0],
              [4,4,4,0,0,0,0,0,0],
              [4,4,4,0,0,0,0,0,0],
              [0,0,0,0,0,0,0,0,0],
              [0,0,0,0,0,0,0,0,0]])
  ),
]

for i, (input_grid, output_grid) in enumerate(examples):
    print(f"Example {i+1}:")
    analyze_example(input_grid, output_grid)
    print("-" * 20)