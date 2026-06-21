import ast

import time
import calendar
from calendar import day_name

import customtkinter as ctk
import mysql.connector
from mysql.connector import Error
from tkinter import filedialog
import qrcode
import re
from PIL import Image, ImageTk
from datetime import datetime, timedelta
import os
import cv2
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
import threading
from PIL import ImageGrab
import smtplib
from pyzbar.pyzbar import decode
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email import encoders

uploaded_image_path = None
face_id_path=None
voice_id_path=None
login_email=None
standard_section=None
teacher_name=None

# -------------------- MySQL: Create tables --------------------
try:
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="auto_attand"
    )
    if connection.is_connected():
        cursor = connection.cursor()

        create_table_query = """
        CREATE TABLE IF NOT EXISTS school_details (
            id INT AUTO_INCREMENT PRIMARY KEY,
            school_name VARCHAR(255),
            principal_name VARCHAR(255),
            principal_email VARCHAR(255),
            principal_phone VARCHAR(250),
            school_address VARCHAR(500)
        )
        """

        create_table_query_class = """
        CREATE TABLE IF NOT EXISTS class_details (
            id INT AUTO_INCREMENT PRIMARY KEY,
            teacher_name VARCHAR(255),
            standard_section VARCHAR(255),
            teacher_email VARCHAR(255),
            teacher_phone VARCHAR(250),
            principal_email VARCHAR(255),
            principal_phone VARCHAR(255),
            school_name VARCHAR(255)
        )
        """
        cursor.execute(create_table_query)
        cursor.execute(create_table_query_class)
        print("Tables created successfully or already exist.")

except Error as e:
    print("Error while connecting to MySQL", e)
finally:
    if connection.is_connected():
        cursor.close()
        connection.close()

ctk.set_appearance_mode("Light")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.title("Automated Attendance System")

screen_width = app.winfo_screenwidth()
screen_height = app.winfo_screenheight()
app.geometry(f"{screen_width}x{screen_height}+0+0")

main_frame = ctk.CTkFrame(app, fg_color="transparent")
main_frame.pack(fill="both", expand=True)

bg_image22 = ctk.CTkImage(
    light_image=Image.open(r"C:\Users\DINESH\PycharmProjects\PythonProjectAttendance\images\register2.png"),
    dark_image=Image.open(r"C:\Users\DINESH\PycharmProjects\PythonProjectAttendance\images\register2.png"),
    size=(screen_width, screen_height)
)

bg_label = ctk.CTkLabel(main_frame, image=bg_image22, text="")
bg_label.place(x=0, y=0, relwidth=1, relheight=1)

register_frame = bg_label  # all widgets will now be placed on top of background

# Entries -------------------------------School-------------------------------
entry_school = ctk.CTkEntry(register_frame, placeholder_text="School Name", height=40, width=450)
entry_school.place(relx=0.08, rely=0.24, anchor="nw")

entry_school_pr = ctk.CTkEntry(register_frame, placeholder_text="Principal Name", height=40, width=450)
entry_school_pr.place(relx=0.08, rely=0.32, anchor="nw")

entry_school_pr_e = ctk.CTkEntry(register_frame, placeholder_text="Email", height=40, width=450)
entry_school_pr_e.place(relx=0.08, rely=0.40, anchor="nw")

entry_school_pr_num = ctk.CTkEntry(register_frame, placeholder_text="Password", height=40, width=450)
entry_school_pr_num.place(relx=0.08, rely=0.48, anchor="nw")

entry_school_pr_ad = ctk.CTkEntry(register_frame, placeholder_text="Address", height=40, width=450)
entry_school_pr_ad.place(relx=0.08, rely=0.56, anchor="nw")

# Entries ---------------------------class------------------------------------------
entry_CT = ctk.CTkEntry(register_frame, placeholder_text="Class Teacher Name", height=40, width=450)
entry_CT.place(relx=0.76, rely=0.25, anchor="n")

entry_ST_S = ctk.CTkEntry(register_frame, placeholder_text="Standard & Section : ex(12A)", height=40, width=450)
entry_ST_S.place(relx=0.76, rely=0.33, anchor="n")

entry_class_e = ctk.CTkEntry(register_frame, placeholder_text="Email", height=40, width=450)
entry_class_e.place(relx=0.76, rely=0.41, anchor="n")

entry_class_num = ctk.CTkEntry(register_frame, placeholder_text="Password", height=40, width=450)
entry_class_num.place(relx=0.76, rely=0.49, anchor="n")
#------------------------------------------Submit function----------------------------------
def submit_data():
    school_name = entry_school.get()
    principal_name = entry_school_pr.get()
    principal_email = entry_school_pr_e.get()
    principal_phone = entry_school_pr_num.get()
    school_address = entry_school_pr_ad.get()

    teacher_name = entry_CT.get()
    standard_section = entry_ST_S.get()
    teacher_email = entry_class_e.get()
    teacher_phone = entry_class_num.get()

    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="auto_attand"
        )
        if connection.is_connected():
            cursor = connection.cursor()

            # ---------------- Insert School Details ----------------
            sql_school = """INSERT INTO school_details
                            (school_name, principal_name, principal_email, principal_phone, school_address)
                            VALUES (%s, %s, %s, %s, %s)"""
            values_school = (school_name, principal_name, principal_email, principal_phone, school_address)
            cursor.execute(sql_school, values_school)

            # ---------------- Insert Class Details ----------------
            sql_class = """INSERT INTO class_details
                            (teacher_name, standard_section, teacher_email, teacher_phone, principal_email, principal_phone, school_name)
                            VALUES (%s, %s, %s, %s, %s, %s, %s)"""
            values_class = (teacher_name, standard_section, teacher_email, teacher_phone, principal_email, principal_phone, school_name)
            cursor.execute(sql_class, values_class)


            connection.commit()
            print("School and Class details inserted successfully!")

    except Error as e:
        print("Error while connecting to MySQL:", e)
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()


submit_btn = ctk.CTkButton(register_frame, text="Save", command=submit_data,
                           height=50, width=150, font=("Arial", 20),fg_color="#3300cc",bg_color="black")
submit_btn.place(relx=0.88, rely=0.82, anchor="nw")

# ---------------------------------------Create ID Page -----------------------------------------------
# ---------------- Frames ----------------
createid_frame = ctk.CTkFrame(main_frame)
vircard = ctk.CTkFrame(main_frame)

# ---------------- Labels & Boxes ----------------
label_createid = ctk.CTkLabel(
    createid_frame,
    text="Card Generate",
    font=("Arial", 30, "bold"),
    text_color="black"
)
label_createid.pack(pady=10, anchor="w")

box_id = ctk.CTkFrame(createid_frame, width=500, height=750, corner_radius=20,
                   border_width=3, border_color="black", fg_color="transparent")
box_id.place(x=15, y=50)

box_id_p = ctk.CTkFrame(createid_frame, width=200, height=200, corner_radius=0,
                   border_width=3, border_color="black", fg_color="transparent")
box_id_p.place(x=134, y=70)


# ---------------- Virtual Card Function ----------------
def go_blank_page(student_name, email, dob, ss, uploaded_image_path=None,
                  t_name_param=None, std_section_param=None, teacher_email_param=None):
    createid_frame.pack_forget()
    vircard.pack(fill="both", expand=True)
    bg_image_vid = ctk.CTkImage(
        light_image=Image.open(r"C:\Users\DINESH\PycharmProjects\PythonProjectAttendance\images\createdid_com.png"),
        dark_image=Image.open(r"C:\Users\DINESH\PycharmProjects\PythonProjectAttendance\images\createdid_com.png"),
        size=(screen_width, screen_height)
    )

    blank_page_v = ctk.CTkLabel(vircard, image=bg_image_vid, text="")
    blank_page_v.place(x=0, y=0, relwidth=1, relheight=1)

    # ---------- Use logged teacher globals ----------
    global login_email, standard_section, teacher_name
    teacher_email = login_email
    std_section = standard_section
    t_name = teacher_name

    if not (t_name and std_section and teacher_email):
        print("❌ No logged teacher info found! Please login first.")
        return

    # ---------- Prepare Table ----------
    table_name = f"{t_name}_{teacher_email}_{std_section}".replace(" ", "_").replace("@", "_").replace(".", "_")
    filename_raw = f"{student_name}{email}{dob}{ss}"
    filename_clean = re.sub(r'[ /,\\-]', '', filename_raw)
    qr_img_path_local = f"C:/Users/DINESH/PycharmProjects/PythonProjectAttendance/images/{filename_clean}.png"

    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="auto_attand"
        )
        cursor = connection.cursor()
        create_table_query = f"""
           CREATE TABLE IF NOT EXISTS `{table_name}` (
               id INT AUTO_INCREMENT PRIMARY KEY,
               student_name VARCHAR(255),
               email VARCHAR(255),
               dob DATE,
               ss VARCHAR(50),
               user_img_path VARCHAR(500),
               qr_img_path VARCHAR(500),
               teacher_name VARCHAR(255),
               standard_section VARCHAR(50),
               teacher_email VARCHAR(255)
           )
        """
        cursor.execute(create_table_query)
        connection.commit()

        user_img_path = uploaded_image_path if uploaded_image_path else None
        insert_query = f"""
            INSERT INTO `{table_name}` (
                student_name, email, dob, ss,
                user_img_path, qr_img_path,
                teacher_name, standard_section, teacher_email
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        cursor.execute(insert_query, (
            student_name, email, dob, ss,
            user_img_path, qr_img_path_local,
            t_name, std_section, teacher_email
        ))
        connection.commit()
        print(f"✅ Inserted {student_name} into table {table_name}")

    except Error as e:
        print(" DB Insert Error:", e)
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

    # ---------- Display Yellow Box ----------
    yellow_box = ctk.CTkFrame(blank_page_v, width=500, height=300, fg_color="yellow",
                              border_width=3, border_color="black")
    yellow_box.place(relx=0.5, rely=0.4, anchor="center")

    # ---------- Display User Image ----------
    if uploaded_image_path and os.path.exists(uploaded_image_path):
        img = Image.open(uploaded_image_path).resize((150, 150))
        ctk_img = ctk.CTkImage(light_image=img, dark_image=img, size=(150, 150))
        user_label = ctk.CTkLabel(yellow_box, image=ctk_img, text="")
        user_label.image = ctk_img
        user_label.place(x=20, y=60)

        name_label = ctk.CTkLabel(yellow_box, text=f"{student_name}", font=("Arial", 18),
                                  text_color="black", justify="left")
        name_label.place(x=20, y=220)

    # ---------- Display QR Code ----------
    if os.path.exists(qr_img_path_local):
        qr_img = Image.open(qr_img_path_local).resize((150, 150))
        qr_ctk_img = ctk.CTkImage(light_image=qr_img, dark_image=qr_img, size=(150, 150))
        qr_label = ctk.CTkLabel(yellow_box, image=qr_ctk_img, text="")
        qr_label.image = qr_ctk_img
        qr_label.place(x=330, y=60)

        # ---------- Take screenshot ----------
        blank_page_v.update()
        x, y = yellow_box.winfo_rootx(), yellow_box.winfo_rooty()
        w, h = x + yellow_box.winfo_width(), y + yellow_box.winfo_height()
        screenshot = ImageGrab.grab(bbox=(x, y, w, h))
        screenshot_path = f"C:/Users/DINESH/PycharmProjects/PythonProjectAttendance/virtual_cards/{student_name}_card.png"
        os.makedirs(os.path.dirname(screenshot_path), exist_ok=True)
        screenshot.save(screenshot_path)

        # ---------- Send Email ----------
        try:
            sender_email = "dineshpdineshp2025@gmail.com"  # <-- replace
            sender_password = "vmqw vzso jtwq pbkg"          # <-- replace
            receiver_email = email

            msg = MIMEMultipart()
            msg['From'] = sender_email
            msg['To'] = receiver_email
            msg['Subject'] = f"Virtual ID Card - {student_name}"

            body = f"Hello {student_name},\n\nHere is your Virtual ID Card."
            msg.attach(MIMEText(body, 'plain'))

            with open(screenshot_path, "rb") as attachment:
                mime_base = MIMEBase("application", "octet-stream")
                mime_base.set_payload(attachment.read())
                encoders.encode_base64(mime_base)
                mime_base.add_header("Content-Disposition",
                                     f"attachment; filename={os.path.basename(screenshot_path)}")
                msg.attach(mime_base)

            server = smtplib.SMTP("smtp.gmail.com", 587)
            server.starttls()
            server.login(sender_email, sender_password)
            server.send_message(msg)
            server.quit()
            print(f" Virtual card sent to {email} successfully!")
            add_member_btn = ctk.CTkButton(
                blank_page_v,
                text="Add Member",
                command=lambda: [
                    vircard.pack_forget(),
                    createid_frame.pack(fill="both", expand=True)
                ],
                height=40,
                width=200,
                fg_color="#9966cc",
                text_color="white",
                hover_color="#cc99ff"
            )
            add_member_btn.place(relx=0.5, rely=0.9, anchor="center")
        except Exception as e:
            print(" Email sending error:", e)


# ---------------- createid() ----------------
def createid():
    dashboard_frame.pack_forget()
    createid_frame.pack(fill="both", expand=True)
    bg_image_create_id_gen = ctk.CTkImage(
        light_image=Image.open(r"C:\Users\DINESH\PycharmProjects\PythonProjectAttendance\images\genid.png"),
        dark_image=Image.open(r"C:\Users\DINESH\PycharmProjects\PythonProjectAttendance\images\genid.png"),
        size=(screen_width, screen_height)
    )
    bg_image_create_id_gen = ctk.CTkLabel(createid_frame, image=bg_image_create_id_gen, text="")
    bg_image_create_id_gen.place(x=0, y=0, relwidth=1, relheight=1)
    def back_to_dashboard():
        createid_frame.pack_forget()
        dashboard_frame.pack(fill="both", expand=True)

    back_btn_create = ctk.CTkButton(
        bg_image_create_id_gen,
        text="< BACK",
        command=back_to_dashboard,
        height=40,
        width=120,
        font=("Arial", 16, "bold"),
        fg_color="black",
        hover_color="gray",
        border_color="black",
        border_width=2,
        text_color="white"
    )
    back_btn_create.place(relx=0.09, rely=0.07, anchor="se")
    # ---------- Entries ----------
    createid_txt = ctk.CTkEntry(bg_image_create_id_gen, placeholder_text="Name", height=40, width=450)
    createid_txt.place(relx=0.33, rely=0.38, anchor="nw")
    createid_e = ctk.CTkEntry(bg_image_create_id_gen, placeholder_text="Parent Email", height=40, width=450)
    createid_e.place(relx=0.33, rely=0.46, anchor="nw")
    createid_dob = ctk.CTkEntry(bg_image_create_id_gen, placeholder_text="DOB", height=40, width=450)
    createid_dob.place(relx=0.33, rely=0.54, anchor="nw")
    createid_ss = ctk.CTkEntry(bg_image_create_id_gen, placeholder_text="Standard & section : ex(12A)", height=40, width=450)
    createid_ss.place(relx=0.33, rely=0.62, anchor="nw")

    # ---------- Save QR Code ----------
    def save_details():
        name = createid_txt.get()
        email = createid_e.get()
        dob = createid_dob.get()
        ss = createid_ss.get()

        filename_raw = f"{name}{email}{dob}{ss}"
        filename_clean = re.sub(r'[ /,\\-]', '', filename_raw)

        qr_data = {name, email, dob, ss}
        qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_H, box_size=10, border=4)
        qr.add_data(qr_data)
        qr.make(fit=True)

        img = qr.make_image(fill_color="black", back_color="white")

        save_dir = filedialog.askdirectory(title="Select Folder to Save QR Code")
        if save_dir:
            full_path = f"{save_dir}/{filename_clean}.png"
            img.save(full_path)
            print(f"QR Code saved at: {full_path}")

    submit_btn = ctk.CTkButton(bg_image_create_id_gen, text="Save Details", command=save_details, height=40, width=200)
    submit_btn.place(relx=0.49, rely=0.72, anchor="nw")

    # ---------- Upload Image ----------
    def upload_image():
        global uploaded_image_path
        file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.gif")])
        if file_path:
            uploaded_image_path = file_path
            img = Image.open(file_path).resize((200, 200))
            ctk_img = ctk.CTkImage(light_image=img, dark_image=img, size=(200, 200))
            img_label = ctk.CTkLabel(bg_image_create_id_gen, image=ctk_img, text="")
            img_label.image = ctk_img
            img_label.place(relx=0.41, rely=0.14)

    upload_btn = ctk.CTkButton(bg_image_create_id_gen, text="Upload Image", command=upload_image, height=40, width=200)
    upload_btn.place(relx=0.33, rely=0.72, anchor="nw")

    # ---------- Generate Virtual Card ----------
    virtual_card = ctk.CTkButton(
        bg_image_create_id_gen,
        text="Submit",
        fg_color="#9966cc",
        font=("Arial",18),
        hover_color="#cc99ff",
        command=lambda: go_blank_page(
            createid_txt.get(),
            createid_e.get(),
            createid_dob.get(),
            createid_ss.get(),
            uploaded_image_path=uploaded_image_path
        ),
        height=40,
        width=200
    )
    virtual_card.place(relx=0.85, rely=0.90)



#--------------------------------------------board-------------------------------------------------
#--------------------------------------------board-------------------------------------------------
#--------------------------------------------board-------------------------------------------------
#--------------------------------------------board-------------------------------------------------
dashboard_frame = ctk.CTkFrame(main_frame)

bg_image = ctk.CTkImage(
    light_image=Image.open(r"C:\Users\DINESH\PycharmProjects\PythonProjectAttendance\images\wall2.png"),
    dark_image=Image.open(r"C:\Users\DINESH\PycharmProjects\PythonProjectAttendance\images\wall2.png"),
    size=(1800, 900)
)
bg_label = ctk.CTkLabel(dashboard_frame, image=bg_image, text="")
bg_label.place(relx=0, rely=0, relwidth=1, relheight=1)
top_bar = ctk.CTkFrame(
    dashboard_frame,
    fg_color="black"
)
top_bar.place(relx=0, rely=0, relwidth=1, relheight=0.1)

label_title = ctk.CTkLabel(top_bar, text="My Top Bar", text_color="white", font=("Arial", 30))
label_title.pack(side="left",padx=20, pady=10)

def show_dashboard(school_name, standard_section, teacher_name):
    login_frame.pack_forget()
    dashboard_frame.pack(fill="both", expand=True)

    # ---------------- Dashboard Background ----------------
    bg_image_dashboard = ctk.CTkImage(
        light_image=Image.open(r"C:\Users\DINESH\PycharmProjects\PythonProjectAttendance\images\dashboard.png"),
        dark_image=Image.open(r"C:\Users\DINESH\PycharmProjects\PythonProjectAttendance\images\dashboard.png"),
        size=(screen_width, screen_height)
    )

    bg_label_dashboard = ctk.CTkLabel(dashboard_frame, image=bg_image_dashboard, text="")
    bg_label_dashboard.place(x=0, y=0, relwidth=1, relheight=1)
    ccdatetime=datetime.now()
    day_nn=ccdatetime.strftime("%A")
    label_day = ctk.CTkLabel(bg_label_dashboard,
                               text=f"{day_nn}",
                               font=("Forte", 40,"bold"),
                               text_color="white",fg_color="black",height=60,bg_color="black")
    label_day.place(relx=0.47, rely=0.81)
    # ---------------- Dashboard Title ----------------
    global label_title
    label_title = ctk.CTkLabel(bg_label_dashboard,
                               text=f"{school_name} - {standard_section}\t|\t{teacher_name}",
                               font=("Impact", 28),
                               text_color="white",fg_color="black",height=80)
    label_title.place(relx=0.0, rely=0.00, relwidth=1)
    label_title.configure(anchor="center")
    bg_image_createid = ctk.CTkImage(
        light_image=Image.open(r"C:\Users\DINESH\PycharmProjects\PythonProjectAttendance\images\idcreate.png"),
        dark_image=Image.open(r"C:\Users\DINESH\PycharmProjects\PythonProjectAttendance\images\idcreate.png"),
        size=(100,100)
    )
    # Dashboard button → go to selectmode
    board_id = ctk.CTkButton(
        dashboard_frame,
        text="CREATE ID",
        image=bg_image_createid,
        command=createid,
        height=200,
        width=270,
        font=("Arial", 20, "bold"),
        fg_color="#90EE90",
        hover_color="#77DD77",
        border_color="#006400",
        border_width=6,
        text_color="black"
    )
    board_id.place(relx=0.12, rely=0.29, anchor="nw")

    def selectmode():
        dashboard_frame.pack_forget()

        mode_frame = ctk.CTkFrame(main_frame, width=1800, height=900, fg_color="white")
        mode_frame.pack(fill="both", expand=True)
        bg_image_id_mode = ctk.CTkImage(
            light_image=Image.open(r"C:\Users\DINESH\PycharmProjects\PythonProjectAttendance\images\selectmode.png"),
            dark_image=Image.open(r"C:\Users\DINESH\PycharmProjects\PythonProjectAttendance\images\selectmode.png"),
            size=(screen_width, screen_height)
        )
        bg_image_id_mode = ctk.CTkLabel(mode_frame, image=bg_image_id_mode, text="")
        bg_image_id_mode.place(x=0, y=0, relwidth=1, relheight=1)

        def back_to_dashboard():
            mode_frame.pack_forget()
            bg_image_id_mode.forget()

            dashboard_frame.pack(fill="both", expand=True)

        back_btn_mode = ctk.CTkButton(
            bg_image_id_mode,
            text="< BACK",
            command=back_to_dashboard,
            height=50,
            width=120,
            font=("Arial", 16, "bold"),
            fg_color="black",
            hover_color="gray",
            border_color="black",
            border_width=2,
            text_color="white"
        )
        back_btn_mode.place(relx=0.01, rely=0.01, anchor="nw")

        # ---------------- ID MODE ----------------
        def id_select():
            mode_frame.pack_forget()

            id_frame = ctk.CTkFrame(main_frame, width=1800, height=900, fg_color="white")
            id_frame.pack(fill="both", expand=True)
            bg_image_id_sle = ctk.CTkImage(
                light_image=Image.open(
                    r"C:\Users\DINESH\PycharmProjects\PythonProjectAttendance\images\idselect.png"),
                dark_image=Image.open(r"C:\Users\DINESH\PycharmProjects\PythonProjectAttendance\images\idselect.png"),
                size=(screen_width, screen_height)
            )
            bg_image_id_mode = ctk.CTkLabel(id_frame, image=bg_image_id_sle, text="")
            bg_image_id_mode.place(x=0, y=0, relwidth=1, relheight=1)

            def back_to_mode():
                id_frame.pack_forget()
                bg_image_id_mode.forget()
                selectmode()

            back_btn_id = ctk.CTkButton(
                id_frame,
                text="< BACK",
                command=back_to_mode,
                height=50,
                width=120,
                font=("Arial", 16, "bold"),
                fg_color="black",
                hover_color="gray",
                border_color="black",
                border_width=2,
                text_color="white"
            )
            back_btn_id.place(relx=0.01, rely=0.01, anchor="nw")

            # Square box for image
            square_box = ctk.CTkFrame(
                id_frame,
                width=250,
                height=250,
                fg_color="white",
                border_color="black",
                border_width=3
            )
            square_box.place(relx=0.5, rely=0.5, anchor="center")
            mail_status_label = ctk.CTkLabel(
                id_frame,
                text="",
                font=("Arial", 16, "bold"),
                text_color="black"
            )
            mail_status_label.place(relx=0.55, rely=0.9, anchor="se")
            # ---------------- Display student image ----------------
            def display_student_image(image_path, usernameing, active_checkk):
                try:
                    img = Image.open(image_path)
                    img = img.resize((250, 250))
                    tk_img = ImageTk.PhotoImage(img)

                    img_label = ctk.CTkLabel(square_box, image=tk_img, text="")
                    img_label.image = tk_img
                    img_label.pack(expand=True)

                    text_label = ctk.CTkLabel(
                        square_box,
                        text=f"{usernameing} - {active_checkk}",
                        font=("Arial", 16, "bold"),
                        text_color="white",
                        fg_color="green",
                        corner_radius=12,
                        padx=12,
                        pady=6
                    )
                    text_label.pack(pady=8)
                except Exception as e:
                    print(" Error loading student image:", e)

            # ---------------- Absent marking ----------------
            def mark_absent_students(all_students_table, daily_table):
                try:
                    connection = mysql.connector.connect(
                        host="localhost",
                        user="root",
                        password="",
                        database="auto_attand"
                    )
                    cursor = connection.cursor(dictionary=True)

                    # Fetch teacher email
                    cursor.execute(f"SELECT teacher_email FROM `{all_students_table}` LIMIT 1")
                    teacher_row = cursor.fetchone()
                    teacher_email = teacher_row["teacher_email"] if teacher_row else None
                    if not teacher_email:
                        print(" No teacher email found!")
                        return
                    mail_status_label.configure(text="⏳ Sending Mails...", text_color="blue")
                    id_frame.update()
                    # Insert absentees into daily_table
                    cursor.execute(f"""
                        INSERT IGNORE INTO `{daily_table}` (student_name, ss, email, teacher_email, Active_C)
                        SELECT a.student_name, a.ss, a.email, a.teacher_email, 'Absent'
                        FROM `{all_students_table}` a
                        LEFT JOIN `{daily_table}` d ON a.email = d.email
                        WHERE d.email IS NULL
                    """)
                    connection.commit()
                    print(f"⏳ Absent students inserted into {daily_table}")

                    # Fetch Present students
                    cursor.execute(f"SELECT student_name, ss, email FROM `{daily_table}` WHERE Active_C='Present'")
                    present_students = cursor.fetchall()

                    # Fetch Absent students
                    cursor.execute(f"SELECT student_name, ss, email FROM `{daily_table}` WHERE Active_C='Absent'")
                    absent_students = cursor.fetchall()

                    # Format email body
                    present_text = "\n".join(
                        [f"{s['student_name']} ({s['ss']}) - {s['email']}" for s in present_students]) or "None"
                    absent_text = "\n".join(
                        [f"{s['student_name']} ({s['ss']}) - {s['email']}" for s in absent_students]) or "None"



                    # ---------------- Send Attendance Report to Teacher ----------------
                    message = MIMEMultipart()
                    message["From"] = "dp0255151@gmail.com"
                    message["To"] = teacher_email
                    message["Subject"] = f"Attendance Report - {daily_table}"

                    body = f"""
             Attendance Report for {daily_table}

            ✅ Present Students:
            {present_text}

            ❌ Absent Students:
            {absent_text}
            """
                    message.attach(MIMEText(body, "plain"))

                    with smtplib.SMTP("smtp.gmail.com", 587) as server:
                        server.starttls()
                        server.login("dp0255151@gmail.com", "ojrc bnpt wzpp klig")  # Your App Password
                        server.sendmail("dp0255151@gmail.com", teacher_email, message.as_string())

                    print("📧 Attendance report sent to teacher!")

                    # ---------------- Send Absence Notification to Parents ----------------
                    for student in absent_students:
                        parent_email = student["email"]
                        student_name = student["student_name"]

                        parent_message = MIMEMultipart()
                        parent_message["From"] = "dp0255151@gmail.com"
                        parent_message["To"] = parent_email
                        parent_message["Subject"] = f"Absence Notification - {daily_table}"

                        parent_body = f"""
Dear Parent,

We would like to inform you that your Son/Daughter, {student_name}, is absent today.

Regards,  
Class Teacher
"""
                        parent_message.attach(MIMEText(parent_body, "plain"))

                        with smtplib.SMTP("smtp.gmail.com", 587) as server:
                            server.starttls()
                            server.login("dp0255151@gmail.com", "ojrc bnpt wzpp klig")  # Your App Password
                            server.sendmail("dp0255151@gmail.com", parent_email, parent_message.as_string())

                        print(f"📧 Absence notification sent to parent of {student_name} ({parent_email})")
                    mail_status_label.configure(text="✅ Mails Sended", text_color="green")
                    id_frame.update()

                except mysql.connector.Error as e:
                    print("❌ DB Error in absent marking:", e)
                except Exception as e:
                    print("❌ Email sending error:", e)
                finally:
                    if connection.is_connected():
                        cursor.close()
                        connection.close()


            # ---------------- QR Scan ----------------
            def scan_qr():
                global table_name2, finalize_percentage_table, all_students_table, daily_table
                cap = cv2.VideoCapture(0)
                scanned_students = {}  # student_key → last scanned time

                while True:
                    ret, frame = cap.read()
                    if not ret:
                        break

                    decoded_objects = decode(frame)
                    for obj in decoded_objects:
                        qr_data = obj.data.decode("utf-8")

                        # Parse QR
                        try:
                            qr_values = ast.literal_eval(qr_data)
                        except:
                            qr_values = qr_data.split(",")

                        name = email = dob = ss = None
                        for val in qr_values:
                            val = val.strip()
                            if "@" in val:
                                email = val
                            elif "/" in val:
                                dob = val
                            elif any(ch.isdigit() for ch in val):
                                ss = val
                            else:
                                name = val

                        student_key = f"{name}_{email}_{ss}"
                        current_time = time.time()

                        # Skip if scanned within 5 seconds
                        if student_key in scanned_students and current_time - scanned_students[student_key] < 5:
                            continue
                        scanned_students[student_key] = current_time

                        try:
                            connection = mysql.connector.connect(
                                host="localhost",
                                user="root",
                                password="",
                                database="auto_attand"
                            )
                            cursor = connection.cursor(dictionary=True)

                            # Fetch teacher info
                            cursor.execute(
                                "SELECT teacher_name, teacher_email, standard_section FROM class_details WHERE standard_section=%s LIMIT 1",
                                (ss,)
                            )
                            result = cursor.fetchone()
                            if result:
                                teacher_name = result["teacher_name"]
                                teacher_email = result["teacher_email"]
                                standard_section = result["standard_section"]
                                table_name2 = f"{teacher_name}_{teacher_email}_{standard_section}".replace(" ",
                                                                                                           "_").replace(
                                    "@", "_").replace(".", "_")
                            else:
                                print("❌ No matching class_details found!")
                                continue

                            # Fetch student from main table
                            cursor.execute(
                                f"SELECT student_name, email, ss, user_img_path FROM `{table_name2}` WHERE student_name=%s AND email=%s AND ss=%s LIMIT 1",
                                (name, email, ss)
                            )
                            student_result = cursor.fetchone()
                            if student_result:
                                # Clear previous image/label
                                for widget in square_box.winfo_children():
                                    widget.destroy()

                                display_student_image(student_result["user_img_path"], name, "Present")
                                square_box.update()

                                # --- all_students table ---
                                all_students_table = f"{table_name2}_all_students"
                                cursor.execute(f"""
                                    CREATE TABLE IF NOT EXISTS `{all_students_table}` (
                                        id INT AUTO_INCREMENT PRIMARY KEY,
                                        student_name VARCHAR(255),
                                        email VARCHAR(255),
                                        ss VARCHAR(50),
                                        teacher_email VARCHAR(255),
                                        standard_section VARCHAR(50),
                                        UNIQUE KEY unique_student (student_name, email, ss)
                                    )
                                """)
                                cursor.execute(f"""
                                    INSERT IGNORE INTO `{all_students_table}` (student_name, email, ss, teacher_email, standard_section)
                                    SELECT student_name, email, ss, %s, %s FROM `{table_name2}`
                                """, (teacher_email, standard_section))
                                connection.commit()

                                # --- daily attendance table ---
                                today = datetime.now()
                                daily_table = f"{today.strftime('%B_%d_%Y')}_{ss}".replace(" ", "_")
                                cursor.execute(f"""
                                    CREATE TABLE IF NOT EXISTS `{daily_table}` (
                                        id INT AUTO_INCREMENT PRIMARY KEY,
                                        student_name VARCHAR(255),
                                        ss VARCHAR(50),
                                        email VARCHAR(255),
                                        teacher_email VARCHAR(255),
                                        Active_C VARCHAR(50),
                                        UNIQUE KEY unique_student (email)
                                    )
                                """)
                                cursor.execute(f"""
                                    INSERT IGNORE INTO `{daily_table}` (student_name, ss, email, teacher_email, Active_C)
                                    VALUES (%s, %s, %s, %s, %s)
                                """, (name, ss, email, teacher_email, "Present"))
                                connection.commit()
                                print(f"✅ Marked {name} Present in {daily_table}")

                                # --- finalize percentage table ---
                                def finalize_percentage_table():
                                    try:
                                        conn2 = mysql.connector.connect(
                                            host="localhost",
                                            user="root",
                                            password="",
                                            database="auto_attand"
                                        )
                                        cur2 = conn2.cursor(dictionary=True)

                                        percentage_table = f"{daily_table}_percentage"
                                        cur2.execute(f"""
                                            CREATE TABLE IF NOT EXISTS `{percentage_table}` (
                                                id INT AUTO_INCREMENT PRIMARY KEY,
                                                student_name VARCHAR(255),
                                                ss VARCHAR(50),
                                                email VARCHAR(255),
                                                teacher_email VARCHAR(255),
                                                Active_C VARCHAR(50),
                                                Percentage FLOAT DEFAULT 100,
                                                UNIQUE KEY unique_student (email)
                                            )
                                        """)

                                        # Copy all rows from daily_table
                                        cur2.execute(f"SELECT * FROM `{daily_table}`")
                                        daily_rows = cur2.fetchall()

                                        # Days in this month
                                        days_in_month = calendar.monthrange(today.year, today.month)[1]
                                        decrement = 100.0 / days_in_month

                                        # 🔎 Reset or carry forward
                                        prev_percentage = {}
                                        if today.day != 1:
                                            from datetime import timedelta
                                            yesterday = today - timedelta(days=1)
                                            prev_table = f"{yesterday.strftime('%B_%d_%Y')}_{ss}_percentage".replace(" ", "_")
                                            try:
                                                cur2.execute(f"SELECT email, Percentage FROM `{prev_table}`")
                                                rows = cur2.fetchall()
                                                if rows:
                                                    for row in rows:
                                                        prev_percentage[row["email"]] = row["Percentage"]
                                                    print(f"📌 Carrying percentages forward from {prev_table}")
                                                else:
                                                    print("⚠️ Yesterday’s table empty, starting at 100%")
                                            except:
                                                print("⚠️ Yesterday’s percentage table not found, starting at 100%")
                                        else:
                                            print("📅 First day of month → all students reset to 100%")

                                        # Insert/update today's percentage table
                                        for row in daily_rows:
                                            email = row["email"]
                                            active_c = row["Active_C"]
                                            percent = 100.0  # default start

                                            if email in prev_percentage:
                                                percent = prev_percentage[email]

                                            # Decrement only if absent
                                            if active_c.strip().lower() != "present":
                                                percent = max(percent - decrement, 0)

                                            cur2.execute(f"""
                                                INSERT INTO `{percentage_table}` (student_name, ss, email, teacher_email, Active_C, Percentage)
                                                VALUES (%s, %s, %s, %s, %s, %s)
                                                ON DUPLICATE KEY UPDATE Active_C=VALUES(Active_C), Percentage=VALUES(Percentage)
                                            """, (row["student_name"], row["ss"], email, row["teacher_email"], active_c,
                                                  percent))

                                        conn2.commit()
                                        print(f"✅ Created/updated {percentage_table} with monthly decreasing percentages")

                                    except Error as e:
                                        print("❌ Percentage update error:", e)
                                    finally:
                                        if conn2.is_connected():
                                            cur2.close()
                                            conn2.close()

                                # Start absent marking after 1 min, then finalize percentage


                            else:
                                print("❌ No matching student found!")

                        except Error as e:
                            print("❌ DB Error:", e)
                        finally:
                            if connection.is_connected():
                                cursor.close()
                                connection.close()

                    cv2.imshow("QR Scanner", frame)
                    if cv2.waitKey(1) & 0xFF == ord('q'):
                        threading.Timer(2, mark_absent_students,
                                        args=(all_students_table, daily_table)).start()
                        threading.Timer(4, finalize_percentage_table).start()
                        break


                cap.release()
                cv2.destroyAllWindows()

            # SCAN button

            scan_btn = ctk.CTkButton(
                id_frame,
                text="SCAN",
                command=scan_qr,
                height=60,
                width=150,
                font=("Arial", 16, "bold"),
                fg_color="#9966cc",
                hover_color="#cc99ff",
                border_color="black",
                border_width=2,
                text_color="white"
            )
            scan_btn.place(relx=0.95, rely=0.95, anchor="se")

        # ID MODE button
        id_btn = ctk.CTkButton(
            mode_frame,
            text="ID MODE",
            command=id_select,
            height=150,
            width=250,
            font=("Arial", 20, "bold"),
            fg_color="#87CEEB",
            hover_color="#4682B4",
            border_color="black",
            border_width=3,
            text_color="black"
        )
        id_btn.place(relx=0.5, rely=0.4, anchor="center")


    bg_image_mark_btn = ctk.CTkImage(
        light_image=Image.open(r"C:\Users\DINESH\PycharmProjects\PythonProjectAttendance\images\marking.png"),
        dark_image=Image.open(r"C:\Users\DINESH\PycharmProjects\PythonProjectAttendance\images\marking.png"),
        size=(100,100)
    )
    board_id = ctk.CTkButton(
        dashboard_frame,
        text="MARK\nATTENDANCE",
        image=bg_image_mark_btn,
        command=selectmode,
        height=200,
        width=200,
        font=("Arial", 20, "bold"),
        fg_color="#FFFF66",
        hover_color="#FFD700",
        border_color="#DAA520",
        border_width=6,
        text_color="black"
    )
    board_id.place(relx=0.32, rely=0.29, anchor="nw")

    def open_view_attendance():
        # Hide dashboard
        dashboard_frame.pack_forget()
        # Create blank page
        view_frame = ctk.CTkFrame(main_frame, width=1800, height=900, fg_color="white")
        view_frame.pack(fill="both", expand=True)
        bg_image_view_atten = ctk.CTkImage(
            light_image=Image.open(r"C:\Users\DINESH\PycharmProjects\PythonProjectAttendance\images\viewatten.png"),
            dark_image=Image.open(r"C:\Users\DINESH\PycharmProjects\PythonProjectAttendance\images\viewatten.png"),
            size=(screen_width, screen_height)
        )
        bg_image_view_atten = ctk.CTkLabel(view_frame, image=bg_image_view_atten, text="")
        bg_image_view_atten.place(x=0, y=0, relwidth=1, relheight=1)
        # -------- Back Button --------
        def go_back():
            view_frame.pack_forget()
            bg_image_view_atten.forget()
            dashboard_frame.pack(fill="both", expand=True)


        back_btn = ctk.CTkButton(
            bg_image_view_atten,
            text="< BACK",
            command=go_back,
            height=50,
            width=120,
            font=("Arial", 16, "bold"),
            fg_color="black",
            hover_color="gray",
            border_color="black",
            border_width=2,
            text_color="white"
        )
        back_btn.place(relx=0.01, rely=0.01, anchor="nw")

        # -------- Input Fields --------
        input_frame = ctk.CTkFrame(bg_image_view_atten, fg_color="white")
        input_frame.place(relx=0.5, rely=0.15, anchor="center")

        month_values = [
            "January", "February", "March", "April", "May", "June",
            "July", "August", "September", "October", "November", "December"
        ]
        month_dropdown = ctk.CTkOptionMenu(input_frame, values=month_values, width=200)
        month_dropdown.set("Select Month")
        month_dropdown.grid(row=0, column=0, padx=5, pady=5)

        date_values = [str(i) for i in range(1, 32)]
        date_dropdown = ctk.CTkOptionMenu(input_frame, values=date_values, width=100)
        date_dropdown.set("Select Date")
        date_dropdown.grid(row=0, column=1, padx=5, pady=5)

        year_entry = ctk.CTkEntry(input_frame, placeholder_text="Year (e.g. 2025)", width=100)
        year_entry.grid(row=0, column=2, padx=5, pady=5)

        ss_entry = ctk.CTkEntry(input_frame, placeholder_text="Class Section (e.g. 10A)", width=150)
        ss_entry.grid(row=0, column=3, padx=5, pady=5)

        # -------- Scrollable Table Frame --------
        table_canvas_width = 1700
        table_canvas_height = 500

        table_outer_frame = ctk.CTkFrame(bg_image_view_atten, fg_color="white", width=table_canvas_width,
                                         height=table_canvas_height)
        table_outer_frame.place(relx=0.5, rely=0.65, anchor="center")

        table_canvas = ctk.CTkCanvas(table_outer_frame, bg="white", width=table_canvas_width,
                                     height=table_canvas_height,
                                     highlightthickness=0)
        table_canvas.pack(side="left", fill="both", expand=True)

        v_scrollbar = ctk.CTkScrollbar(table_outer_frame, orientation="vertical", command=table_canvas.yview)
        v_scrollbar.pack(side="right", fill="y")

        table_canvas.configure(yscrollcommand=v_scrollbar.set)

        table_frame = ctk.CTkFrame(table_canvas, fg_color="white", width=table_canvas_width)
        table_canvas.create_window((0, 0), window=table_frame, anchor="nw")

        def fetch_attendance():
            for widget in table_frame.winfo_children():
                widget.destroy()

            month = month_dropdown.get().strip()
            date = date_dropdown.get().strip()
            year = year_entry.get().strip()
            ss = ss_entry.get().strip()

            if not (month and date and year and ss):
                ctk.CTkLabel(table_frame, text="⚠️ Please enter all fields!", font=("Arial", 16, "bold"),
                             text_color="red").pack()
                return
            date = date.zfill(2)
            table_name = f"{month}_{date}_{year}_{ss}_percentage".replace(" ", "_")

            try:
                connection = mysql.connector.connect(host="localhost", user="root", password="", database="auto_attand")
                cursor = connection.cursor(dictionary=True)
                cursor.execute(f"SELECT * FROM `{table_name}`")
                rows = cursor.fetchall()

                if not rows:
                    ctk.CTkLabel(table_frame, text=f"No attendance records found in {table_name}",
                                 font=("Arial", 16, "bold"), text_color="red").pack()
                    return

                # -------- Stats Calculation --------
                total_students = len(rows)
                total_present = sum(1 for student in rows if student["Active_C"] == "Present")
                total_absent = total_students - total_present

                # -------- Show Stats --------
                stats_frame = ctk.CTkFrame(bg_image_view_atten, fg_color="white")
                stats_frame.place(relx=0.5, rely=0.25, anchor="center")

                ctk.CTkLabel(stats_frame, text=f"Total Students: {total_students}", font=("Arial", 16, "bold"),
                             text_color="black").grid(row=0, column=0, padx=20, pady=10)
                ctk.CTkLabel(stats_frame, text=f"Present: {total_present}", font=("Arial", 16, "bold"),
                             text_color="green").grid(row=0, column=1, padx=20, pady=10)
                ctk.CTkLabel(stats_frame, text=f"Absent: {total_absent}", font=("Arial", 16, "bold"),
                             text_color="red").grid(row=0, column=2, padx=20, pady=10)

                # -------- Table Headers --------
                headers = ["Student Name", "Email", "Class", "Status", "Percentage"]
                col_widths = [400, 400, 200, 150, 150]

                for col, (header, width) in enumerate(zip(headers, col_widths)):
                    ctk.CTkLabel(table_frame, text=header, font=("Arial", 14, "bold"), text_color="white",
                                 fg_color="black", width=width, height=30, corner_radius=6).grid(row=0, column=col,
                                                                                                 padx=5, pady=5,
                                                                                                 sticky="nsew")

                for row_idx, student in enumerate(rows, start=1):
                    ctk.CTkLabel(table_frame, text=student["student_name"], font=("Arial", 13),
                                 width=col_widths[0]).grid(row=row_idx, column=0, padx=5, pady=5, sticky="nsew")
                    ctk.CTkLabel(table_frame, text=student["email"], font=("Arial", 13),
                                 width=col_widths[1]).grid(row=row_idx, column=1, padx=5, pady=5, sticky="nsew")
                    ctk.CTkLabel(table_frame, text=student["ss"], font=("Arial", 13),
                                 width=col_widths[2]).grid(row=row_idx, column=2, padx=5, pady=5, sticky="nsew")

                    status_color = "green" if student["Active_C"] == "Present" else "red"
                    ctk.CTkLabel(table_frame, text=student["Active_C"], font=("Arial", 13, "bold"), text_color="white",
                                 fg_color=status_color, corner_radius=8, width=col_widths[3]).grid(row=row_idx,
                                                                                                   column=3,
                                                                                                   padx=5, pady=5,
                                                                                                   sticky="nsew")

                    ctk.CTkLabel(table_frame, text=f"{student['Percentage']:.2f}%", font=("Arial", 13),
                                 width=col_widths[4]).grid(row=row_idx, column=4, padx=5, pady=5, sticky="nsew")

                table_frame.update_idletasks()
                table_canvas.configure(scrollregion=table_canvas.bbox("all"))

                # -------- Generate PDF --------
                pdf_filename = f"Attendance_{month}_{date}_{year}_{ss}.pdf"
                doc = SimpleDocTemplate(pdf_filename, pagesize=A4)
                elements = []
                styles = getSampleStyleSheet()

                elements.append(Paragraph("Attendance Report", styles['Title']))
                elements.append(Spacer(1, 12))
                elements.append(Paragraph(f"Class: {ss}   Date: {date}-{month}-{year}", styles['Normal']))
                elements.append(
                    Paragraph(f"Total Students: {total_students} | Present: {total_present} | Absent: {total_absent}",
                              styles['Normal']))
                elements.append(Spacer(1, 12))

                data = [["Student Name", "Email", "Class", "Status", "Percentage"]]
                for student in rows:
                    data.append([
                        student["student_name"],
                        student["email"],
                        student["ss"],
                        student["Active_C"],
                        f"{student['Percentage']:.2f}%"
                    ])

                table = Table(data, colWidths=[120, 150, 70, 70, 70])
                table.setStyle(TableStyle([
                    ("BACKGROUND", (0, 0), (-1, 0), colors.black),
                    ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                    ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                    ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                    ("BOTTOMPADDING", (0, 0), (-1, 0), 8),
                    ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
                ]))
                elements.append(table)
                doc.build(elements)

                # -------- Send Report Button --------
                def send_report():
                    sender_email = "dp0255151@gmail.com"
                    sender_pass = "ojrc bnpt wzpp klig"
                    receiver_email = login_email

                    msg = MIMEMultipart()
                    msg['From'] = sender_email
                    msg['To'] = receiver_email
                    msg['Subject'] = f"Attendance Report - {ss} {date}-{month}-{year}"

                    part = MIMEBase("application", "octet-stream")
                    with open(pdf_filename, "rb") as f:
                        part.set_payload(f.read())
                    encoders.encode_base64(part)
                    part.add_header("Content-Disposition", f"attachment; filename={pdf_filename}")
                    msg.attach(part)

                    try:
                        server = smtplib.SMTP("smtp.gmail.com", 587)
                        server.starttls()
                        server.login(sender_email, sender_pass)
                        server.sendmail(sender_email, receiver_email, msg.as_string())
                        server.quit()
                        print("✅ Report sent successfully!")
                    except Exception as e:
                        print("❌ Error sending email:", e)

                send_btn = ctk.CTkButton(view_frame, text="Send Report", command=send_report, fg_color="green",
                                         text_color="white")
                send_btn.place(relx=0.5, rely=0.95, anchor="center")

            except Error as e:
                print("❌ DB Error while fetching attendance:", e)
                ctk.CTkLabel(table_frame, text=f"❌ Error: {e}", font=("Arial", 16, "bold"), text_color="red").pack()
            finally:
                if connection.is_connected():
                    cursor.close()
                    connection.close()

        submit_btn = ctk.CTkButton(input_frame, text="Fetch Attendance", command=fetch_attendance, fg_color="blue",
                                   text_color="white")
        submit_btn.grid(row=0, column=4, padx=10, pady=5)
    bg_image_view = ctk.CTkImage(
        light_image=Image.open(r"C:\Users\DINESH\PycharmProjects\PythonProjectAttendance\images\viewat.png"),
        dark_image=Image.open(r"C:\Users\DINESH\PycharmProjects\PythonProjectAttendance\images\viewat.png"),
        size=(100,100)
    )
    # Dashboard button → VIEW ATTENDANCE
    board_id = ctk.CTkButton(
        dashboard_frame,
        text="VIEW\nATTENDANCE",
        image=bg_image_view,
        height=200,
        width=200,
        font=("Arial", 20, "bold"),
        fg_color="#3399FF",
        hover_color="#1E90FF",
        border_color="#00008B",
        border_width=6,
        text_color="black",
        command=open_view_attendance
    )
    board_id.place(relx=0.52, rely=0.29, anchor="nw")

    def open_student_info():
        # Hide dashboard frame
        dashboard_frame.pack_forget()

        # Create blank page frame
        info_frame = ctk.CTkFrame(main_frame, width=1800, height=900, fg_color="white")
        info_frame.pack(fill="both", expand=True)
        bg_image_stu_in = ctk.CTkImage(
            light_image=Image.open(
                r"C:\Users\DINESH\PycharmProjects\PythonProjectAttendance\images\studentinfo.png"),
            dark_image=Image.open(r"C:\Users\DINESH\PycharmProjects\PythonProjectAttendance\images\studentinfo.png"),
            size=(screen_width, screen_height)
        )
        bg_image_stu_in = ctk.CTkLabel(info_frame, image=bg_image_stu_in, text="")
        bg_image_stu_in.place(x=0, y=0, relwidth=1, relheight=1)

        # ---------------- Back Button ----------------
        def go_back():
            info_frame.destroy()
            bg_image_stu_in.destroy()# remove current frame
            dashboard_frame.pack(fill="both", expand=True)  # show previous dashboard

        back_btn = ctk.CTkButton(
            info_frame,
            text="< BACK",
            command=go_back,
            height=50,
            width=120,
            font=("Arial", 16, "bold"),
            fg_color="black",
            hover_color="gray",
            border_color="black",
            border_width=2,
            text_color="white"
        )
        back_btn.place(relx=0.01, rely=0.01, anchor="nw")

        # Square box to show student image/info
        square_box = ctk.CTkFrame(
            info_frame,
            width=300,
            height=350,
            fg_color="white",
            border_color="black",
            border_width=3
        )
        square_box.place(relx=0.5, rely=0.5, anchor="center")

        # ---------------- Display student info ----------------
        def display_student_info(student):
            try:
                # Clear previous content
                for widget in square_box.winfo_children():
                    widget.destroy()

                # Show Image
                img = Image.open(student["user_img_path"])
                img = img.resize((250, 250))
                tk_img = ImageTk.PhotoImage(img)

                img_label = ctk.CTkLabel(square_box, image=tk_img, text="")
                img_label.image = tk_img
                img_label.pack()

                # Show details below the image
                details_text = f"""
        Name   : {student['student_name']}
        Email  : {student['email']}
        Class  : {student['ss']}
                """
                details_label = ctk.CTkLabel(
                    square_box,
                    text=details_text.strip(),
                    font=("Arial", 14, "bold"),
                    text_color="black",
                    justify="left"
                )
                details_label.pack(pady=8)

            except Exception as e:
                print("❌ Error displaying student info:", e)

        # ---------------- QR Scan Function ----------------
        def scan_qr_once():
            cap = cv2.VideoCapture(0)
            scanned_qr_data = None
            email, ss, name, dob = None, None, None, None

            while True:
                ret, frame = cap.read()
                if not ret:
                    break

                decoded_objects = decode(frame)
                if decoded_objects:
                    obj = decoded_objects[0]
                    qr_data = obj.data.decode("utf-8")
                    scanned_qr_data = qr_data

                    print("📌 Scanned QR Data:", scanned_qr_data)

                    # Parse QR safely
                    try:
                        qr_values = ast.literal_eval(qr_data)
                        if isinstance(qr_values, set):
                            qr_values = list(qr_values)
                        elif isinstance(qr_values, str):
                            qr_values = [qr_values]
                    except:
                        qr_values = qr_data.split(",")

                    # Extract fields using patterns
                    email = next((v for v in qr_values if "@" in v), None)
                    dob = next((v for v in qr_values if "/" in v), None)
                    ss = next((v for v in qr_values if str(standard_section).lower() in str(v).lower()), None)
                    name = next((v for v in qr_values if v not in [email, ss, dob]), None)

                    break  # Stop scanning

                cv2.imshow("QR Scanner", frame)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break

            cap.release()
            cv2.destroyAllWindows()

            # Connect to DB and fetch student
            if email and ss:
                try:
                    connection = mysql.connector.connect(
                        host="localhost",
                        user="root",
                        password="",
                        database="auto_attand"
                    )
                    cursor = connection.cursor(dictionary=True)

                    global teacher_name, login_email, standard_section
                    table_name2 = f"{teacher_name.strip()}_{login_email.strip()}_{standard_section.strip()}"
                    table_name2 = table_name2.replace(" ", "_").replace("@", "_").replace(".", "_").replace(",", "_").lower()

                    print("📌 Using Table:", table_name2)

                    # Print all rows in this table
                    cursor.execute(f"SELECT * FROM `{table_name2}`")
                    all_rows = cursor.fetchall()
                    print("📌 All data in table:", table_name2)
                    for row in all_rows:
                        print(row)

                    # Fetch student by email + class
                    cursor.execute(
                        f"SELECT student_name, email, ss, user_img_path FROM `{table_name2}` WHERE email=%s AND ss=%s LIMIT 1",
                        (email, ss)
                    )
                    student_result = cursor.fetchone()
                    if student_result:
                        display_student_info(student_result)
                    else:
                        print("❌ No matching student found!")

                except Error as e:
                    print("❌ DB Error:", e)
                finally:
                    if connection.is_connected():
                        cursor.close()
                        connection.close()

        # SCAN button
        scan_btn = ctk.CTkButton(
            info_frame,
            text="SCAN QR",
            command=scan_qr_once,
            height=60,
            width=150,
            font=("Arial", 16, "bold"),
            fg_color="#FF6347",
            hover_color="#CD5C5C",
            border_color="black",
            border_width=2,
            text_color="white"
        )
        scan_btn.place(relx=0.5, rely=0.85, anchor="center")
    bg_image_user_btn = ctk.CTkImage(
        light_image=Image.open(r"C:\Users\DINESH\PycharmProjects\PythonProjectAttendance\images\userb.png"),
        dark_image=Image.open(r"C:\Users\DINESH\PycharmProjects\PythonProjectAttendance\images\userb.png"),
        size=(100,100)
    )
    # Dashboard button
    board_id = ctk.CTkButton(
        dashboard_frame,
        text="STUDENT\nINFO",
        image=bg_image_user_btn,
        height=200,
        width=270,
        font=("Arial", 20, "bold"),
        fg_color="#FF69B4",
        hover_color="#FF1493",
        border_color="#C71585",
        border_width=6,
        text_color="black",
        command=open_student_info
    )
    board_id.place(relx=0.72, rely=0.29, anchor="nw")


#-------------------------------------------Login--------------------------------------------------
login_frame = ctk.CTkFrame(main_frame)
label_login = ctk.CTkLabel(login_frame, text="LOGIN PAGE", font=("Arial", 30))
label_login.pack(pady=50)

def open_login_screen():
    register_frame.pack_forget()
    login_frame.pack(fill="both", expand=True)

    bg_image_login = ctk.CTkImage(
        light_image=Image.open(r"C:\Users\DINESH\PycharmProjects\PythonProjectAttendance\images\login.png"),
        dark_image=Image.open(r"C:\Users\DINESH\PycharmProjects\PythonProjectAttendance\images\login.png"),
        size=(screen_width, screen_height)
    )

    bg_label_login = ctk.CTkLabel(login_frame, image=bg_image_login, text="")
    bg_label_login.place(x=0, y=0, relwidth=1, relheight=1)

    # ------------------------ Login Entries ------------------------
    global entry_e_log, entry_p_log
    entry_e_log = ctk.CTkEntry(bg_label_login, placeholder_text="Email", height=50, width=450)
    entry_e_log.place(relx=0.52, rely=0.19, anchor="n")

    entry_p_log = ctk.CTkEntry(bg_label_login, placeholder_text="Password", height=50, width=450)
    entry_p_log.place(relx=0.52, rely=0.29, anchor="n")

    # ------------------------ Login Button ------------------------
    login_btn_log = ctk.CTkButton(bg_label_login, text="Login", command=login_page_check,
                                  height=50, width=150, font=("Arial", 20),fg_color="#3300cc")
    login_btn_log.place(relx=0.57, rely=0.40, anchor="nw")

def login_page_check():
    global login_email, standard_section, teacher_name
    login_check_email = entry_e_log.get()
    login_check_pass = entry_p_log.get()

    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="auto_attand"
        )
        if connection.is_connected():
            cursor = connection.cursor(dictionary=True)

            cursor.execute("""
                SELECT teacher_name, school_name, standard_section, teacher_phone, principal_email
                FROM class_details
                WHERE teacher_email = %s
            """, (login_check_email,))

            class_data = cursor.fetchone()

            if not class_data:
                ctk.CTkLabel(login_frame, text="Email not found!", font=("Arial", 20), text_color="RED").pack(pady=270)
                return

            expected_password = (
                class_data["standard_section"]
                + class_data["teacher_phone"]
                + class_data["principal_email"]
            )

            if login_check_pass == expected_password:
                login_email = login_check_email
                standard_section = class_data["standard_section"]
                teacher_name = class_data["teacher_name"]
                print("Login Email:", login_email)
                print("Standard Section:", standard_section)
                print("Teacher Name:", teacher_name)
                show_dashboard(class_data["school_name"], class_data["standard_section"], class_data["teacher_name"])
            else:
                ctk.CTkLabel(login_frame, text="Incorrect Password!", font=("Arial", 20), text_color="RED").pack(pady=250)

    except Error as e:
        print("Error while connecting to MySQL:", e)
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

login_btn = ctk.CTkButton(register_frame, text="Login", command=open_login_screen,
                          height=50, width=150, font=("Arial", 20), fg_color="#3300cc", bg_color="black")
login_btn.place(relx=0.78, rely=0.82, anchor="nw")

app.mainloop()