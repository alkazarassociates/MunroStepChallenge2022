# Phase.py   Control what options are available based on time.

class Project:
    def __init__(self):
        self.challenge_name = "Team Step Challenge 2023"
        self.year = 2023
        self.next_year = self.year + 1    

class PhaseObject(Project):
    def __init__(self, name, allow_group_registration, allow_secondary_groups, teams_assigned, groups_modifiable, allow_registration, allow_step_entry,
                 challenge_over, teams_revealed):
        super().__init__()
        self._name = name
        self.allow_group_registration = allow_group_registration
        self._allow_2_groups_per_admin = allow_secondary_groups
        self._teams_assigned = teams_assigned
        self._allow_group_modifications = groups_modifiable
        self.allow_registration = allow_registration
        self.allow_step_entry = allow_step_entry
        self.challenge_over = challenge_over
        self.teams_revealed = teams_revealed
    
    def Name(self):
        return self._name
    
    def allow_2_groups_per_admin(self):
        return self._allow_2_groups_per_admin
    
    def teams_assigned(self):
        return self._teams_assigned
    
    def allow_group_modifications(self):
        return self._allow_group_modifications
       

PHASE_PREREG = PhaseObject('PREREG',
                           allow_group_registration=True,
                           allow_secondary_groups=True, 
                           teams_assigned=False,
                           groups_modifiable=True,
                           allow_registration=False,
                           allow_step_entry=False,
                           challenge_over=False,
                           teams_revealed=False)
#                'allow_peaker_registration_in_group': True,
#                'allow_group_registration': True,

PHASE_REGISTRATION = PhaseObject('REGISTRATION',
                                 allow_group_registration=True,
                                 allow_secondary_groups=False, 
                                 teams_assigned=False,
                                 groups_modifiable=False,
                                 allow_registration=True,
                                 allow_step_entry=False,
                                 challenge_over=False,
                                 teams_revealed=False)
#                      'allow_peaker_registration_in_group': True,
#                      'allow_group_registration': True}
