import enum

class UserGenderEnum(str, enum.Enum):
    male= "male"    
    female = "female"
    non_binary = "non_binary"
    self_describe = "self_describe"


class UserAgeGroupEnum(str, enum.Enum):
    age_18_25 = "18_25"
    age_25_35 = "25_35"
    age_35_plus = "35_plus"

class UserDrivingStyleEnum(str, enum.Enum):
    safe = "safe"
    dynamic = "dynamic"
    eco = "eco"
    vibe = "vibe"