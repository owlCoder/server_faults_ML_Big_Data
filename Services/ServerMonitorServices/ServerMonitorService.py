import threading
import time
from typing import List
import pandas as pd
from threading import Event
from datetime import datetime
from Presentation.ServerStatusShow.ServerStatusUI import show_servers_status
import gc
from Services.ServerWorkSimulationWithFaultsServices.ServerWorkSimulationWithFaultsService import FaultSimulator

class ServerMonitor:
    def __init__(self, servers: List, update_interval: int = 5):
        self.servers = servers
        self.update_interval = update_interval
        self._stop_event = Event()
        self._monitor_thread = None
        self._start_time = None
        self._total_uptime = 0
        self._status_history = []

    def start_monitoring(self):
        if self._monitor_thread is None or not self._monitor_thread.is_alive():
            self._stop_event.clear()
            self._start_time = datetime.now()
            self._monitor_thread = threading.Thread(target=self._monitor_loop)
            self._monitor_thread.daemon = True
            self._monitor_thread.start()
            print("\n🔄 Server monitoring started...")
            print(f"Monitoring {len(self.servers)} servers with {self.update_interval}s interval")

    def stop_monitoring(self):
        print("\n⏹️ Stopping server monitoring...")
        self._stop_event.set()
        if self._monitor_thread and self._monitor_thread.is_alive():
            self._monitor_thread.join(timeout=5)

        if self._start_time:
            self._total_uptime = (datetime.now() - self._start_time).total_seconds()
            print(f"Total monitoring time: {self._total_uptime:.1f} seconds")

        self._monitor_thread = None
        self._print_monitoring_summary()
        gc.collect()

    def _print_monitoring_summary(self):
        print("\n📊 Monitoring Summary:")
        for server in self.servers:
            fault_count = len(server.lista_otkaza)
            print(f"\nServer: {server.naziv} (ID: {server.id_servera})")
            print(f"Total faults: {fault_count}")
            if self._total_uptime > 0:
                faults_per_hour = (fault_count * 3600) / self._total_uptime
                print(f"Fault rate: {faults_per_hour:.2f} faults/hour")

    def _monitor_loop(self):
        last_check = time.time()
        while not self._stop_event.is_set():
            try:
                current_time = time.time()
                if current_time - last_check >= self.update_interval:
                    status = {
                        'timestamp': datetime.now(),
                        'server_states': [
                            {
                                'id': server.id_servera,
                                'name': server.naziv,
                                'faults': len(server.lista_otkaza)
                            }
                            for server in self.servers
                        ]
                    }
                    self._status_history.append(status)

                    # Print current status
                    print("\n📡 Server Status Update:")
                    show_servers_status(self.servers)
                    last_check = current_time

                # Small sleep to prevent CPU hogging
                time.sleep(0.1)

            except Exception as e:
                print(f"❌ Error in monitor loop: {str(e)}")
                break
            finally:
                gc.collect()


class SimulationManager:
    def __init__(self, simulation_interval: int = 3):
        self.simulation_interval = simulation_interval
        self._stop_event = Event()
        self._simulator = None
        self._monitor = None

    def run_simulation(self,
                       users_data: pd.DataFrame,
                       posts_data: pd.DataFrame,
                       comments_data: pd.DataFrame,
                       servers_cluster: List) -> None:
        """
        Main simulation runner with improved resource management and cleanup.
        """
        try:
            print("\n🚀 Starting simulation...")
            self._simulator = FaultSimulator()
            self._monitor = ServerMonitor(servers_cluster)

            # Start monitoring
            self._monitor.start_monitoring()

            # Initial grouping of comments
            print("\n⏳ Processing comment data...")
            grouped_comments = self._simulator.group_similar_comments(comments_data)
            print("✅ Comment processing complete")

            print("\n▶️ Beginning fault simulation...")
            while not self._stop_event.is_set():
                self._simulator.handle_fault(
                    users_data,
                    comments_data,
                    posts_data,
                    servers_cluster,
                    grouped_comments
                )
                time.sleep(self.simulation_interval)
                gc.collect()

        except KeyboardInterrupt:
            print("\n⚠️ Received shutdown signal...")
        except Exception as e:
            print(f"\n❌ Simulation error: {str(e)}")
        finally:
            self._cleanup()

    def stop_simulation(self):
        print("\n🛑 Stopping simulation...")
        self._stop_event.set()
        self._cleanup()

    def _cleanup(self):
        if self._monitor:
            self._monitor.stop_monitoring()
            self._monitor = None

        if self._simulator:
            self._simulator.cleanup()
            self._simulator = None

        gc.collect()
        print("\n✅ Simulation cleanup complete")


def run_simulation(users_data: pd.DataFrame,
                   posts_data: pd.DataFrame,
                   comments_data: pd.DataFrame,
                   servers_cluster: List,
                   simulation_interval: int = 3) -> None:
    """
    Wrapper function to maintain backward compatibility
    """
    manager = SimulationManager(simulation_interval)
    manager.run_simulation(users_data, posts_data, comments_data, servers_cluster)