from docx import Document
from docx.shared import Pt, Cm
from docx.enum.section import WD_ORIENT, WD_SECTION

d = Document()
st = d.styles["Normal"]; st.font.name = "Calibri"; st.font.size = Pt(11)
H = lambda s, l=1: d.add_heading(s, l)
P = lambda s: d.add_paragraph(s)
B = lambda s: d.add_paragraph(s, style="List Bullet")

d.add_heading("Report 1: Literature Review and Research Problem", 0)
d.add_heading("Predictive Quality in Semiconductor Manufacturing: Can Defect-Prediction Models Survive Process Drift?", 2)
P("[Student Name 1 – ID] · [Student Name 2 – ID]\nIndependent Study and Industrial Applications · Due: 16 October 2026")

# ---------------------------------------------------------------- 1
H("1. Introduction to the Research Topic")
P("Manufacturers want to know whether a product is defective as early as possible. In many factories, however, quality is only confirmed at the end of the line, in a final electrical or functional test. By then, material, machine time and labor have already been spent on a product that may be scrapped. Predictive quality is the use of process data (sensor readings, machine settings, material properties) to estimate the quality of a product before, or without, the final test (Tercan & Meisen, 2022).")
H("What is the problem?", 2)
P("This project studies defect prediction in semiconductor manufacturing. Each production run is described by hundreds of sensor measurements, and the final test labels it pass or fail. The analytical problem is to learn a model that predicts the label from the sensors. Three features make the problem hard: (i) very few defects compared with good products (class imbalance), (ii) many sensors, many of them noisy or missing, and (iii) a process that changes over time, so that a model trained on past data may not work on future data.")
H("Why is it important, and where does it occur?", 2)
P("Semiconductor fabrication involves a very long sequence of tightly controlled steps, and process equipment records large amounts of data. The same situation appears in many other industries (injection molding, steel, automotive assembly, food), wherever sensor data and end-of-line quality tests exist. Better early detection can reduce scrap, rework and test cost, and can shorten the time needed to find the root cause of a quality problem.")
H("Why is it relevant to Industrial Engineering?", 2)
P("The problem sits at the intersection of several core Industrial Engineering topics: quality engineering and Statistical Process Control (SPC), cost of poor quality, yield improvement, inspection planning, and data-driven decision making in Industry 4.0 environments. The key IE question is not only 'how accurate is the model?' but also 'what decision does it support and what does a wrong decision cost?'. A missed defect (false negative) and a false alarm (false positive) have very different costs, so model evaluation must reflect this.")
H("Who is affected and what are the consequences?", 2)
P("Production engineers and quality managers rely on such models to decide which products to inspect or scrap. If a model looks good in a laboratory evaluation but fails in production, the consequences are missed defects reaching customers, unnecessary scrapping of good products, and loss of trust in data-driven tools. This is why the way a model is validated matters as much as the model itself.")

# ---------------------------------------------------------------- 2
H("2. Literature Review")
P("The literature was searched using Google Scholar and publisher databases (MDPI, Springer, Elsevier, IEEE, ACM) with combinations of the keywords 'predictive quality', 'SECOM', 'semiconductor fault detection', 'class imbalance', 'concept drift', 'multivariate SPC' and 'Hotelling T2'. Peer-reviewed journal and conference papers were preferred; one arXiv preprint is included and marked as such. The review is organized around four themes.")
H("2.1 Predictive quality in manufacturing", 2)
P("Two systematic reviews describe the landscape. Tercan and Meisen (2022) reviewed predictive-quality studies published between 2012 and 2021 and organized them by manufacturing process, data and machine-learning model. Kang, Catal and Tekinerdogan (2020) screened 271 papers on machine learning in production lines and analysed 39 primary studies. Both reviews show that the field is broad and fragmented: studies use different data, targets and metrics, and Tercan and Meisen note that an overall view of methods and open obstacles is missing. This makes it difficult to compare results across papers and motivates studies that use a common, public benchmark.")
H("2.2 Studies on the SECOM benchmark", 2)
P("SECOM is a public semiconductor dataset (McCann & Johnston, 2008) that has been used in many studies. Most of them focus on handling its three data problems. Kerdprasop and Kerdprasop (2011) combined feature selection with boosting to handle the imbalance between pass and fail cases. Salem, Taheri and Yuan (2018) compared 288 combinations of data pruning, imputation, feature selection and classifiers and proposed a KNN-based imputation method. Park et al. (2024) studied preprocessing choices (missing-value handling, dimensionality reduction, resampling and scaling) with several models. Zheng et al. (2025) used multi-objective feature selection with a self-paced ensemble and reported improvements in AUROC and AUPRC. Nuhu et al. (2023) compared synthetic-data generation, imputation and feature-selection techniques with ten models and reported accuracies between 99.5% and 100%.")
P("Two observations follow from these studies. First, the emphasis is on preprocessing and on choosing a good feature-selection or resampling method. Second, results vary widely between papers (for example, accuracies close to 100% in some studies, while others report moderate AUROC values), and the validation design is not always described in a way that allows comparison. Accuracy values near 100% on a dataset where about 93% of runs are good deserve caution, because accuracy is a weak metric under strong imbalance and the result also depends on whether resampling was applied before or after splitting the data. The full-text evaluation design of each study should be checked as part of the next step of this project.")
H("2.3 Statistical process control versus machine learning", 2)
P("The classical way to monitor many correlated process variables is multivariate SPC. Kourti and MacGregor (1995) describe how the univariate control chart is extended with the Hotelling T2 statistic and with projection methods such as PCA and PLS. These methods learn the normal behaviour of the process and signal when a new observation departs from it. For semiconductor processes, He and Wang (2007) proposed a k-nearest-neighbour rule that also needs only normal-operation data and avoids distributional assumptions. In the SECOM studies reviewed above, machine-learning classifiers are the main tools, and direct comparison with a classical SPC baseline is rarely reported.")
H("2.4 Process drift and model reliability", 2)
P("Concept drift means that the relationship between inputs and the target, or the distribution of the inputs, changes over time. Gama et al. (2014) survey strategies for detecting and adapting to such changes. Hinder, Vaquet and Hammer (2024) point out that locating and explaining drift is less studied than detecting it. In an industrial setting, Jourdan et al. (2021, preprint) trained several algorithms on the first part of a 36-month gas-sensor dataset and tested them on the rest: all showed strong degradation in accuracy over time. Although that dataset is not a production-quality dataset, the finding is directly relevant: a model that performs well under random validation may still fail when applied to later data.")
H("2.5 Synthesis", 2)
P("Previous studies have mainly focused on improving prediction through preprocessing, feature selection and resampling on SECOM, while the drift literature shows that performance often degrades over time. The two lines of work are rarely connected: SECOM studies seldom test whether their models hold up on later production runs, and the drift literature rarely uses SECOM. Classical SPC methods, the standard tool of industrial quality engineers, are also seldom used as a baseline for the machine-learning models on this benchmark.")

# ---------------------------------------------------------------- table (landscape)
sec = d.add_section(WD_SECTION.NEW_PAGE); sec.orientation = WD_ORIENT.LANDSCAPE
sec.page_width, sec.page_height = sec.page_height, sec.page_width
sec.left_margin = Cm(1.8); sec.right_margin = Cm(1.8)
H("3. Literature Comparison Table")
rows = [
    ("Tercan & Meisen (2022)", "Predictive quality in manufacturing", "Review of studies from 2012–2021", "Systematic review", "Categorizes studies by process, data and ML model; shows no overall view of methods and open challenges exists", "Review only; no common benchmark or comparison of results"),
    ("Kang, Catal & Tekinerdogan (2020)", "ML in production lines", "271 papers screened, 39 primary studies", "Systematic literature review", "Categorizes problems, industrial domains, algorithms and variables used", "Descriptive; does not test model robustness over time"),
    ("Kerdprasop & Kerdprasop (2011)", "Fault detection, semiconductor", "SECOM", "Feature selection + boosting", "Feature selection and boosting used to cope with 500+ signals and pass/fail imbalance", "Older study; validation design and time effects not examined"),
    ("Salem, Taheri & Yuan (2018)", "Fault diagnosis with imbalanced, incomplete data", "SECOM", "288 combinations of pruning, imputation, feature selection, classifiers; KNN-based imputation", "Proposed imputation outperformed standard imputation methods; broad comparison of pipeline choices", "Focus on preprocessing; no chronological evaluation described"),
    ("Nuhu et al. (2023)", "Fault diagnosis, semiconductor", "SECOM", "Synthetic data generation, imputation, feature selection, 10 ML models", "Reported accuracies of 99.5–100%", "Very high accuracy on imbalanced data; evaluation design should be checked (e.g. resampling before split)"),
    ("Park et al. (2024)", "Preprocessing for ML in semiconductor process", "SECOM", "Missing values, dimensionality reduction, resampling, scaling; several ML models; G-mean among metrics", "Shows that preprocessing choices strongly affect results", "Single dataset; no time-aware validation described"),
    ("Zheng et al. (2025)", "Semiconductor defect detection", "SECOM", "MOEA/D feature selection + self-paced ensemble", "AUROC rose from 0.685 to 0.770 and AUPRC from 0.932 to 0.972 with feature selection", "Single dataset; no drift or SPC comparison reported"),
    ("Kourti & MacGregor (1995)", "Multivariate process monitoring", "Process data (tutorial paper)", "Hotelling T2, PCA, PLS", "Explains how multivariate SPC monitors many correlated variables using projection methods", "Not a classification study; no comparison with modern ML"),
    ("He & Wang (2007)", "Fault detection in semiconductor processes", "Semiconductor process data", "k-nearest-neighbour rule (FD-kNN)", "Nonparametric method that needs only normal-operation data", "Pre-dates the SECOM-based ML studies; not benchmarked against them"),
    ("Gama et al. (2014)", "Concept drift adaptation", "Survey (various)", "Drift detection and adaptation strategies", "Characterizes and categorizes strategies for learning under drift", "General ML survey; not specific to manufacturing quality"),
    ("Jourdan et al. (2021, arXiv preprint)", "Reliability of ML in manufacturing environments under drift", "Gas Sensor Array Drift data, 36 months, 13,910 runs", "SVM, decision tree, KNN, random forest, neural network; trained on first 10 months", "All algorithms degraded strongly over time; calibration also degraded", "Single non-production dataset; preprint"),
    ("Hinder, Vaquet & Hammer (2024)", "Locating and explaining concept drift", "Survey", "Drift localization and explanation methods", "Localization and explanation are less studied than detection", "General survey; no manufacturing quality case study"),
]
t = d.add_table(rows=1, cols=6); t.style = "Light Grid Accent 1"
for i, h in enumerate(["Author / Year", "Problem", "Dataset", "Method", "Main Findings", "Limitation / Gap"]):
    t.rows[0].cells[i].text = h
for r in rows:
    c = t.add_row().cells
    for i, v in enumerate(r):
        c[i].text = v
for row in t.rows:
    for c in row.cells:
        for p in c.paragraphs:
            for run in p.runs:
                run.font.size = Pt(8.5)
P("Note: entries were compiled from the abstracts and publisher summaries of the papers. Findings and limitations should be confirmed against the full texts before the final paper.")

sec2 = d.add_section(WD_SECTION.NEW_PAGE); sec2.orientation = WD_ORIENT.PORTRAIT
sec2.page_width, sec2.page_height = sec2.page_height, sec2.page_width

# ---------------------------------------------------------------- 4
H("4. Research Gap")
P("Based on the reviewed literature, three gaps can be identified.")
B("Gap 1 – Time-aware validation on SECOM. The SECOM studies reviewed concentrate on preprocessing, feature selection and resampling. The dataset contains timestamps, but the reviewed summaries do not report whether models were tested on later production runs than those used for training. The drift literature (Gama et al., 2014; Jourdan et al., 2021) suggests that random validation can give an optimistic picture.")
B("Gap 2 – Connection between drift and prediction performance. Studies on drift in manufacturing rarely use SECOM, and SECOM studies rarely measure how much the sensors change over time. Whether the sensors chosen by feature selection are themselves stable has not been examined in the reviewed work.")
B("Gap 3 – Classical SPC as a baseline. Multivariate SPC (Kourti & MacGregor, 1995; He & Wang, 2007) is the standard industrial tool, but the SECOM machine-learning studies reviewed do not compare against it, and they typically evaluate with accuracy-style metrics rather than the cost of wrong decisions.")
P("A pilot run of our own code supports that these gaps are worth investigating (Section 7).")

# ---------------------------------------------------------------- 5
H("5. Research Objective")
P("The objective of this study is to evaluate how reliably machine-learning models predict defects on the SECOM semiconductor dataset when they are validated in a time-aware manner, to quantify how process drift contributes to any performance loss, and to compare the machine-learning models with a classical multivariate SPC baseline using both statistical metrics and a cost-based decision criterion.")

# ---------------------------------------------------------------- 6
H("6. Research Questions")
B("RQ1: How does the predictive performance of common machine-learning models (logistic regression, random forest, XGBoost) on SECOM differ between random cross-validation and chronological (time-ordered) validation?")
B("RQ2: To what extent do the sensor distributions change over time, and are the sensors selected by the models more or less affected by this drift than the sensors in general?")
B("RQ3: How does a classical multivariate SPC method (PCA-based Hotelling T2 chart) compare with the machine-learning models under chronological validation?")
B("RQ4: Under assumed cost ratios between missed defects and false alarms, which decision threshold minimizes total cost, and does using a model reduce cost compared with no inspection or full inspection?")

# ---------------------------------------------------------------- 7
H("7. Preliminary Research Plan")
tbl = [
    ("Data source", "UCI SECOM dataset (McCann & Johnston, 2008): 1,567 production runs, 590 sensor variables, pass/fail label, timestamps (July–October 2008); 104 failures (6.6%)."),
    ("Variables", "Inputs: 590 anonymised sensors (after removing sensors with over 50% missing values and constant sensors). Output: fail (1) / pass (0)."),
    ("Proposed methodology", "Preprocessing pipeline (median imputation, scaling, mutual-information feature selection) fitted only on training data; class weighting and SMOTE for imbalance; logistic regression, random forest and XGBoost; validation by stratified cross-validation and by chronological and walk-forward splits; drift analysis with the Kolmogorov–Smirnov test; PCA-based Hotelling T2 chart as SPC baseline; cost-based threshold analysis; SHAP for interpretation."),
    ("Metrics", "PR-AUC, ROC-AUC, best-threshold F1; bootstrap confidence intervals. Accuracy is not used as the main metric because of class imbalance."),
    ("Software / tools", "Python (pandas, scikit-learn, imbalanced-learn, XGBoost, SHAP, SciPy); code shared in a public GitHub repository."),
    ("Expected analysis", "Comparison of random and time-aware validation; proportion of drifting sensors; SPC versus ML under time-ordered testing; cost curves for different cost ratios."),
    ("Expected outputs", "Tables and figures answering RQ1–RQ4, a discussion of why random validation is optimistic, and practical recommendations for validating predictive-quality models."),
]
t2 = d.add_table(rows=0, cols=2); t2.style = "Light Grid Accent 1"
for a, b in tbl:
    c = t2.add_row().cells; c[0].text = a; c[1].text = b
P("")
P("Pilot run. To check feasibility, a first version of this analysis was already implemented (https://github.com/Atytmr07/secom-predictive-quality). In the pilot, a random forest reached a PR-AUC of about 0.19 under random cross-validation (random guessing is about 0.07), but performance fell close to the random level when the model was trained on the first 70% of runs and tested on the last 30%. A first drift test indicated that a majority of the sensors changed significantly between the two periods. These preliminary results are exploratory; the final methodology and statistical analysis will be completed in Reports 2 and 3.")

# ---------------------------------------------------------------- refs
H("References")
refs = [
    "Gama, J., Žliobaitė, I., Bifet, A., Pechenizkiy, M., & Bouchachia, A. (2014). A survey on concept drift adaptation. ACM Computing Surveys, 46(4), Article 44. https://doi.org/10.1145/2523813",
    "He, Q. P., & Wang, J. (2007). Fault detection using the k-nearest neighbor rule for semiconductor manufacturing processes. IEEE Transactions on Semiconductor Manufacturing, 20(4), 345–354.",
    "Hinder, F., Vaquet, V., & Hammer, B. (2024). One or two things we know about concept drift – a survey on monitoring in evolving environments. Part B: locating and explaining concept drift. Frontiers in Artificial Intelligence. https://doi.org/10.3389/frai.2024.1330258",
    "Jourdan, N., Sen, S., Husom, E. J., Garcia-Ceja, E., Biegel, T., & Metternich, J. (2021). On the reliability of machine learning applications in manufacturing environments. arXiv:2112.06986 (preprint).",
    "Kang, Z., Catal, C., & Tekinerdogan, B. (2020). Machine learning applications in production lines: A systematic literature review. Computers & Industrial Engineering. https://doi.org/10.1016/j.cie.2020.106773",
    "Kerdprasop, K., & Kerdprasop, N. (2011). Feature selection and boosting techniques to improve fault detection accuracy in the semiconductor manufacturing process. Proceedings of the International MultiConference of Engineers and Computer Scientists (IMECS 2011), 398–403.",
    "Kourti, T., & MacGregor, J. F. (1995). Process analysis, monitoring and diagnosis, using multivariate projection methods. Chemometrics and Intelligent Laboratory Systems, 28, 3–21. https://doi.org/10.1016/0169-7439(95)80036-9",
    "McCann, M., & Johnston, A. (2008). SECOM [Dataset]. UCI Machine Learning Repository. https://archive.ics.uci.edu/dataset/179/secom",
    "Nuhu, A. A., Zeeshan, Q., Safaei, B., & Shahzad, M. A. (2023). Machine learning-based techniques for fault diagnosis in the semiconductor manufacturing process: a comparative study. The Journal of Supercomputing.",
    "Park, H.-J., Koo, Y.-S., Yang, H.-Y., Han, Y.-S., & Nam, C.-S. (2024). Study on data preprocessing for machine learning based on semiconductor manufacturing processes. Sensors, 24(17), 5461. https://doi.org/10.3390/s24175461",
    "Salem, M., Taheri, S., & Yuan, J. S. (2018). An experimental evaluation of fault diagnosis from imbalanced and incomplete data for smart semiconductor manufacturing. Big Data and Cognitive Computing, 2(4), 30. https://doi.org/10.3390/bdcc2040030",
    "Tercan, H., & Meisen, T. (2022). Machine learning and deep learning based predictive quality in manufacturing: a systematic review. Journal of Intelligent Manufacturing, 33(7), 1879–1905.",
    "Zheng, H., Gao, X., Yang, X., Jing, G., Yang, M., & Liu, Y. (2025). A multi-objective feature selection and self-paced ensemble framework for semiconductor defect detection. Advances in Production Engineering & Management, 20(4), 458–474.",
]
for r in refs:
    P(r)
d.save("reports/Report1_Literature_Review.docx")
