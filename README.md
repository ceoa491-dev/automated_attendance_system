# automated_attendance_system

## 📖 Overview

The Automated Attendance System is a desktop application developed to automate student attendance management and reduce manual work in educational institutions. The system allows teachers to manage students, generate digital ID cards, track attendance, and automatically notify teachers and parents through email.

---

## 🏫 School & Teacher Management

The system allows administrators to create and manage schools and teacher accounts. Teachers can be assigned to specific classes and can manage student attendance efficiently.

### Features

* Create and manage school information.
* Add and manage teacher accounts.
* Assign teachers to specific classes.

### Screenshot

![School & Teacher Management](images/school_teacher_management.png)

---

## 👨‍🎓 Student Registration

Teachers can register student information including personal and academic details. All records are stored securely in the database.

### Features

* Register student details.
* Store student name, class, email, and parent information.
* Secure data storage using MySQL.

### Screenshot

![Student Registration](images/student_registration.png)

---

## 🆔 Digital ID Card Generation

Teachers can generate digital student ID cards directly from the application. The generated ID cards are automatically delivered to students through Gmail.

### Features

* Automatic ID card generation.
* Email delivery to student Gmail accounts.
* Digital student identification.

### Screenshot

![ID Card Generation](images/id_card_generation.png)

---

## 📷 ID Card Scanning

Students can scan their ID cards using a webcam. The system retrieves and displays student information instantly.

### Features

* Webcam-based scanning using OpenCV.
* Displays student information.
* Fast student verification.

### Information Displayed

* Student Name
* Class
* Email Address

### Screenshot

![ID Card Scanning](images/id_card_scanning.png)

---

## ✅ Automated Attendance Tracking

Attendance is marked automatically when students scan their ID cards.

### Features

* Automatic attendance recording.
* Present status assigned after successful scan.
* Students without a scan are marked absent.

### Screenshot

![Attendance Tracking](images/attendance_tracking.png)

---

## 📧 Email Notification System

The system automatically communicates attendance information to teachers and parents.

### Features

* Daily attendance reports sent to teachers.
* Absence alerts sent to parents.
* Automated email notifications.

### Screenshot

![Email Notifications](images/email_notifications.png)

---

## 📊 Attendance Reports

Teachers can generate attendance reports for specific classes and dates.

### Features

* View attendance records by class and date.
* Display present and absent students.
* Calculate attendance percentage.
* Share reports via email.

### Screenshot

![Attendance Report](images/attendance_report.png)

---

## ⚙️ Technologies Used

| Technology    | Purpose                      |
| ------------- | ---------------------------- |
| Python        | Core Application Development |
| CustomTkinter | Modern GUI Design            |
| Tkinter       | GUI Components               |
| MySQL         | Database Management          |
| OpenCV        | ID Card Scanning             |
| SMTP          | Email Notifications          |

---

## 🔄 System Workflow

1. Teacher registers students.
2. Digital ID cards are generated.
3. ID cards are sent to student email accounts.
4. Students scan their ID cards.
5. Attendance is marked automatically.
6. Reports are generated.
7. Teachers and parents receive email notifications.

---

## 🚀 Future Enhancements

* Face Recognition Attendance
* QR Code Based Attendance
* Cloud Database Integration
* Mobile Application Support
* Real-Time Analytics Dashboard

---

## 👨‍💻 Author

**Dinesh**

Computer Science Student | Python Developer | Software Development Enthusiast

GitHub: https://github.com/ceoa491-dev
