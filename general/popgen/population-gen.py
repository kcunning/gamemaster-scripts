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
        # chance for a child to be generated on their own
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
        # Should probably move this to be more efficient, but w/e
        first_names = self.get_lines('female_names.txt')
        first_names.extend(self.get_lines('male_names.txt'))
        surnames = self.get_lines('surnames.txt')

        return choice(first_names), choice(surnames)

    def get_job(self):
        ses_jobs = {
            'rich': ['none'],
            'affluent': ['shopkeep', 'artisan', 'trader', 'landlord', 'service'],
            'comfortable': ['shopkeep', 'artisan', 'trader', 'service', 'guard'],
            'struggling': ['worker', 'field hand', 'guard', 'service'],
            'poor': ['worker', 'field hand', 'beggar', 'service']
        }

        return choice(ses_jobs[self.ses])



    def __init__(self, vals={}):

        print "Creating resident with", vals

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
        return self.first_name + " " + self.family_name

    def __repr__(self):
        return self.first_name + " " + self.family_name

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
        btypes = ['residence', 'merchant', 'artisan', 'temple']
        chances = [50, 20, 20]

        if 'type' in vals and vals['type'] in btypes:
            return vals['type']

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
        print "Making a family for", r
        fam = []

        print "\tDo they have a spouse?"
        c = self.get_random_group([True, False], [50])
        if c:
            d = {'age': r.age, 
                'ses': r.ses, 
                'family_name': r.family_name,
                'job': r.job}  # For now, assume they have the same job
            spouse = Resident(d)
            fam.append(spouse)
            print "\tSpouse is", spouse
            r.spouse = spouse
            spouse.spouse = r
            parents = [r, spouse]
        else:
            print "\tNo spouse"
            parents = [r]

        # Make them a house
        b = Building({'type': r.job})

        # How many children?
        options = [0, 1, 2, 3]
        chances = [60, 30, 15]
        n = self.get_random_group(options, chances)

        print "\tMaking", n, "members."
        
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
            print "\tCreated", r
            fam.append(r)
        
        b.residents = fam

        self.buildings.append(b)

        return fam

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

