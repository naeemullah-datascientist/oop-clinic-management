from tkinter import *
from tkinter.ttk import Separator, Style
import sqlite3
import tkinter.messagebox
from tkinter import font
from datetime import datetime, timedelta
from tkinter import PhotoImage
from PIL import Image, ImageTk

conn = sqlite3.connect('database.db')
c = conn.cursor()
ids = []
number = []
patients = []

class Doctor:
    def __init__(self, name):
        self.name = name
        self.available_slots = self.generate_time_slots()
    def generate_time_slots(self):
        base_time = datetime.strptime("03:00", "%H:%M")
        time_slots = [base_time + timedelta(minutes=30 * i) for i in range(7)]
        return [time.strftime("%H:%M"+" pm") for time in time_slots]

class AppointmentManager:
    def __init__(self):
        self.doctors = [
            Doctor("Dr. Omer           Cardiologist"),
            Doctor("Dr. Idrees         Orthopedic"),
            Doctor("Dr. Bukhari        Psychologist"),
            Doctor("Dr. Abdullah       Dermatologist")
        ]

    def get_doctor_names(self):
        return [doctor.name for doctor in self.doctors]

    def get_doctor_by_name(self, name):
        for doctor in self.doctors:
            if doctor.name == name:
                return doctor
        return None

class Application:
    def __init__(self, window):
        self.window = window
        self.v = IntVar()
        self.appointment_manager = AppointmentManager()
        c.execute("SELECT * FROM appointments")
        self.alldata = c.fetchall()
        self.main = Frame(window, width=700, height=700, bg="#C0C0C0")
        self.showdetailsframe = Frame(self.window)
        self.updateframe = Frame(self.window)
        self.deleteframe = Frame(self.window)
        self.doctor_var = StringVar(self.main)
        self.doctor_var.set(self.appointment_manager.get_doctor_names()[0])
        self.time_var = StringVar(self.main)
        self.time_var.set(self.appointment_manager.get_doctor_by_name(self.doctor_var.get()).available_slots[0])
        self.img = Image.open("hospital pic.jpg") 
        preferred_width = 300
        preferred_height = 435

        self.img = self.img.resize((preferred_width, preferred_height), Image.ANTIALIAS) 
        self.img = ImageTk.PhotoImage(self.img)
        self.image_label = Label(self.main, image=self.img)
        self.image_label.place(x=400, y=10)  

    def startpage(self):
        self.heading = Label(self.main, text="Hospital Management System", font=('Centaur 20 bold'), fg='black',
                             bg="#B22222", relief=SUNKEN)
        self.heading.place(x=60, y=20)
        self.name = Label(self.main, text="Patients Name", font=('arial 12 bold'), bg="#C0C0C0")
        self.name.place(x=0, y=110)
        self.name_ent = Entry(self.main, width=30)
        self.name_ent.place(x=140, y=110)
        self.age = Label(self.main, text="Age", font=('arial 12 bold'), bg="#C0C0C0")
        self.age.place(x=0, y=155)
        Label(self.main, text="Gender", font=('arial 12 bold'), bg="#C0C0C0").place(x=0, y=210)
        a = Radiobutton(self.main, text="Male", padx=20, font="ariel 10 bold", variable=self.v, value=1,
                        bg="#C0C0C0").place(x=130, y=210)
        b = Radiobutton(self.main, text="Female", padx=20, font="ariel 10 bold", variable=self.v, value=2,
                        bg="#C0C0C0").place(x=220, y=210)

        self.location = Label(self.main, text="Choose Doctor", font=('arial 12 bold'), bg="#C0C0C0")
        self.location.place(x=0, y=255)

        doctors = self.appointment_manager.get_doctor_names()
        self.doctor_menu = OptionMenu(self.main, self.doctor_var, *doctors, command=self.update_time_options)
        self.doctor_menu.place(x=140, y=255)

        Label(self.main, text="Select Time", font=('arial 12 bold'), bg="#C0C0C0").place(x=0, y=300)
        times = self.appointment_manager.get_doctor_by_name(self.doctor_var.get()).available_slots
        self.time_menu = OptionMenu(self.main, self.time_var, *times)
        self.time_menu.place(x=140, y=300)
        self.phone = Label(self.main, text="Contact Number", font=('arial 12 bold'), bg="#C0C0C0")
        self.phone.place(x=0, y=345)
        self.age_ent = Entry(self.main, width=30)
        self.age_ent.place(x=140, y=160)
        self.phone_ent = Entry(self.main, width=30)
        self.phone_ent.place(x=140, y=345)
        self.submit = Button(self.main, text="Add Appointment", font="aried 12 bold", width=15, height=2,
                             bg='#347C2C', command=self.add_appointment)
        self.submit.place(x=150, y=380)
        self.final_id = 0
        if ids:
            self.final_id = max(ids)
        self.main.pack()

    def update_time_options(self, *args):
        selected_doctor = self.appointment_manager.get_doctor_by_name(self.doctor_var.get())
        self.time_menu['menu'].delete(0, 'end') 
        for time_slot in selected_doctor.available_slots:
            self.time_menu['menu'].add_command(label=time_slot, command=lambda slot=time_slot: self.time_var.set(slot))
        self.time_var.set(selected_doctor.available_slots[0])

    def add_appointment(self):
        self.val1 = self.name_ent.get()
        self.val2 = self.age_ent.get()
        if self.v.get() == 1:
            self.val3 = "Male"
        elif self.v.get() == 2:
            self.val3 = "Female"
        else:
            self.val3 = "Not Specified"
        self.val4 = self.time_var.get()
        self.val5 = self.doctor_var.get()
        self.val6 = self.phone_ent.get()

        if self.val1 == '' or self.val2 == '' or self.val3 == '' or self.val4 == '' or self.val5 == '' or self.val6 == '':
            tkinter.messagebox.showinfo("Warning", "Please Fill Up All Boxes")
        else:
            sql = "INSERT INTO 'appointments' ( name, age, gender, time, location, phone) VALUES(?, ?, ?, ?, ?, ? )"
            c.execute(sql, (self.val1, self.val2, self.val3, self.val4, self.val5, self.val6))
            conn.commit()
            tkinter.messagebox.showinfo("Success", "\n Appointment for " + str(self.val1) + " has been added")
            self.main.destroy()
            self.__init__(self.window)
            self.startpage()

    def homee(self):
        self.main.destroy()
        self.showdetailsframe.destroy()
        self.updateframe.destroy()
        self.deleteframe.destroy()
        self.__init__(self.window)
        self.startpage()
        self.main.pack()

    def showdetails(self):
        self.main.destroy()
        self.showdetailsframe.destroy()
        self.updateframe.destroy()
        self.deleteframe.destroy()
        self.__init__(self.window)
        self.create_showdetails_frame()
        self.showdetailsframe.pack()

    def create_showdetails_frame(self):
        count1 = 0
        count2 = 0
        clmnname = ['App No.', 'Name', 'Age', 'Gender', 'Doctor', 'Time', 'Contact']
        
        for i in range(len(clmnname)):
            Label(self.showdetailsframe, text=clmnname[i], font="ariel 12 bold").grid(row=0, column=i * 2)
            Separator(self.showdetailsframe, orient=VERTICAL).grid(row=0, column=i * 2 + 1, sticky='ns')

        for i in range(len(self.alldata)):
            displayed_appointment_number = count1 + 1

            if self.alldata[i][0] != displayed_appointment_number:
                c.execute("UPDATE appointments SET id=? WHERE id=?", (displayed_appointment_number, self.alldata[i][0]))
                conn.commit()

            Label(self.showdetailsframe, text=displayed_appointment_number, font="ariel 10").grid(row=count1 + 2, column=0)
            Separator(self.showdetailsframe, orient=VERTICAL).grid(row=count1 + 2, column=1, sticky='ns')

            for j in range(1, 7):
                if j == 1:
                    Label(self.showdetailsframe, text=self.alldata[i][j], font="ariel 10").grid(row=count1 + 2, column=2)
                elif j == 2:
                    Label(self.showdetailsframe, text=self.alldata[i][j], font="ariel 10").grid(row=count1 + 2, column=4)
                elif j == 3:
                    Label(self.showdetailsframe, text=self.alldata[i][j], font="ariel 10").grid(row=count1 + 2, column=6)
                elif j == 4:
                    Label(self.showdetailsframe, text=self.alldata[i][j], font="ariel 10").grid(row=count1 + 2, column=8)
                elif j == 6:
                    Label(self.showdetailsframe, text=self.alldata[i][j], font="ariel 10").grid(row=count1 + 2, column=10)
                elif j == 5:
                    Label(self.showdetailsframe, text=self.alldata[i][j], font="ariel 10").grid(row=count1 + 2, column=12)

                Separator(self.showdetailsframe, orient=VERTICAL).grid(row=count1 + 2, column=count2 * 2 + 1, sticky='ns')
                count2 += 1

            count2 = 0
            count1 += 1

    def updatee(self):
        self.main.destroy()
        self.showdetailsframe.destroy()
        self.updateframe.destroy()
        self.deleteframe.destroy()
        self.__init__(self.window)
        self.id = Label(self.updateframe, text="Enter Patient's Name To Update", font=('arial 12 bold'), fg="red")
        self.id.place(x=0, y=12)
        self.idnet = Entry(self.updateframe, width=20)
        self.idnet.place(x=320, y=18)
        self.search = Button(self.updateframe, text="Search", font="aried 12 bold", width=10, height=1, bg='#347C2C',
                            command=self.update1)
        self.search.place(x=160, y=50)
        self.updateframe.pack(fill='both', expand=True)

    def update1(self):
        self.input = self.idnet.get()
        sql = "SELECT * FROM appointments WHERE name LIKE ?"
        self.res = c.execute(sql, (self.input,))
        for self.row in self.res:
            self.name1 = self.row[1]
            self.age = self.row[2]
            self.gender = self.row[3]
            self.location = self.row[4]
            self.time = self.row[5]
            self.phone = self.row[6]

        self.uname = Label(self.updateframe, text="Patient's Name", font=('arial 14 bold'))
        self.uname.place(x=0, y=140)

        self.uage = Label(self.updateframe, text="Age", font=('arial 14 bold'))
        self.uage.place(x=0, y=180)

        self.ugender = Label(self.updateframe, text="Gender", font=('arial 14 bold'))
        self.ugender.place(x=0, y=220)

        self.utime = Label(self.updateframe, text="Time", font=('arial 14 bold'))
        self.utime.place(x=0, y=260)

        self.ulocation = Label(self.updateframe, text="Location", font=('arial 14 bold'))
        self.ulocation.place(x=0, y=300)

        self.uphone = Label(self.updateframe, text="Phone Number", font=('arial 14 bold'))
        self.uphone.place(x=0, y=340)

        self.ent1 = Entry(self.updateframe, width=30)
        self.ent1.place(x=180, y=140)
        self.ent1.insert(END, str(self.name1))

        self.ent2 = Entry(self.updateframe, width=30)
        self.ent2.place(x=180, y=180)
        self.ent2.insert(END, str(self.age))

        self.ent3 = Entry(self.updateframe, width=30)
        self.ent3.place(x=180, y=220)
        self.ent3.insert(END, str(self.gender))

        self.ent4 = Entry(self.updateframe, width=30)
        self.ent4.place(x=180, y=260)
        self.ent4.insert(END, str(self.time))

        self.ent5 = Entry(self.updateframe, width=30)
        self.ent5.place(x=180, y=300)
        self.ent5.insert(END, str(self.location))

        self.ent6 = Entry(self.updateframe, width=30)
        self.ent6.place(x=180, y=340)
        self.ent6.insert(END, str(self.phone))

        self.update = Button(self.updateframe, text="Update", font="aried 12 bold", width=10, height=1,
                            bg='#347C2C', command=self.update2)
        self.update.place(x=25, y=380)
        self.updateframe.pack()

    def update2(self):
        self.var1 = self.ent1.get()
        self.var2 = self.ent2.get()
        self.var3 = self.ent3.get()
        self.var4 = self.ent4.get()
        self.var5 = self.ent5.get()
        self.var6 = self.ent6.get()

        query = "UPDATE appointments SET name=?, age=?, gender=?, location=?, time=?, phone=? WHERE name LIKE ?"
        c.execute(query, (self.var1, self.var2, self.var3, self.var4, self.var5, self.var6, self.input))
        conn.commit()
        tkinter.messagebox.showinfo("Updated", "Successfully Updated.")
        self.updateframe.destroy()
        self.__init__(self.window)
        self.updatee()
        self.updateframe.pack()

    def deletee(self):
        self.main.destroy()
        self.showdetailsframe.destroy()
        self.updateframe.destroy()
        self.deleteframe.destroy()
        self.__init__(self.window)
        self.id = Label(self.deleteframe, text="Enter Patient's Name To Delete", font=('arial 12 bold'), fg="red")
        self.id.place(x=0, y=12)
        self.idnet = Entry(self.deleteframe, width=20)
        self.idnet.place(x=320, y=18)
        self.search = Button(self.deleteframe, text="Search", font="aried 12 bold", width=10, height=1,
                            bg='#347C2C', command=self.delete1)
        self.search.place(x=160, y=50)
        self.deleteframe.pack(fill='both', expand=True)

    def delete1(self):
        self.input = self.idnet.get()
        sql = "SELECT * FROM appointments WHERE name LIKE ?"
        self.res = c.execute(sql, (self.input,))
        for self.row in self.res:
            self.name1 = self.row[1]
            self.age = self.row[2]
            self.gender = self.row[3]
            self            .location = self.row[4]
            self.time = self.row[5]
            self.phone = self.row[6]

        self.uname = Label(self.deleteframe, text="Patient's Name", font=('arial 14 bold'))
        self.uname.place(x=0, y=140)

        self.uage = Label(self.deleteframe, text="Age", font=('arial 14 bold'))
        self.uage.place(x=0, y=180)

        self.ugender = Label(self.deleteframe, text="Gender", font=('arial 14 bold'))
        self.ugender.place(x=0, y=220)

        self.utime = Label(self.deleteframe, text="Time", font=('arial 14 bold'))
        self.utime.place(x=0, y=260)

        self.ulocation = Label(self.deleteframe, text="Location", font=('arial 14 bold'))
        self.ulocation.place(x=0, y=300)

        self.uphone = Label(self.deleteframe, text="Phone Number", font=('arial 14 bold'))
        self.uphone.place(x=0, y=340)

        self.ent1 = Entry(self.deleteframe, width=30)
        self.ent1.place(x=180, y=140)
        self.ent1.insert(END, str(self.name1))

        self.ent2 = Entry(self.deleteframe, width=30)
        self.ent2.place(x=180, y=180)
        self.ent2.insert(END, str(self.age))

        self.ent3 = Entry(self.deleteframe, width=30)
        self.ent3.place(x=180, y=220)
        self.ent3.insert(END, str(self.gender))

        self.ent4 = Entry(self.deleteframe, width=30)
        self.ent4.place(x=180, y=260)
        self.ent4.insert(END, str(self.time))

        self.ent5 = Entry(self.deleteframe, width=30)
        self.ent5.place(x=180, y=300)
        self.ent5.insert(END, str(self.location))

        self.ent6 = Entry(self.deleteframe, width=30)
        self.ent6.place(x=180, y=340)
        self.ent6.insert(END, str(self.phone))

        self.delete_button = Button(self.deleteframe, text="Delete", font="aried 12 bold", width=10, height=1,
                                    bg='#347C2C', command=self.delete2)
        self.delete_button.place(x=25, y=380)
        self.deleteframe.pack()

    def delete2(self):
        sql2 = "DELETE FROM appointments WHERE name LIKE ?"
        c.execute(sql2, (self.idnet.get(),))
        conn.commit()
        tkinter.messagebox.showinfo("Success", "Deleted Successfully")
        self.ent1.destroy()
        self.ent2.destroy()
        self.ent3.destroy()
        self.ent4.destroy()
        self.ent5.destroy()
        self.ent6.destroy()
        self.deleteframe.destroy()
        self.__init__(self.window)
        self.deletee()
        self.deleteframe.pack()


def on_hover(event):
    event.widget.event_generate('<<MenuSelect>>')


def menubar():
    main_menu = Menu()
    window.config(menu=main_menu)

    home_menu = Menu(main_menu, tearoff=False)
    show_details_menu = Menu(main_menu, tearoff=False)
    update_menu = Menu(main_menu, tearoff=False)
    delete_menu = Menu(main_menu, tearoff=False)
    exit_menu = Menu(main_menu, tearoff=False)

    main_menu.add_cascade(label="Home", menu=home_menu)
    main_menu.add_cascade(label="Show Details", menu=show_details_menu)
    main_menu.add_cascade(label="Update", menu=update_menu)
    main_menu.add_cascade(label="Delete", menu=delete_menu)
    main_menu.add_cascade(label="Exit", menu=exit_menu)

    home_menu.add_command(label="Go to Home", command=b.homee)
    show_details_menu.add_command(label="Show Details", command=b.showdetails)
    update_menu.add_command(label="Update Data", command=b.updatee)
    delete_menu.add_command(label="Delete Data", command=b.deletee)
    exit_menu.add_command(label="Exit", command=window.quit)

    main_menu.configure(
        bg="#FF0000",
        activebackground="#347C2C",
        activeforeground="black"
    )

    font_style = font.Font(weight="bold")

    for menu_item in (home_menu, show_details_menu, update_menu, delete_menu, exit_menu):
        menu_item.configure(font=font_style)

    for menu_item in (home_menu, show_details_menu, update_menu, delete_menu, exit_menu):
        menu_item.bind("<Enter>", on_hover)


window = Tk()
b = Application(window)
b.startpage()
window.config(menu=menubar())
window.title("Hospital Management")
window.geometry("700x460")
window.resizable(False, False)
window.mainloop() 


                                        
    