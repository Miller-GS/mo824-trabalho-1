import random as rd
from pathlib import Path

outdir = Path("./instances")

def generate_instance(n, seed, id):
    rd.seed(seed)
    lines = dict()
    subset_dims = [rd.randint(1,n) for _ in range(n)]

    lines[0] = str(n)
    lines[1] = " ".join(str(ss) for ss in subset_dims)
    for i in range(n):
        ssd = subset_dims[i]
        lines[i+2] = " ".join(str(rd.randint(1, n)) for _ in range(ssd))
    for i in range(n):
        lines[i + 2 + n] = " ".join(str(rd.randint(-n, n)) for _ in range(n-i))

    with open(outdir / f"instance_{id}.txt", "w") as file:
        for k, v in lines.items():
            file.write(f"{v}\n")


def main():
    N = [25, 50, 100, 200, 400]
    S_seeds = [42, 69, 420]

    id = 0
    for i, n in enumerate(N):
        for j, seed in enumerate(S_seeds):
            generate_instance(n, seed, id)
            id += 1

    return


if __name__=="__main__":
    main()
    