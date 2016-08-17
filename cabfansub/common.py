import datetime
import json
import random
import string

import bcrypt


def paramsParse(paramsList, paramsValue):
    params = {}
    for paramName, paramType in paramsList.items():
        tmp = paramsValue[paramName]
        if paramType == "int":
            tmp = int(tmp)
        elif paramType == "float":
            tmp = float(tmp)
        elif paramType == "json":
            tmp = json.loads(tmp)
        elif paramType == "bool":
            if tmp == "true":
                tmp = True
            else:
                tmp = False
        params[paramName] = tmp
    return params


def overThreshold(coLevel, dustLevel):
    return coLevel >= 222 or dustLevel >= 0.2


def timeSubtract(days=0, hours=0, minutes=0, seconds=0):
    delta = datetime.timedelta(days=days, hours=hours, minutes=minutes, seconds=seconds)
    return datetime.datetime.now(datetime.timezone.utc) - delta


def hashPassword(pwd):
    if type(pwd) is str:
        pwd = pwd.encode("utf-8")
    return bcrypt.hashpw(pwd, bcrypt.gensalt())


def checkPassword(hash, pwd):
    if type(pwd) is str:
        pwd = pwd.encode("utf-8")
    if type(hash) is str:
        hash = hash.encode("utf-8")
    return bcrypt.hashpw(pwd, hash) == hash


def genRandomString(length):
    rand = random.SystemRandom()
    letters = string.ascii_letters + string.digits
    return ''.join(rand.choice(letters) for _ in range(length))


def utcNow():
    return datetime.datetime.now(datetime.timezone.utc)


def fromTimestamp(timestamp):
    timestamp = int(timestamp)
    return datetime.datetime.fromtimestamp(timestamp=timestamp, tz=datetime.timezone.utc)


def verifyPhoneNumber(phone):
    try:
        obj = phonenumbers.parse(phone, None)
    except phonenumbers.NumberParseException:
        return False
    return phonenumbers.is_valid_number(obj) and phonenumbers.is_possible_number(obj)


def genRandomNumber(rangeFrom, rangeTo):
    rand = random.SystemRandom()
    return rand.randint(rangeFrom, rangeTo)
