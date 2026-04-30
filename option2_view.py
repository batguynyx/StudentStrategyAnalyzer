import pandas as pd
import matplotlib.pyplot as plt
import os

print("\n--- 📊 VIEW STUDENT DASHBOARD ---")

if not os.path.exists("students.csv"):
    print("❌ No data found")
    input("\nPress Enter to return...")
else:
    df = pd.read_csv("students.csv")

    # ================= SHOW ALL =================
    print("\n===== ALL STUDENTS =====")
    print(df[["StudentID","Name","Stream","Effectiveness","Timestamp"]])

    # ================= ASK FOR COMPARISON GRAPH =================
    print("\nDo you want to see comparison graph of all students?")
    print("1. Yes")
    print("2. No")

    g_all = input("Enter choice: ")

    if g_all == "1":
        latest_df = df.sort_values("Timestamp").groupby("StudentID").tail(1)

        color_map = {
            "sci": "blue",
            "comm": "green",
            "arts": "orange",
            "jee": "red",
            "neet": "purple"
        }

        colors = [color_map.get(s, "gray") for s in latest_df["Stream"]]

        plt.figure()
        plt.bar(latest_df["StudentID"], latest_df["Effectiveness"], color=colors)

        plt.xticks(rotation=45)
        plt.title("Student Effectiveness Comparison")
        plt.xlabel("Student ID")
        plt.ylabel("Effectiveness")

        from matplotlib.patches import Patch
        legend_elements = [
            Patch(facecolor='blue', label='Science'),
            Patch(facecolor='green', label='Commerce'),
            Patch(facecolor='orange', label='Arts'),
            Patch(facecolor='red', label='JEE'),
            Patch(facecolor='purple', label='NEET')
        ]
        plt.legend(handles=legend_elements)

        plt.tight_layout()
        plt.show()

    # ================= ASK FOR SPECIFIC =================
    print("\nDo you want to view detailed analysis of a student?")
    print("1. Yes")
    print("2. No")

    ch = input("Enter choice: ")

    if ch == "1":
        sid = input("Enter Student ID (e.g., JEE001): ")

        student_df = df[df["StudentID"] == sid]

        if student_df.empty:
            print("❌ Student not found")

        else:
            student_df = student_df.sort_values("Timestamp")

            print("\n===== STUDENT HISTORY =====")
            print(student_df[["Timestamp","Effectiveness","Performance"]])

            # ================= PROGRESS =================
            if len(student_df) > 1:
                first = student_df.iloc[0]["Effectiveness"]
                latest_val = student_df.iloc[-1]["Effectiveness"]

                print("\n===== PROGRESS =====")

                if latest_val > first:
                    print(f"📈 Improved by {round(latest_val - first,2)}%")
                elif latest_val < first:
                    print(f"📉 Declined by {round(first - latest_val,2)}%")
                else:
                    print("➖ No change")

            # ================= GRAPH CHOICE =================
            print("\nShow graphs?")
            print("1. Progress (Line)")
            print("2. Factors (Bar)")
            print("3. Both")
            print("4. Skip")

            g = input("Enter choice: ")

            if g in ["1","3"]:
                plt.figure()
                plt.plot(student_df["Timestamp"], student_df["Effectiveness"], marker='o')
                plt.xticks(rotation=45)
                plt.title("Effectiveness Over Time")
                plt.tight_layout()
                plt.show()

            if g in ["2","3"]:
                latest = student_df.iloc[-1]
                labels = ["Academic","Sleep","Lifestyle","Self","Strategy","Burnout"]
                values = [latest[x] for x in labels]

                plt.figure()
                plt.bar(labels, values)
                plt.title("Latest Factor Scores")
                plt.show()

            # ================= ANALYSIS =================
            latest = student_df.iloc[-1]

            print("\n===== CURRENT ANALYSIS =====")

            for factor in ["Academic","Sleep","Lifestyle","Self","Strategy"]:
                if latest[factor] < 40:
                    print(f"{factor}: Low")
                elif latest[factor] < 70:
                    print(f"{factor}: Average")
                else:
                    print(f"{factor}: High")

            print(f"Burnout: {'High' if latest['Burnout']>70 else 'Moderate' if latest['Burnout']>40 else 'Low'}")

            # ================= RECOMMENDATIONS =================
            print("\n===== RECOMMENDATIONS =====")

            if latest["Sleep"] < 50:
                print("👉 Fix sleep schedule")

            if latest["Lifestyle"] < 50:
                print("👉 Improve lifestyle and reduce distractions")

            if latest["Strategy"] < 50:
                print("👉 Focus on revision and mistake analysis")

            if latest["Burnout"] > 60:
                print("👉 Reduce stress and take breaks")

            if latest["Self"] < 50:
                print("👉 Build consistency with small goals")

    input("\nPress Enter to return to main menu...")