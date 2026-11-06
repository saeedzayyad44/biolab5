COMP = {"A": "T", "T": "A", "C": "G", "G": "C"}


def revcomp(s):
    return "".join(COMP[b] for b in reversed(s))


def detect(seq, ir_min=8, ir_max=15, dr_min=4, dr_max=8,
           body_min=10, te_max=200):
    found = {}
    n = len(seq)
    for i in range(dr_min, n):                      # candidate start
        for L in range(ir_min, ir_max + 1):         # candidate IR length
            if i + L > n:
                break
            right_ir = revcomp(seq[i:i + L])
            j = seq.find(right_ir, i + L + body_min)
            while j != -1 and j + L - i <= te_max:
                end = j + L - 1
                # look for direct repeats around the element
                dr = 0
                for t in range(dr_max, dr_min - 1, -1):
                    if i - t >= 0 and end + 1 + t <= n and \
                            seq[i - t:i] == seq[end + 1:end + 1 + t]:
                        dr = t
                        break
                if dr:
                    key = (i, end)
                    if key not in found or found[key]["ir"] < L:
                        found[key] = {"start": i, "end": end, "ir": L,
                                      "dr": seq[i - dr:i]}
                j = seq.find(right_ir, j + 1)
    return sorted(found.values(), key=lambda d: d["start"])


if __name__ == "__main__":
    with open("sequence.txt") as f:
        seq = f.read().strip().upper()

    hits = detect(seq)
    print(f"Sequence length: {len(seq)} bp")
    print(f"Detected transposable elements: {len(hits)}\n")
    for k, h in enumerate(hits, 1):
        print(f"  #{k}: start={h['start'] + 1:>4}  end={h['end'] + 1:>4}  "
              f"IR length={h['ir']}  direct repeat={h['dr']}")