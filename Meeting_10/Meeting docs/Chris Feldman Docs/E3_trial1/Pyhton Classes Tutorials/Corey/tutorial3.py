# OOP Tutorial 3 (https://www.youtube.com/watch?v=rq8cL2XMM5M)

class Employee:
   
   num_of_emps = 0
   raise_amount = 1.04
    
   def __init__(self, first, last, pay):
      self.first = first
      self.last = last
      self.pay = pay
      self.email = first + '.' + last + '@company.com'
      Employee.num_of_emps += 1
        
   def fullname(self):
      return '{} {}'.format(self.first, self.last)
      
   def apply_raise(self):
      self.pay = int(self.pay * self.raise_amount)
      
   @classmethod
   def set_raise_amt(cls, amount):
      cls.raise_amount = amount
   
   @classmethod
   def from_string(cls, emp_str):
      first, last, pay = emp_str.split('-')
      return cls(first, last, pay)
      
   @staticmethod
   def is_workday(day):
      if day.weekday() == 5 or day.weekday() == 6:
         return False
      return True

#print(Employee.num_of_emps)   
emp1 = Employee('Bharadwaj', 'Dogga', 50000)
emp2 = Employee('Friend1', 'Lastname1', 70000)

import datetime
my_date = datetime.date(2016, 7, 11)

print(Employee.is_workday(my_date))


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



