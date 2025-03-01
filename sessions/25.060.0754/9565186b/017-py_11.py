import numpy as np

def analyze_neighbors(grid, row, col, target_color=8):
    """
    Analyzes the neighbors of a pixel in a grid.

    Args:
      grid: The 2D numpy array representing the grid.
      row: The row index of the pixel.
      col: The column index of the pixel.
      target_color: the color of interest

    Returns:
      A dictionary containing neighbor counts, or None if the pixel is
      not the color specified.
    """
    if grid[row, col] != target_color:
        return None

    height, width = grid.shape
    neighbors = {}
    neighbor_colors = []

    for i in range(max(0, row - 1), min(height, row + 2)):
        for j in range(max(0, col - 1), min(width, col + 2)):
            if (i, j) != (row, col):  # Exclude the pixel itself
                neighbor_color = grid[i, j]
                neighbor_colors.append(neighbor_color)
                neighbors[neighbor_color] = neighbors.get(neighbor_color, 0) + 1

    return {
      'neighbors': neighbors,
        'neighbor_colors': neighbor_colors
    }

def analyze_transformation(input_grid, output_grid):
    """
    Analyzes the transformation of azure pixels in a pair of grids.

    Returns: A list of dictionaries containing info about each azure pixel.
    """
    transformations = []
    for i, row in enumerate(input_grid):
        for j, pixel in enumerate(row):
          if pixel == 8:
            analysis = analyze_neighbors(input_grid, i, j)
            if analysis is not None:
                analysis['output_color'] = output_grid[i,j]
                analysis['row'] = i
                analysis['col'] = j
                transformations.append(analysis)
    return transformations

task = {
  "train": [
    {
      "input": [
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 8, 8, 8, 0, 0, 0, 0, 0, 0],
        [0, 8, 5, 8, 0, 0, 0, 0, 0, 0],
        [0, 8, 8, 8, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 2, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
      ],
      "output": [
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 5, 5, 5, 0, 0, 0, 0, 0, 0],
        [0, 5, 5, 5, 0, 0, 0, 0, 0, 0],
        [0, 5, 5, 5, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 2, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
      ]
    },
    {
      "input": [
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 8, 8, 8, 8, 8, 0, 0],
        [0, 0, 8, 8, 8, 8, 8, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0]
      ],
      "output": [
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 5, 5, 5, 5, 5, 0, 0],
        [0, 0, 5, 5, 5, 5, 5, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0]
      ]
    },
      {
      "input": [
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 8, 8, 8, 8, 8, 0, 0],
        [0, 0, 8, 8, 8, 8, 8, 8, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0]
      ],
      "output": [
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 5, 5, 5, 5, 5, 0, 0],
        [0, 0, 5, 5, 5, 5, 5, 8, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0]
      ]
    }
  ]
}

for example in task["train"]:
    input_grid = np.array(example["input"])
    output_grid = np.array(example["output"])
    analysis = analyze_transformation(input_grid, output_grid)
    print(f"Example Analysis:\n{analysis}\n")