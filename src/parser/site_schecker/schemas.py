import datetime
from typing import List
from pydantic import BaseModel, ConfigDict


class CheckResult(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    result: str


class CheckResultError(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    result: str
    error: str
    trace: str


class CheckZamenaResult(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    result: str


class CheckZamenaResultFailed(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    result: str = "Error"
    error: str
    trace: str


class CheckZamenaResultSuccess(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    result: str = "Success"
    link: str
    images: List[str]
    date: datetime.date


class CheckZamenaResultInvalidFormat(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    result: str = "InvalidFormat"
    link: str
    file: str
    date: datetime.date


class CheckZamenaResultFailedDownload(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    result: str = "FailedDownload"
    link: str
    date: datetime.date


class CheckZamenaResultHashChanged(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    result: str = "HashChanged"
    link: str
    images: List[str]
    date: datetime.date


class CheckResultFoundNew(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    result: str = "FoundNew"
    checks: List[
        CheckZamenaResult
        | CheckZamenaResultSuccess
        | CheckZamenaResultFailed
        | CheckZamenaResultInvalidFormat
        | CheckZamenaResultFailedDownload
    ] = []


class CheckResultCheckExisting(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    result: str = "CheckExisting"
    checks: List[
        CheckZamenaResult
        | CheckZamenaResultSuccess
        | CheckZamenaResultFailed
        | CheckZamenaResultHashChanged
        | CheckZamenaResultInvalidFormat
        | CheckZamenaResultFailedDownload
    ] = []
