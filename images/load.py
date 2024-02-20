import os
import mysql.connector
from mysql.connector import errorcode
import glob

try:
    cnx = mysql.connector.connect(user='kmsbusch', password='Artscape209-5',host='kmsbusch.mysql.pythonanywhere-services.com',database='kmsbusch$images')

except mysql.connector.Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("Something is wrong with your user name or password")
    elif err.errno == errorcode.ER_BAD_DB_ERROR:
        print("Database does not exist")
    else:
        print(err)
#else:
#    cnx.close()


cursor = cnx.cursor()

add_employee = ("INSERT INTO employees "
               "(first_name, last_name, hire_date, gender, birth_date) "
               "VALUES (%s, %s, %s, %s, %s)")

add_image = ("insert into images (image_name, image_bigimage, image_thumbs) values (%(fname)s, load_file(%(big_image)s), load_file(%(thumb)s))")

#get all .txt files in my_path
my_path='/home/kmsbusch/mysite/images/'
files=glob.glob(my_path+'*.jpg')
 
#print (files)

fname = ''

for file in files:
    fname = (os.path.basename(fname))
    data  = {'fname': fname, 'big_image':file, 'thumb':file}
    cursor.execute(add_image, data)

#print(cnx)

cnx.commit()

cursor.close()
 
cnx.close()
