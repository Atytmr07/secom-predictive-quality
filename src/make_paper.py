"""Makale taslağı (Report 4 için). Tüm sayılar reports/*.csv içindeki gerçek analiz çıktılarından gelir."""
import pandas as pd
from docx import Document
from docx.shared import Pt, Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH

R = "reports/"
d = Document()
st = d.styles["Normal"]; st.font.name = "Times New Roman"; st.font.size = Pt(11)
for lvl, sz in ((1, 14), (2, 12)):
    d.styles[f"Heading {lvl}"].font.name = "Times New Roman"; d.styles[f"Heading {lvl}"].font.size = Pt(sz)

H = lambda s, l=1: d.add_heading(s, l)
P = lambda s: d.add_paragraph(s)
B = lambda s: d.add_paragraph(s, style="List Bullet")
tab_n = [0]; fig_n = [0]


def table(caption, header, rows, size=9):
    tab_n[0] += 1
    c = d.add_paragraph(f"Table {tab_n[0]}. {caption}"); c.runs[0].bold = True
    t = d.add_table(rows=1, cols=len(header)); t.style = "Light Grid Accent 1"
    for i, h in enumerate(header):
        t.rows[0].cells[i].text = h
    for r in rows:
        cells = t.add_row().cells
        for i, v in enumerate(r):
            cells[i].text = str(v)
    for row in t.rows:
        for cell in row.cells:
            for p in cell.paragraphs:
                for run in p.runs:
                    run.font.size = Pt(size)
    d.add_paragraph("")


def figure(path, caption, width=6.0):
    fig_n[0] += 1
    d.add_picture(R + path, width=Inches(width)); d.paragraphs[-1].alignment = WD_ALIGN_PARAGRAPH.CENTER
    c = d.add_paragraph(f"Figure {fig_n[0]}. {caption}"); c.runs[0].italic = True


f2 = lambda v: f"{v:.2f}"
f3 = lambda v: f"{v:.3f}"

# ============================================================ TITLE
t = d.add_heading("Does the Validation Protocol Inflate Defect-Prediction Performance? A Time-Aware Evaluation on the SECOM Semiconductor Dataset", 0)
P("[Author 1 name], [Author 2 name]\n[Department, University]\nIndependent Study and Industrial Applications, Report 4 (draft for supervisor review)")

H("Abstract")
P("Studies on the public SECOM semiconductor dataset usually report results from random cross-validation, although production data are ordered in time. This study asks how much the validation protocol changes the apparent performance of defect-prediction models, whether sensor drift explains the difference, and whether the models outperform a classical multivariate control chart and a cost-based benchmark. Logistic regression, random forest and XGBoost were evaluated on 1,567 production runs (104 failures) under random, blocked, chronological and walk-forward validation. Sensor drift was tested with Kolmogorov–Smirnov tests, the models were compared with a PCA-based Hotelling T² chart, and cost-based decision thresholds were examined. For random forest, lift over random guessing fell from 2.69 under random cross-validation to 0.95 under a chronological split and 1.12 under walk-forward validation; the other models showed the same direction. About 61% of the usable sensors drifted, yet models built on stable sensors did not outperform models built on drifting sensors, and the T² chart was also indistinguishable from random guessing. A cost saving of about 35% seen in cross-validation disappeared when thresholds were chosen on earlier runs only. On this dataset, random validation therefore overstates both statistical and economic value. Confidence intervals are wide because only 26 failures fall in the chronological test set.")
P("Keywords: predictive quality; validation protocol; concept drift; statistical process control; semiconductor manufacturing; class imbalance")

# ============================================================ 1 INTRODUCTION
H("1. Introduction")
H("1.1 Background", 2)
P("In many factories, product quality is confirmed only at the end of the line, in a final electrical or functional test. By then, material, machine time and labour have been spent on products that may be scrapped. Predictive quality uses process data, such as sensor readings, machine settings and material properties, to estimate product quality before or without that final test (Tercan & Meisen, 2022). Semiconductor manufacturing is a typical setting: the process has many steps, equipment records hundreds of variables, and failures are rare.")
P("The SECOM dataset (McCann & Johnston, 2008) has become a common benchmark for this task. It contains 1,567 production runs described by 590 anonymised sensor values and a pass/fail label, with about 6.6% failures. Because the data are small, imbalanced, partly missing and high-dimensional, much of the SECOM literature concentrates on data preparation: imputation, feature selection and resampling (Kerdprasop & Kerdprasop, 2011; Salem et al., 2018; Park et al., 2024; Zheng et al., 2025).")
H("1.2 Problem and motivation", 2)
P("A defect-prediction model is useful only if it works on production that has not happened yet. Production data, however, are ordered in time, and the process can change as equipment ages, materials vary and operating conditions shift. The concept-drift literature warns that models validated on randomly selected records may perform much worse on later data (Gama et al., 2014; Jourdan et al., 2021). In random cross-validation, a test run has neighbours from the same weeks in the training set, so the model is rewarded for recognising a period rather than for predicting the future.")
P("The question matters for Industrial Engineering because the model supports a decision: which products to inspect, rework or scrap. A missed defect and a false alarm have different costs. If the validation protocol is optimistic, a plant may adopt a model whose statistical and economic value is smaller than reported, or absent.")
H("1.3 Research gap", 2)
P("Based on the abstracts and summaries of the studies reviewed in Section 2, three points appear to be insufficiently examined for SECOM. First, the reviewed SECOM studies focus on data preparation and prediction scores, and their summaries do not describe a time-ordered evaluation, although the dataset has timestamps. Second, the link between sensor drift and loss of predictive performance is rarely measured on this dataset. Third, classical multivariate statistical process control (SPC), the standard industrial monitoring tool, is rarely used as a baseline against which machine-learning models are compared, and evaluation seldom considers the cost of wrong decisions. These statements describe the studies we reviewed; a wider full-text search is needed before claiming that the points have never been studied.")
H("1.4 Objective and research questions", 2)
P("The objective is to measure how strongly the validation protocol changes the apparent performance of defect-prediction models on SECOM, to quantify sensor drift and test whether it accounts for the loss in performance, and to compare the models with an SPC baseline using statistical and cost-based criteria. The study addresses four research questions.")
B("RQ1: How does model performance differ between random cross-validation and time-aware validation?")
B("RQ2: How much do sensor distributions change over time, and is the loss of performance related to drift?")
B("RQ3: How does a PCA-based Hotelling T² chart compare with the machine-learning models on later production runs?")
B("RQ4: Under assumed cost ratios between missed defects and false alarms, does a model-based decision threshold reduce total cost compared with inspecting nothing or everything?")
H("1.5 Contribution", 2)
P("The study does not propose a new algorithm. Its contributions are empirical: (i) a side-by-side comparison of four validation protocols using the same pipeline, with uncertainty intervals; (ii) a drift analysis in which the sensor subsets are defined from the training period only, so that the test period does not influence the selection; (iii) an SPC baseline on the same data; and (iv) a check of whether a cost saving seen in cross-validation survives when the decision threshold is fixed on earlier data. All code is public (see Declarations).")

# ============================================================ 2 LITERATURE
H("2. Literature Review")
P("The literature was searched through Google Scholar and publisher databases with the keywords \"predictive quality\", \"SECOM\", \"semiconductor fault detection\", \"class imbalance\", \"concept drift\", \"multivariate SPC\" and \"Hotelling T2\". Peer-reviewed publications were preferred; one arXiv preprint is included and marked. The entries were checked against abstracts and publisher pages, and the full texts still have to be verified (see Limitations). The review is organised in four themes.")
H("2.1 Predictive quality in manufacturing", 2)
P("Two systematic reviews describe the field. Tercan and Meisen (2022) reviewed predictive-quality studies from 2012 to 2021 and grouped them by manufacturing process, data and model, concluding that an overall view of methods and open obstacles is missing. Kang et al. (2020) screened 271 papers on machine learning in production lines and analysed 39 primary studies. Both show a broad and fragmented field with varied data, targets and metrics, which makes results hard to compare and motivates work on a shared public benchmark.")
H("2.2 Studies on the SECOM benchmark", 2)
P("Most SECOM studies address the three data problems of missing values, many noisy features and rare failures. Kerdprasop and Kerdprasop (2011) combined feature selection with boosting to handle the pass/fail imbalance. Salem et al. (2018) compared 288 combinations of pruning, imputation, feature selection and classifiers and proposed a nearest-neighbour imputation method. Park et al. (2024) examined preprocessing choices with several models. Zheng et al. (2025) combined multi-objective feature selection with a self-paced ensemble, and Nuhu et al. (2023) compared synthetic-data generation, imputation and feature selection with ten models, reporting accuracies between 99.5% and 100%.")
P("Two features of this work are relevant here. The emphasis is on preprocessing and score improvement, and the reported results vary widely, from near-perfect accuracy to moderate AUROC values. Accuracy near 100% on a dataset where about 93% of runs pass deserves caution, since accuracy is weak under strong imbalance and results also depend on whether resampling was applied before or after splitting the data. We could not verify the evaluation design of these studies from their abstracts, so we do not compare our numbers with theirs directly.")
H("2.3 Statistical process control and machine learning", 2)
P("Multivariate SPC is the classical way to monitor many correlated variables. Kourti and MacGregor (1995) describe how the Hotelling T² statistic and projection methods such as PCA and PLS extend the univariate control chart: they learn normal behaviour from in-control data and signal when a new observation departs from it. For semiconductor processes, He and Wang (2007) proposed a k-nearest-neighbour rule that also needs only normal-operation data. In the SECOM studies above, machine-learning classifiers are the main tools, and comparison with an SPC baseline is not reported in the summaries we reviewed.")
H("2.4 Process drift and model reliability", 2)
P("Concept drift refers to changes over time in the data distribution or in the relation between inputs and target. Gama et al. (2014) survey strategies to detect and adapt to it, and Hinder et al. (2024) note that locating and explaining drift is less studied than detecting it. In an industrial example, Jourdan et al. (2021, preprint) trained several algorithms on the first ten months of a 36-month gas-sensor dataset and tested them on the remainder; all degraded strongly over time. That dataset is not production-quality data, but the finding supports the concern that random validation can hide a loss of performance on later data.")
H("2.5 Synthesis", 2)
P("The literature on SECOM concentrates on improving predictions through data preparation, while the drift literature shows that performance often decays over time. The two lines are rarely connected: SECOM studies seldom report testing on later runs, and drift studies rarely use SECOM. SPC baselines and cost-based evaluation are also seldom combined with machine learning on this benchmark. The present study addresses this combination on a single, well-known dataset.")

# ============================================================ 3 METHODOLOGY
H("3. Methodology")
H("3.1 Study design", 2)
P("The study is a quantitative, retrospective experiment on a public dataset. Figure 1 summarises the process. The hypotheses were stated as follows: H1, lift over random guessing is lower under time-aware validation than under random cross-validation; H2a, sensors flagged as drifting within the training period shift more between training and test periods than stable sensors; H2b, models trained on stable sensors perform better on later runs than models trained on the same number of drifting sensors; H3, on held-out later runs the machine-learning models are not significantly better than the T² chart; H4, a model-based threshold lowers total cost compared with inspecting nothing or everything, but less so when validated chronologically. A pilot run was made while preparing the first report, so the hypotheses were formulated with some knowledge of it; the results below were produced by a fixed-seed re-run of the final code.")
figure("flowchart.png", "Methodological flowchart of the study.", width=3.6)
H("3.2 Preprocessing and models", 2)
P("Sensors with more than 50% missing values were removed before modelling (a rule that does not use the label). All further steps were placed in a pipeline that is fitted on training data only: median imputation, removal of constant sensors, standardisation and selection of the 40 sensors with the highest mutual information with the label. This prevents information from the test data from influencing preprocessing. Three classifiers were used: logistic regression (C = 0.05, balanced class weights), random forest (300 trees, minimum leaf size 3, balanced subsample weights) and XGBoost (300 trees, depth 3, learning rate 0.05, subsample 0.8, column sampling 0.6, positive-class weight equal to the ratio of passes to failures). Logistic regression was also combined with SMOTE oversampling inside the training folds. These standard models were chosen deliberately, because the focus is the validation protocol and not model novelty. Hyperparameters were not tuned extensively, since tuning on 104 positives risks fitting noise.")
H("3.3 Validation protocols", 2)
P("The same pipeline and models were evaluated under four protocols. (1) Random stratified 5-fold cross-validation. (2) Blocked 5-fold cross-validation, in which runs are split into five contiguous blocks without shuffling; the remaining blocks, including later ones, are used for training. (3) A chronological split: the first 70% of runs (1,096 runs, 78 failures) for training and the last 30% (471 runs, 26 failures) for testing. (4) Walk-forward evaluation: training on the first 500 runs and predicting the next 150, then expanding the training window and repeating, which covers the remaining 1,067 runs (45 failures). Predictions of all test folds were pooled before computing a metric. Cross-validation results in Table 2 are averages over three repetitions with different seeds, whereas Table 3 uses a single random split.")
H("3.4 Evaluation metrics", 2)
P("Accuracy is not informative here because predicting \"pass\" for every run gives about 93% accuracy. The main metric is PR-AUC (average precision), whose value for random guessing equals the defect rate. Because the defect rate differs between protocols (6.6%, 6.6%, 5.5% and 4.2% respectively), results are compared through lift, defined as PR-AUC divided by the defect rate of the evaluated runs. ROC-AUC and best-threshold F1 are secondary. Uncertainty is shown with 95% bootstrap intervals (500 resamples of the pooled predictions for lift; 1,000 for PR-AUC elsewhere). The intervals reflect the small number of failures but do not model the dependence between runs.")
H("3.5 Drift analysis", 2)
P("Drift was measured with the two-sample Kolmogorov–Smirnov (KS) test for each of the 446 sensors that were not constant and had at most 50% missing values, comparing the first 70% and last 30% of runs, with a Bonferroni-corrected significance level of 0.05/446. To test whether drift explains the loss of performance without leaking test information, sensors were labelled using the training period only: the 1,096 training runs were split into two halves, and each sensor was tested between halves. Sensors with a Bonferroni-significant difference were labelled drifting (208 sensors); sensors with p ≥ 0.05 were labelled stable (101 sensors); the remaining 137 were left out. Random forests were then trained on 101-sensor subsets drawn at random from the drifting pool, from the stable pool and from all 446 sensors (20 draws each) and tested on the last 30% of runs. The stable pool has exactly 101 sensors, so every stable draw contains the same sensors in a different column order; the variation among stable draws therefore reflects only the model's sensitivity to column order and not a choice of sensors. As a check, the mean KS distance between the training and test periods was computed for the two labelled groups.")
H("3.6 SPC baseline", 2)
P("A PCA model retaining 90% of the variance (123 components) was fitted on the good runs of the training period after median imputation and standardisation. The Hotelling T² statistic of a run, computed in the principal-component space, was used as an anomaly score, with the upper control limit set at the 99th percentile of the training T² values (553.4). On the test period the T² score was evaluated with PR-AUC and ROC-AUC, like the classifiers.")
H("3.7 Cost analysis", 2)
P("Total cost was defined as C_FN times the number of missed failures plus C_FP times the number of good runs flagged, with C_FP = 1 and C_FN in {5, 10, 20, 50}. No plant cost data exist for SECOM, so the ratios are assumptions and the analysis is a sensitivity analysis, not an estimate of real savings. Two benchmarks were used: inspecting nothing (all runs accepted) and inspecting everything. The optimal threshold was first found on cross-validated random forest scores for all runs, which is optimistic because the threshold and the evaluation use the same data. As a stricter check, the threshold was chosen on out-of-fold predictions within the training period only and then applied to the later 30% of runs.")
H("3.8 Reproducibility", 2)
P("All random processes use fixed seeds, including the mutual-information step. Analyses were run in Python with pandas, scikit-learn, imbalanced-learn, XGBoost, SciPy and SHAP. The code, figures and result tables are in the public repository listed in the Declarations.")

# ============================================================ 4 DATA AND ANALYSIS
H("4. Data and Analysis")
H("4.1 Dataset", 2)
table("Characteristics of the SECOM dataset and of the data after preparation.", ["Item", "Value"], [
    ("Source", "UCI Machine Learning Repository (McCann & Johnston, 2008)"),
    ("Production runs", "1,567 (19 July – 17 October 2008)"),
    ("Sensors", "590 anonymised numeric variables; physical meaning not disclosed"),
    ("Failures", "104 (6.6%); 1,463 passes"),
    ("Missing cells", "About 4.5% of all values"),
    ("Sensors removed for >50% missing values", "28"),
    ("Constant sensors", "116"),
    ("Sensors in the drift analysis (non-constant, ≤50% missing)", "446"),
    ("Missing share among those 446 sensors", "median 0.2%, maximum 45.6%"),
    ("Outlying values (robust z-score > 3.5)", "3.0% of cells; 74 sensors have more than 5% outlying values"),
    ("Sensor pairs with |r| > 0.9", "347"),
    ("Mean number of outlying sensors per run", "failed runs 16.2, passed runs 13.2 (descriptive)"),
])
P("The label is coded 1 for failure and 0 for pass (the original file uses 1 and −1). Outliers were kept because extreme values may carry the signal in defect detection. The high number of strongly correlated sensors motivates feature selection and PCA.")
figure("fig_eda.png", "Exploratory analysis: (a) class distribution, (b) distribution of the missing-value share per sensor, (c) weekly defect rate.", width=6.4)
P("Figure 2 shows the strong imbalance and that most sensors have almost no missing values, while a small group of sensors is largely missing. The defect rate is not constant over time: it was 11.8% in the first 500 runs (59 failures) and 4.2% in the remaining 1,067 runs (45 failures). This is the reason for comparing protocols through lift, and it already suggests that the process changed during the three months.")

# ============================================================ 5 RESULTS
H("5. Results")
H("5.1 Overall model performance", 2)
m = pd.read_csv(R + "model_results.csv"); b = pd.read_csv(R + "cv_bootstrap.csv").set_index("model")
rows = []
for _, r in m.iterrows():
    ci = b.loc[r.model]
    rows.append((r.model, f3(r.cv_prauc), f"{f3(ci.lo)}–{f3(ci.hi)}", f3(r.cv_roc), f3(r.cv_bestF1), f3(r.time_prauc), f3(r.time_roc)))
table("Model performance in repeated cross-validation and on the chronological hold-out. The bootstrap interval refers to PR-AUC of the averaged out-of-fold scores, which is slightly higher than the fold-wise average in the first PR-AUC column. Random guessing gives PR-AUC 0.066 in cross-validation and 0.055 on the hold-out.",
      ["Model", "CV PR-AUC", "95% CI (bootstrap)", "CV ROC-AUC", "CV best F1", "Hold-out PR-AUC", "Hold-out ROC-AUC"], rows, size=8.5)
P("In cross-validation, random forest was best (PR-AUC 0.187), followed by XGBoost (0.153) and logistic regression (0.120); SMOTE did not improve logistic regression. On the chronological hold-out all models were close to random guessing, and the ROC-AUC of random forest (0.483) was not above 0.5.")

H("5.2 Validation protocols (RQ1)", 2)
p = pd.read_csv(R + "protocol_comparison.csv")
order = ["Random stratified 5-fold", "Blocked 5-fold (contiguous, future in train)", "Chronological 70/30", "Walk-forward (expanding)"]
rows = []
for mod, lab in (("LogReg (class_weight)", "Logistic regression"), ("RandomForest", "Random forest"), ("XGBoost", "XGBoost")):
    for pr in order:
        r = p[(p.model == mod) & (p.protocol == pr)].iloc[0]
        rows.append((lab, pr.replace(" (contiguous, future in train)", ""), int(r.n_test), f3(r.base_rate), f3(r.prauc), f2(r.lift), f"{f2(r.lift_lo)}–{f2(r.lift_hi)}", f3(r.roc)))
table("Performance of the same pipeline under four validation protocols. Lift = PR-AUC divided by the defect rate of the evaluated runs.",
      ["Model", "Protocol", "Runs evaluated", "Defect rate", "PR-AUC", "Lift", "95% CI of lift", "ROC-AUC"], rows, size=8.5)
figure("fig_protocol_lift.png", "Lift over random guessing by validation protocol with 95% bootstrap intervals.", width=5.8)
P("For every model, lift was highest under random cross-validation and lower under the time-aware protocols (Table 3, Figure 3). For random forest, lift fell from 2.69 (95% CI 2.06–3.54) under random cross-validation to 1.60 under blocked cross-validation, 0.95 (0.81–1.39) under the chronological split and 1.12 (0.89–1.82) under walk-forward evaluation. XGBoost fell from 2.09 to 1.05 and 1.30, and logistic regression from 1.81 to 1.18 and 1.25. Under the chronological protocol the intervals of all three models include 1, so performance cannot be distinguished from random guessing. The intervals are wide, especially for the chronological test with only 26 failures, and the ordering among the three time-aware protocols is not reliable. H1 is supported in direction for all three models.")
P("Table 3 uses a fixed configuration. A separate set of walk-forward experiments (Table 4; random forest with 300 trees and minimum leaf size 5, logistic regression with C = 0.01) varied the number of selected sensors and the training window. The best configuration was a random forest on all sensors with an expanding window (PR-AUC 0.067 against a defect rate of 0.042, lift about 1.6); reducing the number of sensors to 10 or 40 or using a sliding window of 500 runs did not help, and several configurations were at or below the random level.")
tw = pd.read_csv(R + "temporal_results.csv")
table("Walk-forward configurations (random guessing: PR-AUC 0.042).", ["Configuration", "PR-AUC", "ROC-AUC"],
      [(r.config, f3(r.prauc), f3(r.roc)) for _, r in tw.iterrows()])

H("5.3 Sensor drift (RQ2)", 2)
figure("fig_drift.png", "Drift between the first 70% and last 30% of runs: (a) the most shifted sensor, (b) distribution of KS distances over all 446 sensors.", width=6.2)
P("Of the 446 sensors, 270 (61%) differed significantly between the first 70% and last 30% of runs (Bonferroni-corrected KS test), and 31 of the 40 sensors selected by mutual information on the first 70% (78%) were among them. The largest shifts were found in s116 (KS = 0.61), s542 (0.56), s543 (0.53), s545 (0.50) and s78 (0.47). Drift is therefore common and the sensors that the model relies on are not more stable than the others.")
P("Labelling sensors from the training period alone worked as a prediction of later change: the mean KS distance between the training and test periods was 0.213 for sensors labelled drifting and 0.107 for sensors labelled stable (H2a supported). However, the labelling did not help prediction (Table 5, Figure 5).")
dl = pd.read_csv(R + "drift_performance_link.csv")
names = {"stabil sensörler": "Stable sensors", "drift'li sensörler": "Drifting sensors", "rastgele (tüm sensörler havuzu)": "Random sensors (all pools)"}
table("Random forest on equal-sized (101 sensors) subsets, tested on the last 30% of runs; mean and standard deviation over 20 draws (for the stable group the subset is the whole group, see Section 3.5). Random guessing: PR-AUC 0.055, ROC-AUC 0.5.",
      ["Sensor subset", "PR-AUC (mean ± SD)", "ROC-AUC (mean ± SD)", "Lift"],
      [(names[r.subset], f"{r.prauc_mean:.3f} ± {r.prauc_sd:.3f}", f"{r.roc_mean:.3f} ± {r.roc_sd:.3f}", f2(r.lift)) for _, r in dl.iterrows()])
figure("fig_drift_link.png", "PR-AUC of random forests trained on stable, drifting and random sensor subsets (last 30% of runs).", width=4.6)
P("Models built only on stable sensors (PR-AUC 0.068) did not outperform models built on drifting sensors (0.076) or on random sensors (0.065), and all three were close to the defect rate of 0.055. The spread among draws (SD about 0.015) is as large as the differences between the groups. H2b is therefore not supported: removing the sensors that drifted within the training period did not restore predictive performance. The standard deviations reflect model and sensor-draw variation only and do not include the sampling uncertainty of a test set with 26 failures.")

H("5.4 SPC versus machine learning (RQ3)", 2)
sv = pd.read_csv(R + "spc_vs_ml.csv")
table("Hotelling T² chart and random forest on the chronological hold-out, with 95% bootstrap intervals. Random guessing: PR-AUC 0.055, ROC-AUC 0.5.",
      ["Method", "PR-AUC (95% CI)", "ROC-AUC (95% CI)"],
      [(r.yontem, f"{f3(r.prauc)} ({f3(r.prauc_lo)}–{f3(r.prauc_hi)})", f"{f3(r.roc)} ({f3(r.roc_lo)}–{f3(r.roc_hi)})") for _, r in sv.iterrows()])
P("The T² chart signalled an alarm for about 3% of the test runs, and none of the alarmed runs was a failure. Both the chart and the random forest have intervals that include the random-guessing value, and they cannot be told apart from each other (H3 supported). The classical method is therefore not a remedy on this dataset.")

H("5.5 Cost-based analysis (RQ4)", 2)
cc = pd.read_csv(R + "cost_cv.csv")
rows = []
for _, r in cc.iterrows():
    best = min(r.no_inspection, r.full_inspection)
    rows.append((int(r.c_fn), f2(r.best_threshold), int(r.model_cost), int(r.no_inspection), int(r.full_inspection), f"{100 * (1 - r.model_cost / best):.1f}%"))
table("Cost analysis with cross-validated random forest scores (optimistic: threshold and evaluation use the same data). Costs are in false-alarm units.",
      ["C_FN / C_FP", "Best threshold", "Model cost", "Inspect nothing", "Inspect everything", "Saving vs best trivial"], rows)
figure("fig_cost_cv.png", "Total cost as a function of the decision threshold for different cost ratios (cross-validated random forest scores).", width=5.0)
P("With cross-validated scores, the model-based threshold had a lower total cost than both trivial strategies for all four ratios, for example 672 against 1,040 (inspect nothing) and 1,463 (inspect everything) at a ratio of 10, a saving of about 35%. This picture changes under the stricter chronological check.")
ch = pd.read_csv(R + "cost_chronological.csv"); labs = {"LogReg (class_weight)": "Logistic regression", "RandomForest": "Random forest", "XGBoost": "XGBoost"}
rows = []
for _, r in ch.iterrows():
    best = r.test_best_trivial
    rows.append((labs[r.model], int(r.c_fn), f2(r.threshold_from_train), int(r.test_cost_model), int(r.test_cost_no_inspection), int(r.test_cost_full_inspection), f"{100 * (r.test_cost_model / best - 1):+.1f}%"))
table("Chronological cost check: threshold chosen from out-of-fold predictions in the first 70% of runs and applied to the last 30% (471 runs, 26 failures). A positive percentage means the model costs more than the best trivial strategy.",
      ["Model", "C_FN / C_FP", "Threshold", "Model cost", "Inspect nothing", "Inspect everything", "Model vs best trivial"], rows, size=8.5)
P("When the threshold was fixed on earlier runs, no model beat the better of the two trivial strategies at any ratio. The model was as costly as the best trivial strategy only for logistic regression at a ratio of 5 (130 against 130), and was more costly in the other eleven cases, by up to 65% (random forest at a ratio of 50: 736 against 445). H4 is therefore supported only for the cross-validated analysis and not for the chronological one. The cost ratios are assumptions, so these figures show the direction of the effect, not savings in money.")

H("5.6 Influential sensors", 2)
sh = pd.read_csv(R + "shap_top.csv")
P("A SHAP analysis of a random forest fitted on all runs ranked sensors s477, s33, s510, s65 and s130 highest (mean absolute SHAP values " + ", ".join(f"{v:.3f}" for v in sh.mean_abs_shap[:5]) + "). Because the sensors are anonymous and the model was fitted on all runs, this ranking is descriptive: it does not support a physical interpretation, and it cannot be assumed to be stable over time given the drift reported above.")

# ============================================================ 6 DISCUSSION
H("6. Discussion")
P("The central result is the ordering of validation protocols. For all three models, the lift over random guessing was largest when the runs were shuffled and smallest when the model had to predict later runs. For random forest, the best model under random cross-validation, lift dropped from about 2.7 to about 1. A plausible reason is that random splitting places runs from the same period into both training and test sets, so that the model can exploit period-specific patterns. This is consistent with the drift literature, in which models degrade on later data (Gama et al., 2014; Jourdan et al., 2021), but our experiment does not isolate the mechanism.")
P("The drift results qualify the simple explanation that drifting sensors cause the loss. Drift is widespread (61% of usable sensors) and it is predictable from the training period: sensors that moved within the training period moved more afterwards. Yet models using only stable sensors were not better than models using drifting sensors. Several explanations remain open. The signal may be weak even in the early period, so that the models rely on chance structure; the relation between sensors and failures may change over time, and not only the distribution of sensor values; and the defect rate itself fell from 11.8% in the first 500 runs to 4.2% afterwards, which suggests changes that the KS tests on single sensors do not capture. With only 26 failures in the test period, the experiment also has little power to detect a modest benefit.")
P("The comparison with the T² chart indicates that the difficulty is not a matter of choosing machine learning over classical SPC. Both were indistinguishable from random guessing on the chronological test. The result agrees with the idea that an in-control model learned from early runs may not describe later runs, but the chart's single configuration (90% variance, 99th percentile limit) was not tuned, and other SPC variants, such as those of He and Wang (2007), were not tested.")
P("The cost analysis shows why the validation protocol matters in practice. With cross-validated scores, a model-based threshold appears to save about 35% at a cost ratio of 10; with a threshold fixed on earlier runs, it costs more than the best trivial strategy in eleven of twelve cases. The optimistic validation therefore inflates economic conclusions as well as statistical ones. The cost ratios are assumed, so the relevant point is the contrast between the two analyses, not the numbers.")
P("Relation to previous studies. Our PR-AUC and lift values cannot be compared directly with the high accuracy and AUROC values reported in some SECOM studies (Nuhu et al., 2023; Zheng et al., 2025), because the metrics, the positive class and the validation designs differ and could not be checked in full text. The finding that random validation is optimistic is, however, a reason to check, in those studies, whether resampling and feature selection were applied inside the training folds and whether any time-ordered evaluation was performed. The practical implication for Industrial Engineering is to test predictive-quality models on later production runs before relying on them, to report uncertainty, and to evaluate decisions with a cost view.")

# ============================================================ 7 CONCLUSION
H("7. Conclusion")
P("On the SECOM dataset, the validation protocol strongly influences how good a defect-prediction model appears. Random forest was about 2.7 times better than random guessing under random cross-validation but not distinguishable from random guessing on a chronological hold-out; logistic regression and XGBoost followed the same pattern. Most sensors drifted, but removing the drifting sensors did not restore performance, a classical Hotelling T² chart was equally uninformative on later runs, and a cost saving found in cross-validation did not survive a chronological check. For predictive-quality studies, time-aware validation and a cost-based evaluation should be reported next to cross-validation, and negative out-of-time results should be reported as findings.")

# ============================================================ 8 LIMITATIONS
H("8. Limitations and Future Research")
B("Single dataset from one process and period; the findings may not generalise.")
B("Few failures: 104 in total and only 26 in the chronological test set. Confidence intervals are wide and the differences among the time-aware protocols cannot be ranked.")
B("The bootstrap intervals resample runs independently and ignore temporal dependence.")
B("Sensors are anonymous, so domain-based feature engineering and physical interpretation were not possible.")
B("Hyperparameters were not tuned and only three standard models and one SPC configuration were tested; other methods might behave differently.")
B("Cost ratios are assumed because no plant cost data are available.")
B("The hypotheses were formulated after a pilot run, so the study is partly exploratory.")
B("The literature entries were checked from abstracts and publisher pages, not from full texts; statements on what other SECOM studies did or did not do must be confirmed.")
P("Future work could repeat the protocol comparison on other public manufacturing datasets that have timestamps, test drift-adaptive approaches such as retraining on sliding windows or online learning, examine drift in the relation between sensors and failures instead of the sensor distributions alone, tune and compare more SPC variants, and use real cost data from a plant.")

# ============================================================ DECLARATIONS
H("Declarations")
P("Data availability. The SECOM dataset is public at https://archive.ics.uci.edu/dataset/179/secom. Code, figures and result tables are available at https://github.com/Atytmr07/secom-predictive-quality.")
P("Ethics. The study uses a public, anonymised industrial dataset and involves no human participants.")
P("Author contributions (CRediT). [To be completed by the authors, for example: Conceptualization; Methodology; Software; Formal analysis; Writing – original draft; Writing – review and editing.]")
P("Conflict of interest. [To be confirmed by the authors: none declared.]")
P("Funding. [To be confirmed by the authors: no external funding.]")
P("Use of AI tools. An AI assistant (Claude, Anthropic) was used to help write and debug the analysis code, to draft text and to find literature. [Authors to confirm and adapt:] The authors are responsible for the accuracy of the analysis, the reported results and the references, and the analysis results were produced by running the code on the data.")

# ============================================================ REFERENCES
H("References")
refs = [
    "Gama, J., Žliobaitė, I., Bifet, A., Pechenizkiy, M., & Bouchachia, A. (2014). A survey on concept drift adaptation. ACM Computing Surveys, 46(4), Article 44. https://doi.org/10.1145/2523813",
    "He, Q. P., & Wang, J. (2007). Fault detection using the k-nearest neighbor rule for semiconductor manufacturing processes. IEEE Transactions on Semiconductor Manufacturing, 20(4), 345–354.",
    "Hinder, F., Vaquet, V., & Hammer, B. (2024). One or two things we know about concept drift – a survey on monitoring in evolving environments. Part B: Locating and explaining concept drift. Frontiers in Artificial Intelligence. https://doi.org/10.3389/frai.2024.1330258",
    "Jourdan, N., Sen, S., Husom, E. J., Garcia-Ceja, E., Biegel, T., & Metternich, J. (2021). On the reliability of machine learning applications in manufacturing environments. arXiv:2112.06986 [Preprint].",
    "Kang, Z., Catal, C., & Tekinerdogan, B. (2020). Machine learning applications in production lines: A systematic literature review. Computers & Industrial Engineering. https://doi.org/10.1016/j.cie.2020.106773",
    "Kerdprasop, K., & Kerdprasop, N. (2011). Feature selection and boosting techniques to improve fault detection accuracy in the semiconductor manufacturing process. Proceedings of the International MultiConference of Engineers and Computer Scientists (IMECS 2011), 398–403.",
    "Kourti, T., & MacGregor, J. F. (1995). Process analysis, monitoring and diagnosis, using multivariate projection methods. Chemometrics and Intelligent Laboratory Systems, 28, 3–21. https://doi.org/10.1016/0169-7439(95)80036-9",
    "McCann, M., & Johnston, A. (2008). SECOM [Data set]. UCI Machine Learning Repository. https://archive.ics.uci.edu/dataset/179/secom",
    "Nuhu, A. A., Zeeshan, Q., Safaei, B., & Shahzad, M. A. (2023). Machine learning-based techniques for fault diagnosis in the semiconductor manufacturing process: A comparative study. The Journal of Supercomputing.",
    "Park, H.-J., Koo, Y.-S., Yang, H.-Y., Han, Y.-S., & Nam, C.-S. (2024). Study on data preprocessing for machine learning based on semiconductor manufacturing processes. Sensors, 24(17), 5461. https://doi.org/10.3390/s24175461",
    "Salem, M., Taheri, S., & Yuan, J. S. (2018). An experimental evaluation of fault diagnosis from imbalanced and incomplete data for smart semiconductor manufacturing. Big Data and Cognitive Computing, 2(4), 30. https://doi.org/10.3390/bdcc2040030",
    "Tercan, H., & Meisen, T. (2022). Machine learning and deep learning based predictive quality in manufacturing: A systematic review. Journal of Intelligent Manufacturing, 33(7), 1879–1905.",
    "Zheng, H., Gao, X., Yang, X., Jing, G., Yang, M., & Liu, Y. (2025). A multi-objective feature selection and self-paced ensemble framework for semiconductor defect detection. Advances in Production Engineering & Management, 20(4), 458–474.",
]
for r in refs:
    P(r)
d.save(R + "Paper_SECOM_validation.docx")
print("saved; tables", tab_n[0], "figures", fig_n[0])
