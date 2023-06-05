import json
import sys

dataCompare = {
    "name" : sys.argv[1],
    "id" : 12345
}

person = json.dumps(dataCompare)

print(person.name)