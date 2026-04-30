import pandas as pd
import os

print("\n--- 🗑 DELETE STUDENT RECORD ---")

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
        student_df = student_df.sort_values("Timestamp").reset_index()

        print("\n===== SELECT RECORD TO DELETE =====")

        for i in range(len(student_df)):
            print(f"{i+1}. {student_df.loc[i,'Timestamp']} | Effectiveness: {student_df.loc[i,'Effectiveness']} | {student_df.loc[i,'Performance']}")

        print(f"{len(student_df)+1}. Delete ALL records")
        print(f"{len(student_df)+2}. Cancel")

        choice = input("Enter choice: ")

        # ================= DELETE ONE =================
        if choice.isdigit():
            choice = int(choice)

            if 1 <= choice <= len(student_df):
                confirm = input("Are you sure you want to delete this record? (yes/no): ")

                if confirm.lower() == "yes":
                    original_index = student_df.loc[choice-1, "index"]
                    df = df.drop(original_index)
                    df.to_csv("students.csv", index=False)
                    print("✅ Record deleted")
                else:
                    print("❌ Cancelled")

            # ================= DELETE ALL =================
            elif choice == len(student_df) + 1:
                confirm = input("⚠️ Delete ALL records of this student? (yes/no): ")

                if confirm.lower() == "yes":
                    df = df[df["StudentID"] != sid]
                    df.to_csv("students.csv", index=False)
                    print("✅ All records deleted")
                else:
                    print("❌ Cancelled")

            # ================= CANCEL =================
            elif choice == len(student_df) + 2:
                print("❌ Cancelled")

            else:
                print("❌ Invalid choice")

        else:
            print("❌ Invalid input")

    input("\nPress Enter to return to main menu...")