import tkinter as tk
import numpy as np
import pickle

from tkinter import messagebox
from tkinter import ttk

with open('RandomForest.pickle', 'rb') as file:
    model = pickle.load(file)

with open('scaler.pkl', 'rb') as file:
    scaler = pickle.load(file)

def submit():
    try:
        age = int(age_var.get())
        ejection_fraction = int(ef_var.get())
        serum_creatinine = int(creatinine_var.get())
        serum_sodium = float(sodium_var.get())
        time = int(followup_var.get())

    except ValueError:
        messagebox.showerror("Input Error", "Please enter valid integers in the numeric fields.")
        return


    # Collect all the input data into a single array
    input_data = np.array([
        [
            age,
            ejection_fraction,
            serum_creatinine,
            serum_sodium,
            time
        ]
    ])
    # Make predictions using the pre-trained model
    input_data = scaler.transform(input_data)
    prediction = model.predict(input_data)

    result_text = "Death" if prediction == 1 else "Not Death"
    print(prediction)
    result_value.config(text=result_text)


def validate_integer(value_if_allowed):
    if value_if_allowed.isdigit() or value_if_allowed == "":
        return True
    else:
        return False

def comboHandler(e):
    selection = combo.get()
    messagebox.showinfo(
        title="Model Selected",
        message=f"Selected model: {selection}"
    )
    global model
    if selection == "RandomForest":
        with open('RandomForest.pickle', 'rb') as file:
            model = pickle.load(file)
    elif selection == "CatBoostClassifier":
        with open('CatBoostClassifier.pickle', 'rb') as file:
            model = pickle.load(file)
    elif selection == "KNN":
        with open('KNeighbors.pickle', 'rb') as file:
            model = pickle.load(file)
    print(model)

root = tk.Tk()
root.title("Death Predictor")

# Register the validation command
vcmd = (root.register(validate_integer), '%P')

# Variables to hold form data
name_var = tk.StringVar()
age_var = tk.StringVar()
ef_var = tk.StringVar()
creatinine_var = tk.StringVar()
sodium_var = tk.StringVar()
followup_var = tk.StringVar()

# Left panel
left_frame = tk.Frame(root)
left_frame.grid(row=0, column=0, padx=10, pady=10, sticky="n")

welcome_label = tk.Label(left_frame, text="Welcome to Death Predictor:")
welcome_label.pack(anchor="w")

# Right panel
right_frame = tk.Frame(root)
right_frame.grid(row=0, column=1, padx=10, pady=10, sticky="n")

combo = ttk.Combobox(right_frame, state="readonly", values=["RandomForest", "CatBoostClassifier", "KNN"])
combo.bind("<<ComboboxSelected>>", comboHandler)

fields = [
    ("Predictor Model:", combo),
    ("Name:", tk.Entry(right_frame, textvariable=name_var)),
    ("Age:", tk.Entry(right_frame, textvariable=age_var, validate="key", validatecommand=vcmd)),
    ("What is your most recent ejection fraction (EF) measurement?", tk.Entry(right_frame, textvariable=ef_var, validate="key", validatecommand=vcmd)),
    ("What is your most recent serum creatinine level?", tk.Entry(right_frame, textvariable=creatinine_var, validate="key", validatecommand=vcmd)),
    ("What is your most recent serum sodium level?", tk.Entry(right_frame, textvariable=sodium_var, validate="key", validatecommand=vcmd)),
    ("Followed up days:", tk.Entry(right_frame, textvariable=followup_var, validate="key", validatecommand=vcmd))
]


for i, (label_text, widget) in enumerate(fields):
    label = tk.Label(right_frame, text=label_text)
    label.grid(row=i, column=0, sticky="w", pady=2)
    widget.grid(row=i, column=1, sticky="w", pady=2)
    submit_button = tk.Button(right_frame, text="Submit", command=submit)
    submit_button.grid(row=len(fields), column=0, columnspan=2, pady=10)

# Center panel for result
center_frame = tk.Frame(root)
center_frame.grid(row=0, column=2, padx=10, pady=10, sticky="n")

result_label = tk.Label(center_frame, text="Based on data you provided:")
result_label.pack()

result_value = tk.Label(center_frame, text="NULL", font=("Helvetica", 32))
result_value.pack()

root.mainloop()
