from pydantic import BaseModel, Field, ConfigDict
from ..utils.enums import UserGenderEnum, UserAgeGroupEnum

class UserProfileBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    age_group: UserAgeGroupEnum = Field(..., description="User's age group")
    driving_experience_years: int = Field(..., description="Years of driving experience")
    gender_identity: UserGenderEnum = Field(..., description="User's gender identity")
    gender_self_description: str | None = Field(None, max_length=100, description="Optional self-description of gender identity")
    
    
class UserProfileIn(UserProfileBase):
    pass

class UserProfileOut(UserProfileBase):
    pass
    