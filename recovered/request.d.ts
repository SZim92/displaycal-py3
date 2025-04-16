se ValueError('Not a valid Python identifier: %r' % s)
        return True

    # The ConvertingXXX classes are wrappers around standard Python containers,
    # and they serve to convert any suitable values in the container. The
    # conversion converts base dicts, lists and tuples to their wrapped
    # equivalents, whereas strings which match a conversion format are converted
    # appropriately.
    #
    # Each wrapper should have a configurator attribute holding the actual
    # configurator to use for conversion.

    class ConvertingDict(dict):
        """A converting dictionary wrapper."""

        def __getitem__(self, key):
            value = dict.__getitem__(self, key)
            result = self.configurator.convert(value)
            # If the converted value is diffe