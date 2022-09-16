from causality import CausalModel

SUZY_BILLY = CausalModel()
SUZY_BILLY.add_constant('ST', True)
SUZY_BILLY.add_constant('BT', True)
SUZY_BILLY.add('SH', lambda vals: vals['ST'])
SUZY_BILLY.add('BH', lambda vals: vals['BT'] and (not vals['SH']))
SUZY_BILLY.add('BS', lambda vals: vals['BH'] or vals['SH'])
