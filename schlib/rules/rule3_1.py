# -*- coding: utf-8 -*-

from rules.rule import *

class Rule(KLCRule):
    """
    Create the methods check and fix to use with the kicad lib files.
    """
    def __init__(self, component):
        super(Rule, self).__init__(component, 'Rule 3.1', 'Using a 100mils grid, pin ends and origin must lie on grid nodes (IEC-60617).')

    def check(self):
        """
        Proceeds the checking of the rule.
        The following variables will be accessible after checking:
            * violating_pins
        """
        self.violating_pins = []
        for pin in self.component.pins:
            posx = int(pin['posx'])
            posy = int(pin['posy'])
            if (posx % 100) != 0 or (posy % 100) != 0:
                self.violating_pins.append(pin)
                self.verboseOut(Verbosity.HIGH, Severity.ERROR, 'pin: {0} ({1}), {2}'.format(pin['name'], pin['num'], positionFormater(pin)))

	"""
	Check if pins share the same coordinate
	"""
	# Sort the pin list by columns: posx, posy, num.
	self.spl = sorted(self.component.pins, key=lambda x: tuple((x['posx'],x['posy'],x['num'])))

	# Empty list to store the duplicates, each entry will become (again) a list of pin numbers.
	self.dupes=[]
	i=0 # Index iterate over all items, and easily refer to the next item.
	while i < (len(self.spl)-1):	# Skip the last pin, implies lists of more than one element.
		posx = self.spl[i]['posx'] # Keep track of the 'current' coordinate.
		posy = self.spl[i]['posy']
		if posx == self.spl[i+1]['posx'] and posy == self.spl[i+1]['posy']:
			self.dupes.append([self.spl[i]['num']])	# Store the element of the matching pair

			while posx == self.spl[i+1]['posx'] and posy == self.spl[i+1]['posy']: # Also store the second and possible more pins with the same coordinate
				self.dupes[-1].append(self.spl[i+1]['num'])
				i+=1 # Advance while keeping the current coordinate
		i+=1 # Advance to the next pin (with a new coordinate)

	if len(self.dupes):
                self.verboseOut(Verbosity.HIGH, Severity.ERROR, 'Found more than one pin on the same coordinate(s):')
		for d in self.dupes:
			self.verboseOut(Verbosity.HIGH, Severity.ERROR, 'Pins {0} share the same coordinate'.format(d))

        return True if len(self.violating_pins) > 0 or len(self.dupes) > 0 else False

    def fix(self):
        """
        Proceeds the fixing of the rule, if possible.
        """
        self.verboseOut(Verbosity.NORMAL, Severity.INFO, "FIX: not yet supported" )
        # TODO
