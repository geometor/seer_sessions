def analyze_grid_pair(input_grid, output_grid):
    """Analyzes a single input-output grid pair and returns a report."""

    input_grid = np.array(input_grid)
    output_grid = np.array(output_grid)
    
    blue_to_grey_count = np.sum((input_grid == 1) & (output_grid == 0))
    other_changes = np.sum((input_grid != output_grid) & ~((input_grid == 1) & (output_grid == 0)) )
    same = np.sum(input_grid == output_grid)


    report = {
        'blue_to_grey': blue_to_grey_count,
        'other_changes': other_changes,
        'pixels_same': same
    }
    return report

# this is arc data representing example pairs of input->output
train_ex = [
    [[[5, 5, 5, 5, 5, 5, 5], [5, 5, 5, 1, 5, 5, 5], [5, 5, 5, 5, 5, 5, 5]], [[5, 5, 5, 5, 5, 5, 5], [5, 5, 5, 0, 5, 5, 5], [5, 5, 5, 5, 5, 5, 5]]],
    [[[5, 5, 5, 1, 5, 5, 5], [5, 5, 5, 5, 5, 5, 5], [5, 5, 5, 1, 5, 5, 5]], [[5, 5, 5, 0, 5, 5, 5], [5, 5, 5, 5, 5, 5, 5], [5, 5, 5, 0, 5, 5, 5]]],
    [[[5, 1, 5, 5, 5, 5, 5, 5, 5, 1, 5], [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5], [5, 5, 5, 1, 5, 5, 5, 5, 5, 1, 5], [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5], [5, 5, 5, 5, 5, 1, 5, 5, 5, 5, 5]], [[5, 0, 5, 5, 5, 5, 5, 5, 5, 0, 5], [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5], [5, 5, 5, 0, 5, 5, 5, 5, 5, 0, 5], [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5], [5, 5, 5, 5, 5, 0, 5, 5, 5, 5, 5]]]
]

reports = []
for example in train_ex:
  reports.append(analyze_grid_pair(example[0], example[1]))

for report in reports:
  print(report)