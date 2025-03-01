def extract_metrics(results):
    metrics = []
    for i, result in enumerate(results):
        metrics.append({
            "example": i + 1,
            "input_dims": result['input_dims'],
            "output_dims": result['output_dims'],
            "input_colors": result['input_colors'],
            "output_colors": result['output_colors'],
            "correct": result['correct']
        })
    return metrics
results = [
    {'input_dims': (10, 10), 'output_dims': (2, 3), 'input_colors': [1, 2, 3], 'output_colors': [0, 2, 3], 'correct': True},
    {'input_dims': (10, 10), 'output_dims': (2, 3), 'input_colors': [1, 2, 3], 'output_colors': [0, 2, 3], 'correct': True},
    {'input_dims': (15, 15), 'output_dims': (2, 3), 'input_colors': [1, 2, 3], 'output_colors': [0, 2, 3], 'correct': True}
]

metrics_report = extract_metrics(results)
print(metrics_report)
