"""
The activity conversion chart.
"""
from django.utils.translation import gettext as _

def GetActivities():
    return {
        _('Aerobic dance'): 137,
        _('Basketball game'): 150,
        _('Bicycling (moderate)'):	147,
        _('Bicycling (fast)'):	170,
        _('Bowling'): 105,
        _('Canoeing'): 112,
        _('Circuit training'): 135,
        _('Dancing'): 149,
        _('Elliptical'): 132,
        _('Gardening'): 115,
        _('Golf (no cart)'): 130,
        _('House cleaning'): 110,
        _('Ice skating (slow)'): 84,
        _('Ice skating (moderate)'): 122,
        _('Ice skating (fast)'): 203,
        _('Inline/roller skating'): 145,
        _('Jumping rope'): 180,
        _('Kayaking'): 132,
        # _('Password Reset (per incident)'): 10,
        _('Pickleball'): 130,
        _('Pilates'): 105,
        _('Racquetball/Squash'): 145,
        _('Rowing (moderate)'): 130,
        _('Rowing (vigorous)'): 153,
        _('Skateboarding'): 152,
        # _('Skiing (downhill)'): 134,
        # _('Skiing (x-country)'): 160,
        _('Soccer (football)'): 145,
        _('Softball'): 132,
        _('Stair-climber'): 160,
        _('Step aerobics'): 153,
        _('Swimming laps'): 138,
        _('Table tennis'): 119,
        _('Tai chi'): 105,
        _('Tennis (singles)'): 146,
        _('Water aerobics'): 134,
        _('Weight-lifting'): 112,
        _('Yoga'): 95,
    }