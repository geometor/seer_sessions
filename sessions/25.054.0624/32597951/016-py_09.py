import numpy as np

def analyze_grid(grid):
    grid_array = np.array(grid)
    unique_colors = np.unique(grid_array)
    color_counts = {color: np.sum(grid_array == color) for color in unique_colors}
    height, width = grid_array.shape
    return {
        "height": height,
        "width": width,
        "unique_colors": unique_colors.tolist(),
        "color_counts": color_counts,
    }

def compare_grids(input_grid, expected_grid):
    input_analysis = analyze_grid(input_grid)
    expected_analysis = analyze_grid(expected_grid)
    pixels_different = np.sum(np.array(input_grid) != np.array(expected_grid))

    return {
      "input": input_analysis,
      "expected": expected_analysis,
        "pixels_different": int(pixels_different),
    }

examples = [
    {
        "input": [
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1],
[0, 0, 0, 0, 0, 8, 8, 8, 8, 8, 0, 0, 0, 0, 0, 0, 0],
[1, 1, 1, 0, 1, 3, 3, 8, 3, 3, 1, 0, 1, 1, 1, 0, 1],
[0, 0, 0, 0, 0, 8, 8, 8, 8, 8, 0, 0, 0, 0, 0, 0, 0],
[1, 1, 0, 1, 1, 3, 8, 3, 3, 3, 0, 1, 1, 1, 0, 1, 1],
[0, 0, 0, 0, 0, 8, 8, 8, 8, 8, 0, 0, 0, 0, 0, 0, 0],
[1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        ],
        "expected":[
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[1, 1, 0, 1, 3, 3, 0, 3, 3, 3, 0, 1, 1, 1, 0, 1, 1],
[0, 0, 0, 0, 0, 8, 8, 8, 8, 8, 0, 0, 0, 0, 0, 0, 0],
[1, 1, 1, 0, 3, 3, 3, 8, 3, 3, 3, 0, 1, 1, 1, 0, 1],
[0, 0, 0, 0, 0, 8, 8, 8, 8, 8, 0, 0, 0, 0, 0, 0, 0],
[1, 1, 0, 1, 3, 3, 8, 3, 3, 3, 0, 1, 1, 1, 0, 1, 1],
[0, 0, 0, 0, 0, 8, 8, 8, 8, 8, 0, 0, 0, 0, 0, 0, 0],
[1, 1, 1, 0, 3, 3, 3, 0, 3, 3, 3, 0, 1, 1, 1, 0, 1],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        ]
    },
    {
      "input": [
[1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1],
[1, 1, 0, 1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 0, 1, 1, 0],
[0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 1, 0, 0, 0, 0, 1],
[0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 1, 1, 0, 0, 0, 1, 0],
[0, 0, 1, 0, 0, 1, 1, 0, 0, 0, 0, 0, 1, 1, 0, 1, 1],
[0, 0, 0, 0, 0, 1, 1, 1, 0, 1, 1, 0, 1, 1, 0, 0, 0],
[0, 0, 0, 1, 0, 0, 1, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0],
[1, 8, 3, 8, 8, 8, 8, 8, 8, 1, 0, 0, 1, 0, 1, 1, 0],
[0, 8, 3, 8, 3, 3, 3, 8, 8, 0, 1, 1, 0, 0, 0, 0, 0],
[0, 3, 3, 8, 3, 3, 8, 3, 8, 0, 0, 1, 1, 0, 0, 0, 0],
[0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0],
[0, 1, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 1, 1],
[1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 1],
[0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0],
[0, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 1],
[0, 1, 1, 0, 1, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0],
[0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 1]
      ],
      "expected": [
[1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1],
[1, 1, 0, 1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 0, 1, 1, 0],
[0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 1, 0, 0, 0, 0, 1],
[0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 1, 1, 0, 0, 0, 1, 0],
[0, 0, 1, 0, 0, 1, 1, 0, 0, 0, 0, 0, 1, 1, 0, 1, 1],
[0, 0, 0, 0, 0, 1, 1, 1, 0, 1, 1, 0, 1, 1, 0, 0, 0],
[0, 0, 0, 3, 0, 0, 3, 3, 0, 0, 0, 0, 0, 1, 0, 0, 0],
[3, 8, 3, 8, 8, 8, 8, 8, 8, 3, 0, 0, 1, 0, 1, 1, 0],
[0, 8, 3, 8, 3, 3, 3, 8, 8, 0, 1, 1, 0, 0, 0, 0, 0],
[0, 3, 3, 8, 3, 3, 8, 3, 8, 0, 0, 1, 1, 0, 0, 0, 0],
[0, 1, 0, 0, 3, 0, 0, 0, 3, 0, 0, 0, 0, 0, 0, 1, 0],
[0, 1, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 1, 1],
[1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 1],
[0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0],
[0, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 1],
[0, 1, 1, 0, 1, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0],
[0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 1]
      ]
    },
  {
      "input": [
[0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1],
[1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 0],
[0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1],
[1, 0, 1, 1, 8, 3, 3, 8, 3, 1, 0, 1, 1, 0, 1, 1, 0],
[0, 1, 0, 0, 3, 8, 8, 3, 8, 0, 1, 0, 0, 1, 0, 0, 1],
[1, 0, 1, 1, 8, 3, 3, 8, 3, 1, 0, 1, 1, 0, 1, 1, 0],
[0, 1, 0, 0, 3, 8, 8, 3, 8, 0, 1, 0, 0, 1, 0, 0, 1],
[1, 0, 1, 1, 8, 3, 3, 8, 3, 1, 0, 1, 1, 0, 1, 1, 0],
[0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1],
[1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 0],
[0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1],
[1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 0],
[0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1],
[1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 0],
[0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1],
[1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 0],
[0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1]
],
    "expected": [
[0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1],
[1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 0],
[0, 1, 0, 0, 3, 0, 0, 3, 0, 0, 1, 0, 0, 1, 0, 0, 1],
[1, 0, 1, 3, 8, 3, 3, 8, 3, 3, 0, 1, 1, 0, 1, 1, 0],
[0, 1, 0, 0, 3, 8, 8, 3, 8, 0, 1, 0, 0, 1, 0, 0, 1],
[1, 0, 1, 3, 8, 3, 3, 8, 3, 3, 0, 1, 1, 0, 1, 1, 0],
[0, 1, 0, 0, 3, 8, 8, 3, 8, 0, 1, 0, 0, 1, 0, 0, 1],
[1, 0, 1, 3, 8, 3, 3, 8, 3, 3, 0, 1, 1, 0, 1, 1, 0],
[0, 1, 0, 0, 3, 0, 0, 3, 0, 0, 1, 0, 0, 1, 0, 0, 1],
[1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 0],
[0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1],
[1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 0],
[0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1],
[1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 0],
[0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1],
[1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 0],
[0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1]
]
  }

]
reports = [compare_grids(ex["input"], ex["expected"]) for ex in examples]

for i, report in enumerate(reports):
    print(f"Example {i+1}:")
    print(f"  Input Grid:  Height={report['input']['height']}, Width={report['input']['width']}, Colors={report['input']['unique_colors']}, Color Counts={report['input']['color_counts']}")
    print(f"  Expected Grid: Height={report['expected']['height']}, Width={report['expected']['width']}, Colors={report['expected']['unique_colors']}, Color Counts={report['expected']['color_counts']}")
    print(f"  Pixels Different: {report['pixels_different']}")
