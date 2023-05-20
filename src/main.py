import datetime
from pprint import pprint
from sqlalchemy import Column, String, Integer, Float, UniqueConstraint, \
    Identity, ForeignKey, distinct, bindparam
from sqlalchemy.orm import relationship, backref
from Building import Buildings
from Rooms import Rooms
from DoorName import DoorNames
from Door import Doors
from Request import Requests
from Hook import Hooks
from Accesses import Accesses
from Key import Keys
from Employee import Employees
from ReturnKey import ReturnKeys
from LostKey import LostKeys

import sqlalchemy.sql.functions
from db_connection import Session, engine
from orm_base import metadata
import logging


def delete_key(session):
    print("Deleting Key 1")
    choice = 1
    requests = session.query(Requests).filter(Requests.key_id == choice)
    for req in requests:
        session.query(ReturnKeys).filter(ReturnKeys.request_request_id == req.request_id).delete()
        session.query(LostKeys).filter(LostKeys.request_request_id == req.request_id).delete()

    session.query(Requests).filter(Requests.key_id == choice).delete()
    session.query(Keys).filter(Keys.key_id == choice).delete()
    session.commit()
    print("check data grip key table")

def delete_employee(session):
    choice = 1
    emp = session.query(Employees).filter(Employees.employee_id == choice)[0]
    hisRequests = session.query(Requests).filter(Requests.employee_id == choice)
    for req in hisRequests:
        session.query(ReturnKeys).filter(ReturnKeys.requests == req).delete()
        session.query(LostKeys).filter(LostKeys.requests == req).delete()

    session.query(Requests).filter(Requests.employee_id == emp.employee_id).delete()
    session.query(Employees).filter(Employees.employee_id == choice).delete()
    session.commit()
    print("\ncheck data grip employee table")

def addDoor(session,building,hook):
    room2: Rooms = Rooms(200,building)
    session.add(room2)
    session.commit()
    door_name2: DoorNames = DoorNames("SouthWest")
    session.add(door_name2)
    session.commit()
    door2: Doors = Doors(door_name2,room2)
    session.add(door2)
    session.commit()
    hook.add_door(door2)
    session.commit()
    print("\ncheck data grip DoorNames,Room, and Accesses")

def create_key(session,hook):
    key2: Keys = Keys(hook)
    session.add(key2)
    session.commit()
    print("\ncheck data grip Key & Hook Table")

def access_rooms(session):
    print("Checking employee David Brown with employee_id 5")
    acrm = session.query(Requests).filter(Requests.employee_id == 5)
    for e in acrm:
        print("Rooms can enter are",e.room_number)

def losing_a_key(session):
    print("\nWe are getting rid of key 4 since you have lost it!!\n")
    choice = 4
    emp = session.query(Keys).filter(Keys.key_id == choice)[0]
    hisRequests = session.query(Requests).filter(Requests.key_id == choice)
    for req in hisRequests:
        session.query(ReturnKeys).filter(ReturnKeys.requests == req).delete()
        session.query(LostKeys).filter(LostKeys.requests == req).delete()

    session.query(Requests).filter(Requests.key_id == emp.key_id).delete()
    session.query(Keys).filter(Keys.key_id == choice).delete()
    session.commit()
    print("\ndeleted the key check the table keys on data grip\nALSO YOU OWE $25 DOLLARS FOR LOSING THEY KEY")

def request_room(session):
    userID =5
    print("\nWe will use Professor Brown employee_id 5 for this example\nAll of the rooms:")
    rooms = session.query(Rooms)
    i = 0
    for room in rooms:
        print(i, ". ", room)
        i += 1
    chosenRoom = None
    choice = int(input("Enter row number of the room number you would like to enter: "))
    chosenRoom = rooms[choice]
    print(chosenRoom)
    haveAccess = session.query(Requests).filter(chosenRoom.room_number == Requests.room_number and
                                                        chosenRoom.building_name == Requests.building_name and
                                                        userID == Requests.employee_id)
    for req in haveAccess:
        returned = session.query(ReturnKeys).filter(ReturnKeys.request_request_id == req.request_id)
        c = 0
        for r in returned:
            c += 1
        if c == 0:
            # you have not returned it
            print("You already have access to this room!")
            return
    emp = session.query(Employees).filter(userID == Employees.employee_id)[0]
    hookdoor = session.query(Accesses).filter(chosenRoom.room_number == Accesses.room_number and
                                                           chosenRoom.building_name == Accesses.building_name)[0]
    key = session.query(Keys).filter(Keys.key_number == hookdoor.hook_number)[0]
    newReq: Requests = Requests(emp, chosenRoom, key)
    session.add(newReq)
    session.commit()
    print("\nSuccessfully submitted a Request check request table on datagrip")



def key_issue(session):
    pass

def get_room(session):
    print("")
    for x in range(6):
        acrm = session.query(Requests).filter(Requests.employee_id == x)
        name = session.query(Employees).filter(Employees.employee_id == x)
        for n in name:
            for e in acrm:
                print(f"Employee {n.first_name} {n.last_name} can enter these rooms {e.room_number}")


if __name__ == '__main__':
    #still works with or without this
    # logging.basicConfig()
    # # use the logging factory to create our first logger.
    # logging.getLogger("sqlalchemy.engine").setLevel(logging.INFO)
    # # use the logging factory to create our second logger.
    # logging.getLogger("sqlalchemy.pool").setLevel(logging.DEBUG)

    metadata.drop_all(bind=engine)  # start with a clean slate while in development

    # Create whatever tables are called for by our "Entity" classes.  The simple fact that
    # your classes that are subtypes of Base have been loaded by Python has populated
    # the metadata object with their definition.  So now we tell SQLAlchemy to create
    # those tables for us.
    metadata.create_all(bind=engine)

    # Do our database work within a context.  This makes sure that the session gets closed
    # at the end of the with, much like what it would be like if you used a with to open a file.
    # This way, we do not have memory leaks.
    with Session() as sess:
        sess.begin()
        print ("Inside the session, woo hoo.")
        building1: Buildings = Buildings("Engineering and Computer Science")
        building2: Buildings = Buildings("Fine Arts 1")
        building3: Buildings = Buildings("Hall of Science")
        building4: Buildings = Buildings("Horn Center")
        building5: Buildings = Buildings("Psychology")
        building6: Buildings = Buildings("Peterson Hall")
        sess.add(building1)
        sess.add(building2)
        sess.add(building3)
        sess.add(building4)
        sess.add(building5)
        sess.add(building6)
        sess.commit()

        # create a room variable
        room1: Rooms = Rooms(100, building1)
        room2: Rooms = Rooms(101, building2)
        room3: Rooms = Rooms(200, building5)
        room4: Rooms = Rooms(107, building6)
        room5: Rooms = Rooms(419, building3)
        room6: Rooms = Rooms(124, building4)
        room7: Rooms = Rooms(518, building3)
        sess.add(room1)
        sess.add(room2)
        sess.add(room3)
        sess.add(room4)
        sess.add(room5)
        sess.add(room6)
        sess.add(room7)
        sess.commit()
        # create a door name variable
        doorName1: DoorNames = DoorNames("North")
        doorName2: DoorNames = DoorNames("West")
        doorName3: DoorNames = DoorNames("South")
        doorName4: DoorNames = DoorNames("East")
        doorName5: DoorNames = DoorNames("Front")
        doorName6: DoorNames = DoorNames("Back")
        sess.add(doorName1)
        sess.add(doorName2)
        sess.add(doorName3)
        sess.add(doorName4)
        sess.add(doorName5)
        sess.add(doorName6)
        sess.commit()
        # create a door
        door1: Doors = Doors(doorName1, room1)
        door2: Doors = Doors(doorName2, room2)
        door3: Doors = Doors(doorName3, room3)
        door4: Doors = Doors(doorName2, room4)
        door5: Doors = Doors(doorName1, room5)
        door6: Doors = Doors(doorName3, room6)
        door7: Doors = Doors(doorName5, room7)
        door8: Doors = Doors(doorName1, room6)
        door9: Doors = Doors(doorName6, room2)
        sess.add(door1)
        sess.add(door2)
        sess.add(door3)
        sess.add(door4)
        sess.add(door5)
        sess.add(door6)
        sess.add(door7)
        sess.add(door8)
        sess.add(door9)
        sess.commit()
        # create a hook
        hook1: Hooks = Hooks()
        hook2: Hooks = Hooks()
        hook3: Hooks = Hooks()
        hook4: Hooks = Hooks()
        hook5: Hooks = Hooks()
        hook6: Hooks = Hooks()
        hook7: Hooks = Hooks()
        hook8: Hooks = Hooks()
        sess.add(hook1)
        sess.add(hook2)
        sess.add(hook3)
        sess.add(hook4)
        sess.add(hook5)
        sess.add(hook6)
        sess.add(hook7)
        sess.add(hook8)
        sess.commit()

        key1: Keys = Keys(hook2)
        key2: Keys = Keys(hook1)
        key3: Keys = Keys(hook5)
        key4: Keys = Keys(hook2)
        key5: Keys = Keys(hook6)
        key6: Keys = Keys(hook8)
        key7: Keys = Keys(hook7)
        key8: Keys = Keys(hook2)
        key9: Keys = Keys(hook3)
        key10: Keys = Keys(hook1)
        key11: Keys = Keys(hook2)
        key12: Keys = Keys(hook7)
        key13: Keys = Keys(hook4)
        sess.add(key1)
        sess.add(key2)
        sess.add(key3)
        sess.add(key4)
        sess.add(key5)
        sess.add(key6)
        sess.add(key7)
        sess.add(key8)
        sess.add(key9)
        sess.add(key10)
        sess.add(key11)
        sess.add(key12)
        sess.add(key13)
        sess.commit()

        # create Accesses!
        hook1.add_door(door1)
        hook1.add_door(door2)
        hook2.add_door(door3)
        hook2.add_door(door4)
        hook3.add_door(door9)
        hook4.add_door(door4)
        hook5.add_door(door5)
        hook6.add_door(door6)
        hook7.add_door(door7)
        hook8.add_door(door8)
        sess.commit()

        # add employees
        employee1: Employees = Employees("Jose", "Jimenez")
        employee2: Employees = Employees("Darin", "Goldstein")
        employee3: Employees = Employees("Sarah", "Taylor")
        employee4: Employees = Employees("Frank", "Murgolo")
        employee5: Employees = Employees("David", "Brown")
        employee6: Employees = Employees("Neal","Terrell")
        sess.add(employee1)
        sess.add(employee2)
        sess.add(employee3)
        sess.add(employee4)
        sess.add(employee5)
        sess.add(employee6)
        sess.commit()

        req1: Requests = Requests(employee1, room6, key5)
        req2: Requests = Requests(employee5, room5, key3)
        req3: Requests = Requests(employee3, room2, key1)
        req4: Requests = Requests(employee2, room1, key1)
        req5: Requests = Requests(employee3, room4, key4)
        req6: Requests = Requests(employee4, room3, key2)
        sess.add(req1)
        sess.add(req2)
        sess.add(req3)
        sess.add(req4)
        sess.add(req5)
        sess.add(req6)
        sess.commit()
        # add lostkey
        lostkey1: LostKeys = LostKeys(req1, datetime.datetime(2022, 11, 15))
        lostkey2: LostKeys = LostKeys(req4, datetime.datetime(2020, 3, 21))
        lostkey3: LostKeys = LostKeys(req3, datetime.datetime(2021, 7, 11))
        lostkey4: LostKeys = LostKeys(req2, datetime.datetime(2019, 7, 5))
        lostkey5: LostKeys = LostKeys(req1, datetime.datetime(2022, 2, 7))
        lostkey6: LostKeys = LostKeys(req1, datetime.datetime(2022, 9, 10))
        lostkey7: LostKeys = LostKeys(req6, datetime.datetime(2022, 11, 30))
        sess.add(lostkey1)
        sess.add(lostkey2)
        sess.add(lostkey3)
        sess.add(lostkey4)
        sess.add(lostkey5)
        sess.add(lostkey6)
        sess.add(lostkey7)
        sess.commit()

        ret1: ReturnKeys = ReturnKeys(req1, datetime.datetime(2022, 11, 10))
        ret2: ReturnKeys = ReturnKeys(req4, datetime.datetime(2022, 3, 21))
        ret3: ReturnKeys = ReturnKeys(req3, datetime.datetime(2021, 7, 6))
        ret4: ReturnKeys = ReturnKeys(req2, datetime.datetime(2001, 9, 14))
        ret5: ReturnKeys = ReturnKeys(req1, datetime.datetime(2022, 8, 13))
        ret6: ReturnKeys = ReturnKeys(req1, datetime.datetime(2022, 9, 10))
        ret7: ReturnKeys = ReturnKeys(req6, datetime.datetime(2022, 11, 13))
        sess.add(ret1)
        sess.add(ret2)
        sess.add(ret3)
        sess.add(ret4)
        sess.add(ret5)
        sess.add(ret6)
        sess.add(ret7)
        sess.commit()


        #------------------------------------------------------------------------------------------------------------

        #a. create a new key DONE
        create_new_key = input("Ready to create a new key? ")
        create_key(sess,hook1)

        #b. request access to a given room by a given employee DONE
        req_room = input("\nReady to request access to a given room by a given employee? ")
        request_room(sess)

        #c. capture the issue of a key to an employee
        issue_key = input("\nReady to capture the issue of a key to an employee? ")
        print("Unfortunately I wasn't sure what this one meant and how to solve it :(")

        #d. capture losing a key DONE
        losing_key = input("\nReady to capture losing a key? ")
        losing_a_key(sess)

        #e. report out all the rooms that an employee can enter, given the keys that he/she already has DONE
        emp_acc = input("\nReady to report out all the rooms that an employee can enter, given the keys that he/she already has? ")
        access_rooms(sess)

        #f. delete a key DONE
        deletethis = input("\nReady to delete key? ")
        delete_key(sess)

        #g. delete an employee Done
        deletethis2 = input("\nReady to delete employee? ")
        delete_employee(sess)

        #h. add a new door that can be opened by an existing hook DONE
        newdoor = input("\nReady to add a new door that can be opened by an existing hook? ")
        addDoor(sess,building1,hook1)

        #i. update an access request to move it to a new employee
        update = input("\nReady to update an access request to move it to a new employee? ")
        print("Unfortunately I could not solve this one :(")

        #j. report out all the employees who can get into a room DONE
        get_a_room = input("\nReady to report out all the employees who can get into a room? ")
        get_room(sess)

    print("Exiting Normally")

