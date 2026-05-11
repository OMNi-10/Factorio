from GameElements.Resource import Resource


class ResourceFlow:
    resource: Resource
    rate: float

    def __init__(self, resource: Resource, rate: float):
        self.resource = resource
        self.rate = rate
