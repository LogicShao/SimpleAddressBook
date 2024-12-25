from dataclasses import dataclass


@dataclass
class ContactPerson:
    name: str
    phone: str
    info: str = ""