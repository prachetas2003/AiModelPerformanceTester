# hardware_monitor.py
import psutil
import time

def get_system_metrics():
    """
    Returns a dictionary with CPU usage (%), memory usage (%), and a timestamp.
    Useful for logging system state before/after each inference.
    """
    cpu_percent = psutil.cpu_percent(interval=None)  # CPU usage since the last call
    mem_info = psutil.virtual_memory()
    return {
        'cpu_percent': cpu_percent,
        'memory_percent': mem_info.percent,
        'timestamp': time.time()
    }
