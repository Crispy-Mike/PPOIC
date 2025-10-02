
class Server:
    def __init__(self, server_id, server_type, capacity, status):
        self.server_id = server_id
        self.server_type = server_type
        self.capacity = capacity
        self.status = status
        self.data_center = None
        self.uptime = 0

    def restart_server(self):
        """Перезагрузить сервер"""
        self.status = "restarting"
        return "Server restarting"

