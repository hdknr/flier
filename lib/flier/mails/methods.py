''' Email Delivery Subsystem
'''


class Address(object):
    ''' Mail Address
    '''
    def bounce(self):
        self.bounced += 1
        self.save()

class Log(object):
    pass
