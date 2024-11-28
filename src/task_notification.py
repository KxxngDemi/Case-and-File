import sqlite3
import smtplib
import sys
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime, timedelta
import time


class TaskNotification:
    def __init__(self):
        self.db_path = 'to_do.db'
        self.sender_email = 'caseandfile021@gmail.com'
        self.sender_password = 'ujem eljp gdtb hjba'
        self.recipient_email = 'y3816040@gmail.com'

    def get_tasks_due(self, date):
        """Get tasks from the database with a specific deadline."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute("""
        SELECT Description 
        FROM Tasks 
        WHERE Deadline = ?
        """, (date,))
        tasks = cursor.fetchall()
        conn.close()

        if tasks:  # Check if tasks is not empty
            return [task[0] for task in tasks]
        else:
            return []  # Return an empty list if no tasks are due

    def send_email(self, subject, body):
        """Send an email with the specified subject and body."""
        try:
            # Set up the MIME
            message = MIMEMultipart()
            message["From"] = self.sender_email
            message["To"] = self.recipient_email
            message["Subject"] = subject
            message.attach(MIMEText(body, "plain"))

            # Connect to the SMTP server
            server = smtplib.SMTP("smtp.gmail.com", 587)
            server.starttls()
            server.login(self.sender_email, self.sender_password)

            # Send the email
            server.sendmail(self.sender_email, self.recipient_email, message.as_string())
            print("Email sent successfully!")
        except Exception as e:
            print(f"An error occurred while sending the email: {e}")
        finally:
            server.quit()

    def task_email_scheduler(self):
        """Check for tasks due today and send an email."""
        today = datetime.now().date()  # Get today's date
        tasks_due_today = self.get_tasks_due(today)

        if tasks_due_today:
            # Compose email
            task_list = "\n- ".join(tasks_due_today)
            body = (
                 "Good morning,\n\n"
                "The following tasks are due today:\n\n"
                f"- {task_list}\n\n"
                "Please ensure these are completed by the end of the day.\n\n"
                "Best regards,\nYour Task Manager"
            )
            self.send_email("Tasks Due Today", body)
        else:
            print("No tasks are due today.")
        sys.exit()

    def schedule_email(self, time_to_send):
        """Schedule the email to be sent at a specific time daily."""
        schedule.every().day.at(time_to_send).do(self.task_email_scheduler)
        print(f"Task email scheduler is set to run daily at {time_to_send}...")

    def run_scheduler(self):
        """Runs a loop for the scheduler"""
        print("Task email scheduler is running...")
        while True:
            schedule.run_pending()
            time.sleep(30)  # Check every 30 seconds


# Example usage
# if __name__ == "__main__":
#     # Initialize the TaskReminder class
#     reminder = TaskNotification()

#     # Schedule the email to be sent at 8:00 am daily
#     reminder.schedule_email("08:00")

#     # Run the scheduler
#     reminder.run_scheduler()
