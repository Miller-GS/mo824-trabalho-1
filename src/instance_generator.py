import random as rd
from pathlib import Path

outdir = Path("./instances")

def generate_subsets(n, method):
    generators = {
        1: lambda i : rd.randint(1,n),
        2: lambda i : int(n * 0.2),
        3: lambda i : i+1,
    }
    return [generators[method](i) for i in range(n)]


def generate_instance(n, method, seed, id):
    lines = dict()
    all_numbers = set()
    subset_dims = generate_subsets(n, method)       

    if subset_dims[0] == None: return

    # Create instance dict
    lines[0] = str(n)
    lines[1] = " ".join(str(ss) for ss in subset_dims)
    for i in range(n):
        ssd = subset_dims[i]
        numbers = rd.sample(range(1, n+1), ssd)         # pra cada subset, gera inteiros aleatórios de 1 a n
        lines[i+2] = " ".join(str(n) for n in numbers)
        all_numbers.update(numbers)
    for i in range(n):
        lines[i + 2 + n] = " ".join(str(rd.randint(-n, n)) for _ in range(n-i))

    # check if instance is valid
    if len(all_numbers) != n:
        print("Invalid instance!")
        generate_instance(n, method, seed + 1, id)
        return 

    # write instance into file
    with open(outdir / f"instance_{id}.txt", "w") as file:
        for k, v in lines.items():
            file.write(f"{v}\n")
        
    return 


def main():
    N = [25, 50, 100, 200, 400]
    seed = 42

    id = 0
    for _, n in enumerate(N):
        for _, method in enumerate([1,2,3]):
            generate_instance(n, method, seed, id)
            id += 1

    return


if __name__=="__main__":
    main()
    