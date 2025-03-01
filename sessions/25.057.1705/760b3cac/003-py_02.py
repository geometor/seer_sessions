def code_execution(examples):
    reports = []
    for i, example in enumerate(examples):
        input_grid = np.array(example['input'])
        expected_output_grid = np.array(example['output'])
        predicted_output_grid = transform(input_grid)
        objects = find_objects(input_grid)

        #build bbox
        for obj in objects:
            min_row = min(pixel[0] for pixel in obj['pixels'])
            max_row = max(pixel[0] for pixel in obj['pixels'])
            min_col = min(pixel[1] for pixel in obj['pixels'])
            max_col = max(pixel[1] for pixel in obj['pixels'])
            obj['bbox'] = (min_row, min_col, max_row, max_col)

        report = {
            'example_index': i,
            'input_shape': input_grid.shape,
            'output_shape': expected_output_grid.shape,
            'objects': [
                {
                    'color': obj['color'],
                    'bbox': obj['bbox']
                }
                for obj in objects
            ],
            'transform_correct': np.array_equal(expected_output_grid, predicted_output_grid)
        }
        reports.append(report)
    return reports

#Assuming train set is available as:
train_set = task["train"]
reports = code_execution(train_set)
for report in reports:
    print(report)