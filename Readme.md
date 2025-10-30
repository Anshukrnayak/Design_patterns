# SOLID Principles in Python

The SOLID principles are five design principles that help make software designs more understandable, flexible, and maintainable. Let's explore each principle with Python examples.

## 1. S - Single Responsibility Principle (SRP)

**Definition**: A class should have only one reason to change, meaning it should have only one job or responsibility.

### Example

```python
# ❌ Violates SRP
class UserManager:
    def __init__(self, user):
        self.user = user
    
    def change_user_name(self, new_name):
        self.user.name = new_name
    
    def save_user_to_database(self):
        # Database saving logic
        print(f"Saving {self.user.name} to database")
    
    def send_welcome_email(self):
        # Email sending logic
        print(f"Sending welcome email to {self.user.name}")

# ✅ Follows SRP
class User:
    def __init__(self, name, email):
        self.name = name
        self.email = email
    
    def change_name(self, new_name):
        self.name = new_name

class UserRepository:
    @staticmethod
    def save(user):
        # Database saving logic
        print(f"Saving {user.name} to database")

class EmailService:
    @staticmethod
    def send_welcome_email(user):
        # Email sending logic
        print(f"Sending welcome email to {user.name}")

# Usage
user = User("John", "john@example.com")
UserRepository.save(user)
EmailService.send_welcome_email(user)
```

## 2. O - Open/Closed Principle (OCP)

**Definition**: Software entities should be open for extension but closed for modification.

### Example

```python
from abc import ABC, abstractmethod
from math import pi

# ❌ Violates OCP
class AreaCalculator:
    def calculate_area(self, shape):
        if isinstance(shape, Rectangle):
            return shape.width * shape.height
        elif isinstance(shape, Circle):
            return pi * shape.radius ** 2
        # Adding a new shape requires modifying this class

# ✅ Follows OCP
class Shape(ABC):
    @abstractmethod
    def area(self):
        pass

class Rectangle(Shape):
    def __init__(self, width, height):
        self.width = width
        self.height = height
    
    def area(self):
        return self.width * self.height

class Circle(Shape):
    def __init__(self, radius):
        self.radius = radius
    
    def area(self):
        return pi * self.radius ** 2

class Triangle(Shape):
    def __init__(self, base, height):
        self.base = base
        self.height = height
    
    def area(self):
        return 0.5 * self.base * self.height

class AreaCalculator:
    def calculate_area(self, shape: Shape):
        return shape.area()

# Usage
calculator = AreaCalculator()
shapes = [Rectangle(4, 5), Circle(3), Triangle(6, 4)]

for shape in shapes:
    print(f"Area: {calculator.calculate_area(shape)}")
```

## 3. L - Liskov Substitution Principle (LSP)

**Definition**: Objects of a superclass should be replaceable with objects of its subclasses without breaking the application.

### Example

```python
# ❌ Violates LSP
class Bird:
    def fly(self):
        return "Flying"
    
    def swim(self):
        return "Swimming"

class Duck(Bird):
    pass

class Penguin(Bird):
    def fly(self):
        raise Exception("Penguins can't fly!")
    # This violates LSP because we can't substitute Penguin for Bird

# ✅ Follows LSP
class Bird:
    def move(self):
        pass

class FlyingBird(Bird):
    def move(self):
        return "Flying"

class SwimmingBird(Bird):
    def move(self):
        return "Swimming"

class Duck(FlyingBird, SwimmingBird):
    def move(self):
        return "Flying or swimming"

class Penguin(SwimmingBird):
    def move(self):
        return "Swimming"

def make_bird_move(bird: Bird):
    return bird.move()

# Usage
birds = [Duck(), Penguin()]
for bird in birds:
    print(make_bird_move(bird))  # Works for all birds
```

## 4. I - Interface Segregation Principle (ISP)

**Definition**: Clients should not be forced to depend on interfaces they do not use.

### Example

```python
from abc import ABC, abstractmethod

# ❌ Violates ISP
class Worker(ABC):
    @abstractmethod
    def work(self):
        pass
    
    @abstractmethod
    def eat(self):
        pass

class HumanWorker(Worker):
    def work(self):
        return "Human working"
    
    def eat(self):
        return "Human eating"

class RobotWorker(Worker):
    def work(self):
        return "Robot working"
    
    def eat(self):
        raise Exception("Robots don't eat!")  # Forced to implement

# ✅ Follows ISP
class Workable(ABC):
    @abstractmethod
    def work(self):
        pass

class Eatable(ABC):
    @abstractmethod
    def eat(self):
        pass

class HumanWorker(Workable, Eatable):
    def work(self):
        return "Human working"
    
    def eat(self):
        return "Human eating"

class RobotWorker(Workable):
    def work(self):
        return "Robot working"

def manage_work(worker: Workable):
    return worker.work()

def manage_lunch(eater: Eatable):
    return eater.eat()

# Usage
human = HumanWorker()
robot = RobotWorker()

print(manage_work(human))
print(manage_work(robot))
print(manage_lunch(human))
# manage_lunch(robot)  # This would be a type error, which is good!
```

## 5. D - Dependency Inversion Principle (DIP)

**Definition**: High-level modules should not depend on low-level modules. Both should depend on abstractions.

### Example

```python
from abc import ABC, abstractmethod

# ❌ Violates DIP
class LightBulb:
    def turn_on(self):
        return "LightBulb: turned on"
    
    def turn_off(self):
        return "LightBulb: turned off"

class Switch:
    def __init__(self):
        self.bulb = LightBulb()  # Direct dependency on concrete class
    
    def operate(self):
        return self.bulb.turn_on()

# ✅ Follows DIP
class Switchable(ABC):
    @abstractmethod
    def turn_on(self):
        pass
    
    @abstractmethod
    def turn_off(self):
        pass

class LightBulb(Switchable):
    def turn_on(self):
        return "LightBulb: turned on"
    
    def turn_off(self):
        return "LightBulb: turned off"

class Fan(Switchable):
    def turn_on(self):
        return "Fan: turned on"
    
    def turn_off(self):
        return "Fan: turned off"

class Switch:
    def __init__(self, device: Switchable):  # Depends on abstraction
        self.device = device
    
    def operate(self):
        return self.device.turn_on()

# Usage
bulb = LightBulb()
fan = Fan()

light_switch = Switch(bulb)
fan_switch = Switch(fan)

print(light_switch.operate())  # LightBulb: turned on
print(fan_switch.operate())    # Fan: turned on
```

## Practical Example Combining All Principles

```python
from abc import ABC, abstractmethod
from typing import List
import json

# SRP: Separate concerns
class Product:
    def __init__(self, name: str, price: float):
        self.name = name
        self.price = price

# OCP: Open for extension
class DiscountStrategy(ABC):
    @abstractmethod
    def apply_discount(self, price: float) -> float:
        pass

class NoDiscount(DiscountStrategy):
    def apply_discount(self, price: float) -> float:
        return price

class PercentageDiscount(DiscountStrategy):
    def __init__(self, percentage: float):
        self.percentage = percentage
    
    def apply_discount(self, price: float) -> float:
        return price * (1 - self.percentage / 100)

# LSP: Substitutable
class Order:
    def __init__(self, discount_strategy: DiscountStrategy = None):
        self.products: List[Product] = []
        self.discount_strategy = discount_strategy or NoDiscount()
    
    def add_product(self, product: Product):
        self.products.append(product)
    
    def calculate_total(self) -> float:
        total = sum(product.price for product in self.products)
        return self.discount_strategy.apply_discount(total)

# ISP: Segregated interfaces
class OrderRepository(ABC):
    @abstractmethod
    def save(self, order: Order):
        pass

class OrderNotification(ABC):
    @abstractmethod
    def send_confirmation(self, order: Order):
        pass

# DIP: Depend on abstractions
class JSONOrderRepository(OrderRepository):
    def save(self, order: Order):
        data = {
            "total": order.calculate_total(),
            "products": [{"name": p.name, "price": p.price} for p in order.products]
        }
        with open("order.json", "w") as f:
            json.dump(data, f)

class EmailNotification(OrderNotification):
    def send_confirmation(self, order: Order):
        print(f"Order confirmed! Total: ${order.calculate_total():.2f}")

class OrderService:
    def __init__(self, 
                 repository: OrderRepository, 
                 notification: OrderNotification):
        self.repository = repository
        self.notification = notification
    
    def process_order(self, order: Order):
        total = order.calculate_total()
        self.repository.save(order)
        self.notification.send_confirmation(order)
        return total

# Usage
products = [
    Product("Laptop", 1000),
    Product("Mouse", 50),
    Product("Keyboard", 80)
]

order = Order(PercentageDiscount(10))
for product in products:
    order.add_product(product)

service = OrderService(JSONOrderRepository(), EmailNotification())
total = service.process_order(order)
print(f"Final total: ${total:.2f}")
```

## Key Benefits of SOLID Principles

1. **Maintainability**: Easier to understand and modify code
2. **Testability**: Classes are easier to test in isolation
3. **Flexibility**: Easier to extend functionality
4. **Reusability**: Components can be reused in different contexts
5. **Reduced Coupling**: Components are less dependent on each other

Remember that these principles are guidelines, not strict rules. Apply them judiciously based on your specific use case and project requirements.


# All Design Patterns - Comprehensive Guide

Design patterns are typical solutions to common problems in software design. They are categorized into three main groups: Creational, Structural, and Behavioral patterns.

## Creational Patterns

### 1. Singleton Pattern
Ensures a class has only one instance and provides a global point of access to it.

```python
class Singleton:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

# Usage
s1 = Singleton()
s2 = Singleton()
print(s1 is s2)  # True

# Alternative with metaclass
class SingletonMeta(type):
    _instances = {}
    
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]

class Database(metaclass=SingletonMeta):
    def __init__(self):
        print("Database connection established")

# Usage
db1 = Database()
db2 = Database()
print(db1 is db2)  # True
```

### 2. Factory Method Pattern
Creates objects without specifying the exact class to create.

```python
from abc import ABC, abstractmethod

class Vehicle(ABC):
    @abstractmethod
    def drive(self):
        pass

class Car(Vehicle):
    def drive(self):
        return "Driving a car"

class Bike(Vehicle):
    def drive(self):
        return "Riding a bike"

class VehicleFactory(ABC):
    @abstractmethod
    def create_vehicle(self) -> Vehicle:
        pass
    
    def deliver_vehicle(self):
        vehicle = self.create_vehicle()
        return f"Delivering {vehicle.drive()}"

class CarFactory(VehicleFactory):
    def create_vehicle(self) -> Vehicle:
        return Car()

class BikeFactory(VehicleFactory):
    def create_vehicle(self) -> Vehicle:
        return Bike()

# Usage
car_factory = CarFactory()
print(car_factory.deliver_vehicle())  # Delivering Driving a car

bike_factory = BikeFactory()
print(bike_factory.deliver_vehicle())  # Delivering Riding a bike
```

### 3. Abstract Factory Pattern
Creates families of related objects without specifying their concrete classes.

```python
from abc import ABC, abstractmethod

# Abstract Products
class Button(ABC):
    @abstractmethod
    def click(self):
        pass

class Checkbox(ABC):
    @abstractmethod
    def check(self):
        pass

# Concrete Products
class WindowsButton(Button):
    def click(self):
        return "Windows button clicked"

class MacButton(Button):
    def click(self):
        return "Mac button clicked"

class WindowsCheckbox(Checkbox):
    def check(self):
        return "Windows checkbox checked"

class MacCheckbox(Checkbox):
    def check(self):
        return "Mac checkbox checked"

# Abstract Factory
class GUIFactory(ABC):
    @abstractmethod
    def create_button(self) -> Button:
        pass
    
    @abstractmethod
    def create_checkbox(self) -> Checkbox:
        pass

# Concrete Factories
class WindowsFactory(GUIFactory):
    def create_button(self) -> Button:
        return WindowsButton()
    
    def create_checkbox(self) -> Checkbox:
        return WindowsCheckbox()

class MacFactory(GUIFactory):
    def create_button(self) -> Button:
        return MacButton()
    
    def create_checkbox(self) -> Checkbox:
        return MacCheckbox()

# Client
class Application:
    def __init__(self, factory: GUIFactory):
        self.button = factory.create_button()
        self.checkbox = factory.create_checkbox()
    
    def operate(self):
        return f"{self.button.click()} and {self.checkbox.check()}"

# Usage
windows_app = Application(WindowsFactory())
print(windows_app.operate())  # Windows button clicked and Windows checkbox checked

mac_app = Application(MacFactory())
print(mac_app.operate())  # Mac button clicked and Mac checkbox checked
```

### 4. Builder Pattern
Constructs complex objects step by step.

```python
class Computer:
    def __init__(self):
        self.cpu = None
        self.ram = None
        self.storage = None
        self.gpu = None
    
    def __str__(self):
        return f"Computer: CPU={self.cpu}, RAM={self.ram}, Storage={self.storage}, GPU={self.gpu}"

class ComputerBuilder:
    def __init__(self):
        self.computer = Computer()
    
    def set_cpu(self, cpu):
        self.computer.cpu = cpu
        return self
    
    def set_ram(self, ram):
        self.computer.ram = ram
        return self
    
    def set_storage(self, storage):
        self.computer.storage = storage
        return self
    
    def set_gpu(self, gpu):
        self.computer.gpu = gpu
        return self
    
    def build(self):
        return self.computer

class ComputerDirector:
    def build_gaming_computer(self):
        return (ComputerBuilder()
                .set_cpu("Intel i9")
                .set_ram("32GB")
                .set_storage("1TB SSD")
                .set_gpu("NVIDIA RTX 4080")
                .build())
    
    def build_office_computer(self):
        return (ComputerBuilder()
                .set_cpu("Intel i5")
                .set_ram("16GB")
                .set_storage("512GB SSD")
                .build())

# Usage
director = ComputerDirector()
gaming_pc = director.build_gaming_computer()
office_pc = director.build_office_computer()

print(gaming_pc)   # Computer: CPU=Intel i9, RAM=32GB, Storage=1TB SSD, GPU=NVIDIA RTX 4080
print(office_pc)   # Computer: CPU=Intel i5, RAM=16GB, Storage=512GB SSD, GPU=None
```

### 5. Prototype Pattern
Creates new objects by copying an existing object (prototype).

```python
import copy
from abc import ABC, abstractmethod

class Prototype(ABC):
    @abstractmethod
    def clone(self):
        pass

class Car(Prototype):
    def __init__(self, model, color, features=None):
        self.model = model
        self.color = color
        self.features = features or []
    
    def clone(self):
        # Deep copy for nested objects
        return copy.deepcopy(self)
    
    def customize(self, color=None, features=None):
        new_car = self.clone()
        if color:
            new_car.color = color
        if features:
            new_car.features.extend(features)
        return new_car
    
    def __str__(self):
        return f"{self.color} {self.model} with features: {', '.join(self.features)}"

# Usage
base_car = Car("Sedan", "White", ["AC", "Radio"])
print(f"Base car: {base_car}")

# Create customized cars from prototype
red_sedan = base_car.customize(color="Red", features=["Sunroof"])
blue_sedan = base_car.customize(color="Blue", features=["Leather Seats", "GPS"])

print(f"Red sedan: {red_sedan}")
print(f"Blue sedan: {blue_sedan}")
print(f"Base car unchanged: {base_car}")
```

## Structural Patterns

### 6. Adapter Pattern
Allows incompatible interfaces to work together.

```python
# Existing class with incompatible interface
class OldPrinter:
    def print_document(self, text):
        return f"Printing: {text}"

# New interface we want to use
class NewPrinterInterface:
    def print(self, content):
        pass

# Adapter
class PrinterAdapter(NewPrinterInterface):
    def __init__(self, old_printer: OldPrinter):
        self.old_printer = old_printer
    
    def print(self, content):
        # Adapt the new interface to the old one
        return self.old_printer.print_document(content)

# Modern client expecting new interface
class Computer:
    def print_document(self, printer: NewPrinterInterface, content):
        return printer.print(content)

# Usage
old_printer = OldPrinter()
adapter = PrinterAdapter(old_printer)
computer = Computer()

result = computer.print_document(adapter, "Hello World")
print(result)  # Printing: Hello World
```

### 7. Bridge Pattern
Decouples an abstraction from its implementation.

```python
from abc import ABC, abstractmethod

# Implementation hierarchy
class Device(ABC):
    @abstractmethod
    def is_enabled(self):
        pass
    
    @abstractmethod
    def enable(self):
        pass
    
    @abstractmethod
    def disable(self):
        pass
    
    @abstractmethod
    def get_volume(self):
        pass
    
    @abstractmethod
    def set_volume(self, percent):
        pass

class TV(Device):
    def __init__(self):
        self._enabled = False
        self._volume = 50
    
    def is_enabled(self):
        return self._enabled
    
    def enable(self):
        self._enabled = True
        return "TV enabled"
    
    def disable(self):
        self._enabled = False
        return "TV disabled"
    
    def get_volume(self):
        return self._volume
    
    def set_volume(self, percent):
        self._volume = percent
        return f"TV volume set to {percent}"

class Radio(Device):
    def __init__(self):
        self._enabled = False
        self._volume = 30
    
    def is_enabled(self):
        return self._enabled
    
    def enable(self):
        self._enabled = True
        return "Radio enabled"
    
    def disable(self):
        self._enabled = False
        return "Radio disabled"
    
    def get_volume(self):
        return self._volume
    
    def set_volume(self, percent):
        self._volume = percent
        return f"Radio volume set to {percent}"

# Abstraction hierarchy
class RemoteControl:
    def __init__(self, device: Device):
        self.device = device
    
    def toggle_power(self):
        if self.device.is_enabled():
            return self.device.disable()
        else:
            return self.device.enable()
    
    def volume_down(self):
        volume = self.device.get_volume()
        return self.device.set_volume(volume - 10)
    
    def volume_up(self):
        volume = self.device.get_volume()
        return self.device.set_volume(volume + 10)

class AdvancedRemoteControl(RemoteControl):
    def mute(self):
        return self.device.set_volume(0)

# Usage
tv = TV()
radio = Radio()

basic_remote = RemoteControl(tv)
print(basic_remote.toggle_power())  # TV enabled
print(basic_remote.volume_up())     # TV volume set to 60

advanced_remote = AdvancedRemoteControl(radio)
print(advanced_remote.toggle_power())  # Radio enabled
print(advanced_remote.mute())          # Radio volume set to 0
```

### 8. Composite Pattern
Composes objects into tree structures to represent part-whole hierarchies.

```python
from abc import ABC, abstractmethod
from typing import List

class FileSystemComponent(ABC):
    @abstractmethod
    def show_details(self, indent=0):
        pass
    
    @abstractmethod
    def get_size(self):
        pass

class File(FileSystemComponent):
    def __init__(self, name, size):
        self.name = name
        self.size = size
    
    def show_details(self, indent=0):
        print("  " * indent + f"📄 {self.name} ({self.size} KB)")
    
    def get_size(self):
        return self.size

class Directory(FileSystemComponent):
    def __init__(self, name):
        self.name = name
        self.children: List[FileSystemComponent] = []
    
    def add(self, component: FileSystemComponent):
        self.children.append(component)
    
    def remove(self, component: FileSystemComponent):
        self.children.remove(component)
    
    def show_details(self, indent=0):
        print("  " * indent + f"📁 {self.name}/ (Total: {self.get_size()} KB)")
        for child in self.children:
            child.show_details(indent + 1)
    
    def get_size(self):
        return sum(child.get_size() for child in self.children)

# Usage
# Create files
file1 = File("document.txt", 150)
file2 = File("image.jpg", 1200)
file3 = File("data.csv", 300)
file4 = File("notes.txt", 50)

# Create directories
root = Directory("Root")
documents = Directory("Documents")
pictures = Directory("Pictures")

# Build tree structure
documents.add(file1)
documents.add(file3)
documents.add(file4)

pictures.add(file2)

root.add(documents)
root.add(pictures)

# Display structure
root.show_details()
```

### 9. Decorator Pattern
Adds behavior to objects dynamically.

```python
from abc import ABC, abstractmethod

# Component
class Coffee(ABC):
    @abstractmethod
    def cost(self):
        pass
    
    @abstractmethod
    def description(self):
        pass

# Concrete Component
class SimpleCoffee(Coffee):
    def cost(self):
        return 5
    
    def description(self):
        return "Simple coffee"

# Base Decorator
class CoffeeDecorator(Coffee):
    def __init__(self, coffee: Coffee):
        self._coffee = coffee
    
    def cost(self):
        return self._coffee.cost()
    
    def description(self):
        return self._coffee.description()

# Concrete Decorators
class MilkDecorator(CoffeeDecorator):
    def cost(self):
        return self._coffee.cost() + 2
    
    def description(self):
        return self._coffee.description() + ", milk"

class SugarDecorator(CoffeeDecorator):
    def cost(self):
        return self._coffee.cost() + 1
    
    def description(self):
        return self._coffee.description() + ", sugar"

class WhippedCreamDecorator(CoffeeDecorator):
    def cost(self):
        return self._coffee.cost() + 3
    
    def description(self):
        return self._coffee.description() + ", whipped cream"

class CaramelDecorator(CoffeeDecorator):
    def cost(self):
        return self._coffee.cost() + 4
    
    def description(self):
        return self._coffee.description() + ", caramel"

# Usage
coffee = SimpleCoffee()
print(f"{coffee.description()}: ${coffee.cost()}")

# Add decorators dynamically
coffee_with_milk = MilkDecorator(coffee)
coffee_with_milk_sugar = SugarDecorator(coffee_with_milk)
fancy_coffee = WhippedCreamDecorator(CaramelDecorator(coffee_with_milk_sugar))

print(f"{coffee_with_milk_sugar.description()}: ${coffee_with_milk_sugar.cost()}")
print(f"{fancy_coffee.description()}: ${fancy_coffee.cost()}")
```

### 10. Facade Pattern
Provides a simplified interface to a complex subsystem.

```python
# Complex subsystem classes
class CPU:
    def start(self):
        return "CPU: Starting..."
    
    def execute(self):
        return "CPU: Executing commands..."
    
    def shutdown(self):
        return "CPU: Shutting down..."

class Memory:
    def load(self):
        return "Memory: Loading data..."
    
    def free(self):
        return "Memory: Freeing memory..."

class HardDrive:
    def read(self):
        return "Hard Drive: Reading data..."
    
    def write(self):
        return "Hard Drive: Writing data..."

# Facade
class ComputerFacade:
    def __init__(self):
        self.cpu = CPU()
        self.memory = Memory()
        self.hard_drive = HardDrive()
    
    def start_computer(self):
        results = []
        results.append(self.cpu.start())
        results.append(self.memory.load())
        results.append(self.hard_drive.read())
        results.append(self.cpu.execute())
        return "\n".join(results)
    
    def shutdown_computer(self):
        results = []
        results.append(self.hard_drive.write())
        results.append(self.memory.free())
        results.append(self.cpu.shutdown())
        return "\n".join(results)

# Client code
computer = ComputerFacade()
print("=== Starting Computer ===")
print(computer.start_computer())
print("\n=== Shutting Down Computer ===")
print(computer.shutdown_computer())
```

### 11. Flyweight Pattern
Minimizes memory usage by sharing as much data as possible with similar objects.

```python
import json
from typing import Dict

# Flyweight
class TreeType:
    def __init__(self, name, color, texture):
        self.name = name
        self.color = color
        self.texture = texture
    
    def display(self, x, y):
        return f"Displaying {self.name} tree at ({x}, {y}) with color {self.color} and texture {self.texture}"

# Flyweight Factory
class TreeFactory:
    _tree_types: Dict[str, TreeType] = {}
    
    @classmethod
    def get_tree_type(cls, name, color, texture):
        key = f"{name}_{color}_{texture}"
        if key not in cls._tree_types:
            cls._tree_types[key] = TreeType(name, color, texture)
            print(f"Creating new TreeType: {key}")
        return cls._tree_types[key]

# Context
class Tree:
    def __init__(self, x, y, tree_type: TreeType):
        self.x = x
        self.y = y
        self.tree_type = tree_type
    
    def display(self):
        return self.tree_type.display(self.x, self.y)

class Forest:
    def __init__(self):
        self.trees = []
    
    def plant_tree(self, x, y, name, color, texture):
        tree_type = TreeFactory.get_tree_type(name, color, texture)
        tree = Tree(x, y, tree_type)
        self.trees.append(tree)
    
    def display(self):
        return [tree.display() for tree in self.trees]

# Usage
forest = Forest()

# Plant trees - same types will be reused
forest.plant_tree(1, 1, "Oak", "Green", "Rough")
forest.plant_tree(2, 3, "Pine", "Dark Green", "Smooth")
forest.plant_tree(3, 5, "Oak", "Green", "Rough")  # Reuses existing Oak type
forest.plant_tree(4, 7, "Maple", "Red", "Smooth")
forest.plant_tree(5, 9, "Pine", "Dark Green", "Smooth")  # Reuses existing Pine type

# Display all trees
for result in forest.display():
    print(result)

print(f"\nTotal TreeType objects created: {len(TreeFactory._tree_types)}")
```

### 12. Proxy Pattern
Provides a surrogate or placeholder for another object to control access to it.

```python
from abc import ABC, abstractmethod
import time

# Subject
class DatabaseQuery(ABC):
    @abstractmethod
    def execute(self, query):
        pass

# Real Subject
class RealDatabaseQuery(DatabaseQuery):
    def execute(self, query):
        # Simulate expensive database operation
        print("Executing expensive database query...")
        time.sleep(2)
        return f"Results for: {query}"

# Proxy
class DatabaseQueryProxy(DatabaseQuery):
    def __init__(self):
        self._real_subject = None
        self._cache = {}
    
    def execute(self, query):
        # Lazy initialization
        if self._real_subject is None:
            self._real_subject = RealDatabaseQuery()
        
        # Cache implementation
        if query in self._cache:
            print("Returning cached results...")
            return self._cache[query]
        
        # Access control and logging
        print(f"Logging query: {query}")
        result = self._real_subject.execute(query)
        self._cache[query] = result
        return result

# Virtual Proxy for lazy loading
class LazyImage:
    def __init__(self, filename):
        self.filename = filename
        self._image = None
    
    def display(self):
        if self._image is None:
            print(f"Loading image: {self.filename}")
            self._image = f"Image data for {self.filename}"
        print(f"Displaying: {self.filename}")

# Usage
print("=== Database Query Proxy ===")
proxy = DatabaseQueryProxy()

# First query - slow
print(proxy.execute("SELECT * FROM users"))
print()

# Same query again - fast (cached)
print(proxy.execute("SELECT * FROM users"))
print()

# Different query - slow
print(proxy.execute("SELECT * FROM orders"))
print()

print("=== Lazy Loading Proxy ===")
image = LazyImage("photo.jpg")
# Image not loaded yet
image.display()  # Loads and displays
image.display()  # Already loaded, just displays
```

## Behavioral Patterns

### 13. Chain of Responsibility Pattern
Passes requests along a chain of handlers.

```python
from abc import ABC, abstractmethod

class Handler(ABC):
    def __init__(self):
        self._next_handler = None
    
    def set_next(self, handler):
        self._next_handler = handler
        return handler
    
    @abstractmethod
    def handle(self, request):
        if self._next_handler:
            return self._next_handler.handle(request)
        return None

class ConcreteHandler1(Handler):
    def handle(self, request):
        if request == "A":
            return f"Handler1: Handling request {request}"
        else:
            return super().handle(request)

class ConcreteHandler2(Handler):
    def handle(self, request):
        if request == "B":
            return f"Handler2: Handling request {request}"
        else:
            return super().handle(request)

class ConcreteHandler3(Handler):
    def handle(self, request):
        if request == "C":
            return f"Handler3: Handling request {request}"
        else:
            return super().handle(request)

class DefaultHandler(Handler):
    def handle(self, request):
        return f"DefaultHandler: No one could handle request {request}"

# Usage
handler1 = ConcreteHandler1()
handler2 = ConcreteHandler2()
handler3 = ConcreteHandler3()
default = DefaultHandler()

# Build chain
handler1.set_next(handler2).set_next(handler3).set_next(default)

# Process requests
requests = ["A", "B", "C", "D", "E"]
for request in requests:
    result = handler1.handle(request)
    print(result)
```

### 14. Command Pattern
Turns requests into stand-alone objects.

```python
from abc import ABC, abstractmethod
from typing import List

# Command Interface
class Command(ABC):
    @abstractmethod
    def execute(self):
        pass
    
    @abstractmethod
    def undo(self):
        pass

# Receiver
class Light:
    def turn_on(self):
        return "Light is ON"
    
    def turn_off(self):
        return "Light is OFF"

class TV:
    def turn_on(self):
        return "TV is ON"
    
    def turn_off(self):
        return "TV is OFF"
    
    def set_channel(self, channel):
        return f"TV channel set to {channel}"

# Concrete Commands
class LightOnCommand(Command):
    def __init__(self, light: Light):
        self.light = light
        self.previous_state = None
    
    def execute(self):
        self.previous_state = "off"
        return self.light.turn_on()
    
    def undo(self):
        if self.previous_state == "off":
            return self.light.turn_off()
        return "Nothing to undo"

class LightOffCommand(Command):
    def __init__(self, light: Light):
        self.light = light
        self.previous_state = None
    
    def execute(self):
        self.previous_state = "on"
        return self.light.turn_off()
    
    def undo(self):
        if self.previous_state == "on":
            return self.light.turn_on()
        return "Nothing to undo"

class TVOnCommand(Command):
    def __init__(self, tv: TV):
        self.tv = tv
        self.previous_state = None
    
    def execute(self):
        self.previous_state = "off"
        return self.tv.turn_on()
    
    def undo(self):
        if self.previous_state == "off":
            return self.tv.turn_off()
        return "Nothing to undo"

# Invoker
class RemoteControl:
    def __init__(self):
        self._commands: List[Command] = []
    
    def execute_command(self, command: Command):
        result = command.execute()
        self._commands.append(command)
        return result
    
    def undo_last_command(self):
        if self._commands:
            command = self._commands.pop()
            return command.undo()
        return "No commands to undo"

# Usage
light = Light()
tv = TV()

light_on = LightOnCommand(light)
light_off = LightOffCommand(light)
tv_on = TVOnCommand(tv)

remote = RemoteControl()

print(remote.execute_command(light_on))  # Light is ON
print(remote.execute_command(tv_on))     # TV is ON
print(remote.execute_command(light_off)) # Light is OFF

print(remote.undo_last_command())        # Light is ON
print(remote.undo_last_command())        # TV is OFF
print(remote.undo_last_command())        # Light is OFF
```

### 15. Interpreter Pattern
Defines a grammatical representation for a language and an interpreter to interpret sentences.

```python
from abc import ABC, abstractmethod
from typing import Dict

# Abstract Expression
class Expression(ABC):
    @abstractmethod
    def interpret(self, context: Dict) -> int:
        pass

# Terminal Expressions
class Number(Expression):
    def __init__(self, value: int):
        self.value = value
    
    def interpret(self, context: Dict) -> int:
        return self.value

class Variable(Expression):
    def __init__(self, name: str):
        self.name = name
    
    def interpret(self, context: Dict) -> int:
        return context.get(self.name, 0)

# Non-terminal Expressions
class Add(Expression):
    def __init__(self, left: Expression, right: Expression):
        self.left = left
        self.right = right
    
    def interpret(self, context: Dict) -> int:
        return self.left.interpret(context) + self.right.interpret(context)

class Subtract(Expression):
    def __init__(self, left: Expression, right: Expression):
        self.left = left
        self.right = right
    
    def interpret(self, context: Dict) -> int:
        return self.left.interpret(context) - self.right.interpret(context)

class Multiply(Expression):
    def __init__(self, left: Expression, right: Expression):
        self.left = left
        self.right = right
    
    def interpret(self, context: Dict) -> int:
        return self.left.interpret(context) * self.right.interpret(context)

# Parser (simplified)
class Parser:
    def parse(self, expression: str) -> Expression:
        tokens = expression.split()
        return self._parse_expression(tokens)
    
    def _parse_expression(self, tokens):
        if len(tokens) == 1:
            token = tokens[0]
            if token.isdigit():
                return Number(int(token))
            else:
                return Variable(token)
        
        # Simple parsing for binary operations
        if '+' in tokens:
            index = tokens.index('+')
            left = self._parse_expression(tokens[:index])
            right = self._parse_expression(tokens[index+1:])
            return Add(left, right)
        elif '-' in tokens:
            index = tokens.index('-')
            left = self._parse_expression(tokens[:index])
            right = self._parse_expression(tokens[index+1:])
            return Subtract(left, right)
        elif '*' in tokens:
            index = tokens.index('*')
            left = self._parse_expression(tokens[:index])
            right = self._parse_expression(tokens[index+1:])
            return Multiply(left, right)

# Usage
context = {'x': 5, 'y': 3, 'z': 2}

parser = Parser()

# Parse and interpret expressions
expressions = [
    "10",
    "x",
    "x + y",
    "x * y + z",
    "x - y * z"
]

for expr in expressions:
    parsed_expr = parser.parse(expr)
    result = parsed_expr.interpret(context)
    print(f"{expr} = {result}")
```

### 16. Iterator Pattern
Provides a way to access elements of an aggregate object sequentially.

```python
from abc import ABC, abstractmethod
from typing import List, Any

# Iterator Interface
class Iterator(ABC):
    @abstractmethod
    def has_next(self) -> bool:
        pass
    
    @abstractmethod
    def next(self) -> Any:
        pass

# Aggregate Interface
class Aggregate(ABC):
    @abstractmethod
    def create_iterator(self) -> Iterator:
        pass

# Concrete Iterator
class ListIterator(Iterator):
    def __init__(self, collection: List[Any]):
        self._collection = collection
        self._position = 0
    
    def has_next(self) -> bool:
        return self._position < len(self._collection)
    
    def next(self) -> Any:
        if self.has_next():
            item = self._collection[self._position]
            self._position += 1
            return item
        raise StopIteration()

# Concrete Aggregate
class NumberCollection(Aggregate):
    def __init__(self):
        self._numbers: List[int] = []
    
    def add_number(self, number: int):
        self._numbers.append(number)
    
    def create_iterator(self) -> Iterator:
        return ListIterator(self._numbers)

# Pythonic way using generators
def number_generator(collection: List[int]):
    for number in collection:
        yield number

# Usage
print("=== Traditional Iterator ===")
collection = NumberCollection()
collection.add_number(1)
collection.add_number(2)
collection.add_number(3)
collection.add_number(5)
collection.add_number(8)

iterator = collection.create_iterator()

while iterator.has_next():
    print(iterator.next())

print("\n=== Python Generator ===")
numbers = [1, 2, 3, 5, 8, 13]
gen = number_generator(numbers)

for number in gen:
    print(number)

print("\n=== Built-in Python Iteration ===")
# Python has built-in iterator protocol
class FibonacciSequence:
    def __init__(self, limit):
        self.limit = limit
    
    def __iter__(self):
        self.a, self.b = 0, 1
        self.count = 0
        return self
    
    def __next__(self):
        if self.count >= self.limit:
            raise StopIteration
        self.a, self.b = self.b, self.a + self.b
        self.count += 1
        return self.a

fib = FibonacciSequence(10)
for num in fib:
    print(num, end=" ")
```

### 17. Mediator Pattern
Defines an object that encapsulates how a set of objects interact.

```python
from abc import ABC, abstractmethod
from typing import List

# Mediator Interface
class Mediator(ABC):
    @abstractmethod
    def notify(self, sender, event):
        pass

# Base Component
class BaseComponent:
    def __init__(self, mediator: Mediator = None):
        self._mediator = mediator
    
    @property
    def mediator(self):
        return self._mediator
    
    @mediator.setter
    def mediator(self, mediator: Mediator):
        self._mediator = mediator

# Concrete Components
class Button(BaseComponent):
    def click(self):
        print("Button: Clicked!")
        self.mediator.notify(self, "click")

class TextBox(BaseComponent):
    def __init__(self, mediator: Mediator = None):
        super().__init__(mediator)
        self._text = ""
    
    def set_text(self, text):
        self._text = text
        print(f"TextBox: Text set to '{text}'")
        self.mediator.notify(self, "text_changed")
    
    def get_text(self):
        return self._text

class CheckBox(BaseComponent):
    def __init__(self, mediator: Mediator = None):
        super().__init__(mediator)
        self._checked = False
    
    def toggle(self):
        self._checked = not self._checked
        state = "checked" if self._checked else "unchecked"
        print(f"CheckBox: Toggled to {state}")
        self.mediator.notify(self, "toggled")

# Concrete Mediator
class DialogMediator(Mediator):
    def __init__(self, button: Button, textbox: TextBox, checkbox: CheckBox):
        self._button = button
        self._button.mediator = self
        self._textbox = textbox
        self._textbox.mediator = self
        self._checkbox = checkbox
        self._checkbox.mediator = self
    
    def notify(self, sender, event):
        if isinstance(sender, Button) and event == "click":
            print("Mediator: Button clicked, validating form...")
            if self._textbox.get_text() and self._checkbox._checked:
                print("Mediator: Form is valid! Submitting...")
            else:
                print("Mediator: Form is invalid!")
        
        elif isinstance(sender, TextBox) and event == "text_changed":
            print("Mediator: Text changed, updating button state...")
            # Enable/disable button based on text presence
            button_state = "enabled" if self._textbox.get_text() else "disabled"
            print(f"Mediator: Button {button_state}")
        
        elif isinstance(sender, CheckBox) and event == "toggled":
            print("Mediator: Checkbox toggled, updating form state...")

# Usage
button = Button()
textbox = TextBox()
checkbox = CheckBox()

mediator = DialogMediator(button, textbox, checkbox)

print("=== User Interaction Simulation ===")
textbox.set_text("Hello World")
checkbox.toggle()
button.click()

print("\n=== Another Interaction ===")
textbox.set_text("")  # Clear text
button.click()
```

### 18. Memento Pattern
Captures and externalizes an object's internal state without violating encapsulation.

```python
from typing import List
from datetime import datetime

# Memento
class TextEditorMemento:
    def __init__(self, content: str):
        self._content = content
        self._timestamp = datetime.now()
    
    def get_content(self):
        return self._content
    
    def get_timestamp(self):
        return self._timestamp
    
    def __str__(self):
        return f"{self._timestamp.strftime('%Y-%m-%d %H:%M:%S')}: {self._content[:20]}..."

# Originator
class TextEditor:
    def __init__(self):
        self._content = ""
    
    def write(self, text: str):
        self._content += text
    
    def get_content(self):
        return self._content
    
    def save(self) -> TextEditorMemento:
        return TextEditorMemento(self._content)
    
    def restore(self, memento: TextEditorMemento):
        self._content = memento.get_content()

# Caretaker
class History:
    def __init__(self):
        self._mementos: List[TextEditorMemento] = []
    
    def push(self, memento: TextEditorMemento):
        self._mementos.append(memento)
    
    def pop(self) -> TextEditorMemento:
        if self._mementos:
            return self._mementos.pop()
        return None
    
    def list_saves(self):
        return [str(memento) for memento in self._mementos]

# Usage
editor = TextEditor()
history = History()

# Edit and save states
editor.write("Hello, ")
history.push(editor.save())

editor.write("World! ")
history.push(editor.save())

editor.write("This is a demo of Memento pattern.")
history.push(editor.save())

print("Current content:", editor.get_content())
print("\nSave history:")
for save in history.list_saves():
    print(f" - {save}")

# Undo changes
print("\n=== Undoing changes ===")
editor.restore(history.pop())
print("After undo:", editor.get_content())

editor.restore(history.pop())
print("After second undo:", editor.get_content())

editor.restore(history.pop())
print("After third undo:", editor.get_content())
```

### 19. Observer Pattern
Defines a one-to-many dependency between objects so that when one object changes state, all its dependents are notified.

```python
from abc import ABC, abstractmethod
from typing import List

# Observer Interface
class Observer(ABC):
    @abstractmethod
    def update(self, temperature: float, humidity: float, pressure: float):
        pass

# Subject Interface
class Subject(ABC):
    @abstractmethod
    def register_observer(self, observer: Observer):
        pass
    
    @abstractmethod
    def remove_observer(self, observer: Observer):
        pass
    
    @abstractmethod
    def notify_observers(self):
        pass

# Concrete Subject
class WeatherStation(Subject):
    def __init__(self):
        self._observers: List[Observer] = []
        self._temperature = 0.0
        self._humidity = 0.0
        self._pressure = 0.0
    
    def register_observer(self, observer: Observer):
        self._observers.append(observer)
    
    def remove_observer(self, observer: Observer):
        self._observers.remove(observer)
    
    def notify_observers(self):
        for observer in self._observers:
            observer.update(self._temperature, self._humidity, self._pressure)
    
    def measurements_changed(self):
        self.notify_observers()
    
    def set_measurements(self, temperature: float, humidity: float, pressure: float):
        self._temperature = temperature
        self._humidity = humidity
        self._pressure = pressure
        self.measurements_changed()
    
    def get_temperature(self):
        return self._temperature
    
    def get_humidity(self):
        return self._humidity
    
    def get_pressure(self):
        return self._pressure

# Concrete Observers
class CurrentConditionsDisplay(Observer):
    def __init__(self, weather_station: WeatherStation):
        self._weather_station = weather_station
        self._temperature = 0.0
        self._humidity = 0.0
        weather_station.register_observer(self)
    
    def update(self, temperature: float, humidity: float, pressure: float):
        self._temperature = temperature
        self._humidity = humidity
        self.display()
    
    def display(self):
        print(f"Current conditions: {self._temperature}°C and {self._humidity}% humidity")

class StatisticsDisplay(Observer):
    def __init__(self, weather_station: WeatherStation):
        self._weather_station = weather_station
        self._max_temp = 0.0
        self._min_temp = 200.0
        self._temp_sum = 0.0
        self._num_readings = 0
        weather_station.register_observer(self)
    
    def update(self, temperature: float, humidity: float, pressure: float):
        self._temp_sum += temperature
        self._num_readings += 1
        
        if temperature > self._max_temp:
            self._max_temp = temperature
        
        if temperature < self._min_temp:
            self._min_temp = temperature
        
        self.display()
    
    def display(self):
        avg_temp = self._temp_sum / self._num_readings
        print(f"Avg/Max/Min temperature: {avg_temp:.1f}/{self._max_temp:.1f}/{self._min_temp:.1f}")

class ForecastDisplay(Observer):
    def __init__(self, weather_station: WeatherStation):
        self._weather_station = weather_station
        self._last_pressure = 0.0
        self._current_pressure = 0.0
        weather_station.register_observer(self)
    
    def update(self, temperature: float, humidity: float, pressure: float):
        self._last_pressure = self._current_pressure
        self._current_pressure = pressure
        self.display()
    
    def display(self):
        if self._current_pressure > self._last_pressure:
            forecast = "Improving weather on the way!"
        elif self._current_pressure == self._last_pressure:
            forecast = "More of the same"
        else:
            forecast = "Watch out for cooler, rainy weather"
        print(f"Forecast: {forecast}")

# Usage
weather_station = WeatherStation()

current_display = CurrentConditionsDisplay(weather_station)
stats_display = StatisticsDisplay(weather_station)
forecast_display = ForecastDisplay(weather_station)

print("=== Weather Station Updates ===")
weather_station.set_measurements(25.0, 65, 1013.1)
print()

weather_station.set_measurements(26.5, 70, 1012.5)
print()

weather_station.set_measurements(23.0, 90, 1014.0)
print()

# Remove an observer
weather_station.remove_observer(forecast_display)
print("=== After removing forecast display ===")
weather_station.set_measurements(21.0, 75, 1015.0)
```

### 20. State Pattern
Allows an object to alter its behavior when its internal state changes.

```python
from abc import ABC, abstractmethod

# State Interface
class State(ABC):
    @abstractmethod
    def insert_coin(self, vending_machine):
        pass
    
    @abstractmethod
    def eject_coin(self, vending_machine):
        pass
    
    @abstractmethod
    def select_product(self, vending_machine, product):
        pass
    
    @abstractmethod
    def dispense(self, vending_machine):
        pass

# Concrete States
class NoCoinState(State):
    def insert_coin(self, vending_machine):
        print("Coin inserted")
        vending_machine.set_state(vending_machine.has_coin_state)
    
    def eject_coin(self, vending_machine):
        print("No coin to eject")
    
    def select_product(self, vending_machine, product):
        print("Please insert a coin first")
    
    def dispense(self, vending_machine):
        print("Please insert a coin first")

class HasCoinState(State):
    def insert_coin(self, vending_machine):
        print("Coin already inserted")
    
    def eject_coin(self, vending_machine):
        print("Coin ejected")
        vending_machine.set_state(vending_machine.no_coin_state)
    
    def select_product(self, vending_machine, product):
        if vending_machine.has_product(product):
            print(f"Product {product} selected")
            vending_machine.set_state(vending_machine.sold_state)
            vending_machine.selected_product = product
        else:
            print(f"Product {product} is out of stock")
            vending_machine.set_state(vending_machine.no_coin_state)

    def dispense(self, vending_machine):
        print("Please select a product first")

class SoldState(State):
    def insert_coin(self, vending_machine):
        print("Please wait, dispensing product")
    
    def eject_coin(self, vending_machine):
        print("Sorry, product already selected")
    
    def select_product(self, vending_machine, product):
        print("Product already selected")
    
    def dispense(self, vending_machine):
        vending_machine.release_product(vending_machine.selected_product)
        if vending_machine.get_count(vending_machine.selected_product) > 0:
            vending_machine.set_state(vending_machine.no_coin_state)
        else:
            vending_machine.set_state(vending_machine.sold_out_state)
        vending_machine.selected_product = None

class SoldOutState(State):
    def insert_coin(self, vending_machine):
        print("Sorry, machine is sold out")
    
    def eject_coin(self, vending_machine):
        print("No coin to eject")
    
    def select_product(self, vending_machine, product):
        print("Sorry, machine is sold out")
    
    def dispense(self, vending_machine):
        print("No product to dispense")

# Context
class VendingMachine:
    def __init__(self):
        self.no_coin_state = NoCoinState()
        self.has_coin_state = HasCoinState()
        self.sold_state = SoldState()
        self.sold_out_state = SoldOutState()
        
        self.state = self.no_coin_state
        self.selected_product = None
        
        # Inventory
        self.products = {
            "A1": {"name": "Coke", "count": 5},
            "A2": {"name": "Pepsi", "count": 3},
            "B1": {"name": "Chips", "count": 0}  # Sold out
        }
    
    def set_state(self, state: State):
        self.state = state
    
    def has_product(self, product_code):
        return (product_code in self.products and 
                self.products[product_code]["count"] > 0)
    
    def get_count(self, product_code):
        return self.products[product_code]["count"]
    
    def release_product(self, product_code):
        if self.products[product_code]["count"] > 0:
            self.products[product_code]["count"] -= 1
            product_name = self.products[product_code]["name"]
            print(f"Dispensing {product_name}")
    
    # Delegated methods
    def insert_coin(self):
        self.state.insert_coin(self)
    
    def eject_coin(self):
        self.state.eject_coin(self)
    
    def select_product(self, product_code):
        self.state.select_product(self, product_code)
    
    def dispense(self):
        self.state.dispense(self)
    
    def display_inventory(self):
        print("\n=== Inventory ===")
        for code, info in self.products.items():
            status = "In stock" if info["count"] > 0 else "Sold out"
            print(f"{code}: {info['name']} - {status} ({info['count']} left)")

# Usage
vending_machine = VendingMachine()

vending_machine.display_inventory()

print("\n=== User Interactions ===")
# Try to select without coin
vending_machine.select_product("A1")

# Insert coin and select product
vending_machine.insert_coin()
vending_machine.select_product("A1")
vending_machine.dispense()

print("\n=== Another Interaction ===")
# Try sold out product
vending_machine.insert_coin()
vending_machine.select_product("B1")

print("\n=== Final Inventory ===")
vending_machine.display_inventory()
```

### 21. Strategy Pattern
Defines a family of algorithms, encapsulates each one, and makes them interchangeable.

```python
from abc import ABC, abstractmethod
from typing import List

# Strategy Interface
class SortStrategy(ABC):
    @abstractmethod
    def sort(self, data: List) -> List:
        pass

# Concrete Strategies
class BubbleSortStrategy(SortStrategy):
    def sort(self, data: List) -> List:
        print("Sorting using Bubble Sort")
        # Simplified bubble sort implementation
        n = len(data)
        for i in range(n):
            for j in range(0, n - i - 1):
                if data[j] > data[j + 1]:
                    data[j], data[j + 1] = data[j + 1], data[j]
        return data

class QuickSortStrategy(SortStrategy):
    def sort(self, data: List) -> List:
        print("Sorting using Quick Sort")
        if len(data) <= 1:
            return data
        pivot = data[len(data) // 2]
        left = [x for x in data if x < pivot]
        middle = [x for x in data if x == pivot]
        right = [x for x in data if x > pivot]
        return self.sort(left) + middle + self.sort(right)

class MergeSortStrategy(SortStrategy):
    def sort(self, data: List) -> List:
        print("Sorting using Merge Sort")
        if len(data) <= 1:
            return data
        
        mid = len(data) // 2
        left = self.sort(data[:mid])
        right = self.sort(data[mid:])
        
        return self.merge(left, right)
    
    def merge(self, left, right):
        result = []
        i = j = 0
        
        while i < len(left) and j < len(right):
            if left[i] < right[j]:
                result.append(left[i])
                i += 1
            else:
                result.append(right[j])
                j += 1
        
        result.extend(left[i:])
        result.extend(right[j:])
        return result

# Context
class Sorter:
    def __init__(self, strategy: SortStrategy = None):
        self._strategy = strategy or BubbleSortStrategy()
    
    def set_strategy(self, strategy: SortStrategy):
        self._strategy = strategy
    
    def sort_data(self, data: List) -> List:
        return self._strategy.sort(data.copy())

# Usage
data = [64, 34, 25, 12, 22, 11, 90, 5]

sorter = Sorter()

print("Original data:", data)

# Use different strategies
strategies = {
    "Bubble Sort": BubbleSortStrategy(),
    "Quick Sort": QuickSortStrategy(),
    "Merge Sort": MergeSortStrategy()
}

for name, strategy in strategies.items():
    sorter.set_strategy(strategy)
    sorted_data = sorter.sort_data(data)
    print(f"{name}: {sorted_data}")

# Real-world example: Payment processing
class PaymentStrategy(ABC):
    @abstractmethod
    def pay(self, amount: float) -> str:
        pass

class CreditCardPayment(PaymentStrategy):
    def __init__(self, card_number, expiry_date):
        self.card_number = card_number
        self.expiry_date = expiry_date
    
    def pay(self, amount: float) -> str:
        return f"Paid ${amount:.2f} using Credit Card ending in {self.card_number[-4:]}"

class PayPalPayment(PaymentStrategy):
    def __init__(self, email):
        self.email = email
    
    def pay(self, amount: float) -> str:
        return f"Paid ${amount:.2f} using PayPal ({self.email})"

class CryptoPayment(PaymentStrategy):
    def __init__(self, wallet_address):
        self.wallet_address = wallet_address
    
    def pay(self, amount: float) -> str:
        return f"Paid ${amount:.2f} using Crypto (Wallet: {self.wallet_address[:8]}...)"

class ShoppingCart:
    def __init__(self):
        self.items = []
        self.payment_strategy = None
    
    def add_item(self, item, price):
        self.items.append((item, price))
    
    def set_payment_strategy(self, strategy: PaymentStrategy):
        self.payment_strategy = strategy
    
    def checkout(self):
        if not self.payment_strategy:
            return "Please set payment method first"
        
        total = sum(price for _, price in self.items)
        result = self.payment_strategy.pay(total)
        self.items.clear()
        return result

# Usage for payment processing
cart = ShoppingCart()
cart.add_item("Laptop", 999.99)
cart.add_item("Mouse", 29.99)

# Different payment methods
cart.set_payment_strategy(CreditCardPayment("1234567812345678", "12/25"))
print(cart.checkout())

cart.add_item("Keyboard", 79.99)
cart.set_payment_strategy(PayPalPayment("user@example.com"))
print(cart.checkout())

cart.add_item("Monitor", 299.99)
cart.set_payment_strategy(CryptoPayment("1A2b3C4d5E6f7G8h9I0j"))
print(cart.checkout())
```

### 22. Template Method Pattern
Defines the skeleton of an algorithm in the base class but lets subclasses override specific steps.

```python
from abc import ABC, abstractmethod

# Abstract Class
class DataProcessor(ABC):
    # Template method
    def process(self, data):
        self.validate_data(data)
        cleaned_data = self.clean_data(data)
        transformed_data = self.transform_data(cleaned_data)
        result = self.analyze_data(transformed_data)
        self.generate_report(result)
        return result
    
    def validate_data(self, data):
        print("Validating data...")
        if not data:
            raise ValueError("Data cannot be empty")
    
    @abstractmethod
    def clean_data(self, data):
        pass
    
    @abstractmethod
    def transform_data(self, data):
        pass
    
    def analyze_data(self, data):
        print("Analyzing data...")
        return f"Analysis result for {len(data)} records"
    
    def generate_report(self, result):
        print(f"Generating report: {result}")

# Concrete Classes
class CSVDataProcessor(DataProcessor):
    def clean_data(self, data):
        print("Cleaning CSV data: Removing empty rows, handling missing values")
        return [row for row in data if row]  # Remove empty rows
    
    def transform_data(self, data):
        print("Transforming CSV data: Parsing columns, converting types")
        return [f"CSV_{item}" for item in data]

class JSONDataProcessor(DataProcessor):
    def clean_data(self, data):
        print("Cleaning JSON data: Validating schema, removing invalid objects")
        return [item for item in data if isinstance(item, dict)]
    
    def transform_data(self, data):
        print("Transforming JSON data: Flattening nested structures")
        return [f"JSON_{item}" for item in data]
    
    def analyze_data(self, data):
        print("Performing advanced JSON analysis...")
        return f"JSON Analysis: {len(data)} valid objects"

class XMLDataProcessor(DataProcessor):
    def clean_data(self, data):
        print("Cleaning XML data: Removing invalid tags, handling namespaces")
        return [item for item in data if item.startswith('<')]
    
    def transform_data(self, data):
        print("Transforming XML data: Converting to object model")
        return [f"XML_{item}" for item in data]
    
    def generate_report(self, result):
        print(f"Generating XML-specific report: {result}")

# Usage
print("=== CSV Data Processing ===")
csv_processor = CSVDataProcessor()
csv_data = ["row1", "row2", "", "row4"]
csv_processor.process(csv_data)

print("\n=== JSON Data Processing ===")
json_processor = JSONDataProcessor()
json_data = [{"name": "John"}, "invalid", {"age": 30}]
json_processor.process(json_data)

print("\n=== XML Data Processing ===")
xml_processor = XMLDataProcessor()
xml_data = ["<user>John</user>", "invalid", "<product>123</product>"]
xml_processor.process(xml_data)
```

### 23. Visitor Pattern
Represents an operation to be performed on elements of an object structure.

```python
from abc import ABC, abstractmethod
from typing import List

# Element Interface
class Element(ABC):
    @abstractmethod
    def accept(self, visitor):
        pass

# Concrete Elements
class Book(Element):
    def __init__(self, title, price, weight):
        self.title = title
        self.price = price
        self.weight = weight  # in grams
    
    def accept(self, visitor):
        return visitor.visit_book(self)

class Electronics(Element):
    def __init__(self, name, price, power_consumption):
        self.name = name
        self.price = price
        self.power_consumption = power_consumption  # in watts
    
    def accept(self, visitor):
        return visitor.visit_electronics(self)

class Clothing(Element):
    def __init__(self, item, price, size):
        self.item = item
        self.price = price
        self.size = size
    
    def accept(self, visitor):
        return visitor.visit_clothing(self)

# Visitor Interface
class Visitor(ABC):
    @abstractmethod
    def visit_book(self, book: Book):
        pass
    
    @abstractmethod
    def visit_electronics(self, electronics: Electronics):
        pass
    
    @abstractmethod
    def visit_clothing(self, clothing: Clothing):
        pass

# Concrete Visitors
class PriceCalculator(Visitor):
    def visit_book(self, book: Book):
        return book.price
    
    def visit_electronics(self, electronics: Electronics):
        return electronics.price
    
    def visit_clothing(self, clothing: Clothing):
        return clothing.price

class ShippingCalculator(Visitor):
    def visit_book(self, book: Book):
        # Books: $2 base + $0.50 per 100g
        return 2 + (book.weight / 100) * 0.50
    
    def visit_electronics(self, electronics: Electronics):
        # Electronics: $5 base + insurance (1% of price)
        return 5 + (electronics.price * 0.01)
    
    def visit_clothing(self, clothing: Clothing):
        # Clothing: $3 flat rate
        return 3

class DiscountCalculator(Visitor):
    def __init__(self, customer_type):
        self.customer_type = customer_type
    
    def visit_book(self, book: Book):
        if self.customer_type == "student":
            return book.price * 0.10  # 10% discount for students
        elif self.customer_type == "premium":
            return book.price * 0.05  # 5% discount for premium
        return 0
    
    def visit_electronics(self, electronics: Electronics):
        if self.customer_type == "premium":
            return electronics.price * 0.15  # 15% discount for premium
        return electronics.price * 0.05  # 5% default discount
    
    def visit_clothing(self, clothing: Clothing):
        if clothing.size in ["S", "M"]:
            return clothing.price * 0.10  # 10% discount for small/medium
        return 0

# Object Structure
class ShoppingCart:
    def __init__(self):
        self.items: List[Element] = []
    
    def add_item(self, item: Element):
        self.items.append(item)
    
    def calculate_total(self, visitor: Visitor):
        total = 0
        for item in self.items:
            total += item.accept(visitor)
        return total
    
    def generate_report(self):
        price_calc = PriceCalculator()
        shipping_calc = ShippingCalculator()
        discount_calc = DiscountCalculator("premium")
        
        print("=== Shopping Cart Report ===")
        total_price = self.calculate_total(price_calc)
        total_shipping = self.calculate_total(shipping_calc)
        total_discount = self.calculate_total(discount_calc)
        
        print(f"Total Price: ${total_price:.2f}")
        print(f"Total Shipping: ${total_shipping:.2f}")
        print(f"Total Discount: ${total_discount:.2f}")
        print(f"Final Amount: ${(total_price + total_shipping - total_discount):.2f}")

# Usage
cart = ShoppingCart()

# Add items to cart
cart.add_item(Book("Python Programming", 49.99, 500))
cart.add_item(Electronics("Laptop", 999.99, 65))
cart.add_item(Clothing("T-Shirt", 29.99, "M"))
cart.add_item(Book("Design Patterns", 39.99, 400))

# Calculate individual components
price_calculator = PriceCalculator()
shipping_calculator = ShippingCalculator()
discount_calculator = DiscountCalculator("premium")

print(f"Total Price: ${cart.calculate_total(price_calculator):.2f}")
print(f"Total Shipping: ${cart.calculate_total(shipping_calculator):.2f}")
print(f"Total Discount: ${cart.calculate_total(discount_calculator):.2f}")

# Generate comprehensive report
cart.generate_report()
```

## Summary Table

| Pattern | Category | Purpose | Key Concept |
|---------|----------|---------|-------------|
| Singleton | Creational | Ensure one instance | Single instance, global access |
| Factory Method | Creational | Create objects without specifying class | Subclasses decide object creation |
| Abstract Factory | Creational | Create families of related objects | Factory of factories |
| Builder | Creational | Construct complex objects step by step | Separate construction from representation |
| Prototype | Creational | Create objects by copying | Clone existing objects |
| Adapter | Structural | Make incompatible interfaces work together | Wrapper that converts interface |
| Bridge | Structural | Separate abstraction from implementation | Composition over inheritance |
| Composite | Structural | Treat individual and composite objects uniformly | Tree structure of objects |
| Decorator | Structural | Add responsibilities dynamically | Wrapper that adds behavior |
| Facade | Structural | Provide simplified interface | Unified interface to subsystem |
| Flyweight | Structural | Share objects to support large quantities | Intrinsic vs extrinsic state |
| Proxy | Structural | Control access to objects | Surrogate or placeholder |
| Chain of Responsibility | Behavioral | Pass request along chain of handlers | Decoupled sender and receiver |
| Command | Behavioral | Encapsulate request as object | Object-oriented callback |
| Interpreter | Behavioral | Define grammar and interpreter | Language processing |
| Iterator | Behavioral | Access elements sequentially | Traverse collection without exposing structure |
| Mediator | Behavioral | Define how objects interact | Centralized communication |
| Memento | Behavioral | Capture and restore object state | Snapshot of object state |
| Observer | Behavioral | One-to-many dependency | Publish-subscribe mechanism |
| State | Behavioral | Change behavior with state | Object behavior depends on state |
| Strategy | Behavioral | Define family of algorithms | Interchangeable algorithms |
| Template Method | Behavioral | Define algorithm skeleton | Let subclasses redefine steps |
| Visitor | Behavioral | Separate algorithm from object structure | Double dispatch |

These patterns provide proven solutions to common software design problems and can significantly improve code quality, maintainability, and flexibility when applied appropriately.