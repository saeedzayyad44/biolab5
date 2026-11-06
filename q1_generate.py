import random

COMP = {"A": "T", "T": "A", "C": "G", "G": "C"}


def revcomp(s):
    return "".join(COMP[b] for b in reversed(s))


def rand_dna(n):
    return "".join(random.choice("ACGT") for _ in range(n))


def make_transposon(ir_len=10, body_min=25, body_max=40):
    ir = rand_dna(ir_len)
    body = rand_dna(random.randint(body_min, body_max))
    return ir + body + revcomp(ir)


def insert(seq, elements, name, te, pos, tsd_len=5):
    """Insert transposon `te` at target site `pos`.
    The bases seq[pos:pos+tsd_len] are duplicated on both sides (direct repeats).
    Positions of elements already in the sequence are updated."""
    q = pos + tsd_len
    block = te + seq[pos:q]                 
    new_seq = seq[:q] + block + seq[q:]
    L = len(block)
    for el in elements:
        if el["start"] >= q:                
            el["start"] += L
            el["end"] += L
        elif el["end"] >= q:              
            el["end"] += L
    elements.append({"name": name, "start": q, "end": q + len(te) - 1,
                     "tsd": seq[pos:q]})
    return new_seq


def build_sequence(seed=7):
    random.seed(seed)
    while True:
        seq = rand_dna(130)                 
        elements = []

        seq = insert(seq, elements, "TE1", make_transposon(), 15)
        seq = insert(seq, elements, "TE2", make_transposon(), 110)

        te1 = elements[0]                   
        pos = random.randint(te1["start"] + 12, te1["end"] - 20)
        seq = insert(seq, elements, "TE3", make_transposon(), pos)

        te2 = elements[1]                   
        seq = insert(seq, elements, "TE4", make_transposon(), te2["end"] - 7)

        if 200 <= len(seq) <= 400:
            return seq, elements


if __name__ == "__main__":
    seq, elements = build_sequence()

    with open("sequence.txt", "w") as f:
        f.write(seq)

    print(f"Artificial DNA sequence ({len(seq)} bp), saved to sequence.txt:")
    for k in range(0, len(seq), 60):
        print(f"{k + 1:>4}  {seq[k:k + 60]}")

    print("\nInserted transposons (1-based positions):")
    for el in sorted(elements, key=lambda d: d["start"]):
        print(f"  {el['name']}: start={el['start'] + 1:>4}  "
              f"end={el['end'] + 1:>4}  direct repeat={el['tsd']}")