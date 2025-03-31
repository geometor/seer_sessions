import numpy as np

def analyze_results(results):
    metrics = []
    for i, res in enumerate(results):
        inp = np.array(res['input'])
        expected = np.array(res['output'])
        transformed = np.array(res['transformed_output'])

        match = np.array_equal(expected, transformed)
        pixels_off = np.sum(expected != transformed)
        size_correct = inp.shape == expected.shape == transformed.shape

        palette_input = set(inp.flatten())
        palette_expected = set(expected.flatten())
        palette_transformed = set(transformed.flatten())
        palette_correct = palette_expected == palette_transformed

        counts_expected = {k: np.sum(expected == k) for k in palette_expected}
        counts_transformed = {k: np.sum(transformed == k) for k in palette_transformed}
        count_correct = counts_expected == counts_transformed

        metrics.append({
            "Example": i + 1,
            "Match": match,
            "Pixels Off": pixels_off,
            "Size Correct": size_correct,
            "Color Palette Correct": palette_correct,
            "Color Count Correct": count_correct,
        })
    return metrics

# Data from the previous run (pasted from the prompt)
results_data = [
    {
        "input": [[9, 6, 5, 7, 7, 7, 7], [8, 7, 1, 7, 7, 7, 7], [0, 8, 9, 7, 7, 7, 7], [7, 7, 7, 7, 7, 7, 7], [7, 7, 7, 1, 8, 4, 7], [7, 7, 7, 4, 7, 6, 7], [7, 7, 7, 6, 2, 4, 7]],
        "output": [[5, 8, 9, 7, 7, 7, 7], [8, 7, 6, 7, 7, 7, 7], [9, 1, 0, 7, 7, 7, 7], [7, 7, 7, 7, 7, 7, 7], [7, 7, 7, 4, 4, 4, 7], [7, 7, 7, 2, 7, 8, 7], [7, 7, 7, 1, 6, 6, 7]],
        "transformed_output": [[5, 1, 9, 7, 7, 7, 7], [6, 7, 8, 7, 7, 7, 7], [9, 8, 0, 7, 7, 7, 7], [7, 7, 7, 7, 7, 7, 7], [7, 7, 7, 4, 6, 4, 7], [7, 7, 7, 8, 7, 2, 7], [7, 7, 7, 1, 4, 6, 7]]
    },
    {
        "input": [[7, 7, 7, 7, 7, 7, 7], [7, 7, 7, 7, 7, 7, 7], [7, 7, 5, 2, 8, 7, 7], [7, 7, 1, 7, 9, 7, 7], [7, 7, 4, 3, 0, 7, 7], [7, 7, 7, 7, 7, 7, 7], [7, 7, 7, 7, 7, 7, 7]],
        "output": [[7, 7, 7, 7, 7, 7, 7], [7, 7, 7, 7, 7, 7, 7], [7, 7, 8, 1, 0, 7, 7], [7, 7, 3, 7, 2, 7, 7], [7, 7, 5, 9, 4, 7, 7], [7, 7, 7, 7, 7, 7, 7], [7, 7, 7, 7, 7, 7, 7]],
        "transformed_output": [[7, 7, 7, 7, 7, 7, 7], [7, 7, 7, 7, 7, 7, 7], [7, 7, 8, 9, 0, 7, 7], [7, 7, 2, 7, 3, 7, 7], [7, 7, 5, 1, 4, 7, 7], [7, 7, 7, 7, 7, 7, 7], [7, 7, 7, 7, 7, 7, 7]]
    },
    {
        "input": [[7, 7, 7, 7, 7, 7, 7], [7, 7, 7, 6, 5, 5, 7], [7, 7, 7, 5, 7, 6, 7], [7, 7, 7, 1, 5, 1, 7], [8, 8, 8, 7, 7, 7, 7], [9, 7, 9, 7, 7, 7, 7], [0, 0, 0, 7, 7, 7, 7]],
        "output": [[7, 7, 7, 7, 7, 7, 7], [7, 7, 7, 5, 5, 1, 7], [7, 7, 7, 5, 7, 5, 7], [7, 7, 7, 6, 6, 1, 7], [8, 9, 0, 7, 7, 7, 7], [0, 7, 8, 7, 7, 7, 7], [8, 9, 0, 7, 7, 7, 7]],
        "transformed_output": [[7, 7, 7, 7, 7, 7, 7], [7, 7, 7, 5, 6, 1, 7], [7, 7, 7, 5, 7, 5, 7], [7, 7, 7, 6, 5, 1, 7], [8, 9, 0, 7, 7, 7, 7], [8, 7, 0, 7, 7, 7, 7], [8, 9, 0, 7, 7, 7, 7]]
    }
]

analysis = analyze_results(results_data)
# print(analysis) # Output already captured in prompt/history