

persons = []
families = {}

class Person():
    lists = {
        "NAME": "name",
        "FAMS": "spouse",
        "FAMC": "child_of",
        "SEX" : "sex"
    }

    def activate(individual, person_id):
        individual.id = person_id
        individual.fam_spouse = []

    def add_list(individual, space, lines):
        if space in Person.lists.keys():
            getattr(individual, "make_{}".format(Person.lists[space]))(space, lines)

    def make_name(individual, space, lines):
        for line in lines[1:]:
            nameType = line.split(" ", 2)[1]
            nameOfType = line.split(" ", 2)[-1]
            setattr(individual, nameType.lower(), nameOfType)
        individual.name = ""
        individual.name += "" if not hasattr(individual, "givn") else individual.givn
        if not hasattr(individual, "_marnm"):
            individual.name += "" if not hasattr(individual, "surn") else " " + individual.surn
        else:
            individual.name += " " + individual._marnm

    def make_spouse(individual, space, lines):
        individual.fam_spouse.append(int(lines[0].split(" ", 2)[-1][2:-1]))
        addSpouseToFamily(int(lines[0].split(" ", 2)[-1][2:-1]), individual)


    def make_child_of(individual, space, lines):
        #if individual.name:
            addChildrenToFamily(int(lines[0].split(" ", 2)[-1][2:-1]), individual)
        

    def make_sex(individual, space, lines):
        individual.sex = lines[0].split(" ", 2)[-1].lower()


class Family():
    def activate(individual, f_id):
        individual.familyId = f_id
        individual.spouses = []
        individual.children = []


def addSpouseToFamily(famId, person):
    if families.get(famId):
        families[famId].spouses.append(person)
    else:
        families[famId] = Family(famId)
        families[famId].spouses.append(person)

def addChildrenToFamily(famId, person):
    if families.get(famId):
        families[famId].children.append(person)
    else:
        families[famId] = Family(famId)
        families[famId].children.append(person)


def unknown_type(lines):
    pass

def parse_head(lines):
    pass

def parse_subm(lines):
    pass


def parse_indi(lines):
    person_id = lines[0].split(" ")[1][2:-1]
    person = Person(person_id)
    space_type = ""
    lines_to_send = []
    for line in lines[1:]:
        if line[0] in "1":
            if space_type:
                person.add_list(space_type, lines_to_send)
                lines_to_send = []
            space_type = line.split(" ")[1]
        lines_to_send.append(line)

    persons.append(person) 

parse = {
    "HEAD": parse_head,
    "SUBM": parse_subm,
    "INDI": parse_indi,
}

with open(tree_file_name, "r") as f:
    line = f.readline()
    space = ""
    lines = []
    while line:
        if line[0] in "0":
            if space: parse.get(space, unknown_type)(lines)
            space = line.split(" ")[-1].strip()
            lines = [line.strip()]
        else: lines.append(line.strip())
            
        line = f.readline()

out = ''
for p in persons:
    if p.name in '': persons.remove(p)
for p in persons:
    if (p.sex == 'f'):
        for fam in p.fam_spouse:
            for ch in families[fam].children:
                out += 'mother("{}","{}").\n'.format(p.name, ch.name)
for p in persons:
    if (p.sex == 'm'):
        for fam in p.fam_spouse:
            for ch in families[fam].children:
                out += 'father("{}","{}").\n'.format(p.name, ch.name)
				
				
				
out_file = "DrachevTree.pl"
tree_file_name = "DrachevTree.ged"


with open(out_file, "w") as o:
    o.write(out)
