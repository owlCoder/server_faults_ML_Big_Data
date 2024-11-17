import random
from datetime import datetime

from Domain.Models.Server import Server
from Services.FaultSimulationServices.FaultPickerService import pick_a_server_fault


def run_simulation_with_faults(users, posts, comments, servers: list[Server]):
    # Choose one random server fault
    fault = pick_a_server_fault(posts)

    # Choose a random server to fail
    random.seed(datetime.now().timestamp())
    faulty_server_index = random.randint(0, 9)

    # Add fault to a server faulty list
    servers[faulty_server_index].dodaj_otkaz(int(fault["Id"].iloc[0]))