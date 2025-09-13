from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel


# Shared properties
class LabResultBase(BaseModel):
    test_name: str
    test_date: datetime
    result_value: str
    normal_range: Optional[str] = None
    unit: Optional[str] = None
    notes: Optional[str] = None


# Properties to receive on lab result creation
class LabResultCreate(LabResultBase):
    user_id: int


# Properties to receive on lab result update
class LabResultUpdate(LabResultBase):
    test_name: Optional[str] = None
    test_date: Optional[datetime] = None
    result_value: Optional[str] = None


# Properties shared by models stored in DB
class LabResultInDBBase(LabResultBase):
    id: int
    user_id: int
    created_at: datetime

    class Config:
        orm_mode = True


# Properties to return to client
class LabResult(LabResultInDBBase):
    pass


# Properties stored in DB
class LabResultInDB(LabResultInDBBase):
    pass


# Properties for listing lab results
class LabResultsList(BaseModel):
    results: List[LabResult]
    total: int
