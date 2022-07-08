# usage python3 booking-api-integration.py


import mysql.connector
import requests
import os
import shutil


dr1 = "/home/pi/project/face-recognition/dataset/door1"
dr2 = "/home/pi/project/face-recognition/dataset/door2"


def readall():
    print("Reading online booking")
    rlist = []
    clist = []
    rclist = [(0, 0), (0, 0)]
    room_id = 0
    client_id = 0



    try:
        connection = mysql.connector.connect(host='sql598.main-hosting.eu',
                                             database='u810911882_sweethotel',
                                             user='u810911882_sweethotel',
                                             password='Sweethotel_gro1')

        cursor = connection.cursor()
        sql_fetch_blob_query = """SELECT * from online_booking """
#         sql_fetch_blob_query = """SELECT * from email_verification """

        cursor.execute(sql_fetch_blob_query)
        record = cursor.fetchall()
        print(cursor.rowcount)
        rc = cursor.rowcount
        if rc > 0:
         for row in record:
          if row[11] == "active":
            print("active")
            room_id = row[3]
            booking_id = row[0]
            client_id = row[2]
            print("Room ID = ", room_id)
            print("Booking ID = ", booking_id)
            print("Client ID = ", client_id)
            rlist.append(int(row[3]))
            clist.append(int(row[2]))
            rclist = [(rlist[i], clist[i]) for i in range(0, len(rlist))]
            print(rclist)

          elif row[11] == "history" or row[11] == "pending":
            print("online but not active")
         return room_id, client_id, rclist


        else:
            print("None")
            shutil.rmtree(dr1)
            shutil.rmtree(dr2)
            print("emptied")
            os.makedirs(dr1)
            os.makedirs(dr2)
            print("created")
            return room_id,client_id, rclist
            
  
            os.system ("python3 face-encoding.py --dataset dataset --encodings encodings.pickle --detection-method hog")
        
            print(" Completed Training!")
            print("Initializing Face Recognition!")
        
            os.system ("python3 face-working-recog-door1.py --cascade haarcascade_frontalface_default.xml --encodings encodings.pickle --door1 14 --door2 17")


    except mysql.connector.Error as error:
        print("Failed to read BLOB data from MySQL table {}".format(error))

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection is closed for online booking")



def readall2(x):
 print("searching image url")
 if x == 0:
    return 0
    print("no client")

 else:
    print("client found")
    try:     
        connection = mysql.connector.connect(host='sql598.main-hosting.eu',
                                             database='u810911882_sweethotel',
                                             user='u810911882_sweethotel',
                                             password='Sweethotel_gro1')

        cursor = connection.cursor()
        sql_fetch_blob_query = """SELECT * from client where id = %s"""

        cursor.execute(sql_fetch_blob_query, (x,))
        record = cursor.fetchall()
        for row in record:
            client_photo = row[1]
            url_root = "http://sweethotel.link/administrator/images/user_images/"
            img_path = url_root + client_photo
            return img_path

    except mysql.connector.Error as error:
        print("Failed to read BLOB data from MySQL table {}".format(error))

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection is closed for clients")

def save_img(x, y, z):
    for a,b in x:
        print(a)


        if a == 0:
             print("No Booking Found, Cleared Dataset")
             os.system ("python3 face-encoding.py --dataset dataset --encodings encodings.pickle --detection-method hog")

             print(" Completed Training!")
             print("Initializing Face Recognition!")

             # os.system ("python3 face-recognition-video-2.py --cascade haarcascade_frontalface_default.xml --encodings encodings.pickle --door1 14 --door2 17")
             os.system ("python3 face-working-recog-door1.py --cascade haarcascade_frontalface_default.xml --encodings encodings.pickle --door1 14 --door2 17")

#################################### DOOR 1 - SOLENOID LOCK - USB CAMERA (src = 1)
        elif a == 35: ###dating 33
             print("saving to door 1")
             response = requests.get(str(y))
             file = open("/home/pi/project/face-recognition/dataset/door1/001.jpg", "wb")

             file.write(response.content)
             file.close()
             print("door1")
             cp = ("/home/pi/project/face-recognition/clients/%s.jpg" % (int(z)))
             file2 = open(cp, "wb")

             file2.write(response.content)
             file2.close()
             print("client folder")

             os.system ("python3 face-encoding.py --dataset dataset --encodings encodings.pickle --detection-method hog")

             print(" Completed Training!")
             print("Initializing Face Recognition!")

             os.system ("python3 face-working-recog-door1.py --cascade haarcascade_frontalface_default.xml --encodings encodings.pickle --door1 14 --door2 17")

             ####### DOOR 2 - PWM SERVO MOTOR - PI CAMERA (src = 0)
        elif a == 36: #### dating 34
            print("saving to door 2")

        #      response = requests.get(str(y))
        #      file = open("/home/pi/project/face-recognition/dataset/door2/002.jpg", "wb")
        # #file = open("003.jpg", "wb")
        #      file.write(response.content)
        #      file.close()
        #      print("door2")
        #      cp = ("/home/pi/project/face-recognition/clients/%s.jpg" % (int(z)))
        #      file2 = open(cp, "wb")
        #
        #      file2.write(response.content)
        #      file2.close()
        #      print("client folder")
        #
        #      os.system ("python3 face-encoding.py --dataset dataset --encodings encodings.pickle --detection-method hog")
        #
        #      print(" Completed Training!")
        #      print("Initializing Face Recognition!")
        #
        #      os.system ("python3 face-working-recog-door2.py --cascade haarcascade_frontalface_default.xml --encodings encodings.pickle --door1 14 --door2 17")

def tpl(x):

    for i,j in x:
        print(i)
        print(j)

readall()

room_rtn, client_rtn, rclist_rtn = readall()
print(rclist_rtn)
readall2(client_rtn)
img_rtn = readall2(client_rtn)
print (img_rtn)


#no booking tes
# client_rtn = 0
# rclist_rtn = [(0, 0), (0, 0)]
# img_rtn = 0

# tpl(rclist_rtn)
save_img(rclist_rtn, img_rtn, client_rtn)

