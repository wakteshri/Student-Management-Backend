#not inporting whole library only importing the class ,
# this sasve the ram ,we need to load in ram this the requirment get lesss

from fastapi import FastAPI ,HTTPException
import psycopg2




app =FastAPI()#app is object and FastAPI is class

connection=psycopg2.connect(
host='localhost',
port='5432',
database ='postgres',
user = 'postgres',
password ='74743427'
)
cursor=connection.cursor()


'''this is decorator it is a function which take the another funchtion 
as an argument ,it extends or modifies its behavior and return new function 
without altering the original functions source code'''


# GET ALL STUDENT
@app.get('/students')
def get_all_students():
    cursor.execute('SELECT * FROM students')
    rows=cursor.fetchall()
    print(rows)
    #[(102, 'pavan', 'React'), (101, 'steve', 'AI')]this is what i get now 
    #[{'id':102, 'name':'pavan', 'course':'React'},{}] i want like this 
    
    result=[]
    for row in rows:
        result.append({
            'id':row[0],
            'name':row[1],
            'course':row[2]
        })
    return result
#GET SINGLE STUDENT

@app.get('/students/{id}')
def get_single_student(id: int):# pydantic give the hit that id should be in the integer 
    try:
        cursor.execute('select * from students where id=%s',(id,))
        row=cursor.fetchone()
        return {
            'id':row[0],
            'name':row[1],
            'course': row[2]
        }
    except:
        raise HTTPException(status_code=404,detail='Invalid Student Id ')
    



