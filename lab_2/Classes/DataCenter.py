class DataCenter:
    def __init__(self, name_data_center, location, security_level):
        self.name_data_center = name_data_center
        self.location = location
        self.security_level = security_level
        self.employees = []
        self.servers = []
        self.backup_systems = []

    def add_server(self, server):
        self.servers.append(server)
        server.data_center = self

