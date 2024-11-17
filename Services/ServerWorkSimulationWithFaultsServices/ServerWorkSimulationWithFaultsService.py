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

    # 1st: Using random forest group up similar comments (answers)
    # TODO

    # 2nd: Using linear regression try to predict right comment (answer) for problem
    # TODO

    # If answer is found print comment (answer) and show which user wrote that comment
    # TODO

    # Otherwise print that server fault couldn't be solved right now
    # TODO