from datetime import datetime
import json
from abc import ABC,abstractmethod

# Single responsibility principle Done.
# Open closed principle Done.
# Liskov substitution principle Done.
# abstract class Done.
# Polymorphism Done.
# Inheritance Done.
# Interface segregation :


class Vehicle(ABC):
    def __init__(self,make,model,year):
        self.make=make
        self.model=model
        self.year=year

    @abstractmethod
    def calculate_insurance(self):
        pass

class FuelVehicle(ABC):
    @abstractmethod
    def refuel(self):
        pass

class ElectricVehicle(ABC):
    @abstractmethod
    def recharge(self):
        pass

# Car child :
class Car(Vehicle,FuelVehicle):
    def calculate_insurance(self):
        if (datetime.now().year-self.year)>5:
            return 1000
        return 500

    def refuel(self):
        print('Refuel you vehicle')

# Truck child :
class Truck(Vehicle,FuelVehicle):
    def calculate_insurance(self):
        if (datetime.now().year-self.year)>5:
            return 2000
        return 1000

    def refuel(self):
        print('Refuel you vehicle')

# Bus child :
class Bus(Vehicle,FuelVehicle):
    def calculate_insurance(self):
        if(datetime.now().year-self.year)>10:
            return 1500
        return 1000

    def refuel(self):
        print('Refuel you vehicle')

# Motor cycle :
class MotorCycle(Vehicle,ElectricVehicle):
    def calculate_insurance(self):
        if(datetime.now().year-self.year)>10:
            return 2500
        return 1500

    def recharge(self):
        print('recharge ')

def main():
    pass

if __name__=='__main__': main()
