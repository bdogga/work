# OOP Tutorial 1 (https://www.youtube.com/watch?v=ZDa-Z5JzLYM)

class employee:
    
    def __init__(self, first, last, pay):
        self.first = first
        self.last = last
        self.pay = pay
        self.email = first + '.' + last + '@company.com'
        
    def fullname(self):
        return '{} {}'.format(self.first, self.last)
    
    
emp1 = employee('Bharadwaj', 'Dogga', 50000)
emp2 = employee('Friend1', 'Lastname1', 70000)

print(emp1.email)
print(emp2.email)


print(emp1.fullname())

#print(emp1)
#print(emp2)


#emp1.first = 'Bharadwaj'
#emp1.last = 'Dogga'
#emp1.email = 'Bharadwaj.Dogga@company.com'
#emp1.pay = 70000

#emp2.first = 'Friend1'
#emp2.last = 'Lastname1'
#emp2.email = 'Friend1.Lastname1@company.com'
#emp2.pay = 90000


