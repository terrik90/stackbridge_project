from pydantic import BaseModel, ConfigDict, Field, PositiveInt, field_validator


class PermissionRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    resource: str
    action: str


class RoleAccessRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    is_active: bool
    permissions: list[PermissionRead] = Field(validation_alias="permisions")


class RolePermissionsUpdate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    permission_ids: list[PositiveInt]

    @field_validator("permission_ids")
    @classmethod
    def validate_unique_permission_ids(
        cls, permission_ids: list[PositiveInt]
    ) -> list[PositiveInt]:
        if len(permission_ids) != len(set(permission_ids)):
            raise ValueError("Идентификаторы прав не должны повторяться")
        return permission_ids


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
