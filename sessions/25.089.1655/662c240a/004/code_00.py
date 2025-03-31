    # Rule 3a: All Distinct MFCs
    if len(set(mfcs)) == 3:
        selected_index = 0 # Select the first subgrid (index 0)
    else:
        # Calculate min/max and indices only if needed
        min_mfc = min(mfcs)
        max_mfc = max(mfcs)
        min_indices = [i for i, mfc in enumerate(mfcs) if mfc == min_mfc]
        max_indices = [i for i, mfc in enumerate(mfcs) if mfc == max_mfc]

        # Rule 3b: Unique Maximum MFC
        if len(max_indices) == 1:
            selected_index = max_indices[0] # Select the subgrid with the unique max
        # Rule 3c: Shared Minimum MFC (exactly two)
        elif len(min_indices) == 2:
            selected_index = max(min_indices) # Select the one with the higher index among the two minimums
        # Rule 3d: Default (covers all other cases, e.g., all MFCs equal, two share max)
        else:
            selected_index = 0 # Select the first subgrid