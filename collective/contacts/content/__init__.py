import warnings
from Products.Archetypes.fieldproperty import ATFieldProperty

class DeprecatedATFieldProperty(ATFieldProperty):
    def __init__(self, name, property, get_transform=None, set_transform=None):
        self._property = property
        super(DeprecatedATFieldProperty, self).__init__(name, get_transform, set_transform)
    def __get__(self, inst, klass):
        warnings.warn("Call to deprecated property %s use %s instead" % (self._property, self._name),
                      category=DeprecationWarning)
        return super(DeprecatedATFieldProperty, self).__get__(inst, klass)
    def __set__(self, inst, value):
        warnings.warn("Call to deprecated property %s use %s instead" % (self._property, self._name),
                      category=DeprecationWarning)
        super(DeprecatedATFieldProperty, self).__set__(inst, value)
