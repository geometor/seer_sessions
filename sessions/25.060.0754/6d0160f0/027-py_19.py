def analyze_example(input_grid, output_grid, predicted_output_grid):
    """Analyzes a single example and its predicted output."""

    # Find gray separator positions.
    gray_rows, gray_cols = find_gray_separators(input_grid)
    horizontal_separators = sorted(list(set(gray_rows)))
    vertical_separators = sorted(list(set(gray_cols)))

    analysis = {
        "horizontal_separators": horizontal_separators,
        "vertical_separators": vertical_separators,
        "segments": []
    }

    # Iterate through horizontal segments
    for i in range(len(horizontal_separators)):
        row_start = 0 if i == 0 else horizontal_separators[i-1] + 1
        row_end = horizontal_separators[i]

        # Iterate through vertical segments within each horizontal segment.
        for j in range(len(vertical_separators) - 1):
            col_start = vertical_separators[j] + 1
            col_end = vertical_separators[j+1]

            segment_data = {
                "row_start": row_start,
                "row_end": row_end,
                "col_start": col_start,
                "col_end": col_end,
                "expected_colors": [],
                "correct_placement_row": -1  # Initialize
            }
            # Determine expected colors and placement row
            if i < len(horizontal_separators): # we have another row of separators
              segment_data["correct_placement_row"] = horizontal_separators[i] + 1
            #get the first position of each color
            top_segment_colors = get_segment_colors(input_grid, row_start, row_end, col_start, col_end)
            segment_data["expected_colors"] = list(top_segment_colors.items())

            analysis["segments"].append(segment_data)

    return analysis

import numpy as np
# Re-run the transformation on the training data to get predicted outputs
train_data = [
  {
        "input": [
            [5, 0, 5, 0, 5, 0, 5],
            [5, 0, 5, 1, 5, 2, 5],
            [5, 0, 5, 0, 5, 0, 5],
            [0, 0, 0, 0, 0, 0, 0],
            [5, 0, 5, 0, 5, 0, 5]
        ],
        "output": [
            [5, 0, 5, 0, 5, 0, 5],
            [5, 0, 5, 1, 5, 2, 5],
            [5, 0, 5, 0, 5, 0, 5],
            [0, 0, 0, 0, 0, 0, 0],
            [5, 0, 5, 0, 5, 0, 5]
        ]
    },
    {
        "input": [
            [5, 0, 5, 0, 5, 0, 5],
            [5, 1, 5, 2, 5, 3, 5],
            [5, 0, 5, 0, 5, 0, 5],
            [0, 0, 0, 0, 0, 0, 0],
            [5, 0, 5, 0, 5, 0, 5]
        ],
        "output": [
            [5, 0, 5, 0, 5, 0, 5],
            [5, 1, 5, 2, 5, 3, 5],
            [5, 0, 5, 0, 5, 0, 5],
            [0, 0, 0, 0, 0, 0, 0],
            [5, 0, 5, 0, 5, 0, 5]
        ]
    },

    {
        "input": [
            [5, 0, 5, 0, 5, 0, 5],
            [5, 4, 5, 8, 5, 3, 5],
            [5, 0, 5, 0, 5, 0, 5],
            [5, 0, 5, 2, 5, 0, 5],
            [5, 0, 5, 0, 5, 0, 5]
        ],
        "output": [
            [5, 0, 5, 0, 5, 0, 5],
            [5, 4, 5, 8, 5, 3, 5],
            [5, 0, 5, 0, 5, 0, 5],
            [5, 0, 5, 2, 5, 0, 5],
            [5, 0, 5, 0, 5, 0, 5]
        ]
    },
     {
        "input": [
           [5, 0, 5, 0, 5, 0, 5, 0, 5],
           [5, 6, 5, 2, 5, 9, 5, 1, 5],
           [5, 0, 5, 0, 5, 0, 5, 0, 5],
           [5, 0, 5, 4, 5, 0, 5, 0, 5],
           [5, 0, 5, 0, 5, 0, 5, 0, 5],
           [0, 0, 0, 0, 0, 0, 0, 0, 0],
           [5, 0, 5, 0, 5, 0, 5, 0, 5]
        ],
        "output": [
            [5, 0, 5, 0, 5, 0, 5, 0, 5],
            [5, 6, 5, 2, 5, 9, 5, 1, 5],
            [5, 0, 5, 0, 5, 0, 5, 0, 5],
            [5, 0, 5, 4, 5, 0, 5, 0, 5],
            [5, 0, 5, 0, 5, 0, 5, 0, 5],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [5, 0, 5, 0, 5, 0, 5, 0, 5]
        ]
    }
]
results = []
for example in train_data:
  input_grid = np.array(example["input"])
  output_grid = np.array(example["output"])
  predicted_output_grid = transform(input_grid)
  analysis = analyze_example(input_grid, output_grid, predicted_output_grid)
  results.append(analysis)

for i, analysis in enumerate(results):
    print(f"Example {i+1}:")
    print(analysis)
    print("-" * 20)