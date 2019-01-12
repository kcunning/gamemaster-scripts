from random import choice, random
from string import lowercase

class Resident:

    def get_random_group(self, names, chances):
        n = int(random() * 100)

        t = 0
        for i in range(len(chances)):
            t += chances[i]
            if n <= t:
                return names[i]
        return names[-1]

    def get_ses_type(self):
        names = ['rich', 'affluent', 'comfortable', 'struggling', 'poor']
        chances = [1, 10, 20, 40]

        return self.get_random_group(names, chances)

    def get_age_type(self):
        # For this, we're assuming that a child is someone too young to work,
        # so the percentage is fairly low.

        # Most children will be generated with a family, so there's only a small
        # chance for a child to be generated on their own. A child generated this
        # way is an orphan
        age_types = ['elderly', 'adult', 'child']
        chances = [20, 78]

        return self.get_random_group(age_types, chances)

    def get_lines(self, fname):
        with open(fname) as f:
            lines = f.readlines()

        data = []
        for line in lines:
            t = line.strip()
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
        ses_jobs = {
            'rich': ['noblilty', 'land owner'],
            'affluent': ['shopkeep', 'artisan', 'trader', 'landlord', 'service', 'temple'],
            'comfortable': ['shopkeep', 'artisan', 'trader', 'service', 'guard', 'temple'],
            'struggling': ['worker', 'field hand', 'guard', 'service', 'temple'],
            'poor': ['worker', 'field hand', 'beggar', 'service', 'temple']
        }

        return choice(ses_jobs[self.ses])



    def __init__(self, vals={}):
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
            self.job = "none"
        

    def __str__(self):
        return "{fn} {ln} ({age}) - {job}".format(fn=self.first_name, 
            ln=self.family_name, age=self.age, job=self.job)

    def __repr__(self):
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
        n = int(random() * 100)
        t = 0
        for i in range(len(chances)):
            t += chances[i]
            if n <= t:
                return names[i]
        return names[-1]

    def get_building_type(self, vals):
        btypes = ['residence', 'merchant', 'artisan', 'temple', 'shopkeep']
        chances = [50, 20, 20, 5]

        if 'type' in vals and vals['type'] in btypes + ['none']:
            return vals['type']
        if 'type' in vals:
            return 'residence'

        return self.get_random_group(btypes, chances)

    def __init__(self, vals={}):

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
        c = self.get_random_group([True, False], [50])
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

        # How many children?
        options = [0, 1, 2, 3]
        chances = [60, 30, 15]
        n = self.get_random_group(options, chances)
        
        if n == 0:
            return []

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
        fields = ['ses', 'age']
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

    def sort_buildings(self):
        self.sectors = {}

        for b in self.buildings:
            r = b.residents[0]
            if not r.ses in self.sectors:
                self.sectors[r.ses] = [b]
            else:
                self.sectors[r.ses].append(b)


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
            elif r.age == 'eldery':
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

