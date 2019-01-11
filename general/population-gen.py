from random import choice, random
from string import lowercase

class Resident:

    def get_random_group(self, names, chances):
        n = int(random() * 100)

        t = 0
        for i in range(len(chances)):
            t += chances[i]
            if n <= chances[i]:
                return names[i]
        return names[-1]

    def get_ses_type(self):
        names = ['rich', 'affluent', 'comfortable', 'struggling', 'poor']
        chances = [1, 10, 20, 40]

        return self.get_random_group(names, chances)

    def get_age_type(self):
        # For this, we're assuming that a child is someone too young to work,
        # so the percentage is fairly low.
        age_types = ['elderly', 'adult', 'child']
        chances = [20, 65]

        return self.get_random_group(age_types, chances)

    def get_name(self):
        ''' One day, this will get a cool name. For now, everyone gets
            a few random letters
        '''
        f = ''
        for i in range(3):
            f += choice(string.lowercase)

        s = ''
        for i in range(4):
            s += choice(string.lowercase)

        return f, s

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

        if not vals:
            self.ses = self.get_ses_type()
            self.age = self.get_age_type()
            self.first_name, self.family_name = self.get_name()

            # Assume a child has no job. I'm using a more medieval use of the term
            # 'child' rather than a modern use. 
            if self.age != 'child':
                self.job = self.get_job()
            else:
                self.job = "none"


def generate_people(n=1000):
    job = {}
    age = {}
    ses = {}

    for i in range(1000):
        r = Resident()
        fields = ['job', 'age', 'ses']

        for field in fields:
            if not getattr(r, field) in locals()[field]:
                locals()[field][getattr(r, field)] = 1
            else:
                locals()[field][getattr(r, field)] += 1

    return job, age, ses

