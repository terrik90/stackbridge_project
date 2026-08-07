from typing import Self

from pydantic import BaseModel, ConfigDict, EmailStr, Field, model_validator


class UserRegister(BaseModel):
    model_config = ConfigDict(extra="forbid")

    first_name: str = Field(min_length=1, max_length=255)
    last_name: str = Field(min_length=1, max_length=255)
    middle_name: str | None = Field(default=None, max_length=255)
    email: EmailStr = Field(max_length=100)
    password: str = Field(min_length=8, max_length=72)
    password_repeat: str = Field(min_length=8, max_length=72)
    role_id: int = Field(gt=0)

    @model_validator(mode="after")
    def validate_password(self) -> Self:
        if self.password != self.password_repeat:
            raise ValueError("Пароли не совпадают")
        return self


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserUpdate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    first_name: str | None = Field(default=None, min_length=1, max_length=255)
    last_name: str | None = Field(default=None, min_length=1, max_length=255)
    middle_name: str | None = Field(default=None, max_length=255)
    email: EmailStr | None = Field(default=None, max_length=100)
    password: str | None = Field(default=None, min_length=8, max_length=72)
    password_repeat: str | None = Field(default=None, min_length=8, max_length=72)
    role_id: int | None = Field(default=None, gt=0)

    @model_validator(mode="after")
    def validate_password(self) -> Self:
        if self.password is None and self.password_repeat is None:
            return self

        if self.password != self.password_repeat:
            raise ValueError("Пароли не совпадают")
        return self


class UserRead(BaseModel):
    model_config = ConfigDict(extra="forbid")

    id: int
    first_name: str
    last_name: str
    middle_name: str | None
    email: EmailStr
    is_active: bool
    role_id: int
