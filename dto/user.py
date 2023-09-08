from phonenumbers import PhoneNumber as _PhoneNumber
from phonenumbers import NumberParseException, PhoneNumberFormat
from phonenumbers import format_number, is_possible_number, parse
from pydantic_core import core_schema
from pydantic import BaseModel, GetCoreSchemaHandler, Field
from typing import Any, Type, Union


class PhoneNumber(_PhoneNumber):

    @classmethod
    def __get_validators__(cls):
        yield cls._validate

    @classmethod
    def __get_pydantic_core_schema__(
            cls, source: Type[Any], handler: GetCoreSchemaHandler
    ) -> core_schema.CoreSchema:
        return core_schema.no_info_after_validator_function(
            cls._validate,
            core_schema.str_schema(),
            serialization=core_schema.plain_serializer_function_ser_schema(
                cls._serialize,
                info_arg=False,
                return_schema=core_schema.str_schema(),
            ),
        )

    @classmethod
    def _validate(cls, value: str, **kwargs) -> str:
        try:
            is_valid = parse(value, None)
        except NumberParseException as ex:
            raise ValueError(f'Invalid phone number: {value}')
        if not is_possible_number(is_valid):
            raise ValueError(f'Invalid phone number: {value}')
        return value

    def json_encode(self) -> str:
        return format_number(self, PhoneNumberFormat.E164)

    @staticmethod
    def _serialize(value: Union[str, _PhoneNumber]) -> str:
        return value


class UserCreate(BaseModel):
    username: str = Field(..., min_length=3, max_length=20)
    password: str = Field(..., min_length=5)
    phone_number: PhoneNumber


class UserGet(BaseModel):
    id: int
    username: str
    phone_number: str
