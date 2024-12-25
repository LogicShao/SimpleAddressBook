from ContactPerson import ContactPerson

import json
import random
import string
import sys


def randStr(length: int = 5):
    return "".join(random.choices(string.ascii_letters + string.digits, k=length))


def randLetterStr(length: int = 5):
    return "".join(random.choices(string.ascii_letters, k=length))


def randIntStr(length: int = 11):
    return "".join(random.choices(string.digits, k=length))


def genRandContactPerson():
    return ContactPerson(
        name=randLetterStr(),
        phone=randIntStr(),
        info='null',
    )


def genRandContactPerson2json(num: int = 10):
    fileName = "addressbook.json"
    contactPersonList = [genRandContactPerson() for _ in range(num)]
    with open(fileName, "w") as file:
        json.dump(
            [contactPerson.__dict__ for contactPerson in contactPersonList], file, indent=4)


if __name__ == "__main__":
    genRandContactPerson2json(int(sys.argv[1]) if len(sys.argv) > 1 else 10)
    print("Done!")
