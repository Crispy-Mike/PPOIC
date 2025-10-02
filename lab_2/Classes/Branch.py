class Branch:
    def __init__(self, name_branch, address, branch_code):
        self.name_branch = name_branch
        self.address = address
        self.branch_code = branch_code
        self.customers = []
        self.employees = []
        self.atms = []
        self.cashiers = []

    def add_atm(self, atm):
        self.atms.append(atm)
        atm.branch = self

