from GameElements.Resource import Resource


class ResourceFlow:
    resource: Resource
    rate: float

    def __init__(self, resource: Resource | str, rate: float):
        if type(resource) == str:
            self.resource = Resource(resource)
        else:
            self.resource = resource
        self.rate = rate
