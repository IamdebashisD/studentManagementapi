from flask import Flask, request, jsonify
import json
from flask_mysqldb import MySQL
import MySQLdb.cursors

app = Flask(__name__)

def even_num_generate(limit):
    for i in range(2, limit+1, 2):
        yield i

# This is Flask to MySQL configuration
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '62674123'
app.config['MYSQL_DB'] = 'students_db'


mysql = MySQL(app)
  
# Created a route or an endpoint for create records    
@app.route('/add_student', methods = ['GET', 'POST'])
def add_student():
    if request.method == 'POST':    
        data = request.get_json()  # Get the json data from the request
        name = data['name']
        address = data['address']
        phone_number = data['phone_number']

        try:
            mycursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            mycursor.execute(
                "INSERT INTO information (name, address, Phone_number) VALUES (%s, %s, %s)",
                (name, address, phone_number)
            )
            
            mysql.connection.commit()

            # Get the id of newly inserted record
            new_id = mycursor.lastrowid
            mycursor.execute("SELECT * FROM information WHERE id = %s", (new_id,))
            new_record = mycursor.fetchone()

            mycursor.close()

            # Return success message along with the new record
            return jsonify({"message" : "Success",
                            "StatusCode" : 200 ,
                            "new_record" : new_record,
                            "lastrowid" : new_id
                            }), 201

        except Exception as e:
            return jsonify({"error":str(e)}), 500

# Endpoint to show all the sudents records
@app.route('/show_all_data', methods=['GET'])
def students_data():
        try:
            mycursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            sql = '''SELECT * FROM information'''
            mycursor.execute(sql)
            rows = mycursor.fetchall() 
            mycursor.close()

            return jsonify(rows), 200
        
        except Exception as e:
            return jsonify({"error":str(e)}), 500 

# Create an endpointy for delete student records by specific Id
# Read operation  
@app.route('/delete_student/<int:id>', methods=['DELETE'])
def delete_data(id):
    try:
        mycursor = mysql.connection.cursor()
        # Execute the delete query
        mycursor.execute("DELETE FROM information WHERE id = %s", (id,))
        mysql.connection.commit()
        
        # Check if any row were affected (if the id existed)
        if mycursor.rowcount > 0:
            mycursor.close()
            return jsonify({"Message": "Record deleted successfully."}), 200
        else:
            mycursor.close()
            return jsonify({"Message": "No record found with this Id."}), 404
            
    except Exception as e:
        return jsonify({"error": str(e)}), 500 
    
# Creating an endpoint for get student by id
# Read operation by individual Id
@app.route('/get_student/<int:id>', methods= ['GET'])
def get_student_byId(id):
    try:
        mycursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        sql = "select * from information where id=%s"
        mycursor.execute(sql,(id,))
        user = mycursor.fetchone()
        mycursor.close()
        if user:
            return jsonify(user), 200
        else:
            return jsonify({"Message": "No student found with this id."}), 404    
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# This route updates a student's data based on given ID
@app.route('/update_data/<int:id>', methods=['PUT'])
def update_data(id):
    if request.method == 'PUT': 
        data = request.get_json() # Get the json data from the request
        name = data['name']
        address = data['address']
        phone_number = data['phone_number']

        try:
            mycursor = mysql.connection.cursor()
            sql = '''UPDATE information SET name = %s, address = %s, Phone_number = %s WHERE id = %s'''
            mycursor.execute(sql, (name, address, phone_number, id))
            mysql.connection.commit()

            # Check if the record was updated
            if mycursor.rowcount > 0:
                mycursor.close()
                return jsonify({'massage' : 'Record updated successfully.'}), 200
            else:
                mycursor.close()
                return jsonify({"Message" : "No record found with this ID"}), 404

        except Exception as e:
            return jsonify({'Error': str(e)}), 500
    

# api for even number generator
@app.route('/api/generate-even-number/<int:limit>', methods = ['GET'])
def get_even_numbers(limit):
    even_numbers = list(even_num_generate(limit))
    return jsonify({"Even number values": even_numbers})   # you can also use key_value_pair instead of using this 

    
    key_value_pair = {f"key{i}": i for i in even_num_generate(limit)} 
    return jsonify(key_value_pair)


@app.route('/square/<int:num>', methods=['GET'])
def square(num):
    return jsonify({'data': num**2})


@app.route('/fibonacci_series', methods = ['GET'])
def fibonacci():
    term = 10
    fib_series = [0, 1]
    for i in range(2, term+1):
        next_term = fib_series[-1] + fib_series[-2]
        fib_series.append(next_term)
    
    return jsonify({'Fibonacci sequence': fib_series})


@app.route('/prime-number-or-not', methods = ['GET'])
def prime() -> int:
    number = 59
    isprime = True

    for i in range (2, number):
        if number > 1 and number % i == 0:
            isprime = False 

    if isprime:
        return jsonify({'message': f'{number} is a prime'})
    return jsonify({'mesaage': f'{number} is not a prime number'})


@app.route('/OTP-generator', methods = ['GET'])
def randdom_OTP_generator():
    import random
    otp = random.randint(10000,1000000 )
    return jsonify({'Your OTP is': otp})


@app.route('/retrieve_data', methods=['GET'])
def retrieve_data() -> str:
    try: 
        mycursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        sql = "SELECT * FROM information"
        mycursor.execute(sql)
        rowValues = mycursor.fetchall()
        mycursor.close()
        content = {}
        employee = []
        for result in rowValues:
            content = {'id': result['id'], 'name': result['name'], 'Address': result['address'], 'Contact': result['Phone_number']}
            employee.append(content)
        return jsonify(employee), 200


    except Exception as e:
        return jsonify({'message': str(e)}), 404
    

# @app.route('/test')
# def test():
#     myset = {1, 2, 3, 4, 5, 5, 6, 6}
#     return jsonify(list(myset))

# @app.route('/test2')
# def tuple():
#     mytuple = (1, 2, 3, 4, 5, 6, 6,7,7)
#     return jsonify(f'tuple: {mytuple}')


class Employee:
   
    number_of_objects = 0
    def __init__(self, name, id, developer, age, company_name) -> None:
        self.__name = name
        self.__id = id
        self.developer = developer
        self.age = age
        self.company_name = company_name
        Employee.number_of_objects += 1

    def showDetails(self) ->None:
        return {'name': self.__name, 'id': self.__id, 'position': self.developer,'age': self.age , 'company_name': self.company_name}
    
    def get_description(self) ->None:
        return f'Hi my name is {self.__name}, working at {self.company_name} as a {self.developer}'
    # @staticmethod    
    def return_aList(self) ->None:
        return [
            [1,2,3,'Iron man',False,277.98],
            [2,3,65,4,True,'Captain america']
        ]
    def list_Of_Dictionaries(self) ->None:
        country = ['south korea', 'india']
        imbd_rating = [8.4, 8.7, 8.2]
        web_series_data = [
            {
                'Queen of Tears': {'country': country[0], 'imbd rating': imbd_rating[2]},
                'Vincenzo': {'country': country[0], 'imbd rating': imbd_rating[0]}, 
                'Night manager': {'country': country[1], 'imbd rating': imbd_rating[1]},
                'Panchayet': {'country': country[1], 'imbd rating': imbd_rating[1]}
            }
        ]
        return web_series_data       
    def docString(self)->None:
        '''Doc string is here'''
        return None

    
@app.route('/test', methods= [ 'GET' ])
def test():  
    haradhan_das = Employee("Haradhan Das", 400453456678, "Junior Python developer", 25, "Infosys")
    akhilesh_ghosh = Employee("Akhilesh Ghosh", 10023423454, "Junior Python developer", 27, "Wippro")
    # haradhan_das.name = 'Debashis Das' # you cannt over write the name attribute , it become a private attributes

    user_details = haradhan_das.showDetails()
    user_description = haradhan_das.get_description()

    userTwo_details = akhilesh_ghosh.showDetails()
    userTwo_description = akhilesh_ghosh.get_description()


    response = {
        'Userone': {
            'user_details' : user_details,
            'user_description': user_description
        },
        'UserTwo':{
            'user_details': userTwo_details,
            'user_description' : userTwo_description
        },
        'list':{
            'return a list': haradhan_das.return_aList()
        },
        'list of dictionary':{
            'web series data': haradhan_das.list_Of_Dictionaries()
        },
        'num_of_object' : Employee.number_of_objects,
        'doc string' : haradhan_das.docString.__doc__        
    }

    return jsonify(response)


class methodAnalyticalProccess:
    def method_one(self):
        return {'data_one': 'value of method one'}
    def method_two(self):
        return {'data_two': 'value of method two'}

@app.route('/combined_data', methods = ['GET'])
def combined_data():
    objectp = methodAnalyticalProccess()
    data_one = objectp.method_one()
    data_two = objectp.method_two()

    combined_data = {**data_one, **data_two}
    return jsonify(combined_data)


if __name__  == "__main__":
    app.run(debug = True)




