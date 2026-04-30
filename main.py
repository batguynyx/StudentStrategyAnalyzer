import importlib

print('''========================================
🎯 Student Strategy Analyzer
========================================''')

while True:

    print('''
----------------------------------------
1. Analyze New Student
2. View Dashboard
3. Delete Record
4. Reanalyze a Student
----------------------------------------
''')

    choice = input("Enter choice: ")

    # ================= OPTION 1 =================
    if choice == "1":
        if "option1_analyze" in globals():
            importlib.reload(option1_analyze)
        else:
            import option1_analyze

    # ================= OPTION 2 =================
    elif choice == "2":
        if "option2_view" in globals():
            importlib.reload(option2_view)
        else:
            import option2_view

    # ================= OPTION 3 =================
    elif choice == "3":
        if "option3_delete" in globals():
            importlib.reload(option3_delete)
        else:
            import option3_delete

    # ================= OPTION 4 =================
    elif choice == "4":
        if "option4_edit" in globals():
            importlib.reload(option4_edit)
        else:
            import option4_edit

    else:
        print("❌ Invalid choice")

    input("\nPress Enter to continue...")
