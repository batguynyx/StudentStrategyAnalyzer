import pandas as pd
import matplotlib.pyplot as plt
import os
from datetime import datetime

print("\n--- ✏️ EDIT / RE-ANALYZE STUDENT ---")

if not os.path.exists("students.csv"):
    print("❌ No data found")
    input("\nPress Enter to return...")
else:
    df = pd.read_csv("students.csv")

    sid = input("Enter Student ID (e.g., JEE001): ")

    student_df = df[df["StudentID"] == sid]

    if student_df.empty:
        print("❌ Student not found")

    else:
        student_df = student_df.sort_values("Timestamp")

        name = student_df.iloc[-1]["Name"]
        stream = student_df.iloc[-1]["Stream"]

        print(f"\n👤 Name: {name}")
        print(f"📘 Stream: {stream.upper()}")

        print("\n===== PREVIOUS RECORDS =====")
        print(student_df[["Timestamp","Effectiveness","Performance"]])

        confirm = input("\nDo you want to re-analyze this student? (yes/no): ")

        if confirm.lower() != "yes":
            print("❌ Cancelled")

        else:
            # ================= ACADEMIC =================
            if stream == "jee":
                marks = float(input("Enter new JEE marks out of 300: "))
                academic_score = (marks/300)*100
            elif stream == "neet":
                marks = float(input("Enter new NEET marks out of 720: "))
                academic_score = (marks/720)*100
            else:
                percent = float(input("Enter new percentage: "))
                if stream == "sci":
                    academic_score = percent * 1.05
                elif stream == "comm":
                    academic_score = percent
                else:
                    academic_score = percent * 0.95
                academic_score = min(100, academic_score)

            # ================= QUESTIONS =================
            questions = [
            ("How many hours do you sleep daily?", "num"),
            ("How many hours do you study daily (self-study)?", "num"),
            ("How many hours of non-study screen time?", "num"),

            ("How do you feel after waking up?\n1 Fresh\n2 Good\n3 Neutral\n4 Tired\n5 Exhausted", "mcq"),
            ("How often do you feel sleepy while studying?\n1 Never\n2 Rare\n3 Sometimes\n4 Often\n5 Always", "mcq"),

            ("Do you exercise at least 3 times a week? (yes/no)", "yesno"),
            ("Do you consume junk food frequently? (yes/no)", "yesno"),

            ("How easily do you get distracted?\n1 Rarely\n2 Slightly\n3 Moderately\n4 Often\n5 Constantly", "mcq"),
            ("How long can you focus continuously (minutes)?", "num"),

            ("How mentally exhausted do you feel daily?\n1 Not at all\n2 Slight\n3 Moderate\n4 High\n5 Extreme", "mcq"),
            ("Do you feel like quitting sometimes? (yes/no)", "yesno"),

            ("How confident are you about your success?\n1 Very low\n2 Low\n3 Medium\n4 High\n5 Very high", "mcq"),
            ("Do you complete your daily study targets? (yes/no)", "yesno"),

            ("How regularly do you revise topics?\n1 Never\n2 Rare\n3 Sometimes\n4 Often\n5 Always", "mcq"),
            ("How often do you practice questions?\n1 Never\n2 Rare\n3 Sometimes\n4 Often\n5 Daily", "mcq"),
            ("Do you analyze your mistakes after tests? (yes/no)", "yesno"),

            ("Do you follow a fixed schedule? (yes/no)", "yesno"),
            ("How consistent is your routine?\n1 Very inconsistent\n2 Inconsistent\n3 Average\n4 Consistent\n5 Very consistent", "mcq"),

            ("How many mock tests do you give weekly?", "num"),
            ("How many hours do you knowingly waste daily?", "num"),
            ]

            answers = []
            i = 0

            while i < len(questions):
                q, t = questions[i]
                print("\n" + q)
                ans = input("Answer (or type 'back'): ")

                if ans.lower() == "back":
                    if i > 0:
                        i -= 1
                        answers.pop()
                    continue

                try:
                    if t == "num":
                        val = float(ans)
                    elif t == "mcq":
                        val = int(ans)
                        if val < 1 or val > 5:
                            raise ValueError
                    elif t == "yesno":
                        if ans.lower() not in ["yes","no"]:
                            raise ValueError
                        val = ans.lower()

                    answers.append(val)
                    i += 1
                except:
                    print("❌ Invalid input")

            # ================= SCORING =================
            sleep_score = (min(5, answers[0]/2) + (6 - answers[3])) * 10

            lifestyle_score = (
                (5 if answers[5]=="yes" else 2) +
                (2 if answers[6]=="yes" else 5) +
                (6 - answers[7])
            ) * 7

            burnout_score = (
                answers[9] +
                (5 if answers[10]=="yes" else 1)
            ) * 10

            self_score = (
                answers[11] +
                (5 if answers[12]=="yes" else 2)
            ) * 10

            strategy_score = (
                answers[13] +
                answers[14] +
                (5 if answers[15]=="yes" else 2) +
                (5 if answers[16]=="yes" else 2) +
                answers[17]
            ) * 5

            effectiveness = (
                0.4 * academic_score +
                0.15 * sleep_score +
                0.1 * lifestyle_score +
                0.15 * self_score +
                0.15 * strategy_score -
                0.25 * burnout_score
            )

            effectiveness = max(0, min(100, effectiveness))
            result = "Excellent" if effectiveness >= 80 else "Average" if effectiveness >= 60 else "Needs Improvement"

            print("\n===== NEW RESULT =====")
            print(f"📈 Effectiveness: {round(effectiveness,2)}%")
            print(f"🏆 {result}")

            # ================= SAVE =================
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            data = {
                "StudentID": sid,
                "Name": name,
                "Stream": stream,
                "Timestamp": timestamp,
                "Academic": round(academic_score,2),
                "Sleep": round(sleep_score,2),
                "Lifestyle": round(lifestyle_score,2),
                "Self": round(self_score,2),
                "Strategy": round(strategy_score,2),
                "Burnout": round(burnout_score,2),
                "Effectiveness": round(effectiveness,2),
                "Performance": result
            }

            df = pd.concat([df, pd.DataFrame([data])], ignore_index=True)
            df.to_csv("students.csv", index=False)

            print("\n✅ New attempt saved!")

            # ================= GRAPH CHOICE =================
            print("\nDo you want to see graphs?")
            print("1. Progress")
            print("2. Factors")
            print("3. Both")
            print("4. Skip")

            g = input("Enter choice: ")

            student_df = df[df["StudentID"] == sid].sort_values("Timestamp")

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
                plt.title("Factor Scores")
                plt.show()

            # ================= ANALYSIS =================
            latest = student_df.iloc[-1]

            print("\n===== FACTOR ANALYSIS =====")

            for factor in ["Academic","Sleep","Lifestyle","Self","Strategy"]:
                if latest[factor] < 40:
                    print(f"{factor}: Low")
                elif latest[factor] < 70:
                    print(f"{factor}: Average")
                else:
                    print(f"{factor}: High")

            print(f"Burnout: {'High' if latest['Burnout']>70 else 'Moderate' if latest['Burnout']>40 else 'Low'}")

            print("\n===== RECOMMENDATIONS =====")

            rec_flag = False
            
            # Sleep
            if latest["Sleep"] < 50:
                print("👉 Fix your sleep schedule. Aim for consistent timing and reduce late-night screen use.")
                rec_flag = True
            elif latest["Sleep"] >= 70:
                print("✅ Your sleep is solid. Maintain this routine.")
            
            # Lifestyle
            if latest["Lifestyle"] < 50:
                print("👉 Improve lifestyle: add exercise and reduce junk food + distractions.")
                rec_flag = True
            elif latest["Lifestyle"] >= 70:
                print("✅ Good lifestyle discipline. Keep it up.")
            
            # Strategy
            if latest["Strategy"] < 50:
                print("👉 Your study strategy needs work: focus on revision and analyzing mistakes.")
                rec_flag = True
            elif latest["Strategy"] >= 70:
                print("✅ Strong study strategy. You're doing things right.")
            
            # Burnout
            if latest["Burnout"] > 60:
                print("👉 You're experiencing burnout. Take breaks and reduce overload.")
                rec_flag = True
            elif latest["Burnout"] < 40:
                print("✅ Burnout is well under control.")
            
            # Self / consistency
            if latest["Self"] < 50:
                print("👉 Work on consistency. Start with small daily achievable goals.")
                rec_flag = True
            elif latest["Self"] >= 70:
                print("✅ Strong mindset and consistency.")
            
            # Academic
            if latest["Academic"] < 50:
                print("👉 Focus more on concept clarity and test practice.")
                rec_flag = True
            elif latest["Academic"] >= 80:
                print("✅ Academic performance is strong.")
            
            # 🔥 FINAL FALLBACK
            if rec_flag == False:
                print("🚀 Overall you're performing well. Focus on consistency and incremental improvement.")

    input("\nPress Enter to return to main menu...")