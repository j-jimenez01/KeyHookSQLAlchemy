-- Created by Vertabelo (http://vertabelo.com)
-- Last modification date: 2022-12-08 00:19:22.179

-- tables
-- Table: accesses
CREATE TABLE accesses (
    hook_number int  NOT NULL,
    door_name varchar(50)  NOT NULL,
    room_number int  NOT NULL,
    building_name varchar(50)  NOT NULL,
    CONSTRAINT accesses_pk PRIMARY KEY (hook_number,door_name,room_number,building_name)
);

-- Table: buildings
CREATE TABLE buildings (
    building_name varchar(50)  NOT NULL,
    CONSTRAINT buildings_pk PRIMARY KEY (building_name)
);

-- Table: door_names
CREATE TABLE door_names (
    door_name varchar(50)  NOT NULL,
    CONSTRAINT door_names_pk PRIMARY KEY (door_name)
);

-- Table: doors
CREATE TABLE doors (
    door_name varchar(50)  NOT NULL,
    room_number int  NOT NULL,
    building_name varchar(50)  NOT NULL,
    CONSTRAINT doors_pk PRIMARY KEY (door_name,room_number,building_name)
);

-- Table: employees
CREATE TABLE employees (
    employee_id serial  NOT NULL,
    first_name varchar(50)  NOT NULL,
    last_name varchar(50)  NOT NULL,
    CONSTRAINT employees_pk PRIMARY KEY (employee_id)
);

-- Table: hooks
CREATE TABLE hooks (
    hook_number serial  NOT NULL,
    CONSTRAINT hooks_pk PRIMARY KEY (hook_number)
);

-- Table: keys
CREATE TABLE keys (
    key_number int  NOT NULL,
    key_id serial  NOT NULL,
    CONSTRAINT keys_pk PRIMARY KEY (key_number,key_id)
);

-- Table: lost_keys
CREATE TABLE lost_keys (
    lost_date date  NOT NULL,
    request_id int  NOT NULL,
    loaned_out_date date  NOT NULL,
    CONSTRAINT lost_keys_pk PRIMARY KEY (lost_date,request_id,loaned_out_date)
);

-- Table: requests
CREATE TABLE requests (
    request_id int  NOT NULL,
    employee_id int  NOT NULL,
    room_number int  NOT NULL,
    building_name varchar(50)  NOT NULL,
    key_number int  NOT NULL,
    key_id int  NOT NULL,
    requested_date date  NOT NULL,
    loaned_out_date date  NOT NULL,
    CONSTRAINT requests_pk PRIMARY KEY (request_id,loaned_out_date)
);

-- Table: return_keys
CREATE TABLE return_keys (
    return_date date  NOT NULL,
    request_id int  NOT NULL,
    loaned_out_date date  NOT NULL,
    CONSTRAINT return_keys_pk PRIMARY KEY (return_date,request_id,loaned_out_date)
);

-- Table: rooms
CREATE TABLE rooms (
    room_number int  NOT NULL,
    building_name varchar(50)  NOT NULL,
    CONSTRAINT rooms_pk PRIMARY KEY (room_number,building_name)
);

-- foreign keys
-- Reference: accesses_door (table: accesses)
ALTER TABLE accesses ADD CONSTRAINT accesses_door
    FOREIGN KEY (door_name, room_number, building_name)
    REFERENCES doors (door_name, room_number, building_name)  
    NOT DEFERRABLE 
    INITIALLY IMMEDIATE
;

-- Reference: accesses_hook (table: accesses)
ALTER TABLE accesses ADD CONSTRAINT accesses_hook
    FOREIGN KEY (hook_number)
    REFERENCES hooks (hook_number)  
    NOT DEFERRABLE 
    INITIALLY IMMEDIATE
;

-- Reference: door_door_name (table: doors)
ALTER TABLE doors ADD CONSTRAINT door_door_name
    FOREIGN KEY (door_name)
    REFERENCES door_names (door_name)  
    NOT DEFERRABLE 
    INITIALLY IMMEDIATE
;

-- Reference: door_room (table: doors)
ALTER TABLE doors ADD CONSTRAINT door_room
    FOREIGN KEY (room_number, building_name)
    REFERENCES rooms (room_number, building_name)  
    NOT DEFERRABLE 
    INITIALLY IMMEDIATE
;

-- Reference: key_hook (table: keys)
ALTER TABLE keys ADD CONSTRAINT key_hook
    FOREIGN KEY (key_number)
    REFERENCES hooks (hook_number)  
    NOT DEFERRABLE 
    INITIALLY IMMEDIATE
;

-- Reference: lost_key_request (table: lost_keys)
ALTER TABLE lost_keys ADD CONSTRAINT lost_key_request
    FOREIGN KEY (request_id, loaned_out_date)
    REFERENCES requests (request_id, loaned_out_date)  
    NOT DEFERRABLE 
    INITIALLY IMMEDIATE
;

-- Reference: request_employee (table: requests)
ALTER TABLE requests ADD CONSTRAINT request_employee
    FOREIGN KEY (employee_id)
    REFERENCES employees (employee_id)  
    NOT DEFERRABLE 
    INITIALLY IMMEDIATE
;

-- Reference: request_key (table: requests)
ALTER TABLE requests ADD CONSTRAINT request_key
    FOREIGN KEY (key_number, key_id)
    REFERENCES keys (key_number, key_id)  
    NOT DEFERRABLE 
    INITIALLY IMMEDIATE
;

-- Reference: request_room (table: requests)
ALTER TABLE requests ADD CONSTRAINT request_room
    FOREIGN KEY (room_number, building_name)
    REFERENCES rooms (room_number, building_name)  
    NOT DEFERRABLE 
    INITIALLY IMMEDIATE
;

-- Reference: return_key_request (table: return_keys)
ALTER TABLE return_keys ADD CONSTRAINT return_key_request
    FOREIGN KEY (request_id, loaned_out_date)
    REFERENCES requests (request_id, loaned_out_date)  
    NOT DEFERRABLE 
    INITIALLY IMMEDIATE
;

-- Reference: room_building (table: rooms)
ALTER TABLE rooms ADD CONSTRAINT room_building
    FOREIGN KEY (building_name)
    REFERENCES buildings (building_name)  
    NOT DEFERRABLE 
    INITIALLY IMMEDIATE
;

-- End of file.

