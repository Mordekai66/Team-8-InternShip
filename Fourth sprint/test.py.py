import tkinter as tk
from tkinter import ttk, Frame, Scrollbar, Text
import google.generativeai as ai
import pandas as pd
import joblib
from datetime import datetime
import webbrowser

courses = {}

data = pd.read_excel(r"C:\Users\J0223067\Desktop\Team-8-InternShip-main\First sprint\data - project.xlsx")
category_list = data["A"].unique().tolist()
programming_language_list = data["B"].unique().tolist()
difficulty_list = data["C"].unique().tolist()
free_paid_list = data["D"].unique().tolist()

model = joblib.load(r"C:\Users\J0223067\Desktop\Team-8-InternShip-main\Second sprint\kmeans_model.pt")
le_a = joblib.load(r"C:\Users\J0223067\Desktop\Team-8-InternShip-main\Second sprint\le_a.pt")
le_b = joblib.load(r"C:\Users\J0223067\Desktop\Team-8-InternShip-main\Second sprint\le_b.pt")
le_c = joblib.load(r"C:\Users\J0223067\Desktop\Team-8-InternShip-main\Second sprint\le_c.pt")
le_d = joblib.load(r"C:\Users\J0223067\Desktop\Team-8-InternShip-main\Second sprint\le_d.pt")

def predict_cluster():
    
    global courses
    a = category_var.get()
    b = programming_language_var.get()
    c = difficulty_var.get()
    d = free_paid_var.get()

    sign = False

    for index, row in data.iterrows():
        if (row.iloc[0] == a and 
            row.iloc[1] == b and 
            row.iloc[2] == c and 
            row.iloc[3] == d):
            sign = True
            break
    if sign:
    
        try:
            new_a_encoded = le_a.transform([a])[0]
            new_b_encoded = le_b.transform([b])[0]
            new_c_encoded = le_c.transform([c])[0]
            new_d_encoded = le_d.transform([d])[0]
    
            test = pd.DataFrame([[new_a_encoded, new_b_encoded, new_c_encoded, new_d_encoded]],
                                columns=['A', 'B', 'C', 'D'])
    
            predict_cluster = model.predict(test)[0]
            courses = {}
            result = ""
            for i, label in enumerate(model.labels_):
                if label == predict_cluster:
                    course_name = data['E'][i].split("\n")[0]
                    course_time = data['E'][i].split("\n")[2]
                    courses[course_name] = course_time
    
                    course = data["E"][i]
                    result += f"Course: {course}\n"
    
            result_text.config(state="normal")
            result_text.delete(1.0, tk.END)
            result_text.tag_configure("rtl", justify="right")
            result_text.insert(tk.END, result,"rtl")
            result_text.config(state="disabled")
            
            
            course_name_menu['values'] = list(courses.keys())
            
        except Exception as e:
            result_text.config(state="normal")
            result_text.delete(1.0, tk.END)
            result_text.tag_configure("rtl", justify="right")
            result_text.insert(tk.END, f"An error occurred: {str(e)}","rtl")
            result_text.config(state="disabled")
    else:
        result_text.config(state="normal")
        result_text.delete(1.0, tk.END)
        result_text.tag_configure("rtl", justify="right")
        result_text.insert(tk.END, "لا توجد كورسات متاحة في الوقت الحالي، وسنقوم بتوفير الكورسات المطلوبة قريبًا.","rtl")
        result_text.config(state="disabled")


def get_work_schedule():
    try:
        
        work_start_time = datetime.strptime(start_time_var.get(), "%H:%M")
        work_end_time = datetime.strptime(end_time_var.get(), "%H:%M")
        work_days = work_days_var.get()

        API_KEY = 'AIzaSyDskMgdh9O5QIAa6gFgSL1jXrtyjPm7vjQ'
        ai.configure(api_key=API_KEY)
        model = ai.GenerativeModel(model_name='gemini-1.5-flash')
        response = model.generate_content(f"""اسم الدورة التدريبية والمنصة: [{course_name_menu.get()}]
مدة الدورة التدريبية: [{courses[course_name_menu.get()]}]
ساعات الدراسة الخاصة بي: من الساعة [{work_start_time}] إلى الساعة [{work_end_time}]
عدد الأيام: [{work_days}]
أحتاج إلى إنشاء جدول زمني بناءً على المدخلات و محتوى الكورس وتزويدي بنصيحة قبل بدء الدورة التدريبية، دون الحاجة إلى إعداد جداول ولا اريد اية كلمة باللغة الانجليزية فقط اريد عربي""")

        result_text_2.config(state="normal")
        result_text_2.delete(1.0, tk.END)
        result_text_2.tag_configure("rtl", justify="right")
        result_text_2.insert(tk.END, response.text,"rtl")
        result_text_2.config(state="disabled")

    except Exception as e:
        result_text_2.config(state="normal")
        result_text_2.delete(1.0, tk.END)
        result_text_2.tag_configure("rtl", justify="right")
        result_text_2.insert(tk.END, result,"rtl")
        result_text_2.insert(tk.END, f"An error occurred: {str(e)}")
        result_text_2.config(state="disabled")



def update_programming_language(event):
    selected_category = category_var.get()

    if selected_category == "programming":
        programming_language_menu.config(state="normal")
        programming_language_menu['values'] = programming_language_list
        programming_language_var.set('')  
    else:
        programming_language_menu.config(state="disabled")
        programming_language_menu['values'] = []
        programming_language_var.set('NAN')

def get_document():
    url = 'https://github.com/Mordekai66/temp/blob/main/README.md'
    webbrowser.open(url)
    
pro = tk.Tk()
pro.title("Course Recommendation System")
pro.geometry("800x550")
pro.configure(bg="#0a182c")  
pro.resizable(False, False)


input_frame = Frame(pro, bg="#0a182c")  
input_frame.grid(row=0, column=0, padx=10, pady=5, sticky="nsew")


tk.Label(input_frame, text="Category", bg="#0a182c", fg="#ffffff").grid(row=1, column=0, padx=10, pady=5)
tk.Label(input_frame, text="Programming Language", bg="#0a182c", fg="#ffffff").grid(row=2, column=0, padx=10, pady=5)
tk.Label(input_frame, text="Difficulty", bg="#0a182c", fg="#ffffff").grid(row=3, column=0, padx=10, pady=5)
tk.Label(input_frame, text="Free/Paid", bg="#0a182c", fg="#ffffff").grid(row=4, column=0, padx=10, pady=5)


category_var = tk.StringVar()
programming_language_var = tk.StringVar()
difficulty_var = tk.StringVar()
free_paid_var = tk.StringVar()

category_menu = ttk.Combobox(input_frame, textvariable=category_var, values=category_list, width=30)
category_menu.grid(row=1, column=1, padx=10, pady=10)
category_menu.bind('<<ComboboxSelected>>', update_programming_language)

programming_language_menu = ttk.Combobox(input_frame, textvariable=programming_language_var, values=programming_language_list, width=30)
programming_language_menu.grid(row=2, column=1, padx=10, pady=10)

difficulty_menu = ttk.Combobox(input_frame, textvariable=difficulty_var, values=difficulty_list, width=30)
difficulty_menu.grid(row=3, column=1, padx=10, pady=10)

free_paid_menu = ttk.Combobox(input_frame, textvariable=free_paid_var, values=free_paid_list, width=30)
free_paid_menu.grid(row=4, column=1, padx=10, pady=10)


predict_button = tk.Button(input_frame, text="Predict", command=predict_cluster, bg="#ff6c00", fg="#ffffff")
predict_button.grid(row=5, column=1, columnspan=2, pady=40)
category_menu.bind("<<ComboboxSelected>>", update_programming_language)

tk.Label(input_frame, text="Course name", bg="#0a182c", fg="#ffffff").grid(row=17, column=0, padx=10, pady=10)
tk.Label(input_frame, text="Work Start Time (HH:MM)", bg="#0a182c", fg="#ffffff").grid(row=18, column=0, padx=10, pady=10)
tk.Label(input_frame, text="Work End Time (HH:MM)", bg="#0a182c", fg="#ffffff").grid(row=19, column=0, padx=10, pady=10)
tk.Label(input_frame, text="Work Days", bg="#0a182c", fg="#ffffff").grid(row=20, column=0, padx=10, pady=10)

start_time_var = tk.StringVar()
end_time_var = tk.StringVar()
work_days_var = tk.StringVar()

course_name = list(courses.keys())
course_name_menu = ttk.Combobox(input_frame, values=course_name, width=30)
course_name_menu.grid(row=17, column=1, padx=10, pady=10)

start_time_entry = tk.Entry(input_frame, textvariable=start_time_var, width=30)
start_time_entry.grid(row=18, column=1, padx=10, pady=10)

end_time_entry = tk.Entry(input_frame, textvariable=end_time_var, width=30)
end_time_entry.grid(row=19, column=1, padx=10, pady=10)

work_days_entry = tk.Entry(input_frame, textvariable=work_days_var, width=30)
work_days_entry.grid(row=20, column=1, padx=10, pady=10)

schedule_button = tk.Button(input_frame, text="Get Schedule", command=get_work_schedule, bg="#ff6c00", fg="#ffffff")
schedule_button.grid(row=22, column=1, columnspan=2, pady=10)


output_frame = Frame(pro, bg="#0a182c")  
output_frame.grid(row=0, column=1, padx=10, pady=5, sticky="nsew")


result_text = Text(output_frame, height=15, width=40, wrap="word", state="disabled")
result_text.grid(row=0, column=0, padx=10, pady=10)
result_text.tag_configure("rtl", justify="right")

result_text_2 = Text(output_frame, height=15, width=40, wrap="word", state="disabled")
result_text_2.grid(row=1, column=0, padx=10, pady=10)
result_text_2.tag_configure("rtl", justify="right")
scrollbar_1 = tk.Scrollbar(output_frame)
scrollbar_1.grid(row=0, column=1, sticky="snew")

result_text = tk.Text(output_frame, height=15, width=40, wrap="word", state="disabled",bg= "#c4cac4",font = ("Arial",11), yscrollcommand=scrollbar_1.set)
result_text.grid(row=0, column=0, padx=0, pady=10)


scrollbar_1.config(command=result_text.yview)


scrollbar_2 = tk.Scrollbar(output_frame)
scrollbar_2.grid(row=1, column=1, sticky="snew")

result_text_2 = tk.Text(output_frame, height=15, width=40, wrap="word", state="disabled",bg= "#c4cac4",font = ("Arial",11), yscrollcommand=scrollbar_2.set)
result_text_2.grid(row=1, column=0, padx=0, pady=10)

scrollbar_2.config(command=result_text_2.yview)


button_doc = tk.Button(pro,text="Get documentation",command=get_document,bg="#ff6c00", fg="#ffffff")
button_doc.place(x=25,y=520)

pro.grid_columnconfigure(0, weight=1)
pro.grid_rowconfigure(0, weight=1)
     
pro.mainloop()