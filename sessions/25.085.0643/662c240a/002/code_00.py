# Correct logic for analyze_subgrid
def analyze_subgrid(subgrid):
    colors, counts = np.unique(subgrid, return_counts=True)
    if len(colors) != 2: return -1, -1, -1

    # Correctly identify minority color based on counts
    if counts[0] < counts[1]:
        minority_color = colors[0]
        minority_pixel_count = counts[0]
    elif counts[1] < counts[0]:
        minority_color = colors[1]
        minority_pixel_count = counts[1]
    else:
         # Tie in counts - examples show this doesn't happen.
         return -2, -2, -2 # Indicate unexpected tie

    component_count = count_minority_components(subgrid, minority_color)
    return component_count, minority_color, minority_pixel_count