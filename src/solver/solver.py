import argparse
import logging
import gurobipy as gp
from pathlib import Path
from gurobipy import GRB
from instance import Instance


def main() -> None:
    args = parse_args()
    instance = Instance.from_input_file(args.input)
    if args.verbose:
        print("Instance loaded:")
        print(instance)

    instance_name = Path(args.input).stem
    logger, env = setup_logger(args.outdir, instance_name)

    model, qbf_variables = build_model(instance, env)

    model.setParam(GRB.Param.TimeLimit, 600)
    model.optimize()
    logger.info("Solution found:")
    for i in range(len(instance.variable_subsets)):
        logger.info(f"Variable {i + 1}: {qbf_variables[i].X}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Max-SC-QBF Solver")
    parser.add_argument("--input", type=str, required=True, help="Input file of the instance")
    parser.add_argument("--outdir", type=str, required=True, help="Saves gurobi log into outdir")
    parser.add_argument("-v", "--verbose", action="store_true", help="Enable verbose output")
    return parser.parse_args()

def setup_logger(outdir: str, instance_name: str) -> logging.Logger:
    Path(outdir).mkdir(parents=True, exist_ok=True)
    log_path =f"{outdir}/{instance_name}.log"
    logging.basicConfig(
        level=logging.INFO,
        filename=Path(log_path),
        encoding="utf-8",
        filemode="a",
        format="%(asctime)s %(levelname)s %(message)s",
    )
    env = gp.Env(logfilename=log_path, params={"LogToConsole": 0})
    return logging.getLogger(), env

def build_model(instance: Instance, env:gp.Env) -> tuple[gp.Model, gp.tupledict[int, gp.Var]]:
    model = gp.Model("Max-SC-QBF", env=env)
    n_variables = len(instance.variable_subsets)
    subsets = instance.variable_subsets

    qbf_variables = model.addVars(n_variables, vtype=GRB.BINARY, name="qbf_var")
    # Used to linearize the QBF. qbf_var_pair[i,j] = 1 means both qbf_var[i] AND qbf_var[j] are 1.
    qbf_variable_pairs = model.addVars(n_variables, n_variables, vtype=GRB.BINARY, name="qbf_var_pair")

    # We want to maximize the result of the Quadratic Binary Function (QBF)
    model.setObjective(
        gp.quicksum(
            qbf_variable_pairs[i,j] * instance.coefficients_matrix[i][j]
            for i in range(n_variables)
            for j in range(n_variables)
        ),
        GRB.MAXIMIZE
    )

    # qbf_var_pairs[i,j] <= qbf_var[i]
    # This ensures that if qbf_var[i] is 0, qbf_var_pairs[i,j] is also 0
    model.addConstrs((
        qbf_variable_pairs[i, j] <= qbf_variables[i]
        for i in range(n_variables)
        for j in range(n_variables)
    ), name="i_0_implies_ij_0")

    # Same for j
    model.addConstrs((
        qbf_variable_pairs[i, j] <= qbf_variables[j]
        for i in range(n_variables)
        for j in range(n_variables)
    ), name="j_0_implies_ij_0")

    # Now, we need to ensure that if both qbf_var[i] and qbf_var[j] are 1, then the combination is also 1
    model.addConstrs((
        qbf_variable_pairs[i, j] >= qbf_variables[i] + qbf_variables[j] - 1
        for i in range(n_variables)
        for j in range(n_variables)
    ), name="i_and_j_1_implies_ij_1")

    # Set Cover constraints, this ensures that the chosen subsets covers all variables
    model.addConstrs((
        gp.quicksum(qbf_variables[i] for i, Si in enumerate(subsets) if k in Si) >= 1
        for k in range(1, n_variables + 1)      # vars goes from 1 to 25
        ), name=f"cover_all_variables")

    return model, qbf_variables

if __name__ == "__main__":
    main()