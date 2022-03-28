
class DuplicateServiceName(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)

class ServiceNotFound(Exception):
     def __init__(self, *args: object) -> None:
        super().__init__(*args)