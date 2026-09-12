from enum import Enum
from typing import Literal, Union

from pydantic import BaseModel, Field

class DataTypeSchema(str, Enum):
    ALERTA = "alerta"
    SENSORES = "sensores"
    LOGIN = "login"

class SensorSchema(BaseModel):
    bpm: float = Field(ge=0, le=300)
    spo2: float = Field(ge=0, le=100)
    bateria: float = Field(ge=0, le=100)

class AlertSchema(BaseModel):
    tipo: str
    mensagem: str

class LoginSchema(BaseModel):
    usuario: str
    senha: str
    pulseira_id : str

class SensorPayloadSchema(BaseModel):
    origem: str
    datatype: Literal[DataTypeSchema.SENSORES]
    data: SensorSchema

class AlertPayloadSchema(BaseModel):
    origem: str
    datatype: Literal[DataTypeSchema.ALERTA]
    data: AlertSchema

class LoginPayloadSchema(BaseModel):
    origem: str
    datatype: Literal[DataTypeSchema.LOGIN]
    data: LoginSchema

PayloadSchema = Union[
    SensorPayloadSchema,
    AlertPayloadSchema,
    LoginPayloadSchema
]