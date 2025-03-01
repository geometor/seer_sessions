import numpy as np

def find_yellow_pixel(grid):
    # Find the coordinates of the yellow pixel (value 4).
    for r in range(len(grid)):
        for c in range(len(grid[0])):
          if grid[r][c] == 4:
            return (r,c)
    return None

def analyze_example(input_grid, output_grid):
    input_grid = np.array(input_grid)
    output_grid = np.array(output_grid)
    yellow_pixel = find_yellow_pixel(input_grid)
    dimensions = input_grid.shape
    same = np.array_equal(input_grid,output_grid)
    return {
        "yellow_pixel": yellow_pixel,
        "dimensions": dimensions,
        "grids_are_equal":same
    }

examples = [
  ([
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 4],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0]
  ],
  [
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 4],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0]
  ]),
  ([
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 4, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
  ],
  [
   [0, 0, 0, 0, 0, 0, 0, 0, 0],
   [0, 0, 0, 4, 0, 0, 0, 0, 0],
   [0, 0, 0, 4, 0, 0, 0, 0, 0],
   [0, 0, 0, 0, 0, 0, 0, 0, 0],
   [0, 0, 0, 0, 0, 0, 0, 0, 0],
  ]),
    ([
    [4, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
  ],
  [
   [4, 0, 0, 0, 0, 0, 0, 0, 0],
   [4, 0, 0, 0, 0, 0, 0, 0, 0],
   [0, 0, 0, 0, 0, 0, 0, 0, 0],
  ]),
    ([
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 4, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
  ],
  [
   [0, 0, 0, 0, 0, 0, 0, 0, 0],
   [0, 0, 0, 0, 0, 0, 0, 0, 0],
   [0, 0, 0, 0, 0, 4, 0, 0, 0],
   [0, 0, 0, 0, 0, 4, 0, 0, 0],
   [0, 0, 0, 0, 0, 0, 0, 0, 0],
  ]),
([
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 4],
  ],
  [
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 4],
  ]),
]
analysis_results = [analyze_example(inp,out) for inp, out in examples]

for i, result in enumerate(analysis_results):
    print(f"Example {i+1}:")
    print(f"  Yellow Pixel Location: {result['yellow_pixel']}")
    print(f"  Grid Dimensions: {result['dimensions']}")
    print(f"  Input == Output : {result['grids_are_equal']}")
