from abc import ABC, abstractmethod
from typing import List, Iterable

# Zoo Management System - Assignment 1
class Animal(ABC):
    def __init__(self, name: str, age: int, species: str):
        self.name = name
        if not self.validate_species(species):
            raise ValueError("Invalid species name provided")
        self.species = species
        self.__age = age
        self.__health = 100
        self.__happiness = 50

    # Properties for encapsulation
    @property
    def age(self) -> int:
        return self.__age

    @age.setter
    def age(self, value: int) -> None:
        if value < 0:
            raise ValueError("Age cannot be negative")
        self.__age = value

    @property
    def health(self) -> int:
        return self.__health

    @health.setter
    def health(self, value: int) -> None:
        if value < 0:
            self.__health = 0
        elif value > 100:
            self.__health = 100
        else:
            self.__health = value

    @property
    def happiness(self) -> int:
        return self.__happiness

    @happiness.setter
    def happiness(self, value: int) -> None:
        if value < 0:
            self.__happiness = 0
        elif value > 100:
            self.__happiness = 100
        else:
            self.__happiness = value

    @abstractmethod
    def make_sound(self) -> str:
        raise NotImplementedError

    def eat(self, food: str) -> str:
        self.health = min(self.health + 10, 100)
        return f"{self.name} is eating {food}."

    def sleep(self) -> str:
        self.health = min(self.health + 5, 100)
        return f"{self.name} is sleeping."

    def __str__(self) -> str:
        return (
            f"{self.name} the {self.species} (Age: {self.age}, "
            f"Health: {self.health}, Happiness: {self.happiness})"
        )

    @staticmethod
    def validate_species(species: str) -> bool:
        if not isinstance(species, str):
            return False
        stripped = species.strip()
        if stripped == "":
            return False
        return all(ch.isalpha() or ch in {" ", "-"} for ch in stripped)

    def _update_happiness(self) -> None:
        if self.health > 80:
            self.happiness = min(self.happiness + 5, 100)
        elif self.health < 40:
            self.happiness = max(self.happiness - 10, 0)
        else:
            self.happiness = max(self.happiness - 2, 0)

    def advance_day(self) -> None:
        self.age = self.age + 1
        self.health = max(self.health - 5, 0)
        self._update_happiness()

    @classmethod
    def from_birth(cls, name: str, **kwargs) -> "Animal":
        return cls(name=name, age=0, **kwargs)


class Mammal(Animal):
    def __init__(self, name: str, age: int, species: str, fur_color: str):
        super().__init__(name, age, species)
        self.fur_color = fur_color

    def nurse(self) -> str:
        return f"{self.name} is nursing its young."


class Bird(Animal):
    def __init__(self, name: str, age: int, species: str, wingspan: float):
        super().__init__(name, age, species)
        self.wingspan = wingspan

    def fly(self) -> str:
        return f"{self.name} is flying with a wingspan of {self.wingspan} meters."


class Reptile(Animal):
    def __init__(self, name: str, age: int, species: str, scale_type: str):
        super().__init__(name, age, species)
        self.scale_type = scale_type

    def bask(self) -> str:
        self.health = min(self.health + 15, 100)
        return f"{self.name} is basking in the sun."


class Lion(Mammal):  # Lion inherits from Mammal
    def __init__(self, name: str, age: int, gender: str):
        super().__init__(name, age, "Lion", "golden")
        self.gender = gender

    def make_sound(self) -> str:
        return "Roar!"

    def hunt(self) -> str:
        self.health = max(self.health - 5, 0)
        return f"{self.name} is hunting for prey."


class Penguin(Bird):
    def __init__(self, name: str, age: int):
        super().__init__(name, age, "Penguin", 0.3)

    def make_sound(self) -> str:
        return "Honk!"

    def swim(self) -> str:
        return f"{self.name} is swimming gracefully."


class Snake(Reptile):
    def __init__(self, name: str, age: int, length: float):
        super().__init__(name, age, "Snake", "smooth")
        self.length = length

    def make_sound(self) -> str:
        return "Hiss!"

    def shed_skin(self) -> str:
        self.health = min(self.health + 20, 100)
        return f"{self.name} is shedding its skin."


class Elephant(Mammal):
    def __init__(self, name: str, age: int, tusk_length: float):
        super().__init__(name, age, "Elephant", "gray")
        self.tusk_length = tusk_length

    def make_sound(self) -> str:
        return "Trumpet!"

    def spray_water(self) -> str:
        return f"{self.name} is spraying water with its trunk."


class Parrot(Bird):
    def __init__(self, name: str, age: int, vocabulary: List[str]):
        super().__init__(name, age, "Parrot", 0.5)
        self.vocabulary = vocabulary

    def make_sound(self) -> str:
        if self.vocabulary:
            return f"{self.name} says: {max(self.vocabulary, key=len)}"
        return "Squawk!"

    def learn_word(self, word: str) -> str:
        self.vocabulary.append(word)
        return f"{self.name} learned a new word: {word}"


# Employee classes
class Employee:
    def __init__(self, name: str, age: int, employee_id: str):
        self.name = name
        self.age = age
        self.employee_id = employee_id
        self.__salary = 30000

    @property
    def salary(self) -> int:
        return self.__salary

    @salary.setter
    def salary(self, value: int) -> None:
        if value < 0:
            raise ValueError("Salary cannot be negative")
        self.__salary = value

    def __str__(self) -> str:
        return f"{self.name} (ID: {self.employee_id}, Age: {self.age}, Salary: ${self.salary})"


class Veterinarian(Employee):
    def __init__(self, name: str, age: int, employee_id: str, specialization: str):
        super().__init__(name, age, employee_id)
        self.specialization = specialization
        self.salary = 50000

    def treat_animal(self, animal: Animal) -> str:
        animal.health = min(animal.health + 30, 100)
        return f"{self.name} treated {animal.name}. {animal.name}'s health is now {animal.health}."

    def __str__(self) -> str:
        return f"Veterinarian {super().__str__()} (Specialization: {self.specialization})"


class Zookeeper(Employee):
    def __init__(self, name: str, age: int, employee_id: str, area: str):
        super().__init__(name, age, employee_id)
        self.area = area
        self.salary = 40000

    def feed_animal(self, animal: Animal, food: str) -> str:
        return animal.eat(food)

    def move_animal(self, animal: Animal, from_enclosure: "Enclosure", to_enclosure: "Enclosure") -> str:
        if animal in from_enclosure.animals:
            from_enclosure.animals.remove(animal)
            to_enclosure.animals.append(animal)
            return f"{self.name} moved {animal.name} from {from_enclosure.name} to {to_enclosure.name}."
        return f"{animal.name} not found in {from_enclosure.name}."

    def __str__(self) -> str:
        return f"Zookeeper {super().__str__()} (Area: {self.area})"


class Enclosure:
    def __init__(self, name: str, size: str, habitat_type: str):
        self.name = name
        self.size = size
        self.habitat_type = habitat_type
        self.animals: List[Animal] = []

    def add_animal(self, animal: Animal) -> str:
        self.animals.append(animal)
        return f"{animal.name} was added to {self.name}."

    def remove_animal(self, animal: Animal) -> str:
        if animal in self.animals:
            self.animals.remove(animal)
            return f"{animal.name} was removed from {self.name}."
        return f"{animal.name} not found in {self.name}."

    def __add__(self, other: "Enclosure") -> "Enclosure":
        # combine two enclosures
        new_name = f"{self.name}_{other.name}_combined"
        new_size = "Large" if self.size == "Large" or other.size == "Large" else "Medium"
        new_habitat = f"{self.habitat_type}/{other.habitat_type}"
        new_enclosure = Enclosure(new_name, new_size, new_habitat)
        new_enclosure.animals = self.animals + other.animals
        return new_enclosure

    def __len__(self) -> int:
        return len(self.animals)

    def __iter__(self) -> Iterable[Animal]:
        return iter(self.animals)

    def __str__(self) -> str:
        animal_list = "\n".join([f"  - {animal}" for animal in self.animals])
        return (
            f"Enclosure: {self.name}\n"
            f"Size: {self.size}\n"
            f"Habitat Type: {self.habitat_type}\n"
            f"Animals ({len(self)}):\n{animal_list}"
        )


## More animals
class Fish(Animal):
    def __init__(self, name: str, age: int, species: str, water_type: str):
        # use Animal.__init__ directly for multiple inheritance
        Animal.__init__(self, name, age, species)
        self.water_type = water_type

    def make_sound(self) -> str:
        return "Blub!"

    def swim(self) -> str:
        return f"{self.name} is swimming in {self.water_type.lower()} water."


class FlyingFish(Fish, Bird):  # multiple inheritance
    def __init__(self, name: str, age: int, wingspan: float, water_type: str):
        Fish.__init__(self, name, age, "FlyingFish", water_type)
        self.wingspan = wingspan

    def make_sound(self) -> str:
        return "Blub-squeak!"

    def glide(self) -> str:
        return f"{self.name} glides above the water with a wingspan of {self.wingspan} meters."


class HybridAnimal(Fish, Bird):
    def __init__(self, name: str, age: int, species: str, wingspan: float, water_type: str):
        Fish.__init__(self, name, age, species, water_type)
        self.wingspan = wingspan

    def make_sound(self) -> str:
        return "Hybrid chirp-blub!"

    def move(self) -> str:
        return f"{self.name} swims and glides with a wingspan of {self.wingspan} meters."


def feed(animal, food: str) -> str:
    return animal.eat(food)

# Zoo management
class Zoo:
    def __init__(self, name: str):
        self.name = name
        self.enclosures: List[Enclosure] = []
        self.employees: List[Employee] = []
        self.day: int = 0

    def add_enclosure(self, enclosure: Enclosure) -> None:
        self.enclosures.append(enclosure)

    def hire_employee(self, employee: Employee) -> None:
        self.employees.append(employee)

    def add_animal_to_enclosure(self, animal: Animal, enclosure: Enclosure) -> None:
        enclosure.add_animal(animal)

    def __iter__(self) -> Iterable[Animal]:
        for enclosure in self.enclosures:
            for animal in enclosure:
                yield animal

    def _treat_sick_animals(self) -> None:
        veterinarians = [e for e in self.employees if isinstance(e, Veterinarian)]
        if not veterinarians:
            return
        for animal in self:
            if animal.health < 60:
                veterinarians[0].treat_animal(animal)

    def _keepers_do_rounds(self) -> None:
        keepers = [e for e in self.employees if isinstance(e, Zookeeper)]
        if not keepers:
            return
        keeper = keepers[0]
        for enclosure in self.enclosures:
            for animal in list(enclosure):
                feed(animal, "standard diet")
        if len(self.enclosures) >= 2 and any(len(e.animals) > 0 for e in self.enclosures):
            src = next((e for e in self.enclosures if len(e.animals) > 0), None)
            dst = next((e for e in self.enclosures if e is not src), None)
            if src and dst:
                keeper.move_animal(src.animals[0], src, dst)

    def simulate_day(self) -> None:
        self.day += 1
        for animal in self:
            animal.advance_day()
        self._treat_sick_animals()
        self._keepers_do_rounds()

    def __str__(self) -> str:
        total_animals = sum(len(e) for e in self.enclosures)
        enclosures_info = "\n\n".join(str(e) for e in self.enclosures)
        return (
            f"Zoo: {self.name} (Day {self.day})\n"
            f"Employees: {len(self.employees)}\n"
            f"Total Animals: {total_animals}\n\n"
            f"{enclosures_info}"
        )


def build_sample_zoo() -> Zoo:
    savannah = Enclosure("Savannah", "Large", "Grassland")
    arctic = Enclosure("Arctic", "Medium", "Cold")
    aquarium = Enclosure("Aquarium", "Large", "Water")

    zoo = Zoo("City Zoo")
    zoo.add_enclosure(savannah)
    zoo.add_enclosure(arctic)
    zoo.add_enclosure(aquarium)

    animals = [
        Lion.from_birth("Simba", gender="Male"),
        Lion("Nala", 3, "Female"),
        Elephant("Dumbo", 5, 1.0),
        Penguin.from_birth("Pingu"),
        Penguin("Skipper", 4),
        Snake("Kaa", 6, 2.4),
        Parrot("Polly", 2, ["Hello", "Cracker", "Goodbye"]),
        Fish("Nemo", 1, "Clownfish", "Saltwater"),
        FlyingFish("Skyfin", 2, wingspan=0.4, water_type="Saltwater"),
        HybridAnimal("Hydra", 3, "Hybrid", wingspan=0.6, water_type="Freshwater"),
    ]

    savannah.add_animal(animals[0])
    savannah.add_animal(animals[1])
    savannah.add_animal(animals[2])
    
    arctic.add_animal(animals[3])
    arctic.add_animal(animals[4])
    
    aquarium.add_animal(animals[5])
    aquarium.add_animal(animals[6])
    aquarium.add_animal(animals[7])
    aquarium.add_animal(animals[8])
    aquarium.add_animal(animals[9])

    vet = Veterinarian("Dr. Jane", 40, "VET001", "General")
    keeper = Zookeeper("Bob", 32, "KEEP001", "All")
    zoo.hire_employee(vet)
    zoo.hire_employee(keeper)
    
    return zoo


def run_simulation(days: int = 3) -> None:
    zoo = build_sample_zoo()
    for i in range(days):
        zoo.simulate_day()
        print(zoo)
        print("-" * 50)


if __name__ == "__main__":
    run_simulation()

