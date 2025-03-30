        if e2 > -dc:
            err -= dc
            r0 += sr
        if e2 < dr:  # <--- This should likely be 'elif' or handled differently
            err += dr
            c0 += sc