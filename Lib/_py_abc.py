from _weakrefset import WeakSet


def get_cache_token():
    """Returns the current ABC cache token.

    The token is an opaque object (supporting equality testing) identifying the
    current version of the ABC cache for virtual subclasses. The token changes
    with every call to ``register()`` on any ABC.
    """
    return ABCMeta._abc_invalidation_counter


class ABCMeta(type):
    """Metaclass for defining Abstract Base Classes (ABCs).

    Use this metaclass to create an ABC.  An ABC can be subclassed
    directly, and then acts as a mix-in class.  You can also register
    unrelated concrete classes (even built-in classes) and unrelated
    ABCs as 'virtual subclasses' -- these and their descendants will
    be considered subclasses of the registering ABC by the built-in
    issubclass() function, but the registering ABC won't show up in
    their MRO (Method Resolution Order) nor will method
    implementations defined by the registering ABC be callable (not
    even via super()).
    """

    # A global counter that is incremented each time a class is
    # registered as a virtual subclass of anything.  It forces the
    # negative cache to be cleared before its next use.
    # Note: this counter is private. Use `abc.get_cache_token()` for
    #       external code.
    _abc_invalidation_counter = 0

    def __new__(mcls, name, bases, namespace, /, **kwargs):
        cls = super().__new__(mcls, name, bases, namespace, **kwargs)
        # Compute set of abstract method names
        abstracts = {name
                     for name, value in namespace.items()
                     if getattr(value, "__isabstractmethod__", False)}
        for base in bases:
            for name in getattr(base, "__abstractmethods__", set()):
                value = getattr(cls, name, None)
                if getattr(value, "__isabstractmethod__", False):
                    abstracts.add(name)
        cls.__abstractmethods__ = frozenset(abstracts)
        # Set up inheritance registry
        cls._abc_registry = WeakSet()
        cls._abc_cache = WeakSet()
        cls._abc_negative_cache = WeakSet()
        cls._abc_negative_cache_version = ABCMeta._abc_invalidation_counter
        return cls

    def register(self, subclass):
        """Register a virtual subclass of an ABC.

        Returns the subclass, to allow usage as a class decorator.
        """
        if not isinstance(subclass, type):
            raise TypeError("Can only register classes")
        if issubclass(subclass, self):
            return subclass  # Already a subclass
        # Subtle: test for cycles *after* testing for "already a subclass";
        # this means we allow X.register(X) and interpret it as a no-op.
        if issubclass(self, subclass):
            # This would create a cycle, which is bad for the algorithm below
            raise RuntimeError("Refusing to create an inheritance cycle")
        self._abc_registry.add(subclass)
        ABCMeta._abc_invalidation_counter += 1  # Invalidate negative cache
        return subclass

    def _dump_registry(self, file=None):
        """Debug helper to print the ABC registry."""
        print(f"Class: {self.__module__}.{self.__qualname__}", file=file)
        print(f"Inv. counter: {get_cache_token()}", file=file)
        for name in self.__dict__:
            if name.startswith("_abc_"):
                value = getattr(self, name)
                if isinstance(value, WeakSet):
                    value = set(value)
                print(f"{name}: {value!r}", file=file)

    def _abc_registry_clear(self):
        """Clear the registry (for debugging or testing)."""
        self._abc_registry.clear()

    def _abc_caches_clear(self):
        """Clear the caches (for debugging or testing)."""
        self._abc_cache.clear()
        self._abc_negative_cache.clear()

    def __instancecheck__(self, instance):
        """Override for isinstance(instance, cls)."""
        # Inline the cache checking
        subclass = instance.__class__
        if subclass in self._abc_cache:
            return True
        subtype = type(instance)
        if subtype is subclass:
            if (
                self._abc_negative_cache_version
                == ABCMeta._abc_invalidation_counter
                and subclass in self._abc_negative_cache
            ):
                return False
            # Fall back to the subclass check.
            return self.__subclasscheck__(subclass)
        return any(self.__subclasscheck__(c) for c in (subclass, subtype))

    def __subclasscheck__(self, subclass):
        """Override for issubclass(subclass, cls)."""
        if not isinstance(subclass, type):
            raise TypeError('issubclass() arg 1 must be a class')
        # Check cache
        if subclass in self._abc_cache:
            return True
        # Check negative cache; may have to invalidate
        if self._abc_negative_cache_version < ABCMeta._abc_invalidation_counter:
            # Invalidate the negative cache
            self._abc_negative_cache = WeakSet()
            self._abc_negative_cache_version = ABCMeta._abc_invalidation_counter
        elif subclass in self._abc_negative_cache:
            return False
        # Check the subclass hook
        ok = self.__subclasshook__(subclass)
        if ok is not NotImplemented:
            assert isinstance(ok, bool)
            if ok:
                self._abc_cache.add(subclass)
            else:
                self._abc_negative_cache.add(subclass)
            return ok
        # Check if it's a direct subclass
        if self in getattr(subclass, '__mro__', ()):
            self._abc_cache.add(subclass)
            return True
        # Check if it's a subclass of a registered class (recursive)
        for rcls in self._abc_registry:
            if issubclass(subclass, rcls):
                self._abc_cache.add(subclass)
                return True
        # Check if it's a subclass of a subclass (recursive)
        for scls in self.__subclasses__():
            if issubclass(subclass, scls):
                self._abc_cache.add(subclass)
                return True
        # No dice; update negative cache
        self._abc_negative_cache.add(subclass)
        return False
