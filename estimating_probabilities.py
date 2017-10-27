def estimate_probabilities(file_name, letters):

    N = len(letters)

    p = {}
    for l in letters:
        p[l] = 0

    p_pair = {}
    for l1 in letters:
        for l2 in letters:
            p_pair[l1 + l2] = 0

    with open(file_name, 'r') as f:
        total = 0
        pair_total = 0
        ch = f.read(1)
        ch = ch.lower()
        prev_ch = ''
        while ch:
            if ch in letters:
                total += 1
                p[ch] += 1
                if prev_ch in letters:
                    p_pair[prev_ch + ch] += 1
                    pair_total += 1
            prev_ch = ch
            ch = f.read(1)

        for ch in p:
            p[ch] /= total

        for pair in p_pair:
            p_pair[pair] /= pair_total

        for l1 in letters:
            for l2 in letters:
                if p[l1] != 0:
                    p_pair[l1 + l2] /= p[l1]

        return p, p_pair
