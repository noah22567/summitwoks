import pymysql

# def mkdb():
#     connection = pymysql.connect(host='127.0.0.1',
#                                      user='root',
#                                      password='Ul1*12characters',
#                                      db='class',
#                                      charset='utf8mb4',
#                                      cursorclass=pymysql.cursors.DictCursor)
#     try:
#         with connection.cursor() as cursor:
#             # Create a new record
#             sql = "Create database hotels; use hotels;\
#                  create table hotels_info(\
#                  Hotel_Name varchar(20) not null,\
#                  Location varchar(25) not null,\
#                  Availability int);"
#
#             cursor.execute(sql)
#
#         # connection is not autocommit by default. So you must commit to save
#         # your changes.
#         connection.commit()
#     finally:
#         connection.close()



def manMySQL(inputs):
    connection = pymysql.connect(host='127.0.0.1',
                                 user='root',
                                 password='Ul1*12characters',
                                 db='hotels',
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)
    try:
        with connection.cursor() as cursor:
            # Create a new record
            cursor.execute(inputs)
        # connection is not autocommit by default. So you must commit to save
        # your changes.
        connection.commit()
    except:
        pass
    finally:
        connection.close()

class Hotel:
    roomcount = 0
    occupiedCnt = 0

    def __init__(self,name,location):
        self.location = location
        self.numOFRooms = [None] * 10
        self.__name__ = name
        availability = self.roomcount - self.occupiedCnt
        manMySQL("Insert into hotels_info(Hotel_Name, Location, Availability) values ('%s','%s','%s')"% \
                (str(name), str(location),str(availability)))
        manMySQL("Create table %s(\
            Room_Number int unique, \
            Bed_Type varchar(15),\
            Smoking varchar(20),\
            Rate int,\
            Customer_Name varchar(20) null);" % \
                  name)

    def addRoom(self,roomnbr,bedtype,smoking,rate):
        self.numOFRooms[self.roomcount] = Room(roomnbr,bedtype,smoking,rate,self.__name__)
        manMySQL("insert into %s(Room_Number,Bed_Type,Smoking, Rate) values ('%s','%s','%s','%s')"% \
                  (str(self.__name__),str(roomnbr),bedtype,smoking,str(rate)))
        self.roomcount += 1

    def isEmpty(self):
        if self.occupiedCnt > 1:
            return False
            pass
        return True

    def isFull(self):
        if self.occupiedCnt == len(self.numOFRooms):
            return False
            pass
        return True

    def addReservation(self,occupentsname, smoking,bedtype):
        isocupied = False
        try:
            for room in self.numOFRooms:
                try:
                    if room.isOccupied() == False:
                        if room.getBedType() == bedtype:
                            if room.getSmoking() == smoking:
                                self.occupiedCnt += 1
                                isocupied = True
                                room.setOccupied()
                                room.setOccupant(occupentsname)
                                print("A reservation has been made for room: ", room.getRoomNum())
                                manMySQL("update %s\
                                set Customer_Name = %s\
                                where Room_Number = %s" % \
                                         (str(self.__name__),occupentsname,str(room.getRoomNum())))
                                break
                except:
                    pass
            if isocupied == False: raise NoRoom("None of the rooms fit the requirements.")
        except NoRoom:
            print('None of the rooms fit the requirements.')

    def cancelReservation(self,roomnbr,occupantName):
        self.occupiedCnt -= 1
        for room in self.numOFRooms:
            try:
                if room.roomNum == roomnbr:
                    room.roomNum = roomnbr
                    room.setOccupant(None)
                    manMySQL("update %s\
                    set Customer_Name = %s\
                    where Room_Number = %s" % \
                    (str(self.__name__), "None", str(room.getRoomNum())))
                    print("The reservation for "+occupantName+" in room "+str(roomnbr)+" has been canceled.")
            except:
                pass

    def _findReservation(self,occupantName):
        found = False
        count = 0
        try:
            for room in self.numOFRooms:
                if occupantName == room.getOccupant():
                    found = True
                    return print('Then index of room ', room.getRoomNum(), ' is ', count)
                count+=1
        except AttributeError:
            return print('NOT_FOUND')

    def printReservationList(self):
        for room in self.numOFRooms:
            try:
                if room.isOccupied() == True:
                    print("Room Number: ", room.getRoomNum(), '\n',
                    "Occupant name: ", room.getOccupant(), '\n',
                    "Smoking room: ", room.getSmoking(), '\n',
                    "Bed Type: ", room.getBedType(), '\n',
                    "Rate: " , room.getRoomRate(), '\n')
            except AttributeError:
                pass

    def getDailySales(self):
        alist = []
        for room in self.numOFRooms:
            try:
                if room.isOccupied() == True:
                    alist.append(room.getRoomRate())
            except AttributeError:
                break
        return sum(alist)

    def occupancyPercentage(self):
        alist = []
        try:
            for room in self.numOFRooms:
                if room.isOccupied() == True:
                    alist.append(1)
        except AttributeError:
            return len(alist)/self.roomcount*100

    def __str__(self):

        print("Hotel Name :".center(40,' ')+self.__name__+"\n",
                "Number of Rooms :".center(40,' ') + str(self.roomcount)+'\n',
                "Number of Occupied Rooms :".center(40,' ')+ str(self.occupiedCnt)+'\n',
                'Room Details are: \n'.center(40,' '))
        for room in self.numOFRooms:
            try:
                print("Room Number: ", room.getRoomNum())
                if room.isOccupied() == True:
                    print("Occupant name: ", room.getOccupant())
                print("Bed Type: ", room.getBedType())
                if room.getSmoking() == "smoking":
                    print("Smoking room: n")
                else:
                    print("Smoking room: s")
                print("Rate: ", room.getRoomRate(),'\n')
            except AttributeError:
                pass

class Room:

    occupantName = None
    occupied = False

    def __init__(self,int,String,char,double,name):
        self.roomNum = int
        self.bedType = String
        self.smoking = char
        self.rate = double
        self.HotelName = name

    def getBedType(self):
        return self.bedType

    def getSmoking(self):
        return self.smoking

    def getRoomNum(self):
        return self.roomNum

    def getRoomRate(self):
        return self.rate

    def getOccupant(self):
        return self.occupantName

    def setOccupied(boolean):
        boolean.occupied = True

    def setOccupant(self,String):
        self.occupantName = String
        manMySQL("update %s \
         set Customer_Name = '%s' \
         where Room_Number = %s "% \
                 (self.HotelName,String,self.roomNum))

        if String == None:
            self.occupied = False

    def setRoomNum(self,int):
        self.roomNum = int
        manMySQL("update %s \
         set Room_Number = '%s' \
         where Room_Number = %s "% \
                 (self.HotelName,int,self.roomNum))

    def setBedType(self,String):
        self.bedType = String
        manMySQL("update %s \
         set Bed_Type= '%s' \
         where Room_Number = %s "% \
                 (self.HotelName,String,self.roomNum))

    def setRate(self,double):
        self.rate = double
        manMySQL("update %s \
         set Rate = '%s' \
         where Room_Number = %s "% \
                 (self.HotelName,rate,self.roomNum))

    def setSmoking(self,char):
        self.smoking = char
        manMySQL("update %s \
         set Smoking = '%s' \
         where Room_Number = %s "% \
                 (self.HotelName,char,self.roomNum))

    def isOccupied(self):
        return self.occupied

class NoRoom(Exception):
    def __init__(self,msg):
        super().__init__(msg)

hotelone = Hotel('bobss','sanford')

hoteltwo = Hotel('rants','fayettville')

hotelone.addRoom(101,"queen", 'non-smoking' ,150)
hotelone.addRoom(102,"king", 'smoking' ,200)

hotelone.addRoom(103,"queen", 'smoking' ,100)

hotelone.addRoom(104,"twin", 'non-smoking' ,130)

hotelone.addRoom(105,"king", 'non-smoking' ,250)
hotelone.addRoom(106,"queen", 'smoking' ,100)

hotelone.addReservation('passme','smoking','twin')
hotelone.addReservation('wassup','non-smoking','twin')
hotelone.addReservation('yaman','non-smoking','queen')
hotelone.addReservation('noah','smoking','king')

print('occupancy percentage', hotelone.occupancyPercentage())

hotelone.cancelReservation(102,'noah')

hotelone.numOFRooms[3].setSmoking('smoking')

print('is occupied ',hotelone.numOFRooms[1].isOccupied())

print('room rate ',hotelone.numOFRooms[1].getRoomRate())

hotelone.occupancyPercentage()

print('the daily sales are ',hotelone.getDailySales())

hotelone.printReservationList()

hotelone._findReservation("noah")

print('occupancy percentage', hotelone.occupancyPercentage())

print(hotelone.isEmpty())
print(hotelone.isFull())
hotelone.getDailySales()

hotelone.__str__()









