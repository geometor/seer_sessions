def analyze_example(input_grid, output_grid):
    """Analyzes a single input-output pair and returns relevant information."""
    import numpy as np
    import utils

    analysis = {}

    # Red object analysis
    red_input_bbox = utils.find_object(input_grid, 2)
    red_output_bbox = utils.find_object(output_grid, 2)
    red_input_obj = utils.get_object(input_grid, 2)
    red_output_obj = utils.get_object(output_grid, 2)
    analysis['red_present'] = red_input_bbox is not None
    if red_input_bbox:
        analysis['red_input_top_left'] = red_input_bbox[0]
        analysis['red_input_bottom_right'] = red_input_bbox[1]
        analysis['red_input_shape'] = red_input_obj.shape
    if red_output_bbox:
        analysis['red_output_top_left'] = red_output_bbox[0]
        analysis['red_output_shape'] = red_output_obj.shape

        # derive shift
        if 'red_input_top_left' in analysis:
            r_shift = analysis['red_output_top_left'][0] - analysis['red_input_top_left'][0]
            c_shift = analysis['red_output_top_left'][1] - analysis['red_input_top_left'][1]
            analysis['red_shift'] = (r_shift, c_shift)

    # Blue object analysis
    blue_input_bbox = utils.find_object(input_grid, 8)
    blue_output_bbox = utils.find_object(output_grid, 8)
    analysis['blue_present'] = blue_input_bbox is not None
    if blue_input_bbox:
        analysis['blue_input_top_left'] = blue_input_bbox[0]
        analysis['blue_input_shape'] = utils.get_object(input_grid, 8).shape

    return analysis

def analyze_results(train_input_output_list):
   report = ""
   for i, (input_grid, output_grid) in enumerate(train_input_output_list):
      analysis = analyze_example(input_grid, output_grid)
      report += f"Example {i+1}:\n"
      for k,v in analysis.items():
         report += f"  {k}: {v}\n"

   return report