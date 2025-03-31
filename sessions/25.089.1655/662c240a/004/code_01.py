    # Rule 1: All Distinct MFCs
    if len(set(mfcs)) == 3:
        selected_index = 0
    else:
        # Calculate min/max and indices only if needed
        min_mfc = min(mfcs)
        max_mfc = max(mfcs)
        min_indices = [i for i, mfc in enumerate(mfcs) if mfc == min_mfc]
        max_indices = [i for i, mfc in enumerate(mfcs) if mfc == max_mfc]

        # Rule 2: Shared Minimum MFC (exactly two)
        if len(min_indices) == 2:
            selected_index = max(min_indices)
        # Rule 3: Unique Maximum MFC
        elif len(max_indices) == 1:
             selected_index = max_indices[0]
        # Rule 4: Default (all equal, shared max, etc.)
        else:
            selected_index = 0