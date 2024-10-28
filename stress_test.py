import os
import psutil
import smtplib

Threshold = 80

def send_email_notification(message):
    # Replace with your email settings
    sender_email = "divyasril2003@gmail.com"
    receiver_email = "divyasril2003@gmail.com"
    password = "Divyasrilalam@2003"

    with smtplib.SMTP("smtp.example.com", 587) as server:
        server.starttls()
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message) 

# Stress test functions
def memory_stress_test():
    usage = psutil.virtual_memory().percent
    print(f"Memory Usage: {usage}%")
    if usage > Threshold:
        print("Memory usage threshold exceeded")

def disk_stress_test():
    usage = psutil.disk_usage('/').percent
    print(f"Disk Usage: {usage}%")
    if usage > Threshold:
        print("Disk usage threshold exceeded")

def network_stress_test():
    usage = psutil.net_io_counters().bytes_sent + psutil.net_io_counters().bytes_recv
    print(f"Network Usage: {usage} bytes")
    if usage > Threshold * 1_000_000: 
        print("Network usage threshold exceeded")

def cpu_stress_test():
    usage = psutil.cpu_percent(interval=1)
    print(f"CPU Usage: {usage}%")
    if usage > Threshold:
        print("CPU usage threshold exceeded")

def mysql_stress_test():
    usage = psutil.cpu_percent(interval=1)
    print(f"MySQL Usage: {usage}%")
    if usage > Threshold:
        print("MySQL usage threshold exceeded")

# Main menu
def main():
    while True:
        print("\nSelect an option:")
        print("1. Memory Stress Testing")
        print("2. Disk Stress Testing")
        print("3. Network Stress Testing")
        print("4. CPU Stress Testing")
        print("5. MySQL Stress Testing")
        print("6. Exit")

        choice = input("Enter your choice: ")

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
            break
        else:
            print("Enter valid option")

if __name__ == "__main__":
    main()
