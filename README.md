<!--===========================================================================
  github.com/codewithvikas96-ui  ·  profile README

  Every panel on this page is generated, not hand-drawn. Two scripts:

    generate_banner.py    -> dark.svg / light.svg              (hero)
    generate_sections.py  -> capabilities / trajectory /       (sections
                             roadmap / buildlog -dark|-light    01, 02, 04, 06)

  generate_sections.py imports its palette and helpers from generate_banner.py,
  so the hero and the body can never drift apart. To update: edit the data
  block at the top of the relevant script, run it, re-upload the SVGs it wrote.
  Prose stays in markdown on purpose — only chrome and diagrams are SVG.
============================================================================-->

<picture>
  <source media="(prefers-color-scheme: dark)"  srcset="https://raw.githubusercontent.com/codewithvikas96-ui/codewithvikas96-ui/main/dark.svg">
  <source media="(prefers-color-scheme: light)" srcset="https://raw.githubusercontent.com/codewithvikas96-ui/codewithvikas96-ui/main/light.svg">
  <img alt="Vikas Vishwakarma — AI/ML Engineer in training" src="https://raw.githubusercontent.com/codewithvikas96-ui/codewithvikas96-ui/main/light.svg">
</picture>

<div align="center">

<a href="https://www.linkedin.com/in/vikas-vishwakarma-62959a387/">
  <img src="https://img.shields.io/badge/LinkedIn-06080C?style=for-the-badge&logo=linkedin&logoColor=2BD3E8&labelColor=06080C" alt="LinkedIn" />
</a>
&nbsp;
<a href="mailto:vikas221018@gmail.com">
  <img src="https://img.shields.io/badge/Email-06080C?style=for-the-badge&logo=gmail&logoColor=3BE08A&labelColor=06080C" alt="Email" />
</a>
&nbsp;
<a href="https://github.com/codewithvikas96-ui?tab=repositories">
  <img src="https://img.shields.io/badge/Repositories-06080C?style=for-the-badge&logo=github&logoColor=FF3D8A&labelColor=06080C" alt="Repositories" />
</a>

</div>

---

## <samp>01 · $ systemctl status capabilities</samp>

<picture>
  <source media="(prefers-color-scheme: dark)"  srcset="https://raw.githubusercontent.com/codewithvikas96-ui/codewithvikas96-ui/main/capabilities-dark.svg">
  <source media="(prefers-color-scheme: light)" srcset="https://raw.githubusercontent.com/codewithvikas96-ui/codewithvikas96-ui/main/capabilities-light.svg">
  <img alt="Capability report — online: Python, mathematics and statistics, data analysis and EDA, classical machine learning, software engineering. Loading: deep learning, natural language processing. Queued: generative AI, AI agents, production AI systems." src="https://raw.githubusercontent.com/codewithvikas96-ui/codewithvikas96-ui/main/capabilities-light.svg">
</picture>

I started in general software development — C, Java, full-stack web, mobile — and
I'm now deliberately moving that foundation toward **Data Science, Machine Learning
and AI engineering**.

The rule I hold myself to: every concept I study has to end up inside something that
runs. Regression became an insurance-cost predictor. Classification became a loan
approval model and a purchase-intent classifier. EDA became an interactive analytics
dashboard.

---

## <samp>02 · $ cat TRAJECTORY.map</samp>

<picture>
  <source media="(prefers-color-scheme: dark)"  srcset="https://raw.githubusercontent.com/codewithvikas96-ui/codewithvikas96-ui/main/trajectory-dark.svg">
  <source media="(prefers-color-scheme: light)" srcset="https://raw.githubusercontent.com/codewithvikas96-ui/codewithvikas96-ui/main/trajectory-light.svg">
  <img alt="Role trajectory — Developer (current) to Data Scientist (in-flight) to ML Engineer (next) to AI Engineer (target). This is a roadmap, not a résumé: each stage is earned by shipping, not by reading." src="https://raw.githubusercontent.com/codewithvikas96-ui/codewithvikas96-ui/main/trajectory-light.svg">
</picture>

**Currently building toward:** deep-learning fundamentals implemented from scratch,
then NLP pipelines, then LLM-powered applications that combine my full-stack
background with model work.

---

## <samp>03 · $ ./project_registry --list</samp>

| # | Project | Domain | Core Stack |
|:--|:--|:--|:--|
| `01` | **IPL 2022 Data Analysis** | Data Analysis | `Pandas` `Seaborn` `Streamlit` |
| `02` | **ShopSmart** | Machine Learning | `scikit-learn` `Decision Tree` |
| `03` | **Loan Approval Prediction** | Machine Learning | `LogReg` `KNN` `GaussianNB` |
| `04` | **Insurance Charges Prediction** | Regression | `scikit-learn` `Feature Eng.` |
| `05` | **QuickFix Lite** | Full-Stack · 🏆 Hackathon | `Web` `Backend` `Database` |
| `06` | **HR Management App** | Mobile · Production | `React Native` `Supabase` |

<br/>

<details open>
<summary><samp>▸ 01 — IPL 2022 Data Analysis</samp></summary>

<br/>

> **Purpose** — Turn a full IPL 2022 season into an interactive analytical story
> instead of a static spreadsheet.

**Stack** `Python` · `Pandas` · `NumPy` · `Matplotlib` · `Seaborn` · `Streamlit`

**What it does**
- Cleans and reshapes raw match-level data into analysis-ready frames
- Explores team, venue and player performance through EDA
- Surfaces the findings in an interactive Streamlit dashboard

**What I learned**
- How much of "analysis" is actually data cleaning and shape decisions
- Choosing the right chart for the question instead of the prettiest one
- Moving a notebook from personal exploration to something others can use

[`→ repository`](https://github.com/codewithvikas96-ui/IPL-2022-EDA)

</details>

<details>
<summary><samp>▸ 02 — ShopSmart</samp></summary>

<br/>

> **Purpose** — Predict whether an online browsing session will generate revenue,
> using behavioural signals from that session.

**Stack** `Python` · `scikit-learn` · `Decision Tree Classifier` · `Pandas`

**What it does**
- Engineers features from raw session behaviour (page types, durations, intent signals)
- Trains and tunes a Decision Tree classifier for purchase-intent prediction
- Evaluates with class-aware metrics, since converting sessions are the minority

**What I learned**
- Feature engineering moved the needle more than swapping models did
- How tree depth trades off between memorising and generalising
- Hyperparameter tuning as a measured process, not trial and error

[`→ repository`](https://github.com/codewithvikas96-ui/shopsmart)

</details>

<details>
<summary><samp>▸ 03 — Loan Approval Prediction</samp></summary>

<br/>

> **Purpose** — Compare classical classifiers on a realistic credit-decision problem
> and understand *why* one wins.

**Stack** `Python` · `Logistic Regression` · `KNN` · `Gaussian Naive Bayes` · `scikit-learn`

**What it does**
- Cleans applicant data and engineers features from income, credit and asset fields
- Handles class imbalance so the minority outcome isn't ignored
- Benchmarks three model families side by side on consistent metrics

**What I learned**
- Accuracy is misleading on imbalanced data — precision, recall and confusion matrices aren't optional
- Each algorithm's assumptions predict where it will fail
- Scaling matters enormously for KNN and not at all for Naive Bayes

[`→ repository`](https://github.com/codewithvikas96-ui/loan-approval-prediction)

</details>

<details>
<summary><samp>▸ 04 — Insurance Charges Prediction</samp></summary>

<br/>

> **Purpose** — Model medical insurance costs and identify which applicant attributes
> actually drive the premium.

**Stack** `Python` · `Regression` · `scikit-learn` · `Pandas` · `Seaborn`

**What it does**
- Derives BMI categories and age groups from continuous variables
- One-hot encodes categorical attributes for model consumption
- Uses Pearson correlation analysis to expose relationships before modelling

**What I learned**
- Binning continuous variables can encode domain knowledge a raw feature can't
- Correlation analysis before modelling saves time during it
- Reading residuals to find where a regression systematically misses

[`→ repository`](https://github.com/codewithvikas96-ui/Insurance-Charge-Prediction)

</details>

<details>
<summary><samp>▸ 05 — QuickFix Lite &nbsp;🏆 hackathon winner</samp></summary>

<br/>

> **Purpose** — Connect students with local service providers through a single
> full-stack platform. Built and shipped under hackathon time pressure — and won.

**Stack** Full-stack web application · Modern web architecture · Backend & database integration

**What it does**
- Two-sided platform linking students with service providers
- Backend and database layer supporting the full request lifecycle
- Built end-to-end within a hackathon window

**What I learned**
- Scoping ruthlessly: what ships in the time available vs. what's nice to have
- Designing a data model early prevents rewrites later
- Building a two-sided flow forces genuinely different UX decisions per role

[`→ repository`](https://github.com/codewithvikas96-ui/quickfix-lite)

</details>

<details>
<summary><samp>▸ 06 — HR Management Application</samp></summary>

<br/>

> **Purpose** — A production-oriented mobile HR platform with real authentication,
> role separation and database-level security.

**Stack** `React Native` · `Expo` · `TypeScript` · `Supabase` · `PostgreSQL` · `Edge Functions`

**What it does**
- Role-based architecture separating employee and administrator capabilities
- Authentication backed by Row Level Security policies at the database layer
- Server-side logic via Supabase Edge Functions
- Typed end to end with TypeScript

**What I learned**
- Security enforced in the database beats security enforced in the UI
- Row Level Security changes how you design schemas, not just permissions
- TypeScript pays for itself the moment the data model grows
- The distance between "it works on my device" and "it's production-ready"

[`→ repository`](https://github.com/codewithvikas96-ui/hr-management-app)

</details>

---

## <samp>04 · $ cat ROADMAP.yml</samp>

<picture>
  <source media="(prefers-color-scheme: dark)"  srcset="https://raw.githubusercontent.com/codewithvikas96-ui/codewithvikas96-ui/main/roadmap-dark.svg">
  <source media="(prefers-color-scheme: light)" srcset="https://raw.githubusercontent.com/codewithvikas96-ui/codewithvikas96-ui/main/roadmap-light.svg">
  <img alt="Learning roadmap — 00 Python and mathematics, 01 data science, 02 machine learning: done. 03 deep learning, 04 NLP: in progress. 05 generative AI, 06 AI agents, 07 production AI: queued." src="https://raw.githubusercontent.com/codewithvikas96-ui/codewithvikas96-ui/main/roadmap-light.svg">
</picture>

<details>
<summary><samp>▸ expand phase breakdown</samp></summary>

<br/>

| Phase | Stage | Contents | State |
|:--|:--|:--|:--|
| `00` | Foundations | Python, linear algebra, probability, statistics | done |
| `01` | Data Science | EDA, cleaning, preprocessing, feature engineering, correlation & statistical analysis | done |
| `02` | Machine Learning | regression, classification, ensembles, clustering, tuning, evaluation | done |
| `03` | Deep Learning | neural networks, backpropagation, optimization, CNNs | active |
| `04` | NLP | tokenization, embeddings, sequence models, transformers | active |
| `05` | Generative AI | prompt engineering, RAG, evaluation of LLM outputs | queued |
| `06` | AI Agents | tool calling, planning loops, multi-step orchestration | queued |
| `07` | Production AI | serving, APIs, monitoring, reproducible pipelines | queued |

</details>

---

## <samp>05 · $ ls -R stack/</samp>

<details open>
<summary><samp>▸ data/ &nbsp;·&nbsp; machine-learning/</samp></summary>

<br/>

| Layer | Stack |
|:--|:--|
| **Data libraries** | `NumPy` · `Pandas` · `Matplotlib` · `Seaborn` |
| **Data techniques** | Exploratory Data Analysis · Data Cleaning · Preprocessing · Feature Engineering |
| **Analysis** | Statistical Analysis · Correlation Analysis · Distribution & Outlier Study |
| **Environment** | `Jupyter Notebook` |

| Family | Models & Methods |
|:--|:--|
| **Framework** | `scikit-learn` |
| **Linear** | Linear Regression · Logistic Regression · `Lasso` · `Ridge` · `ElasticNet` |
| **Instance / Probabilistic** | K-Nearest Neighbours · Naive Bayes · Support Vector Machines |
| **Trees & Ensembles** | Decision Trees · Random Forest · `XGBoost` · `LightGBM` · `CatBoost` |
| **Unsupervised** | K-Means · DBSCAN · PCA |
| **Anomaly Detection** | Isolation Forest · Local Outlier Factor |
| **Workflow** | `GridSearchCV` · Hyperparameter Tuning · Cross-Validation · Model Evaluation |

</details>

<details>
<summary><samp>▸ ai/ &nbsp;— in progress</samp></summary>

<br/>

| Track | Direction |
|:--|:--|
| **Deep Learning** | neural network fundamentals, training dynamics, architectures |
| **NLP** | text preprocessing, embeddings, language model behaviour |
| **Generative AI** | LLM application patterns, retrieval-augmented generation |
| **AI Agents** | tool use, reasoning loops, task automation |
| **Applied AI** | AI-powered full-stack applications, AI-driven automation |

</details>

<details>
<summary><samp>▸ engineering/</samp></summary>

<br/>

| Category | Technologies |
|:--|:--|
| **Programming** | `Python` · `C` · `C++` · `Java` · `JavaScript` · `TypeScript` |
| **Web** | `HTML` · `CSS` · `AngularJS` |
| **Backend** | `Node.js` · `Express.js` · `Supabase Edge Functions` |
| **Database** | `SQL` · `MySQL` · `Oracle PL/SQL` · `PostgreSQL` · `MongoDB` |
| **Mobile** | `React Native` · `Expo` |
| **Platform** | `Supabase` — Auth · Row Level Security · Postgres |
| **Desktop** | `PyQt5` |
| **Tools** | `Git` · `GitHub` · `Jupyter` |

</details>

---

## <samp>06 · $ tail -f ~/logs/build.log</samp>

<picture>
  <source media="(prefers-color-scheme: dark)"  srcset="https://raw.githubusercontent.com/codewithvikas96-ui/codewithvikas96-ui/main/buildlog-dark.svg">
  <source media="(prefers-color-scheme: light)" srcset="https://raw.githubusercontent.com/codewithvikas96-ui/codewithvikas96-ui/main/buildlog-light.svg">
  <img alt="Build log — comparing boosting families XGBoost vs LightGBM vs CatBoost; implementing backpropagation by hand before trusting a framework; building text preprocessing pipelines from tokenization upward; sharpening EDA workflow; keeping notebooks reproducible; next: first end-to-end deep learning project, served behind an API." src="https://raw.githubusercontent.com/codewithvikas96-ui/codewithvikas96-ui/main/buildlog-light.svg">
</picture>

---

## <samp>07 · $ git log --stat</samp>

<div align="center">

<img width="49%" src="https://github-readme-stats-sage-beta.vercel.app/api?username=codewithvikas96-ui&show_icons=true&count_private=true&include_all_commits=true&hide_rank=true&hide_border=true&title_color=3BE08A&icon_color=2BD3E8&text_color=7E8A99&bg_color=0B0F14" alt="GitHub stats" />
<img width="49%" src="https://github-readme-stats-sage-beta.vercel.app/api/top-langs/?username=codewithvikas96-ui&layout=compact&langs_count=8&hide_border=true&title_color=3BE08A&text_color=7E8A99&bg_color=0B0F14" alt="Top languages" />

<br/><br/>

<picture>
  <source media="(prefers-color-scheme: dark)"  srcset="https://raw.githubusercontent.com/codewithvikas96-ui/codewithvikas96-ui/output/github-snake-dark.svg" />
  <source media="(prefers-color-scheme: light)" srcset="https://raw.githubusercontent.com/codewithvikas96-ui/codewithvikas96-ui/output/github-snake.svg" />
  <img alt="Contribution graph" src="https://raw.githubusercontent.com/codewithvikas96-ui/codewithvikas96-ui/output/github-snake.svg" />
</picture>

</div>

---

## <samp>08 · $ cat PHILOSOPHY.md</samp>

```console
  A notebook that runs once is a result.
  A system that runs every day is engineering.

  I don't stop at model.fit(). I want to know why the loss
  curve bends where it does, what the residuals are hiding,
  and what breaks the first time a real user touches it.

  Every technique gets the same treatment:

      read the math  →  implement it  →  break it
                     →  measure it    →  ship something that uses it

  Tools change every year. The habit of taking something
  apart until it makes sense doesn't.
```

---

<div align="center">

<samp>**`$ echo "open to Data Science / ML internships and collaboration"`**</samp>

<br/>

<a href="mailto:vikas221018@gmail.com">
  <img src="https://img.shields.io/badge/reach_out-06080C?style=for-the-badge&logo=gmail&logoColor=3BE08A&labelColor=06080C" alt="Email" />
</a>
&nbsp;
<a href="https://www.linkedin.com/in/vikas-vishwakarma-62959a387/">
  <img src="https://img.shields.io/badge/connect-06080C?style=for-the-badge&logo=linkedin&logoColor=2BD3E8&labelColor=06080C" alt="LinkedIn" />
</a>

<br/><br/>

<samp>`└─$ exit 0`</samp>

</div>
