import numpy as np

def analyze_results(pairs, transform_func):
    results = []
    for i, (input_grid, expected_output) in enumerate(pairs):
        input_grid = np.array(input_grid)
        expected_output = np.array(expected_output)
        predicted_output = transform_func(input_grid)
        correct = np.array_equal(predicted_output, expected_output)
        results.append({
            "pair": i + 1,
            "input_shape": input_grid.shape,
            "output_shape": expected_output.shape,
            "predicted_shape": predicted_output.shape,
            "correct": correct,
            "differences": [] if correct else np.where(predicted_output != expected_output)
        })
    return results

# Assuming 'pairs' and 'transform' are defined as in the original notebook. I have included pair 3
pairs = [
    (
        [[6, 6],
         [6, 0]],
        [[6, 8, 6, 8],
         [8, 0, 8, 8],
         [6, 8, 0, 8],
         [8, 8, 8, 0]]
    ),
    (
        [[0, 6, 0],
         [0, 6, 0],
         [0, 6, 0]],
        [[8, 6, 8, 8, 8],
         [8, 0, 8, 8, 8],
         [8, 6, 8, 8, 8],
         [8, 0, 8, 8, 8],
         [8, 6, 8, 8, 8],
         [8, 0, 8, 8, 0]]
    ),
        (
        [[6, 0, 6, 0, 6, 0],
        [0, 0, 0, 0, 0, 0],
        [6, 0, 6, 0, 6, 0],
        [0, 0, 0, 0, 0, 0]],
        [[6, 8, 0, 8, 6, 8, 0, 8, 6, 8, 0, 8],
        [8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8],
        [0, 8, 0, 8, 0, 8, 0, 8, 0, 8, 0, 8],
        [8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8],
        [6, 8, 0, 8, 6, 8, 0, 8, 6, 8, 0, 8],
        [8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8],
        [0, 8, 0, 8, 0, 8, 0, 8, 0, 8, 0, 0]]
    )
]

results = analyze_results(pairs, transform)

for result in results:
    print(f"Pair {result['pair']}:")
    print(f"  Input Shape: {result['input_shape']}")
    print(f"  Output Shape: {result['output_shape']}")
    print(f"  Predicted Output Shape: {result['predicted_shape']}")
    print(f"  Correct: {result['correct']}")
    if not result['correct']:
        print(f"Differences at (row, col): {result['differences']}")