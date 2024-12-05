from flask import Flask, request, jsonify, Response
import json
from flask_mysqldb import MySQL
from flask_mail import Mail, Message
import MySQLdb.cursors
from typing import Any, Optional, NoReturn
import MySQLdb
import re
 
app = Flask(__name__)

def even_num_generate(limit):
    for i in range(2, limit+1, 2):
        yield i

# This is Flask to Flask-mail configuration
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'adebashisdas626@gmail.com'
app.config['MAIL_PASSWORD'] = 'nhnf ijme dryb cqhq'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)   # instance of the mail class        

# This is Flask to MySQL configuration
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '62674123'
app.config['MYSQL_DB'] = 'students_db'

mysql = MySQL(app)
  
# Created a route or an endpoint for create records    
@app.route('/add_student', methods = ['GET', 'POST'])
def add_student() -> Response:   
    mycursor: None = None
    try:
        data: dict[str, str] = request.get_json()  # Get the json data from the request

        if not data or not data.get('name') or not data.get('address') or not data.get('phone_number') or not data.get('email'):        
            return jsonify({
                "error": "Invalid input. All fields (Name, Address, Contact number) are required."
            }), 400
        

        name: str = data['name']
        address: str = data['address']
        phone_number: str = data['phone_number']
        email: str = data['email']

        if not (isinstance(name, str) and len(name) <= 30):
            return jsonify({"error": "The 'name' field must be a string and not exceed 40 characters"}), 400
        if not (isinstance(address, str) and len(address) <= 80):
            return jsonify({"error": "The 'address' field must be a string and not exceed 80 characters"}), 400
        if not (isinstance(phone_number, str) and phone_number.isdigit() and len(phone_number) == 10):
            return jsonify({"error": "The 'contact number' field must be a string and not exceed 10 characters"}), 400
        if not (isinstance(email, str) and len(email) <= 255 and re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', email)):
            return jsonify({"error": "The 'email' field must be a valid email address"}), 400
            
           
        mycursor: MySQLdb.cursors.Cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

        #check if email id exist or not 
        mycursor.execute("SELECT email FROM information WHERE email = %s", (email,))
        existing_email = mycursor.fetchone()
        if existing_email:
            return jsonify({"message": "Invalid email! Email already exist."}), 400
        
        # database insertion
        mycursor.execute(
            "INSERT INTO information (name, address, Phone_number, email) VALUES (%s, %s, %s, %s)",
            (name, address, phone_number, email)
        )
        
        mysql.connection.commit()

        # Send a welcome email if the email is valid and exist
        if email.endswith('@gmail.com'):
            msg = Message(
            'Welcome to our service',
            sender = 'adebashisdas626@gmail.com',
            recipients = [email])
            msg.body = f'Hello {name},\n\nThank you for registering with our service!'
            mail.send(msg)

        # Get the id of newly inserted record
        new_id: Optional[int] = mycursor.lastrowid
        mycursor.execute("SELECT * FROM information WHERE id = %s", (new_id,))
        new_record = mycursor.fetchone()


        # Return success message along with the new record
        return jsonify({"message" : "Success",
                        "StatusCode" : 200,
                        "new_record" : new_record,
                        "lastrowid" : new_id
                        }), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if mycursor:
            mycursor.close()

# Endpoint to show all the student records
@app.route('/show_all_data', methods = ['GET'])
def students_data() -> Response:
        mycursor: None = None
        try:
            mycursor: MySQLdb.cursors.Cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            sql: str = '''SELECT * FROM information'''
            mycursor.execute(sql)
            rows = mycursor.fetchall() 
            return jsonify({"data": rows}), 200
        
        except Exception as e:
            return jsonify({"error": str(e), "status": 500}), 500 
        
        finally:
            if mycursor:
                mycursor.close()

# Create an endpointy for delete student records by specific Id
# Read operation  
@app.route('/delete_student/<int:id>', methods = ['DELETE'])
def delete_data(id) -> Response:
    mycursor: None = None
    try:
        mycursor: MySQLdb.cursors.Cursor = mysql.connection.cursor()
        # Execute the delete query
        mycursor.execute("DELETE FROM information WHERE id = %s", (id,))
        mysql.connection.commit()
        
        # Check if any row were affected (if the id existed)
        if mycursor.rowcount > 0:
            return jsonify({"Message": "Record deleted successfully."}), 200
        else:
            return jsonify({"Message": "No record found with this Id."}), 404
            
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
    finally:
        if mycursor:
            mycursor.close()
    
# Creating an endpoint for get student by id
# Read operation by individual Id
@app.route('/get_student/<int:id>', methods = ['GET'])
def get_student_byId(id) -> Response:
    mycursor: None = None
    try:
        mycursor: MySQLdb.cursors.Cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        sql: str = "select * from information where id = %s"
        mycursor.execute(sql, (id,))
        user = mycursor.fetchone()
        if user:
            return jsonify({"data": user, "message": "Success", "status": 200}), 200
        else:
            return jsonify({"Message": "No student found with this id.", "status": 404}), 404    
    
    except Exception as e:
        return jsonify({'error': str(e), 'status': 500}), 500

    finally:
        if mycursor:
            mycursor.close()

# This route updates a student's data based on given ID
@app.route('/update_data/<int:id>', methods = ['PUT'])
def update_data(id) -> Response:
    mycursor: None = None
    try:
        data: dict[str, str] = request.get_json() # Get the json data from the request dgadjagd

        if not data or not data.get('name') or not data.get('address') or not data.get('phone_number'):
            return jsonify({
                "error": "Invalid input. All fields (Name, Address, Contact number) are required."
            }), 400
        
        name: str = data['name']
        address: str = data['address']
        phone_number: str = data['phone_number']

        # Additional validation checks for length and type
        if not (isinstance(name, str) and len(name) <= 30):
            return jsonify({"error": "The 'name' field must be a string and not exceed 40 characters"}), 400
        if not (isinstance(address, str) and len(address) <= 80):
            return jsonify({"error": "The 'address' field must be a string and not exceed 80 characters"}), 400
        if not (isinstance(phone_number, str) and phone_number.isdigit() and len(phone_number) == 10):
            return jsonify({"error": "The 'contact number' field must be a string and not exceed 10 characters"}), 400

        mycursor: MySQLdb.cursors.Cursor = mysql.connection.cursor()
        sql: str = '''UPDATE information SET name = %s, address = %s, Phone_number = %s WHERE id = %s'''
        mycursor.execute(sql, (name, address, phone_number, id))
        mysql.connection.commit()

        # Check if the record was updated
        if mycursor.rowcount > 0:
            return jsonify({"message" : "Record updated successfully."}), 200
        else:
            return jsonify({"Message" : "No record found with this ID"}), 404

    except Exception as e:
        return jsonify({'Error': str(e)}), 500
    
    finally:
        if mycursor:
            mycursor.close()
    

# api for even number generator
@app.route('/api/generate-even-number/<int:limit>', methods = ['GET'])
def get_even_numbers(limit) -> Response:
    even_numbers = list(even_num_generate(limit))
    return jsonify({"Even number values": even_numbers})   # you can also use key_value_pair instead of using this 

    
    key_value_pair = {f"key{i}": i for i in even_num_generate(limit)} 
    return jsonify(key_value_pair)


@app.route('/square/<int:num>', methods = ['GET'])
def square(num) -> Response:
    return jsonify({'data': num**2})


@app.route('/fibonacci_series', methods = ['GET'])
def fibonacci() -> list[int]:
    term: int = 10
    fib_series: list[int] = [0, 1]
    for i in range(2, term+1):
        next_term = fib_series[-1] + fib_series[-2]
        fib_series.append(next_term)
    
    return jsonify({'Fibonacci sequence': fib_series})


@app.route('/prime-number-or-not', methods = ['GET'])
def prime() -> int:
    number: int = 59
    isprime: bool = True

    for i in range (2, number):
        if number > 1 and number % i == 0:
            isprime = False 

    if isprime:
        return jsonify({'message': f'{number} is a prime'})
    return jsonify({'mesaage': f'{number} is not a prime number'})


@app.route('/OTP-generator', methods = ['GET'])
def random_OTP_generator() -> Response:
    import random
    otp: int = random.randint(10000,1000000)
    return jsonify({'Your OTP is': otp}), 200


@app.route('/retrieve_data', methods = ['GET'])
def retrieve_data() -> Response:
    try: 
        mycursor: MySQLdb.cursors.Cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        sql: str = "SELECT * FROM information"
        mycursor.execute(sql)
        rowValues = mycursor.fetchall()
        mycursor.close()
        content: dict = {}
        employee: list[dict] = []
        for result in rowValues:
            content = {'id': result['id'], 'name': result['name'], 'Address': result['address'], 'Email': result['email'], 'Contact': result['Phone_number']}
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

# create a class for testing api test
class Employee:
    number_of_objects: int = 0
    def __init__(self, name: str, id: int, developer: str, age: int, company_name: str) -> None:
        self.__name = name
        self.__id = id
        self.developer = developer
        self.age = age
        self.company_name = company_name
        Employee.number_of_objects += 1

    def showDetails(self) -> None:
        return {'name': self.__name, 'id': self.__id, 'position': self.developer,'age': self.age , 'company_name': self.company_name}
    
    def get_description(self) -> None:
        return f'Hi my name is {self.__name}, working at {self.company_name} as a {self.developer}'
    # @staticmethod    
    def return_aList(self) -> None:
        return [
            [1,2,3,'Iron man',False,277.98],
            [2,3,65,4,True,'Captain america']
        ]
    def list_Of_Dictionaries(self) -> None:
        country: list[str] = ['south korea', 'india']
        imbd_rating: list[float] = [8.4, 8.7, 8.2]
        web_series_data: list[dict] = [
            {
                'Queen of Tears': {'country': country[0], 'imbd rating': imbd_rating[2]},
                'Vincenzo': {'country': country[0], 'imbd rating': imbd_rating[0]}, 
                'Night manager': {'country': country[1], 'imbd rating': imbd_rating[1]},
                'Panchayet': {'country': country[1], 'imbd rating': imbd_rating[1]}
            }
        ]
        return web_series_data       
    def docString(self) -> None:
        '''Doc string is here'''
        return None

    
@app.route('/test', methods = ['GET'])
def test():  
    haradhan_das: Employee = Employee("Haradhan Das", 40041534456678, "Junior Python developer", 25, "Infosys")
    akhilesh_ghosh: Employee = Employee("Akhilesh Ghosh", 100234243454, "Junior Python developer", 27, "Wippro")
    vishal_mehra: Employee = Employee("Vishal Mehra", 3554342663334, "Senior frontend developer", 44, "TCS-Tata Consultant Service")
    # haradhan_das.name = 'Debashis Das' # you cannt over write the name attribute , it become a private attributes

    user_details = haradhan_das.showDetails()
    user_description = haradhan_das.get_description()

    userTwo_details = akhilesh_ghosh.showDetails()
    userTwo_description = akhilesh_ghosh.get_description()

    userThree_details = vishal_mehra.showDetails()
    userThree_description = vishal_mehra.get_description()


    response = {
        'Userone': {
            'user_details' : user_details,
            'user_description': user_description
        },
        'UserTwo':{
            'user_details': userTwo_details,
            'user_description' : userTwo_description
        },
        'UserThree':{
        'user_details': userThree_details,
        'user_description' : userThree_description
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

    return jsonify(response), 200


class methodAnalyticalProccess:
    def method_one(self):
        return {'data_one': 'value of method one'}
    def method_two(self):
        return {'data_two': 'value of method two'}
    def method_three(self):
        return {'data_three': 'value of method three'}
    def method_four(self):
        return {'data_four': 'value of method four'}
    def method_five(self):
        return {'data_five': 'value of method five'}

@app.route('/combined_data', methods = ['GET'])
def combined_data():
    objectp = methodAnalyticalProccess()
    data_one = objectp.method_one()
    data_two = objectp.method_two()
    data_three = objectp.method_three()
    data_four = objectp.method_four()
    data_five = objectp.method_five()



    combined_data = {**data_one, **data_two, **data_three, **data_four, **data_five}
    return jsonify(combined_data)


@app.route('/linear_search', methods = ['GET'])
def linear_search_Two() -> Response | NoReturn:
    '''
    Perform a linear search on a given array to find the target value

    Query parameter:
    - array: List of integer to search in.
    - target: Integer value to searcg for.

    Returns:
    - JSON response indicating success or failure of the search.  
    '''
    # Extract the array and target from query parameters
    my_array = request.args.getlist('array', type = int)
    target = request.args.get('target', type = int)

    # Validate inputs
    if not my_array or target is None:
        return jsonify({"message": "Invalid input!, array and target is required"}), 400

    target = int(target)
    default_return: Response = jsonify({'message': 'Target not found'}), 404

    # Perform the linear search
    for index , value in enumerate(my_array):
        if value == target:
            return jsonify({"target": target,
                           "message": "target found in the container",
                           "position": index+1
            }), 200
    return default_return



if __name__  == "__main__":
    app.run(debug = True)




