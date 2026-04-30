import pandas as pd
import matplotlib.pyplot as plt
import os
from datetime import datetime

print("\n--- 🔍 New Student Analysis ---")

name = input("Enter Name: ")

print("\nChoose Stream:")
print("1. Science\n2. Commerce\n3. Arts\n4. JEE\n5. NEET")

while True:
    s = input("Enter choice: ")
    if s in ["1","2","3","4","5"]:
        break

stream_map = {"1":"sci","2":"comm","3":"arts","4":"jee","5":"neet"}
stream = stream_map[s]

# ================= ID GENERATION =================
prefix = {"sci":"SCI","comm":"COM","arts":"ART","jee":"JEE","neet":"MED"}
stream_prefix = prefix[stream]

if os.path.exists("students.csv"):
    df_temp = pd.read_csv("students.csv")
    stream_df = df_temp[df_temp["StudentID"].str.startswith(stream_prefix)]

    if not stream_df.empty:
        last_id = stream_df["StudentID"].iloc[-1]
        num = int(last_id[len(stream_prefix):])
        new_num = num + 1
    else:
        new_num = 1
else:
    new_num = 1

student_id = stream_prefix + str(new_num).zfill(3)

print(f"\n🆔 Student ID: {student_id}")

# ================= ACADEMIC =================
if stream == "jee":
    marks = float(input("Enter your JEE marks out of 300: "))
    academic_score = (marks/300)*100
elif stream == "neet":
    marks = float(input("Enter your NEET marks out of 720: "))
    academic_score = (marks/720)*100
else:
    percent = float(input("Enter your percentage: "))
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

print("\n========================================")
print(f"👤 {name}")
print(f"🆔 {student_id}")
print(f"📈 Effectiveness: {round(effectiveness,2)}%")
print(f"🏆 {result}")
print("========================================")

# ================= SAVE =================
timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

data = {
"StudentID": student_id,
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

df_new = pd.DataFrame([data])

if not os.path.exists("students.csv"):
    df_new.to_csv("students.csv", index=False)
else:
    df = pd.read_csv("students.csv")
    df = pd.concat([df, df_new], ignore_index=True)
    df.to_csv("students.csv", index=False)

print("\n✅ Data saved successfully!")

# ================= GRAPH CHOICE =================
print("\nDo you want to see graphs?")
print("1. Progress (Line Graph)")
print("2. Factor Scores (Bar Graph)")
print("3. Both")
print("4. Skip")

g_choice = input("Enter choice: ")

df = pd.read_csv("students.csv")
student_df = df[df["StudentID"] == student_id].sort_values("Timestamp")

if g_choice in ["1","3"]:
    plt.figure()
    plt.plot(student_df["Timestamp"], student_df["Effectiveness"], marker='o')
    plt.xticks(rotation=45)
    plt.title("Effectiveness Over Time")
    plt.tight_layout()
    plt.show()

if g_choice in ["2","3"]:
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

if latest["Sleep"] < 50:
    print("👉 Fix sleep schedule immediately")

if latest["Lifestyle"] < 50:
    print("👉 Improve exercise and reduce distractions")

if latest["Strategy"] < 50:
    print("👉 Focus on revision and mistake analysis")

if latest["Burnout"] > 60:
    print("👉 Reduce pressure and take proper breaks")

if latest["Self"] < 50:
    print("👉 Build consistency with small achievable goals")

print("\n===== ADVANCED INSIGHTS =====")

flag = False

if latest["Burnout"] > 70 and latest["Strategy"] > 70:
    print("⚠️ You're working hard but burning out")
    flag = True

if latest["Self"] < 40 and latest["Strategy"] > 60:
    print("⚠️ Good plan but poor execution")
    flag = True

if latest["Sleep"] < 40 and latest["Burnout"] > 60:
    print("⚠️ Sleep is causing burnout")
    flag = True

if flag == False:
    print("✅ No critical issues detected. Keep improving.")

input("\nPress Enter to return to main menu...")