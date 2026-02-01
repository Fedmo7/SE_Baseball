from dataclasses import dataclass


@dataclass
class Team:
    id: int
    team_code: str
    team_name: str
    salary:float


    def __str__(self):
        return f'{self.team_code} ({self.team_name})'

    def __hash__(self):
        return hash(self.id)

    def __eq__(self, other):
        if isinstance(other, Team):
            return self.id == other.id
        return False