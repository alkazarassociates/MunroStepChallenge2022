# Phase.py   Control what options are available based on time.
import datetime


class Project:
    def __init__(self):
        self.challenge_name = "Team Step Challenge 2023"
        self.year = 2023
        self.next_year = self.year + 1
        self.domain = 'tsc23' + '.' + 'alkazarassociates.com'

    def switch_to_test_server(self):
        self.domain = 'test' + '.' + 'alkazarassociates.com'


class PhaseObject(Project):
    def __init__(self, name, allow_group_registration, allow_secondary_groups, teams_assigned, groups_modifiable, allow_registration, allow_registration_in_group,
                 allow_step_entry,
                 challenge_over, teams_revealed, allow_non_group_peakers):
        super().__init__()
        self._name = name
        self.allow_group_registration = allow_group_registration
        self._allow_2_groups_per_admin = allow_secondary_groups
        self._teams_assigned = teams_assigned
        self._allow_group_modifications = groups_modifiable
        self.allow_registration = allow_registration
        self.allow_registration_in_group = allow_registration_in_group
        self.allow_step_entry = allow_step_entry
        self.challenge_over = challenge_over
        self.teams_revealed = teams_revealed
        self.allow_non_group_peakers = allow_non_group_peakers
        self.challenge_start_date = datetime.date(self.year, 9, 1)
        self.challenge_end_date = datetime.date(self.year, 10, 1)
    
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
                           allow_registration_in_group=False,
                           allow_step_entry=False,
                           challenge_over=False,
                           teams_revealed=False,
                           allow_non_group_peakers=False)

PHASE_REGISTRATION = PhaseObject('REGISTRATION',
                                 allow_group_registration=True,
                                 allow_secondary_groups=False, 
                                 teams_assigned=False,
                                 groups_modifiable=False,
                                 allow_registration=True,
                                 allow_registration_in_group=True,
                                 allow_step_entry=False,
                                 challenge_over=False,
                                 teams_revealed=False,
                                 allow_non_group_peakers=False)
