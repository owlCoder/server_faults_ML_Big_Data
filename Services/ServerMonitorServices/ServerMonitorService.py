import threading
import time
from typing import List
import pandas as pd
from threading import Event
from Presentation.ServerStatusShow.ServerStatusUI import show_servers_status
import gc
from Services.ServerWorkSimulationWithFaultsServices.ServerWorkSimulationWithFaultsService import FaultSimulator

class ServerMonitor:
    def __init__(self, servers: List, update_interval: int = 5):
        self.servers = servers
        self.update_interval = update_interval
        self._stop_event = Event()
        self._monitor_thread = None

    def start_monitoring(self):
        if self._monitor_thread is None or not self._monitor_thread.is_alive():
            self._stop_event.clear()
            self._monitor_thread = threading.Thread(target=self._monitor_loop)
            self._monitor_thread.daemon = True
            self._monitor_thread.start()

    def stop_monitoring(self):
        self._stop_event.set()
        if self._monitor_thread and self._monitor_thread.is_alive():
            self._monitor_thread.join(timeout=5)
        self._monitor_thread = None
        gc.collect()

    def _monitor_loop(self):
        while not self._stop_event.is_set():
            try:
                show_servers_status(self.servers)
                time.sleep(self.update_interval)
            except Exception as e:
                print(f"Error in monitor loop: {str(e)}")
                break
            finally:
                gc.collect()


def run_simulation(users_data: pd.DataFrame,
                   posts_data: pd.DataFrame,
                   comments_data: pd.DataFrame,
                   servers_cluster: List,
                   simulation_interval: int = 3) -> None:
    """
    Main simulation runner with improved resource management and cleanup.
    """
    simulator = None
    monitor = None

    try:
        simulator = FaultSimulator()
        monitor = ServerMonitor(servers_cluster)

        monitor.start_monitoring()
        grouped_comments = simulator.group_similar_comments(comments_data)

        while True:
            simulator.handle_fault(
                users_data,
                comments_data,
                posts_data,
                servers_cluster,
                grouped_comments
            )
            time.sleep(simulation_interval)
            gc.collect()

    except KeyboardInterrupt:
        print("\nShutting down simulation...")
    except Exception as e:
        print(f"Simulation error: {str(e)}")
    finally:
        if monitor:
            monitor.stop_monitoring()
        if simulator:
            simulator.cleanup()
        gc.collect()