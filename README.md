# StudentStrategyAnalyzer
A modular Python CLI application that analyzes student strategy, computes effectiveness scores, visualizes trends, and supports reanalysis with historical tracking.
# 🎯 Student Strategy Analyzer

A Python-based **CLI analytics system** that evaluates student performance across multiple factors like academics, lifestyle, strategy, and mental health — and provides actionable insights, progress tracking, and recommendations.

---

## 🚀 Features

### 🔍 1. Analyze New Student

* Stream-based evaluation (Science, Commerce, Arts, JEE, NEET)
* 20+ descriptive questions (numeric, MCQ, yes/no)
* Smart scoring system:

  * Academic
  * Sleep
  * Lifestyle
  * Strategy
  * Self-discipline
  * Burnout
* Generates:

  * 📈 Effectiveness Score
  * 🏆 Performance Category

---

### 📊 2. View Dashboard

* Displays all student records
* Stream-colored comparison graph
* Individual student deep-dive:

  * 📈 Progress over time (line graph)
  * 📊 Factor breakdown (bar graph)
* Shows:

  * Improvement / decline trends
  * Factor-wise analysis
  * Smart recommendations

---

### 🗑 3. Delete Record

* View all records of a student before deleting
* Delete:

  * Specific attempt (by timestamp)
  * OR entire history
* Confirmation system to prevent mistakes

---

### ✏️ 4. Reanalyze a Student

* Re-run full analysis for an existing student
* Preserves history (no data loss)
* Tracks progress across attempts
* Includes:

  * Graphs
  * Analysis
  * Recommendations

---

## 🧠 Scoring System

The final **Effectiveness Score (0–100)** is calculated using:

* Academic Performance → 40%
* Sleep → 15%
* Lifestyle → 10%
* Self → 15%
* Strategy → 15%
* Burnout → -25% (negative impact)

---

## 📈 Visualization

* **Line Graph** → Progress over time
* **Bar Graph** → Factor-wise breakdown
* **Comparison Graph** → Multi-student performance (color-coded by stream)

---

## 🗂 Data Storage

All data is stored in:

```bash
students.csv
```

Each entry includes:

* Student ID (e.g., JEE001, SCI002)
* Timestamp
* All factor scores
* Effectiveness
* Performance category

---

## 🧱 Project Structure

```bash
project/
│
├── main.py
├── option1_analyze.py
├── option2_view.py
├── option3_delete.py
├── option4_edit.py
│
├── students.csv (auto-created)
```

---

## ▶️ How to Run

```bash
python main.py
```

---

## 🎯 Key Highlights

* Modular CLI application (no messy single-file code)
* Real-world analytics logic (not just input/output)
* Tracks **progress over time**
* Provides **actionable insights**, not just scores
* Clean UX with controlled navigation

---

## ⚠️ Notes

* Built without functions (`def`) as per academic constraints
* Uses:

  * `pandas`
  * `matplotlib`
* Graphs require a GUI environment

---

## 💡 Future Improvements

* 🔔 Alert system (low-performing students)
* 🏆 Ranking system
* 📊 Export reports
* 🌐 Web interface (Flask / Streamlit)

---

## 👤 Author

Developed as a student analytics system project.

---

## ⭐ If you found this useful

Give it a star ⭐ — and feel free to build on top of it!
