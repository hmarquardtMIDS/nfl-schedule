class Team:
    def __init__(self, name, division, conference):
        self.name = name
        self.division = division
        self.conference = conference

    def __str__(self):
        return f"{self.name} ({self.division}, {self.conference})"
