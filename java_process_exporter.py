import time
import psutil
from prometheus_client import start_http_server, Gauge

# Prometheus metrics
PROCESS_UPTIME = Gauge('java_process_uptime_seconds', 'Uptime of the Java process in seconds')
PROCESS_CPU = Gauge('java_process_cpu_percent', 'CPU usage of the Java process in percent')
PROCESS_MEMORY = Gauge('java_process_memory_percent', 'Memory usage of the Java process in percent')
PROCESS_STATUS = Gauge('java_process_status', 'Status of the Java process (1 = running, 0 = not running)')

# Configuration for the Java process
PROCESS_IDENTIFIER = "YourJavaApp"  # This can be part of the Java command line (e.g., "MyApp")

def get_java_process_by_name(name):
    """Get the Java process by name (or part of the name)."""
    for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
        if name in ' '.join(proc.info['cmdline']):
            return proc
    return None

def collect_metrics():
    """Collect metrics for the Java process running on the local server."""
    proc = get_java_process_by_name(PROCESS_IDENTIFIER)

    if proc:
        # Get the uptime of the process (time since it started)
        uptime = time.time() - proc.create_time()
        
        # Get CPU and memory usage
        cpu_percent = proc.cpu_percent(interval=1)
        memory_percent = proc.memory_percent()

        # Update Prometheus metrics
        PROCESS_UPTIME.set(uptime)
        PROCESS_CPU.set(cpu_percent)
        PROCESS_MEMORY.set(memory_percent)
        PROCESS_STATUS.set(1)  # Process is running
    else:
        print(f"Java process {PROCESS_IDENTIFIER} not found.")
        PROCESS_STATUS.set(0)  # Process is not running

def parse_uptime_to_seconds(uptime):
    """Convert process uptime (e.g., '1-10:15:30' or '01:02:03') to seconds."""
    try:
        if '-' in uptime:  # Format like "1-10:15:30"
            days, time_str = uptime.split('-')
            hours, minutes, seconds = map(int, time_str.split(":"))
            return int(days) * 86400 + hours * 3600 + minutes * 60 + seconds
        elif ':' in uptime:  # Format like "01:02:03"
            hours, minutes, seconds = map(int, uptime.split(":"))
            return hours * 3600 + minutes * 60 + seconds
        else:
            return int(uptime)  # If uptime is just in seconds
    except Exception as e:
        print(f"Error parsing uptime: {e}")
        return 0  # Return 0 seconds if unable to parse uptime

if __name__ == '__main__':
    # Start Prometheus HTTP server on port 8000
    start_http_server(8000)

    print(f"Monitoring Java process: {PROCESS_IDENTIFIER} locally...")
    while True:
        collect_metrics()
        time.sleep(5)  # Collect metrics every 5 seconds
