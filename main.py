#not inporting whole library only importing the class ,
# this sasve the ram ,we need to load in ram this the requirment get lesss

from fastapi import FastAPI ,HTTPException
import psycopg2
from pydantic import BaseModel
from  dotenv import load_dotenv
import os
load_dotenv()





app =FastAPI()#app is object and FastAPI is class

connection=psycopg2.connect(
host=os.getenv('DB_HOST'),
port=os.getenv('DB_PORT'),
database =os.getenv('DB_DATABASE'),
user = os.getenv('DB_USER'),
password =os.getenv('DB_PASSWORD')
)
cursor=connection.cursor()

class Student(BaseModel):
    id:int =None
    name:str =None
    course:str =None





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

#Create Student Record

@app.post('/students')
def Create_Student_Records(student: Student):
    try:
        cursor.execute('INSERT INTO students VALUES (%s,%s,%s)',(student.id,student.name,student.course))
        connection.commit()
        raise HTTPException(status_code=201,detail="student record created successflly")
    except psycopg2.IntegrityError:
        connection.rollback()
        raise HTTPException(status_code=404,detail="student id already exist ")

#update student record 
@app.put('/students/{id}')
def update_student_record(student :Student,id:int):
    cursor.execute('UPDATE students SET id=%s,name=%s,course=%s WHERE id=%s',(student.id,student.name,student.course,id))
    if(cursor.rowcount==0):
            raise HTTPException(status_code=404,detail='Invlid details')
    connection.commit()
    raise HTTPException (status_code=200,detail='student data  record updated successfully')


#update partially using patch


@app.patch('/students/{id}')
def partial_update(id :int,student:Student):
    if(student.id != None):
        cursor.execute('UPDATE students SET id=%s WHERE id=%s',(student.name,id))
    
    if(student.name != None):
        cursor.execute('UPDATE students SET name=%s WHERE id=%s',(student.name,id))
    
    if(student.course != None):
        cursor.execute('UPDATE students SET course=%s WHERE id=%s',(student.name,id))

    if(cursor.rowcount==0):
        raise HTTPException(status_code=404,detail='Invlid id entered')
    connection.commit()
    raise HTTPException(status_code=200,detail='partial update successfully ')


#delete the record Student 

@app.delete('/students/{id}')
def delete_student_record(id :int):
    cursor.execute('DELETE FROM students WHERE id=%s',(id,))
    if(cursor.rowcount==0):
            raise HTTPException(status_code=404,detail='INVALID ID')
    connection.commit()
    raise HTTPException(status_code=200,detail='record deleted successfully')
    
        



    



