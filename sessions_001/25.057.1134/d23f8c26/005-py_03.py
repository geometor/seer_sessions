import numpy as np

def analyze_example(input_grid, output_grid):
    input_grid = np.array(input_grid)
    output_grid = np.array(output_grid)

    input_dims = input_grid.shape
    output_dims = output_grid.shape
    input_colors = np.unique(input_grid)
    output_colors = np.unique(output_grid)

    color_changes = []
    for r in range(input_dims[0]):
        for c in range(input_dims[1]):
            if input_grid[r, c] != output_grid[r, c]:
              color_changes.append(
                  {
                      "location": (r, c),
                      "from": int(input_grid[r, c]),
                      "to": int(output_grid[r, c])
                  }
              )

    print(f"Input Dimensions: {input_dims}")
    print(f"Output Dimensions: {output_dims}")
    print(f"Input Colors: {input_colors}")
    print(f"Output Colors: {output_colors}")
    print(f"Color Changes: {color_changes}")

# example data:
train = [
    ([
        [8, 7, 8],
        [8, 7, 8],
        [8, 7, 8],
     ],
     [
        [0, 7, 0],
        [0, 7, 0],
        [0, 7, 0],
     ]),
    ([
        [5, 0, 5],
        [5, 1, 0],
        [0, 0, 0],
     ],
     [
        [0, 0, 0],
        [0, 1, 0],
        [0, 0, 0],
     ]),
     ([
        [0, 0, 0],
        [0, 0, 0],
        [2, 0, 2],
     ],
     [
        [0, 0, 0],
        [0, 0, 0],
        [0, 0, 0],
     ]),
]

for i in [0,1,2]:
  print(f'Example {i}:')
  analyze_example(train[i][0], train[i][1])
