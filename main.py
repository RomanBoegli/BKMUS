import pandas as pd
from scipy import stats
from tabulate import tabulate

# Load the file
file_path = "DataCollection_Dummy.xlsx"
df = pd.read_excel(file_path, header=3)

# Clean columns
df = df.drop(
    columns=[col for col in df.columns if "Unnamed" in str(col)], errors="ignore"
)

# Label backup fields
df["BackupPrompt"] = df["Prompt"].map({1: "Yes", 0: "No"})
df["BackupProof"] = df["Validation"].map({1: "Yes", 0: "No"})

# Heuristics
heuristics = ["G1", "G2", "G3", "G4", "G5", "G6", "G7", "G8"]
df["TaskTotal"] = df[heuristics].sum(axis=1)
df["TaskMean"] = df[heuristics].mean(axis=1)

# ---------------------
# H1: Descriptive stats
# ---------------------
print("\n\033[1m--- H1: Wallet-Level Averages ---\033[0m")
h1_summary = df.groupby("Wallet")[heuristics + ["TaskMean"]].mean().round(2)
print(tabulate(h1_summary, headers="keys", tablefmt="fancy_grid"))  # type: ignore

# H1 conclusion (descriptive only)
print(
    "Manual comparison with results form table above and Eskandari et al. (2018)'s reported usability challenges is required to determine improvement."
)

# ---------------------
# H2: Conditional test
# ---------------------
print("\n\033[1m--- H2: Group Comparison by Wallet Type ---\033[0m")
wallet_means = df.groupby(["Wallet", "Type"])["TaskMean"].mean().reset_index()
group_hw = wallet_means[wallet_means["Type"] == "Hardware"]["TaskMean"]
group_sw = wallet_means[wallet_means["Type"] == "Software"]["TaskMean"]
group_cu = wallet_means[wallet_means["Type"] == "Custodial"]["TaskMean"]

normality_ok = False
levene_ok = False

if all(len(g) >= 3 for g in [group_hw, group_sw, group_cu]):
    sh_hw = stats.shapiro(group_hw)
    sh_sw = stats.shapiro(group_sw)
    sh_cu = stats.shapiro(group_cu)
    normality_ok = all(p > 0.05 for p in [sh_hw.pvalue, sh_sw.pvalue, sh_cu.pvalue])
    print(
        f"Shapiro-Wilk p-values: HW={sh_hw.pvalue:.3f}, SW={sh_sw.pvalue:.3f}, CU={sh_cu.pvalue:.3f}"
    )
else:
    print("Not enough data for normality test.")

if all(len(g) >= 2 for g in [group_hw, group_sw, group_cu]):
    levene = stats.levene(group_hw, group_sw, group_cu)
    levene_ok = bool(levene.pvalue > 0.05)
    print(f"Levene's test p-value: {levene.pvalue:.3f}")
else:
    levene = None
    print("Not enough data for Levene's test.")

if normality_ok and levene_ok:
    print("\033[92m Using ANOVA (assumptions met)\033[0m")
    h2_result = stats.f_oneway(group_hw, group_sw, group_cu)
    print(f"ANOVA F={h2_result.statistic:.3f}, p={h2_result.pvalue:.4f}")
else:
    print("\033[93m Assumptions not met → Using Kruskal-Wallis\033[0m")
    h2_result = stats.kruskal(group_hw, group_sw, group_cu)
    print(f"Kruskal-Wallis H={h2_result.statistic:.3f}, p={h2_result.pvalue:.4f}")

# H2 conclusion
if h2_result.pvalue < 0.05:
    print("✅ H2 supported: significant difference between wallet types.")
else:
    print("❌ H2 not supported: no significant difference.")

# ---------------------
# H3a: Prompt vs. G1 and G5
# ---------------------
print("\n\033[1m--- H3a: Backup Prompt Effect ---\033[0m")
g1_prompt = df.groupby(["Wallet", "Expert", "BackupPrompt"])["G1"].mean().reset_index()
g5_prompt = df.groupby(["Wallet", "Expert", "BackupPrompt"])["G5"].mean().reset_index()

g1p_yes = g1_prompt[g1_prompt["BackupPrompt"] == "Yes"]["G1"]
g1p_no = g1_prompt[g1_prompt["BackupPrompt"] == "No"]["G1"]
g5p_yes = g5_prompt[g5_prompt["BackupPrompt"] == "Yes"]["G5"]
g5p_no = g5_prompt[g5_prompt["BackupPrompt"] == "No"]["G5"]

g1_stat = stats.mannwhitneyu(g1p_yes, g1p_no, alternative="two-sided")
g5_stat = stats.mannwhitneyu(g5p_yes, g5p_no, alternative="two-sided")

print(f"G1: U={g1_stat.statistic:.2f}, p={g1_stat.pvalue:.4f}")
print(f"G5: U={g5_stat.statistic:.2f}, p={g5_stat.pvalue:.4f}")

# H3a conclusions
if g1_stat.pvalue < 0.05:
    print("✅ H3a (G1): supported - prompt has a significant effect.")
else:
    print("❌ H3a (G1): not supported - no significant effect.")

if g5_stat.pvalue < 0.05:
    print("✅ H3a (G5): supported - prompt has a significant effect.")
else:
    print("❌ H3a (G5): not supported - no significant effect.")

# ---------------------
# H3b: Validation vs. G1 and G5
# ---------------------
print("\n\033[1m--- H3b: Backup Validation Effect ---\033[0m")
g1_val = df.groupby(["Wallet", "Expert", "BackupProof"])["G1"].mean().reset_index()
g5_val = df.groupby(["Wallet", "Expert", "BackupProof"])["G5"].mean().reset_index()

g1v_yes = g1_val[g1_val["BackupProof"] == "Yes"]["G1"]
g1v_no = g1_val[g1_val["BackupProof"] == "No"]["G1"]
g5v_yes = g5_val[g5_val["BackupProof"] == "Yes"]["G5"]
g5v_no = g5_val[g5_val["BackupProof"] == "No"]["G5"]

g1v_stat = stats.mannwhitneyu(g1v_yes, g1v_no, alternative="two-sided")
g5v_stat = stats.mannwhitneyu(g5v_yes, g5v_no, alternative="two-sided")

print(f"G1: U={g1v_stat.statistic:.2f}, p={g1v_stat.pvalue:.4f}")
print(f"G5: U={g5v_stat.statistic:.2f}, p={g5v_stat.pvalue:.4f}")

# H3b conclusions
if g1v_stat.pvalue < 0.05:
    print("✅ H3b (G1): supported - validation has a significant effect.")
else:
    print("❌ H3b (G1): not supported - no significant effect.")

if g5v_stat.pvalue < 0.05:
    print("✅ H3b (G5): supported - validation has a significant effect.")
else:
    print("❌ H3b (G5): not supported - no significant effect.")
