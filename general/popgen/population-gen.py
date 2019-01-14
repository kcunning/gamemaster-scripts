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
        if not 'first_names' in globals():
            global first_names, surnames
            first_names = self.get_lines('female_names.txt')
            first_names.extend(self.get_lines('male_names.txt'))
            surnames = self.get_lines('surnames.txt')

        return choice(first_names), choice(surnames)

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
            'affluent': ['shopkeep', 'artisan', 'trader', 'landlord', 'service'],
            'comfortable': ['shopkeep', 'artisan', 'trader', 'service', 'guard', 'temple'],
            'struggling': ['worker', 'field hand', 'guard', 'service'],
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
        self.first_name, self.family_name = self.get_name()
        self.parents = [] # If a child is generated this way, they're an orphan
        self.spouse = None

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
        btypes = ['residence', 'merchant', 'artisan', 'temple', 'shopkeep']
        chances = [50, 20, 20, 5]

        if 'type' in vals and vals['type'] in btypes + ['none']:
            return vals['type']
        if 'type' in vals:
            return 'residence'

        return self.get_random_group(btypes, chances)

    def __init__(self, vals={}):
        ''' Creates a building. If nothing is sent in vals, it will be a random
            empty building. Residents are set in the Town class during population
            generation.
        '''
        self.type = self.get_building_type(vals)
        self.residents = []


class Town:
    def get_random_group(self, names, chances):
        n = int(random() * 100)
        t = 0
        for i in range(len(chances)):
            t += chances[i]
            if n <= t:
                return names[i]
        return names[-1]

    def generate_family(self, r, t):
        fam = []
        # Spouse?
        c = self.get_random_group([True, False], [70])
        if c:
            d = {'age': r.age, 
                'ses': r.ses, 
                'family_name': r.family_name,
                'job': r.job}  # For now, assume they have the same job
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
        self.sectors = {}

        for b in self.buildings:
            r = b.residents[0]
            if not r.ses in self.sectors:
                self.sectors[r.ses] = [b]
            else:
                self.sectors[r.ses].append(b)

    def print_town_csv(self, delimeter="\t"):
        hc = ["First name", "Family name","Age","Building","SES", "Job"]
        hr = delimeter.join(hc)
        print hr

        rc = ["{fname}", "{lname}","{age}", "{building}", "{ses}", "{job}"]
        rt = delimeter.join(rc)

        for b in self.buildings:
            for r in b.residents:
                print rt.format(
                    fname=r.first_name,
                    lname=r.family_name,
                    age=r.age,
                    building=b.type,
                    ses=r.ses,
                    job=r.job)

    def __init__(self, n=1000):
        ''' Generate a town of people! 

            Note that you'll likely get more than n residents due to how 
            families are generated

            For each resident, we check to see if that resident has any
            children. If so, we go ahead and create that child.

            TODO:
                * Add a spouse
                * Add 'parent of' and 'child of' to Resident
                * Eventually put families in houses
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
                fam = self.generate_family(r, "none")
                self.residents.extend(fam)
                b = Building({'type': r.job})
                b.residents = [r]
                self.buildings.append(b)
            elif r.age == 'child':
                b = Building({'type': 'none'})
                b.residents = [r]
                self.buildings.append(b)

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

t = Town()
t.print_town_stats()
t.print_town_csv()