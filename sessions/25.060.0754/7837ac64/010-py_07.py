def analyze_examples(train_ex):
    results = []
    for i, (input_grid, expected_output) in enumerate(train_ex):
        input_array = np.array(input_grid)
        expected_output_array = np.array(expected_output)
        blue_first, green_first = find_first_occurrence(input_array, [1, 3])

        results.append({
            "example": i + 1,
            "input_shape": input_array.shape,
            "output_shape": expected_output_array.shape,
            "blue_first": blue_first,
            "green_first": green_first,
            "row_diff": green_first[0] - blue_first[0] if blue_first[0] is not None and green_first[0] is not None else None,
            "col_diff": green_first[1] - blue_first[1] if blue_first[1] is not None and green_first[1] is not None else None,
        })
    return results

import numpy as np
from previous_code import find_first_occurrence # Assuming previous code is in 'previous_code.py'

train_ex = [
  [
    [[5, 5, 5, 5, 5, 5], [5, 5, 5, 5, 5, 5], [5, 5, 5, 5, 5, 5], [5, 5, 5, 5, 5, 1], [5, 5, 5, 5, 5, 3]],
    [[0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 1], [0, 0, 0, 0, 0, 3]]
  ],
  [
    [[5, 5, 5, 5, 5, 5, 5], [5, 5, 5, 5, 5, 5, 5], [5, 5, 5, 5, 5, 5, 5], [5, 5, 5, 5, 5, 5, 5], [5, 5, 5, 5, 5, 1, 5], [5, 5, 5, 5, 5, 3, 5]],
    [[0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 1, 0], [0, 0, 0, 0, 0, 3, 0]]
  ],
  [
    [[5, 5, 5, 5, 5, 5, 5, 5], [5, 5, 5, 5, 5, 5, 5, 5], [5, 5, 5, 5, 5, 5, 5, 5], [5, 5, 5, 5, 5, 1, 5, 5], [5, 5, 5, 5, 5, 3, 5, 5], [5, 5, 5, 5, 5, 5, 5, 1], [5, 5, 5, 5, 5, 5, 5, 3]],
    [[0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 1, 0, 0], [0, 0, 0, 0, 0, 3, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 1], [0, 0, 0, 0, 0, 0, 0, 3]]
  ],
  [
    [[5, 5, 5, 5, 5, 5, 5, 5], [5, 5, 5, 5, 5, 5, 5, 5], [5, 5, 5, 5, 5, 5, 5, 5], [5, 5, 5, 5, 5, 1, 5, 5], [5, 5, 5, 5, 5, 3, 5, 5], [5, 5, 5, 5, 5, 5, 1, 5], [5, 5, 5, 5, 5, 5, 3, 5]],
    [[0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 1, 0, 0], [0, 0, 0, 0, 0, 3, 0, 0], [0, 0, 0, 0, 0, 0, 1, 0], [0, 0, 0, 0, 0, 0, 3, 0]]
  ],
  [
    [[5, 5, 5, 5, 5, 5, 5, 5, 5, 5], [5, 5, 5, 5, 5, 5, 5, 5, 5, 5], [5, 5, 5, 5, 5, 5, 5, 5, 5, 5], [5, 5, 5, 5, 5, 1, 5, 5, 5, 5], [5, 5, 5, 5, 5, 3, 5, 5, 5, 5], [5, 5, 5, 5, 5, 5, 5, 5, 5, 5], [5, 5, 5, 5, 5, 5, 1, 5, 5, 5], [5, 5, 5, 5, 5, 5, 3, 5, 5, 5]],
    [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 1, 0, 0, 0, 0], [0, 0, 0, 0, 0, 3, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 1, 0, 0, 0], [0, 0, 0, 0, 0, 0, 3, 0, 0, 0]]
  ]
]
analysis_results = analyze_examples(train_ex)
for result in analysis_results:
    print(result)