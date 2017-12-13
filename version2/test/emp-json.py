import json

class Employee:
    def __init__(self, firstName, lastName):
        self.firstName = firstName
        self.lastName = lastName

    def toJSON(self):
        return {'Employees': {'firstName': self.firstName,
                              'lastName':  self.lastName }}


empList = []

employee = Employee('Gerald','Sternagl')
empList.append(employee)
employee = Employee('Kim','Sternagl')
empList.append(employee)
employee = Employee('Alycia','Sternagl')
empList.append(employee)
employee = Employee('Fabio','Sternagl')
empList.append(employee)
employee = Employee('Simba','Sternagl')
empList.append(employee)


jsonStr = json.dumps([e.toJSON() for e in empList])

print("Employee List:", jsonStr)


