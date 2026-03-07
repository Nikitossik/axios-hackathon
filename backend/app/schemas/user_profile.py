from pydantic import BaseModel, Field, ConfigDict
from ..utils.enums import UserGenderEnum, UserAgeGroupEnum, UserDrivingStyleEnum

class UserProfileBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    age_group: UserAgeGroupEnum = Field(..., description="User's age group")
    driving_experience_years: int = Field(..., description="Years of driving experience")
    gender_identity: UserGenderEnum = Field(..., description="User's gender identity")
    driving_style: UserDrivingStyleEnum | None = Field(None, description="User's driving style")

    
class UserProfileUpdate(BaseModel):
    age_group: UserAgeGroupEnum | None = Field(None, description="User's age group")
    driving_experience_years: int | None = Field(None, description="Years of driving experience")
    driving_style: UserDrivingStyleEnum | None = Field(None, description="User's driving style")
class UserProfileIn(UserProfileBase):
    pass

class UserProfileOut(UserProfileBase):
    pass
    