def report(transform, in_grid, out_grid):
    predicted_grid = transform(in_grid)
    if predicted_grid == out_grid:
        return "Correct"
    
    report = {
      "match":False,
      "correct_pixels": 0,
      "incorrect_pixels": 0,
      "total_pixels_predicted": 0,
      "total_pixels_expected": 0,
      "predicted_shape": [],
      "output_shape": [],
    }

    if predicted_grid is not None and out_grid is not None:
        report["predicted_shape"] = [len(predicted_grid), len(predicted_grid[0]) if predicted_grid else 0]
        report["output_shape"] = [len(out_grid), len(out_grid[0]) if out_grid else 0]
        
        min_rows = min(len(predicted_grid), len(out_grid))
        min_cols = min(len(predicted_grid[0]) if predicted_grid else 0, len(out_grid[0]) if out_grid else 0)

        for i in range(min_rows):
            for j in range(min_cols):
                if predicted_grid[i][j] == out_grid[i][j]:
                    report["correct_pixels"] += 1
                else:
                    report["incorrect_pixels"] += 1

        report["total_pixels_predicted"] = report["predicted_shape"][0] * report["predicted_shape"][1]
        report["total_pixels_expected"] = report["output_shape"][0] * report["output_shape"][1]
        report['match'] = predicted_grid == out_grid

    return report