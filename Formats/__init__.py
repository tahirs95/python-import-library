from .UnitConversion import UnitConversion

# Initializing Pint's Unit Registry
conversion = UnitConversion()
ureg = conversion.getUnitRegistry()
Quantity = ureg.Quantity