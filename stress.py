import os
import psutil
import time
import requests
import multiprocessing

THRESHOLD = 80  

# Stress increase functions
def increase_memory_stress():
    memory_list = []
    process = psutil.Process(os.getpid())
    while process.memory_percent() < THRESHOLD:
        memory_list.append(' ' * 1024 * 1024)  # 1 MB per iteration
        print(f"Memory Usage: {process.memory_percent()}%")  # Print usage during stress
    print("Memory stress test reached target usage.")

def increase_disk_stress():
    with open("stress_test_file", "wb") as f:
        while psutil.disk_usage('/').percent < THRESHOLD:
            f.write(b'0' * 1024 * 1024 * 10)  # Write 10 MB at a time
            print(f"Disk Usage: {psutil.disk_usage('/').percent}%")  
    print("Disk stress test reached target usage.")
    os.remove("stress_test_file")

def increase_network_stress():
    url = "https://www.google.com/"  
    while (psutil.net_io_counters().bytes_recv * 100 / psutil.virtual_memory().total) < THRESHOLD:  # Rough estimate for % usage
        requests.get(url)
        print(f"Network usage estimated: {(psutil.net_io_counters().bytes_recv * 100 / psutil.virtual_memory().total):.2f}%")  
    print("Network stress test reached target usage.")

def increase_cpu_stress():
    def stress():
        while True:
            pass  # Infinite loop to max out CPU

    processes = [multiprocessing.Process(target=stress) for _ in range(multiprocessing.cpu_count())]
    for p in processes:
        p.start()
        print(f"Initial CPU Usage: {psutil.cpu_percent(interval=1)}%")
    time.sleep(5)  # Run for a few seconds to increase CPU usage
    for p in processes:
        print(f"CPU Usage: {psutil.cpu_percent(interval=1)}%")  
        p.terminate()
    print("CPU stress test completed.")

# Monitoring functions
def memory_stress_test():
    usage = psutil.virtual_memory().percent
    print(f"Memory Usage: {usage}%")
    if usage < THRESHOLD:
        print("Increasing memory stress to exceed threshold.")
        increase_memory_stress()
    else:
        print("Memory usage exceeded threshold!")

def disk_stress_test():
    usage = psutil.disk_usage('/').percent
    print(f"Disk Usage: {usage}%")
    if usage < THRESHOLD:
        print("Increasing disk stress to exceed threshold.")
        increase_disk_stress()
    else:
        print("Disk usage exceeded threshold!")

def network_stress_test():
    print("Increasing network stress to attempt to reach threshold.")
    increase_network_stress()

def cpu_stress_test():
    usage = psutil.cpu_percent(interval=1)
    print(f"Initial CPU Usage: {usage}%")
    if usage < THRESHOLD:
        print("Increasing CPU stress to exceed threshold.")
        increase_cpu_stress()
    else:
        print("CPU usage exceeded threshold!")

def mysql_stress_test():
    exporter_url = "http://192.168.0.104:9104/metrics"  
    thresholds = {
        "process_cpu_seconds_total": 1.0  
    }

    try:
        response = requests.get(exporter_url)
        response.raise_for_status()

        metrics = {}
        for line in response.text.splitlines():
            if line.startswith("#"):
                continue
            if "process_cpu_seconds_total" in line:
                try:
                    metrics["process_cpu_seconds_total"] = float(line.split()[-1])
                except ValueError:
                    print(f"Warning: Could not convert value to float: {line}")

        # Check CPU time threshold
        if "process_cpu_seconds_total" in metrics:
            print(f"process_cpu_seconds_total: {metrics['process_cpu_seconds_total']}")
            if metrics["process_cpu_seconds_total"] > thresholds["process_cpu_seconds_total"]:
                print(f"Alert: CPU usage exceeds threshold - {metrics['process_cpu_seconds_total']} seconds (Threshold: {thresholds['process_cpu_seconds_total']} seconds)")
            else:
                print("CPU usage is within limits.")

    except requests.RequestException as e:
        print(f"Failed to retrieve metrics from mysqld_exporter: {e}")

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
            print("Enter a valid option")

if __name__ == "__main__":
    main()