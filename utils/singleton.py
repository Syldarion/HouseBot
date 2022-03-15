class Singleton:
    def __init__(self, cls):
        self._cls = cls
        self._instance = None

    def instance(self):
        if not self._instance:
            self._instance = self._cls()
        return self._instance

    def __call__(self, *args, **kwargs):
        raise TypeError(f"Access this Singleton through {str(self._cls)}.instance()")

    def __instancecheck__(self, instance):
        return isinstance(instance, self._cls)
