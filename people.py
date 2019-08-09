"""
    This is the people module and supports all the ReST actions for the
    PEOPLE collection
    """

# System modules
from datetime import datetime


# 3rd party modules
from flask import make_response, abort

import json
import redis


def get_timestamp():
    return datetime.now().strftime(("%Y-%m-%d %H:%M:%S"))

# Data to serve with our API
PEOPLE = {
    "Farrell" :{
        "fname": "Doug",
        "lname": "Farrell",
        "timestamp": get_timestamp(),
    },
    "Brockman": {
        "fname": "Kent",
        "lname": "Brockman",
        "timestamp": get_timestamp(),
    },
    "Easter": {
        "fname": "Bunny",
        "lname": "Easter",
        "timestamp": get_timestamp(),
    }
}
r = redis.StrictRedis(db=1,host="m-nginx_db_1",charset="utf-8",port = 6379, decode_responses=True)
#r.flushdb()


for l_name, person in PEOPLE.items():
        #print(l_name,json.dumps(person))
#r.execute_command('JSON.SET', l_name, '.', json.dumps(person))
#print(type(l_name))
#print(l_name,person)
#print(type(json.dumps(person)))
        if not r.exists(l_name):
            stringified_obj= json.dumps(person)
        #print(l_name,stringified_obj)
            r.set(str(l_name), stringified_obj)
    #pipe.hmset(l_name, person)
r.bgsave()
#pipe.execute()

def read_all():
    """
        This function responds to a request for /api/people
        with the complete lists of people
        :return:        json string of list of people
        """
    # Create the list of people from our data
    reply=[]
    
    for key in r.keys():
        #print (item)
        #print(type(item))
        #key=item
        #print(r.get((item))) --WRONG
        #print(key)
        #print(type(key))
        ans=r.get(key)
        #print(type(ans))
        #print(ans)
        #print("xxxxxxxxxx")
        #ans=json.dumps(ans)
        #print(ans)
        reply.append(json.loads(ans))
    #reply.append(json.loads(r.execute_command('JSON.GET', str(item))))

    return [res for res in reply]



def read_one(id):
    """
        This function responds to a request for /api/people/{lname}
        with one matching person from people
        :param lname:   last name of person to find
        :return:        person matching last name
        """
    # Does the person exist in people?
    if id in r.keys():
        person = r.get(id)
        person=json.loads(person)

    # otherwise, nope, not found
    else:
        abort(
              404, "Person with id {id} not found".format(id=id)
              )

    return person


def create(person):
    """
        This function creates a new person in the people structure
        based on the passed in person data
        :param person:  person to create in people structure
        :return:        201 on success, 406 on person exists
        """
    lname = person.get("lname", None)
    fname = person.get("fname", None)
    
    person={
        "fname":fname,
        "lname": lname,
        "timestamp": get_timestamp(),
            }
    #print(lname,fname,person)

    # Does the person exist already?
    #
    #print(r.exists(lname))
    if not r.exists(lname):
        #print("inside")
        #print(lname,fname,person)
        #s_json = json.dumps(person)
        stringified_obj= json.dumps(person)
        #print(lname,stringified_obj)
        r.set(str(lname), stringified_obj)
        r.bgsave()
        return make_response(
                             "{lname} successfully created".format(lname=lname), 201
                             )

# Otherwise, they exist, that's an error
    else:
        abort(
              406,
              "Peron with last_name {lname} already exists".format(lname=lname),
          )


def update(lname, person):
    """
        This function updates an existing person in the people structure
        :param lname:   last name of person to update in the people structure
        :param person:  person to update
        :return:        updated person structure
        """
    
    # Does the person exist in people?
    if r.exists(lname):
        r.delete(lname)
        create(person)
        ans=r.get(str(lname))
        ans=json.loads(ans)
        r.bgsave()
        return ans

    
    # otherwise, nope, that's an error
    else:
        abort(
              404, "Person with last name {lname} not found".format(lname=lname)
              )


def delete(lname):
    """
        This function deletes a person from the people structure
        :param lname:   last name of person to delete
        :return:        200 on successful delete, 404 if not found
        """
    # Does the person to delete exist?
    if r.exists(lname):
        r.delete(lname)
        r.bgsave()
        return make_response(
                             "{lname} successfully deleted".format(lname=lname), 200
                             )
    
    # Otherwise, nope, person to delete not found
    else:
        abort(
              404, "Person with last name {lname} not found".format(lname=lname)
              )
