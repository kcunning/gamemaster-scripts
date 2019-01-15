from random import choice, random
from string import lowercase

# To do:
# Class for shops
# Docs!

class Resident:
    ''' A resident is a single person within a town.

        Each resident has an age, a socioeconomic status(SES), a name
        and a job. Optionally, they can have a spouse and parents.

        Children are assumed to have no job. Note that 'children' in this case
        are simply 'people too young to work.' Also, a child randomly generated
        by this class is assumed to be an orpha, since family units are generated
        via the Town class.

        Values can be sent into the init. Any values sent in will overwrite the 
        randomly generated values.
    '''

    def get_random_group(self, names, chances):
        ''' Given a list of options and the chance for each, return one of the
            named groups. The index of each named group matches the index of the chance
            of it being picked.

            The length of `chances` should be one less than `names`. 

            Example: If you send in the named groups `["one", "two", "three"] and the
            chances `[40, 20]`, the chances of getting "one" is 40% and "two" is 20%.
            Since 100 - 40 - 20 is 40, the chances of getting "three" is 40%.

            The reason the chances are expicitly stated for the last item in `names`
            is just to make fiddling with numbers easier. It was a pain to keep having
            to make sure they all added up to 100.
        '''
        n = int(random() * 100)

        t = 0
        for i in range(len(chances)):
            t += chances[i]
            if n <= t:
                return names[i]
        return names[-1]

    def get_ses_type(self):
        ''' Returns a random socioeconomic status.
        '''
        names = ['rich', 'affluent', 'comfortable', 'struggling', 'poor']
        chances = [1, 10, 20, 40]

        return self.get_random_group(names, chances)

    def get_age_type(self):
        ''' Returns a random age type. Note that this doens't spell out an
            explicit age. This is to give the GM more freedom in describing
            characters.

            For this, we're assuming that a child is someone too young to work,
            so the percentage is fairly low.

            Most children will be generated with a family, so there's only a small
            chance for a child to be generated on their own. A child generated this
            way is an orphan
        '''
        
        age_types = ['elderly', 'adult', 'child']
        chances = [20, 78]

        return self.get_random_group(age_types, chances)

    def get_traits(self, n=3):
        ''' Get some random traits for a person. List is from:

            http://ideonomy.mit.edu/essays/traits.html
        '''
        # YES, GLOBALS ARE BAD, DO AS I SAY NOT AS I DO
        if not 'traits' in globals():
            global traits
            traits = self.get_lines("traits.txt")
        ts = []
        while len(ts) != n:
            t = choice(traits)
            if not t in ts:
                ts.append(t)
        return ts

    def get_lines(self, fname):
        ''' Gets lines from a file, cleans them up, and returns them.
        '''
        with open(fname) as f:
            lines = f.readlines()

        data = []
        for line in lines:
            t = line.strip()
            # I don't values with unicode characters right now.
            if t != str(t): continue 
            if t: data.append(t)

        return data


    def get_name(self):
        ''' Make a name. Names from:

            https://www.mithrilandmages.com/utilities/MedievalBrowse.php?letter=C&fms=M
        '''
        # DO NOT DO AS I DO, CHILDREN. GLOBALS ARE BAD.
        # Global brought in so that we only get the first names and such once.
        if not 'first_names_f' in globals():
            global first_names_f, first_names_m, surnames
            first_names_f = self.get_lines('female_names.txt')
            first_names_m = self.get_lines('male_names.txt')
            surnames = self.get_lines('surnames.txt')
        if self.gender == "female":
            fn = choice(first_names_f)
        else:
            fn = choice(first_names_m)
        return fn, choice(surnames)

    def get_job(self):
        ''' Returns a job based on `Resident.ses`. Requires SES being set.

            Note that some jobs occur in more than one category. Presumably,
            the Residents with a higher SES have better positions, such as the head
            of the guard or a successful merchant.

            "Service" is generally someone who doesn't create or offer a good. They
            might be a servant, a money counter, or some other job that fits that SES.

            "Worker" is generally someone who helps a producer / seller, but doesn't own
            their own business or make their own goods.
        '''
        ses_jobs = {
            'rich': ['noblilty', 'land owner'],
            'affluent': ['shopkeep', 'artisan', 'trader', 'landlord', 'service', 'tavern'],
            'comfortable': ['shopkeep', 'artisan', 'trader', 'service', 'guard', 'temple',
                'tavern'],
            'struggling': ['worker', 'field hand', 'guard', 'service', 'tavern'],
            'poor': ['worker', 'field hand', 'beggar', 'service']
        }

        return choice(ses_jobs[self.ses])



    def __init__(self, vals={}):
        ''' Initializes a single Resident. 

            Values can be passed in that overwrite randomly generated values.

            Children are not given jobs. In this script, it is assumed that a
            child is simply someone too young to work. They may help out the 
            family business, but they don't have a 'job'.
        '''
        self.ses = self.get_ses_type()
        self.age = self.get_age_type()
        self.gender = self.get_random_group(['male', 'female', 'indeterminate'], [49, 49])
        self.first_name, self.family_name = self.get_name()
        self.parents = [] # If a child is generated this way, they're an orphan
        self.spouse = None
        self.traits = self.get_traits()

        # Overwrite any vals we sent in after wasting precious electrons
        for val in vals:
            setattr(self, val, vals[val])

        # Assume a child has no job. I'm using a more medieval use of the term
        # 'child' rather than a modern use. 
        if self.age != 'child' and not hasattr(self, 'job'):
            self.job = self.get_job()
        else:
            self.job = "child"
        

    def __str__(self):
        ''' Returns name of the Resident, along with their age and job.
        '''
        return "{fn} {ln} ({age}) - {job}".format(fn=self.first_name, 
            ln=self.family_name, age=self.age, job=self.job)

    def __repr__(self):
        ''' Returns name of the Resident, along with their age and job.
        '''
        return "{fn} {ln} ({age}) - {job}".format(fn=self.first_name, 
            ln=self.family_name, age=self.age, job=self.job)

class Building:
    ''' A building, described generically, so that we don't have to worry
        about ses. Assumes someone older than an adult lives within.

        The first adult placed determines the SES of the house.

        Because this is a medieval style place, families can live in places
        of business.
    '''

    def get_lines(self, fname):
        ''' Gets lines from a file, cleans them up, and returns them.
        '''
        with open(fname) as f:
            lines = f.readlines()

        data = []
        for line in lines:
            t = line.strip()
            # I don't values with unicode characters right now.
            if t != str(t): continue 
            if t: data.append(t)

        return data

    def get_random_group(self, names, chances):
        ''' Given a list of options and the chance for each, return one of the
            named groups. The index of each named group matches the index of the chance
            of it being picked.

            The length of `chances` should be one less than `names`. 

            Example: If you send in the named groups `["one", "two", "three"] and the
            chances `[40, 20]`, the chances of getting "one" is 40% and "two" is 20%.
            Since 100 - 40 - 20 is 40, the chances of getting "three" is 40%.

            The reason the chances are expicitly stated for the last item in `names`
            is just to make fiddling with numbers easier. It was a pain to keep having
            to make sure they all added up to 100.
        '''
        n = int(random() * 100)
        t = 0
        for i in range(len(chances)):
            t += chances[i]
            if n <= t:
                return names[i]
        return names[-1]

    def get_building_type(self, vals):
        ''' Returns a building type. 

            If the value sent in vals['type'] is none, or is contained in the
            possible types of buildings, that value is sent back. This is so
            certain people will live in a building that makes sense (a temple worker
            in a temple, a merchant in a merchant house, etc).

            If a value is sent in vals, but it doesn't match the building types (or none),
            "residence" is sent back. This is for people who wouldn't live at their
            place of work.

            Finally, if nothing is sent in vals, a random building is sent back.
        '''
        btypes = ['residence', 'merchant', 'artisan', 'temple', 'shopkeep', 'tavern']
        chances = [50, 20, 15, 5]

        subtypes = {
            'residence': ['residence'],
            'merchant': ['merchant'],
            'artisan': ['bookmaker', 'scribe', 
                'carpenter', 'tailor', 'glassblower', 'jewelry maker', 
                'artist', 'potter', 'cobbler', 'stonemason'],
            'temple': ['LG temple', 'NG temple', 'CG temple', 'LN temple', 
                'N temple', 'CN temple'],
            'shopkeep': ['general goods', 'magic goods', 'armor and weapons'],
            'none': ['street', 'shack'],
            'tavern': ['tavern']
        }
        subtype_chances = {
            'residence': [100],
            'merchant': [100],
            'artisan': [int(100/len(subtypes['artisan']))] * (len(subtypes['artisan']) - 1),
            'temple': [int(100/len(subtypes['temple']))] * (len(subtypes['temple']) - 1),
            'shopkeep': [int(100/len(subtypes['shopkeep']))] * (len(subtypes['shopkeep']) - 1),
            'none': [50],
            'tavern': [100]
        }

        if not 'type' in vals:
            t = self.get_random_group(btypes, chances)
        elif vals['type'] not in btypes:
            t = 'residence'
        else:
            t = vals['type']

        return t, self.get_random_group(subtypes[t], subtype_chances[t])

    def get_random_building_name(self):
        if not "nouns" in globals():
            global nouns, adjs
            nouns = self.get_lines("nouns.txt")
            adjs = self.get_lines("adjectives.txt")

        subtypes = ['general goods', 'magic goods', 'armor and weapons']

        self.subtype = choice(subtypes)

        tpls = [
            ["{} and {}", ["noun", "noun"]],
            ["{}'s {}", ["noun", "noun"]],
            ["The {} {}", ["adj", "noun"]],
            ["{}'s {}", ["surname", "subtype"]],
            ["{} by {}", ["subtype", "firstname"]]
        ]

        tpl = choice(tpls)

        vals = []
        for i in tpl[1]:
            if i == "noun":
                vals.append(choice(nouns))
            elif i == "adj":
                vals.append(choice(adjs))
            elif i == "surname":
                vals.append(self.residents[0].family_name)
            elif i == "subtype":
                vals.append(self.subtype)
            elif i == "firstname":
                vals.append(self.residents[0].first_name)

        return tpl[0].format(*vals).title().replace("'S", "'s").replace("s's", "'s")

    def __init__(self, vals={}):
        ''' Creates a building. If nothing is sent in vals, it will be a random
            empty building. Residents are set in the Town class during population
            generation.
        '''
        self.type, self.subtype = self.get_building_type(vals)
        self.residents = []


class Town:
    ''' A town is a split into sections (neighborhoods). Sections contain buildings,
        and buildings contain residents (from one to seven). 

        Creating a town will generate a random number of residents and houses, and
        sort the buildings into neighborhoods depending on the wealth level (SES)
        of the residents.

    '''
    def get_random_group(self, names, chances):
        ''' Given a list of options and the chance for each, return one of the
            named groups. The index of each named group matches the index of the chance
            of it being picked.

            The length of `chances` should be one less than `names`. 

            Example: If you send in the named groups `["one", "two", "three"] and the
            chances `[40, 20]`, the chances of getting "one" is 40% and "two" is 20%.
            Since 100 - 40 - 20 is 40, the chances of getting "three" is 40%.

            The reason the chances are expicitly stated for the last item in `names`
            is just to make fiddling with numbers easier. It was a pain to keep having
            to make sure they all added up to 100.
        '''
        n = int(random() * 100)
        t = 0
        for i in range(len(chances)):
            t += chances[i]
            if n <= t:
                return names[i]
        return names[-1]

    def generate_family(self, r, t):
        ''' Given a single resident, generates a family for that resident.

            There is a 50/50 chance that the resident will be given a spouse.
            Spouses have the same job as each other for now.

            If the resident is an adult, they will be given somewhere between zero
            and five children.

            `t` is the type of 'child' the resident will be given. For now, 
            only adults can have children, and those children have the age type of
            'child'. 
        '''
        fam = []
        # Spouse?
        c = self.get_random_group([True, False], [70])
        if c:
            g = self.get_random_group(['opposite', 'same'], [85])
            if g == 'opposite' and r.gender == "male":
                gen = 'female'
            elif g == 'opposite' and r.gender == "female":
                gen = 'male'
            elif r.gender == "indeterminate":
                gen = choice(['male', 'female', 'indeterminate'])
            else:
                gen = r.gender
            d = {'age': r.age, 
                'ses': r.ses, 
                'family_name': r.family_name,
                'job': r.job, # For now, assume they have the same job
                'gender': gen}  
            spouse = Resident(d)
            spouse.job = r.job
            fam.append(spouse)
            r.spouse = spouse
            spouse.spouse = r
            parents = [r, spouse]
        else:
            parents = [r]

        if r.age == "elderly":
            return fam

        # How many children?
        options = [0, 1, 2, 3, 4, 5]
        chances = [20, 30, 15, 10, 10]
        n = self.get_random_group(options, chances)
        
        if n == 0:
            return fam

        for i in range(n):
            d = {'age': t}
            # Assume the child has the same ses and family name as the parent
            if t == 'child':
                d['ses'] = r.ses
                d['family_name'] = r.family_name
                d['parents'] = parents

            r = Resident(d)
            fam.append(r)

        return fam

    def print_town_stats(self):
        ''' Prints out the high level stats for a town in a horrible format.
        '''
        print "Number of residents:", len(self.residents)
        print "Number of buildings:", len(self.buildings)

        ses = {}
        age = {}
        btypes = {}
        job = {}
        fields = ['ses', 'age', 'job']
        for r in self.residents:
            for field in fields:
                if not getattr(r, field) in locals()[field]:
                    locals()[field][getattr(r, field)] = 1
                else:
                    locals()[field][getattr(r, field)] += 1

        for b in self.buildings:
            if not b.type in btypes:
                btypes[b.type] = 1
            else:
                btypes[b.type] += 1

        print "SES", ses
        print "AGE", age
        print "Building types", btypes
        print "Jobs", job

    def sort_buildings(self):
        ''' Sorts buildings (and therefore, families) into sectors.

            Each family has a small chance of living one step up or one step down
            from their current SES. Maybe they like saving on rent, or the family
            has fallen on hard times but can't move (or refuses to). 

            Note that no one is automatically assigned to the slums or a private
            estate due to their SES. There is a chance of being moved up or down a
            tier (5% up, 5% down).
        '''
        sectors = ['slums', 'poor', 'middle class', 'upper middle class', 'exclusive', 'private estate']
        sdict = {
            'poor': 'poor',
            'struggling': 'poor',
            'comfortable': 'middle class',
            'affluent': 'upper middle class',
            'rich': 'exclusive'
        }

        self.sectors = {}

        for b in self.buildings:
            r = b.residents[0]
            s = sdict[r.ses]

            i = sectors.index(s)
            s = self.get_random_group([s, sectors[i-1], sectors[i+1]], [90, 5])

            if not s in self.sectors:
                self.sectors[s] = [b]
            else:
                self.sectors[s].append(b)

    def print_town_csv(self, delimeter="\t"):
        ''' This function does not work as it says on the tin for now. For ease
            of troubleshooting, it just prints out tab separated values and does
            not use the `csv` library. 

            TODO: Give an option to allow for printing to a file

            TODO: Actually use the CSV library
        '''
        hc = ["First name", "Family name","Age","Gender","Building","Subtype", "Name", "SES    ", "Job", "Traits", "Sector"]
        hr = delimeter.join(hc)
        print hr

        rc = ["{fname}", "{lname}","{age}", "{gender}", "{building}", "{sub}", "{name}", 
            "{ses}   ", "{job}", "{traits}", "{sector}"]
        rt = delimeter.join(rc)

        for s in self.sectors:
            for b in self.sectors[s]:
                for r in b.residents:
                    print rt.format(
                        fname=r.first_name,
                        lname=r.family_name,
                        age=r.age,
                        building=b.type,
                        ses=r.ses,
                        job=r.job,
                        gender=r.gender,
                        traits=", ".join(r.traits).lower(),
                        sector=s,
                        sub=b.subtype,
                        name=b.name)

    def __init__(self, n=1000):
        ''' Generate a town of people! 

            Note that you'll likely get more than n residents due to how 
            families are generated

            For each resident, we check to see if that resident has any
            children. If so, we go ahead and create that child.

            TODO:
                * Add 'parent of' and 'child of' to Resident
        '''
        self.residents = []
        self.buildings = []

        while len(self.residents) < n:
            r = Resident()
            self.residents.append(r)
            if r.age == 'adult':
                fam = self.generate_family(r, 'child')
                self.residents.extend(fam)
                b = Building({'type': r.job})
                b.residents = [r] + fam
                self.buildings.append(b)
            elif r.age == 'elderly':
                fam = self.generate_family(r, 'none')
                self.residents.extend(fam)
                b = Building({'type': r.job})
                b.residents = [r] + fam
                self.buildings.append(b)
            elif r.age == 'child':
                b = Building({'type': 'none'})
                b.residents = [r]
                self.buildings.append(b)

            if not b.type in ['residence', 'artisan', 'none']:
                b.name = b.get_random_building_name()
            else:
                b.name = ''

        self.sort_buildings()


def generate_people(n=1000):
    ''' Just a test function for seeing how a town of 1000 people
        shakes out
    '''
    job = {}
    age = {}
    ses = {}

    for i in range(n):
        r = Resident()
        fields = ['job', 'age', 'ses']

        for field in fields:
            if not getattr(r, field) in locals()[field]:
                locals()[field][getattr(r, field)] = 1
            else:
                locals()[field][getattr(r, field)] += 1

    return job, age, ses

t = Town(500)
t.print_town_stats()
t.print_town_csv()