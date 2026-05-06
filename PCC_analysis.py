import pandas as pd
import argparse

parser = argparse.ArgumentParser()

parser.add_argument("-input_gene", "--input_gene", required=True)
parser.add_argument("-input_matrix", "--input_matrix", required=True)
parser.add_argument("-output", "--output", default="correlations.xlsx")

args = parser.parse_args()


target_df = pd.read_csv(args.input_gene, header=None)
target_genes = target_df.iloc[:, 0].dropna().astype(str).str.strip().tolist()

df = pd.read_csv(args.input_matrix, sep="\t", index_col=0)


all_pairs = {}
max_length = 0

for target in target_genes:
    if target not in df.index:
        print(f"No {target} in matrix")
        all_pairs[target] = []
        continue

    target_data = df.loc[target]

    correlations = df.apply(lambda row: row.corr(target_data), axis=1).drop(target)
    correlations_sorted = correlations.sort_values(ascending=False)

    pairs = list(zip(correlations_sorted.index, correlations_sorted.values))

    all_pairs[target] = pairs
    if len(pairs) > max_length:
        max_length = len(pairs)


num_targets = len(target_genes)
nrows = 2 + max_length
ncols = 1 + 2 * num_targets

table = [["" for _ in range(ncols)] for _ in range(nrows)]


for j, target in enumerate(target_genes):
    gene_col = 1 + 2*j
    score_col = 2 + 2*j

    table[0][gene_col] = target
    table[1][gene_col] = "0"

    pairs = all_pairs[target]
    for i, (gene_name, score) in enumerate(pairs):
        row_index = i + 2
        table[row_index][gene_col] = gene_name
        table[row_index][score_col] = score


result_df = pd.DataFrame(table)

with pd.ExcelWriter(args.output, engine="openpyxl") as writer:
    result_df.to_excel(writer, sheet_name="AllResults", header=False, index=False)

print(f"{args.output} saved.")