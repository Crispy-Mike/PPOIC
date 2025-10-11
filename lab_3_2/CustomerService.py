import datetime

class CustomerService:
    def __init__(self, agent_id, name, language_skills, specialization):
        self.agent_id = agent_id
        self.name = name
        self.language_skills = language_skills
        self.specialization = specialization
        self.active_tickets = []
        self.resolved_tickets = []
        self.satisfaction_score = 0

    def create_support_ticket(self, passenger, issue_type, description, priority):
        ticket = {
            'ticket_id': f"TICK{len(self.active_tickets) + 1}",
            'passenger': passenger,
            'issue_type': issue_type,
            'description': description,
            'priority': priority,
            'status': 'open',
            'created_date': datetime.now()
        }
        self.active_tickets.append(ticket)
        return ticket['ticket_id']

    def resolve_ticket(self, ticket_id, solution):
        ticket = next((t for t in self.active_tickets if t['ticket_id'] == ticket_id), None)
        if ticket:
            ticket['status'] = 'resolved'
            ticket['solution'] = solution
            ticket['resolved_date'] = datetime.now()
            self.active_tickets.remove(ticket)
            self.resolved_tickets.append(ticket)
            self.satisfaction_score += 1