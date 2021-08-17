# Data Transfer Objects:
class Vaccines:
    def __init__(self, list1):
        self.id = list1[0]
        self.date = list1[1]
        self.supplier = list1[2]
        self.quantity = list1[3]


class Suppliers:
    def __init__(self, list1):
        self.id = list1[0]
        self.name = list1[1]
        self.logistic = list1[2]


class Clinics:
    def __init__(self, list1):
        self.id = list1[0]
        self.location = list1[1]
        self.demand = int(list1[2])
        self.logistic = int(list1[3])


class Logistics:
    def __init__(self, list1):
        self.id = list1[0]
        self.name = list1[1]
        self.count_sent = list1[2]
        self.count_received = list1[3]
