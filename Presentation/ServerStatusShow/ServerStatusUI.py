from Domain.Models.Server import Server


def show_servers_status(serveri: list[Server]):
    # ASCII art for the server
    ascii_server = (
        " ---------- \n"
        " | SERVER | \n"
        " ---------- \n"
    )

    # Define the layout for rows
    row_layouts = [4, 3, 2, 1]
    row_count = 0

    result = ""
    server_index = 0

    for row_size in row_layouts:
        if server_index >= len(serveri):
            break

        # Collect ASCII art for the current row
        row_ascii_art = []
        for i in range(row_size):
            if server_index >= len(serveri):
                break

            server = serveri[server_index]

            # Generate centered info
            info_lines = [
                server.id_servera[0:8],  # First 8 chars of id_servera
                server.naziv.split(' ')[0],  # Server name
                f"{len(server.lista_otkaza)} faults",  # Fault count
            ]
            # Calculate maximum width of ASCII art for centering
            max_width = len(ascii_server.splitlines()[0])
            centered_info = "\n".join(
                line.center(max_width) for line in info_lines
            )
            # Combine ASCII art and centered info
            server_ascii = ascii_server + centered_info
            row_ascii_art.append(server_ascii)
            server_index += 1

        # Append the row to the result
        max_lines = max(len(s.splitlines()) for s in row_ascii_art)
        for line_num in range(max_lines):
            result += "  ".join(
                server.splitlines()[line_num] if line_num < len(server.splitlines()) else " " * 10
                for server in row_ascii_art
            ) + "\n"

        result += "\n"  # Add space between rows

    print(result)
