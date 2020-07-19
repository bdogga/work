# OOP Tutorial 4 (https://www.youtube.com/watch?v=RSl87lqOXDE)

class Employee:
   
   raise_amt = 1.04
    
   def __init__(self, first, last, pay):
      self.first = first
      self.last = last
      self.pay = pay
      self.email = first + '.' + last + '@company.com'
      
        
   def fullname(self):
      return '{} {}'.format(self.first, self.last)
      
   def apply_raise(self):
      self.pay = int(self.pay * self.raise_amt)

class Developer(Employee):
   pass

      
dev_1 = Employee('Bharadwaj', 'Dogga', 50000)
dev_2 = Employee('Friend1', 'Lastname1', 70000)

print(dev_1.email)
print(dev_2.email)


#import datetime
#my_date = datetime.date(2016, 7, 11)

#print(Employee.is_workday(my_date))


#emp_str_1 = 'John-Doe-70000'
#emp_str_2 = 'Jane-Doe-90000'
#emp_str_3 = 'Steve-Smith-60000'

#first, last, pay = emp_str_1.split('-')

#new_emp_1 = Employee(first, last, pay)
#new_emp_1 = Employee.from_string(emp_str_1)

#print(new_emp_1.email)
#print(new_emp_1.pay)

#Employee.set_raise_amt(1.05)
#emp1.set_raise_amt(1.05)

#print(Employee.raise_amount)
#print(emp1.raise_amount)
#print(emp2.raise_amount)


#print(Employee.num_of_emps)

#emp1.raise_amount = 1.05

#print(emp1.__dict__)

#print(Employee.__dict__)
#print(emp1.__dict__)


#print(emp1.pay)
#emp1.apply_raise()
#print(emp1.pay)



