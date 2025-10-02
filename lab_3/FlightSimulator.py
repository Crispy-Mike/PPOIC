class FlightSimulator:
    def __init__(self, sim_id, model, location, available=True):
        self.sim_id = sim_id
        self.model = model
        self.location = location
        self.available = available
        self.training_sessions = []
        self.maintenance_schedule = []

    def schedule_training(self, pilot, date, duration):
        if not self.available:
            raise Exception("Тренажер недоступен")
        session = {
            'pilot': pilot,
            'date': date,
            'duration': duration,
            'completed': False
        }
        self.training_sessions.append(session)
        return "Тренировка запланирована"

    def conduct_training(self, session_index):
        session = self.training_sessions[session_index]
        session['completed'] = True
        return f"Тренировка для {session['pilot'].name} завершена"