import os
import psutil
import smtplib
import time
import sys

THRESHOLD = 80   #set threshold

def send_email_notification(subject, message):
    sender_email = "divyasril2003@gmail.com"
    receiver_email = "divyasril2003@gmail.com"
    password = "fsgl zbaa nwhm octv"

    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(sender_email, password)
            full_message = f"Subject: {subject}\n\n{message}"
            server.sendmail(sender_email, receiver_email, full_message)
            print("Email sent successfully")
    except Exception as e:
        print(f"Failed to send email: {e}")

def memory_stress_test():
    usage = psutil.virtual_memory().percent
    print(f"Memory Usage: {usage}%")
    if usage > THRESHOLD:
        send_email_notification("Memory Usage Alert", "Memory usage exceeded threshold!")

def disk_stress_test():
    usage = psutil.disk_usage('/').percent
    print(f"Disk Usage: {usage}%")
    if usage > THRESHOLD:
        send_email_notification("Disk Usage Alert", "Disk usage exceeded threshold!")

def network_stress_test():
    net_io = psutil.net_io_counters()
    usage = (net_io.bytes_sent + net_io.bytes_recv) / (1024 * 1024)
    print(f"Network Usage: {usage:.2f} MB")
    if usage > THRESHOLD:
        send_email_notification("Network Usage Alert", "Network usage exceeded threshold!")

def cpu_stress_test():
    usage = psutil.cpu_percent(interval=1)
    print(f"CPU Usage: {usage}%")
    if usage > THRESHOLD:
        send_email_notification("CPU Usage Alert", "CPU usage exceeded threshold!")

def mysql_stress_test():
    for proc in psutil.process_iter(['pid', 'name', 'cpu_percent']):
        if 'mysqld' in proc.info['name']:
            mysql_usage = proc.info['cpu_percent']
            print(f"MySQL Usage: {mysql_usage}%")
            if mysql_usage > THRESHOLD:
                send_email_notification("MySQL Usage Alert", "MySQL usage exceeded threshold!")
            return
    print("MySQL service not found.")

def main(choice):
    if choice == '1':
        memory_stress_test()
    elif choice == '2':
        disk_stress_test()
    elif choice == '3':
        network_stress_test()
    elif choice == '4':
        cpu_stress_test()
    elif choice == '5':
        mysql_stress_test()
    elif choice == '6':
        print("Exiting")
    else:
        print("Enter a valid option")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Please provide a choice as a command-line argument.")
    else:
        main(sys.argv[1])
