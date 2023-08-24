# Phase.py   Control what options are available based on time.

class PhaseObject:
    def __init__(self, name, allow_secondary_groups, teams_assigned, groups_modifiable):
        self._name = name
        self._allow_2_groups_per_admin = allow_secondary_groups
        self._teams_assigned = teams_assigned
        self._allow_group_modifications = groups_modifiable
    
    def Name(self):
        return self._name
    
    def allow_2_groups_per_admin(self):
        return self._allow_2_groups_per_admin
    
    def teams_assigned(self):
        return self._teams_assigned
    
    def allow_group_modifications(self):
        return self._allow_group_modifications
    

PHASE_PREREG = PhaseObject('PREREG',
                           allow_secondary_groups=True, 
                           teams_assigned=False,
                           groups_modifiable=True)
#                'allow_peaker_registration' : False,
#                'allow_peaker_registration_in_group': True,
#                'allow_step_entry': False,
#                'allow_group_registration': True,

PHASE_REGISTRATION = PhaseObject('REGISTRATION',
                                  allow_secondary_groups=False, 
                                  teams_assigned=False,
                                  groups_modifiable=False)
#                      'allow_peaker_registration': True,
#                      'allow_peaker_registration_in_group': True,
#                      'allow_step_entry': False,
#                      'allow_group_registration': True}


