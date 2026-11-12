from docx import Document
from docx.shared import Pt, Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docstyle import restyle

d = Document()
H = lambda s, l=1: d.add_heading(s, l)
P = lambda s: d.add_paragraph(s)
B = lambda s: d.add_paragraph(s, style="List Bullet")
tab_n = [0]


def center(text, bold=False, italic=False, size=None):
    p = d.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p.add_run(text); r.bold = bold; r.italic = italic
    if size: r.font.size = Pt(size)
    return p


def table(caption, header, rows, size=10):
    tab_n[0] += 1
    c = d.add_paragraph(); r = c.add_run(f"Table {tab_n[0]}. "); r.bold = True; c.add_run(caption)
    c.paragraph_format.keep_with_next = True
    t = d.add_table(rows=1, cols=len(header))
    for i, h in enumerate(header):
        t.rows[0].cells[i].text = h
    for row in rows:
        cells = t.add_row().cells
        for i, v in enumerate(row):
            cells[i].text = v
    for row in t.rows:
        for cell in row.cells:
            for p in cell.paragraphs:
                for run in p.runs:
                    run.font.size = Pt(size)
    d.add_paragraph("")


# ------------------------------------------------------------------ title block
d.add_heading("Report 2: Methodology and Research Design", 0)
center("Predictive Quality in Semiconductor Manufacturing: Does the Validation Protocol Inflate Defect-Prediction Performance?", bold=True)
center("[Student Name 1] (ID: [number]) · [Student Name 2] (ID: [number])")
center("Independent Study and Industrial Applications · [Department, University]")
center("13 November 2026", italic=True)

# ------------------------------------------------------------------ 1
H("1. Refined Research Problem")
P("Report 1 showed that studies on the public SECOM semiconductor dataset concentrate on data preparation and on improving prediction scores, while the concept-drift literature warns that models validated on randomly selected records can be over-optimistic about future production (Gama et al., 2014; Jourdan et al., 2021). The course instructor reviewed Report 1 and approved the topic and the dataset, so the research problem is unchanged: how reliable is defect prediction on SECOM when the model must predict later production runs and not randomly selected ones?")
P("To keep the study achievable within the semester, the scope is narrowed in five ways. (i) One public dataset is used (SECOM). (ii) Three standard classifiers are compared, and no new algorithm is proposed. (iii) One classical multivariate statistical process control (SPC) method, a PCA-based Hotelling T² chart, serves as a baseline. (iv) Four validation protocols are compared. (v) Cost is analysed through a sensitivity analysis with assumed cost ratios. Deep learning, online or adaptive learning and additional datasets are left to future work.")
P("Transparency note. A pilot version of the analysis was run while Report 1 was being prepared, in order to check that the study is feasible (code: https://github.com/Atytmr07/secom-predictive-quality). The hypotheses in Section 2 were therefore formulated with some knowledge of that pilot. In Report 3, results will be labelled as exploratory where this matters, and the complete analysis will be re-run with fixed random seeds before any value is reported.")

# ------------------------------------------------------------------ 2
H("2. Final Research Objective, Research Questions and Hypotheses")
H("2.1 Research objective", 2)
P("The objective of this study is to measure how strongly the validation protocol changes the apparent performance of defect-prediction models on the SECOM dataset, to quantify sensor drift and test whether it explains the loss of performance on later production runs, and to compare machine-learning models with a PCA-based Hotelling T² control chart using statistical and cost-based criteria.")
H("2.2 Research questions and hypotheses", 2)
table("Research questions, hypotheses and the analyses that answer them.", ["RQ", "Research question", "Hypothesis", "Analysis (Section 7)"], [
    ("RQ1", "How does the performance of logistic regression, random forest and XGBoost differ between random cross-validation and time-aware validation?",
     "H1: For each model, lift over random guessing is lower under chronological and walk-forward validation than under random stratified cross-validation.",
     "7.1 Protocol comparison"),
    ("RQ2", "How much do sensor distributions change over time, and is the loss of performance related to drift?",
     "H2a: Sensors flagged as drifting within the training period shift more between the training and test periods than stable sensors. H2b: Models trained only on stable sensors perform better on later runs than models trained on the same number of drifting sensors.",
     "7.2 Drift analysis"),
    ("RQ3", "How does a PCA-based Hotelling T² chart compare with the machine-learning models on later production runs?",
     "H3: On chronologically held-out runs, the PR-AUC of the best machine-learning model is not significantly higher than that of the T² chart.",
     "7.3 SPC comparison"),
    ("RQ4", "Under assumed cost ratios between missed defects and false alarms, does a model-based decision threshold reduce total cost compared with inspecting nothing or inspecting everything?",
     "H4: For sufficiently high missed-defect to false-alarm cost ratios, a model-based threshold has lower total cost than both trivial strategies in cross-validation; this advantage is expected to be smaller or absent under chronological validation, with the threshold chosen on the training period only.",
     "7.4 Cost analysis"),
])
P("Hypotheses are evaluated descriptively, using effect sizes and confidence intervals, and not through a single p-value. The reason is that the number of failures is small (104 in total) and the evaluation metrics are not normally distributed.")

# ------------------------------------------------------------------ 3
H("3. Research Methodology")
P("The study is a quantitative, retrospective experiment based on supervised classification (machine learning), multivariate statistical process control (quality control) and distribution-shift testing (statistical analysis). It is a comparative design: the same pipeline, the same models and the same data are evaluated under different validation protocols, so that differences in results can be attributed to the protocol. Table 2 lists the methodological components and the reason for each choice.")
table("Methodological components and their justification.", ["Component", "Choice", "Justification"], [
    ("Task", "Binary classification (fail = 1, pass = 0)", "The final in-house test gives a pass/fail label, so predictive quality here is a classification problem (Tercan & Meisen, 2022)."),
    ("Models", "Logistic regression (class-weighted); random forest; XGBoost", "A transparent linear baseline and two tree ensembles that cope with many correlated, partly missing features. Standard models keep the focus on validation and not on model novelty."),
    ("Class imbalance", "Class weights; SMOTE as a comparison for logistic regression", "About 6.6% of runs fail. Class weighting leaves the data unchanged; SMOTE is included because resampling is common in SECOM studies (Nuhu et al., 2023; Park et al., 2024)."),
    ("Preprocessing", "Removal of sensors with more than 50% missing values and of constant sensors; median imputation; standardisation; selection of 40 sensors by mutual information", "Simple and transparent steps. All steps are fitted on training data only, inside each fold (a pipeline), to prevent data leakage."),
    ("SPC baseline", "PCA retaining 90% of the variance, fitted on good runs of the training period; Hotelling T² as anomaly score; upper control limit at the 99th percentile of the training T² values", "T² with projection methods is the standard multivariate SPC tool for many correlated variables and needs only normal-operation data (Kourti & MacGregor, 1995)."),
    ("Drift test", "Two-sample Kolmogorov–Smirnov (KS) test per sensor, with Bonferroni correction", "Non-parametric, no distributional assumption, applicable to every sensor. Drifting sensors are defined from the training period only, so that information from the test period cannot influence the selection."),
    ("Validation protocols", "Random stratified 5-fold; blocked 5-fold; chronological 70/30 split; walk-forward with an expanding window", "The four protocols form a gradient from ignoring time to respecting it fully, which answers RQ1 directly (Gama et al., 2014; Jourdan et al., 2021)."),
    ("Uncertainty", "Bootstrap 95% confidence intervals", "With 104 failures, point estimates are unstable. Intervals show whether a result differs from random guessing or from another method."),
])
P("Hyperparameters are kept at reasonable fixed values and are not tuned extensively. Tuning on 104 positive examples risks fitting noise, and the study question concerns the protocol, not the best possible model. All random processes use fixed seeds, including the mutual-information step.")

# ------------------------------------------------------------------ 4
H("4. Research Framework / Methodological Flowchart")
P("Figure 1 shows the research process from problem definition to conclusions.").paragraph_format.keep_with_next = True
d.add_picture("reports/flowchart.png", width=Inches(5.4)); d.paragraphs[-1].alignment = WD_ALIGN_PARAGRAPH.CENTER
c = d.add_paragraph(); r = c.add_run("Figure 1. "); r.bold = True; c.add_run("Methodological flowchart of the study.")
c.alignment = WD_ALIGN_PARAGRAPH.CENTER

# ------------------------------------------------------------------ 5
H("5. Dataset / Data Collection")
P("No new data are collected. The study uses the public SECOM dataset (McCann & Johnston, 2008), available from the UCI Machine Learning Repository at https://archive.ics.uci.edu/dataset/179/secom. The files were downloaded on 5 October 2026 and are described in Table 3.")
table("Description of the SECOM dataset and data-quality findings.", ["Item", "Description"], [
    ("Source and citation", "McCann, M., & Johnston, A. (2008). SECOM [Data set]. UCI Machine Learning Repository."),
    ("Observations", "1,567 production runs of a semiconductor manufacturing process."),
    ("Time period", "19 July 2008 to 17 October 2008. A timestamp is supplied with each label."),
    ("Target", "Pass/fail result of the in-house test: 1,463 pass and 104 fail (6.6%). The original coding (−1 = pass, 1 = fail) is recoded to 0/1."),
    ("Features", "590 anonymised numeric sensor measurements. Physical meaning, units and sensor types are not disclosed."),
    ("Missing values", "About 4.5% of all cells are missing. 28 sensors have more than 50% missing values and are removed. In the remaining non-constant sensors the median missing share is about 0.2% and the maximum about 46%; these are imputed with the median."),
    ("Constant sensors", "116 sensors have a single value and are removed. After both removals, 446 sensors remain for the drift analysis."),
    ("Outliers", "With a robust z-score (median absolute deviation) threshold of 3.5, about 3% of the cells in the 446 sensors are flagged, and 74 sensors have more than 5% flagged values. Outliers are retained, because in defect detection extreme values may carry the signal. Failed runs have on average more flagged sensors (16.2) than passed runs (13.2); this is a descriptive observation only."),
    ("Correlation structure", "347 sensor pairs have an absolute correlation above 0.9, so many sensors are redundant. This motivates feature selection and PCA."),
    ("Data-quality issues", "Anonymous sensors (no domain-based feature engineering), few failures, strong class imbalance, and possible process changes during the three months. The failure share was 11.8% in the first 500 runs and 4.2% in the remaining 1,067 runs."),
    ("Preprocessing requirements", "Imputation, removal of constant and sparse sensors, standardisation, feature selection and imbalance handling, all inside the training folds."),
])

# ------------------------------------------------------------------ 6
H("6. Variables")
table("Variable description.", ["Variable", "Description", "Type", "Unit", "Role in analysis"], [
    ("X1 … X590 (s0 … s589 in the code)", "Anonymised process and sensor measurements", "Numerical (continuous)", "Not disclosed", "Independent variables (features). 446 retained for drift analysis; 40 selected per training fold for modelling."),
    ("Time stamp", "Date and time of the production run", "Date-time", "Date-time", "Used only to order runs and to define chronological splits and drift periods. Not used as a feature."),
    ("Y", "Final in-house test result: fail = 1, pass = 0", "Binary categorical", "–", "Dependent variable (target)."),
    ("T² score", "Hotelling T² statistic of a run in the PCA space of good runs", "Numerical (derived)", "Dimensionless", "Anomaly score of the SPC baseline."),
    ("Model score", "Predicted probability of failure from a classifier", "Numerical (derived)", "0–1", "Used for threshold selection and evaluation."),
    ("Drift status", "Whether a sensor differs significantly between the first and second half of the training period", "Binary (derived)", "–", "Grouping variable for the stable versus drifting sensor experiment."),
])

# ------------------------------------------------------------------ 7
H("7. Proposed Analysis")
H("7.1 Validation-protocol comparison (RQ1)", 2)
P("The same three models and the same preprocessing pipeline are evaluated under four protocols: (1) random stratified 5-fold cross-validation; (2) blocked 5-fold cross-validation, in which the runs are split into five contiguous blocks without shuffling and the remaining blocks, including later ones, form the training set; (3) a chronological split, with the first 70% of the runs for training and the last 30% for testing; and (4) walk-forward evaluation, which trains on the first 500 runs, predicts the next 150, and then expands the training window and repeats. Predictions from all test folds are pooled before a metric is computed. Lift (PR-AUC divided by the defect rate of the evaluated runs) is reported with bootstrap confidence intervals, because the defect rate differs between protocols and raw PR-AUC values are therefore not comparable. This analysis is necessary because it isolates the effect of the protocol, holding model and data constant.")
H("7.2 Drift analysis and its link to performance (RQ2)", 2)
P("For each retained sensor, a two-sample KS test compares the distribution in the first 70% with that in the last 30% of runs, using a Bonferroni-corrected significance level. To test whether drift explains the loss of performance without using test information, sensors are labelled stable or drifting from the training period only (first half versus second half of the training runs). Models are then trained on equal-sized random subsets of stable sensors, of drifting sensors and of all sensors, and evaluated on the last 30% of runs. A check compares the mean KS distance between the training and test periods for the two labelled groups. This analysis is necessary because drift is the commonly proposed explanation for time-related loss of performance, and the equal-sized subsets separate the effect of sensor type from the effect of the number of sensors.")
H("7.3 SPC versus machine learning (RQ3)", 2)
P("A PCA model is fitted on the good runs of the training period only, the T² score is computed for later runs, and its PR-AUC and ROC-AUC on the chronologically held-out runs are compared with those of the machine-learning models, with bootstrap confidence intervals. The comparison is necessary because SPC is the standard industrial approach and therefore the natural baseline for any machine-learning claim.")
H("7.4 Cost-based decision analysis (RQ4)", 2)
P("Total cost is defined as C_FN times the number of missed failures plus C_FP times the number of good runs flagged, with C_FP = 1 and C_FN in {5, 10, 20, 50}. No plant cost data exist for SECOM, so the ratios are assumptions and the analysis is a sensitivity analysis, not an estimate of real savings. The cost-minimising threshold is compared with two trivial strategies, inspecting nothing and inspecting everything. The analysis is first done on cross-validated scores, where the threshold and the evaluation use the same data and the result is optimistic. As a stricter check, the threshold is chosen on out-of-fold predictions within the training period and applied to the last 30% of runs. This analysis is necessary because an Industrial Engineering decision depends on the cost of wrong decisions, not on a statistical score alone.")
H("7.5 Descriptive and exploratory analysis", 2)
P("Before modelling, descriptive statistics, missing-value and outlier summaries, correlation structure, class distribution and the defect rate over time are examined. These analyses document data quality and justify the preprocessing choices. SHAP values of a random forest are used to see which sensors contribute most; because sensors are anonymous, this is descriptive and no physical interpretation is claimed.")

# ------------------------------------------------------------------ 8
H("8. Evaluation Criteria")
table("Evaluation criteria and the reason each is appropriate.", ["Criterion", "Why it is appropriate for this problem"], [
    ("PR-AUC (average precision)", "Summarises the precision–recall trade-off over all thresholds and concentrates on the rare failed class. Its value for random guessing equals the defect rate, which makes interpretation direct."),
    ("Lift = PR-AUC / defect rate", "Makes results comparable across protocols whose evaluated runs have different defect rates."),
    ("ROC-AUC", "Threshold-independent ranking quality. Reported as a secondary measure, because it can look favourable under strong imbalance."),
    ("Best-threshold F1 and MCC", "Single-number summaries of one decision rule; MCC uses all four cells of the confusion matrix and is robust to imbalance. Used descriptively only."),
    ("Total cost under assumed ratios", "Industrial decisions depend on the unequal cost of missed defects and false alarms."),
    ("Bootstrap 95% confidence interval", "With 104 failures, intervals show whether a difference from random guessing, or between methods, is meaningful."),
])
P("Accuracy is not used as a performance measure. Predicting \"pass\" for every run would already give about 93% accuracy while detecting no failure at all. A result is considered different from random guessing only if its confidence interval excludes the random-guessing value.")

# ------------------------------------------------------------------ 9
H("9. Expected Results")
P("Expected results are expectations, not findings. Based on the literature reviewed in Report 1, we expect (i) performance to be highest under random cross-validation and lower under time-aware protocols; (ii) a considerable share of sensors to show statistically significant changes over the three months; (iii) the classical T² chart to be a reasonable but not clearly better or worse alternative to machine learning on later runs; and (iv) a model-based threshold to be more useful when missed defects are much more costly than false alarms. No particular numerical value is assumed. If the results contradict these expectations, they will be reported as they are, and unsupported hypotheses will be stated as unsupported.")

# ------------------------------------------------------------------ summary + limitations
H("10. Summary of the Research Design")
table("Answers to the guiding questions of Report 2.", ["Question", "Answer"], [
    ("What data will I use?", "The public SECOM dataset: 1,567 runs, 590 anonymised sensors, pass/fail labels and timestamps."),
    ("What methodology will I apply?", "Supervised classification with three standard models, a PCA-based Hotelling T² chart as SPC baseline, KS-based drift analysis and a cost-sensitivity analysis."),
    ("Why did I choose this methodology?", "The research problem concerns the reliability of defect prediction on later production. The methods allow the validation protocol to be varied while model and data are held constant, and the SPC baseline and cost analysis connect the result to Industrial Engineering practice."),
    ("How exactly will I analyse the data?", "By comparing four validation protocols (7.1), testing drift and its link to performance (7.2), comparing SPC with machine learning (7.3) and analysing cost thresholds (7.4)."),
    ("How will I evaluate my results?", "PR-AUC, lift, ROC-AUC and total cost, with bootstrap confidence intervals; accuracy is not used."),
])
H("11. Limitations of the Design")
B("Single dataset from one process and period; the findings may not generalise to other factories.")
B("Only 104 failures, so confidence intervals will be wide, especially for the chronological test set.")
B("Anonymous sensors prevent domain-based feature engineering and physical interpretation.")
B("Cost ratios are assumed because real plant costs are not available.")
B("Hyperparameters are not tuned extensively, and only three standard models and one SPC configuration are tested.")
B("The hypotheses were formulated after a pilot run, so parts of the study remain exploratory.")

H("References")
refs = [
    "Gama, J., Žliobaitė, I., Bifet, A., Pechenizkiy, M., & Bouchachia, A. (2014). A survey on concept drift adaptation. ACM Computing Surveys, 46(4), Article 44. https://doi.org/10.1145/2523813",
    "Jourdan, N., Sen, S., Husom, E. J., Garcia-Ceja, E., Biegel, T., & Metternich, J. (2021). On the reliability of machine learning applications in manufacturing environments. arXiv:2112.06986 [Preprint].",
    "Kourti, T., & MacGregor, J. F. (1995). Process analysis, monitoring and diagnosis, using multivariate projection methods. Chemometrics and Intelligent Laboratory Systems, 28, 3–21. https://doi.org/10.1016/0169-7439(95)80036-9",
    "McCann, M., & Johnston, A. (2008). SECOM [Data set]. UCI Machine Learning Repository. https://archive.ics.uci.edu/dataset/179/secom",
    "Nuhu, A. A., Zeeshan, Q., Safaei, B., & Shahzad, M. A. (2023). Machine learning-based techniques for fault diagnosis in the semiconductor manufacturing process: A comparative study. The Journal of Supercomputing.",
    "Park, H.-J., Koo, Y.-S., Yang, H.-Y., Han, Y.-S., & Nam, C.-S. (2024). Study on data preprocessing for machine learning based on semiconductor manufacturing processes. Sensors, 24(17), 5461. https://doi.org/10.3390/s24175461",
    "Tercan, H., & Meisen, T. (2022). Machine learning and deep learning based predictive quality in manufacturing: A systematic review. Journal of Intelligent Manufacturing, 33(7), 1879–1905.",
]
for r in refs:
    p = P(r); p.paragraph_format.left_indent = Inches(0.5); p.paragraph_format.first_line_indent = Inches(-0.5)

restyle(d, 12, 1.15)
d.save("reports/Report2_Methodology.docx")
print("saved", tab_n[0], "tables")
