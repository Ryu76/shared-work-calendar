"""Pydantic request models shared by the HTTP boundary.

Validation rules are preserved verbatim from the former monolithic application
module so moving them does not change accepted requests or error responses.
"""
from __future__ import annotations

import re
from datetime import date
from typing import Literal

from pydantic import BaseModel, Field, field_validator


class LoginIn(BaseModel):
    login_id: str = Field(min_length=1, max_length=50)
    password: str = Field(min_length=1, max_length=200)


class PasswordChangeIn(BaseModel):
    current_password: str = Field(min_length=1, max_length=200)
    new_password: str = Field(min_length=8, max_length=200)


class UserIn(BaseModel):
    login_id: str = Field(min_length=1, max_length=50)
    name: str = Field(min_length=1, max_length=50)
    role: Literal["ADMIN", "MEMBER"] = "MEMBER"
    temporary_password: str = Field(min_length=8, max_length=200)

    @field_validator("login_id", "name")
    @classmethod
    def non_blank_text(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("로그인 ID와 이름은 공백만 입력할 수 없습니다.")
        return value


class UserPatch(BaseModel):
    name: str | None = Field(None, min_length=1, max_length=50)
    role: Literal["ADMIN", "MEMBER"] | None = None
    is_active: bool | None = None
    password: str | None = Field(None, min_length=8, max_length=200)

    @field_validator("name")
    @classmethod
    def non_blank_name(cls, value: str | None) -> str | None:
        if value is None:
            return None
        value = value.strip()
        if not value:
            raise ValueError("이름은 공백만 입력할 수 없습니다.")
        return value


class ContactIn(BaseModel):
    name: str = Field(min_length=1, max_length=50)
    phone: str = Field(min_length=3, max_length=30)
    organization: str = Field(min_length=1, max_length=100)

    @field_validator("name", "organization")
    @classmethod
    def non_blank_text(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("공백만 입력할 수 없습니다.")
        return value

    @field_validator("phone")
    @classmethod
    def valid_phone(cls, value: str) -> str:
        value = value.strip()
        if not re.fullmatch(r"[0-9+() .-]{3,30}", value) or len(re.sub(r"\D", "", value)) < 3:
            raise ValueError("연락처는 숫자와 전화번호 기호만 사용할 수 있습니다.")
        return value


class OrganizationIn(BaseModel):
    name: str = Field(min_length=1, max_length=100)

    @field_validator("name")
    @classmethod
    def non_blank_name(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("기관명은 공백만 입력할 수 없습니다.")
        return value


class OrganizationPatch(BaseModel):
    name: str | None = Field(None, min_length=1, max_length=100)
    is_active: bool | None = None

    @field_validator("name")
    @classmethod
    def non_blank_name(cls, value: str | None) -> str | None:
        if value is None:
            return None
        return OrganizationIn.non_blank_name(value)


class ContactPatch(BaseModel):
    name: str | None = Field(None, min_length=1, max_length=50)
    phone: str | None = Field(None, min_length=3, max_length=30)
    organization_id: int | None = Field(None, gt=0)
    is_active: bool | None = None

    @field_validator("name")
    @classmethod
    def non_blank_name(cls, value: str | None) -> str | None:
        if value is None:
            return None
        value = value.strip()
        if not value:
            raise ValueError("요청 담당자명은 공백만 입력할 수 없습니다.")
        return value

    @field_validator("phone")
    @classmethod
    def valid_phone(cls, value: str | None) -> str | None:
        if value is None:
            return None
        return ContactIn.valid_phone(value)


class TaskIn(BaseModel):
    assignee_ids: list[int] = Field(min_length=1, max_length=100)
    contact: ContactIn
    description: str = Field(min_length=1, max_length=5000)
    status: Literal["RECEIVED", "IN_PROGRESS", "COMPLETED"] = "RECEIVED"
    received_date: date | None = None
    completed_date: date | None = None
    due_date: date | None = None

    @field_validator("assignee_ids")
    @classmethod
    def unique_assignees(cls, values):
        if len(values) != len(set(values)):
            raise ValueError("처리자가 중복되었습니다.")
        return values

    @field_validator("description")
    @classmethod
    def non_blank_description(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("업무 설명은 공백만 입력할 수 없습니다.")
        return value


class TaskUpdateIn(BaseModel):
    """PATCH semantics: omitted fields retain their stored value."""

    assignee_ids: list[int] | None = Field(None, min_length=1, max_length=100)
    contact: ContactIn | None = None
    description: str | None = Field(None, min_length=1, max_length=5000)
    status: Literal["RECEIVED", "IN_PROGRESS", "COMPLETED"] | None = None
    received_date: date | None = None
    completed_date: date | None = None
    # Explicit JSON null clears the due date; an omitted field preserves it.
    due_date: date | None = None

    @field_validator("assignee_ids")
    @classmethod
    def unique_assignees(cls, values):
        if values is not None and len(values) != len(set(values)):
            raise ValueError("처리자가 중복되었습니다.")
        return values

    @field_validator("description")
    @classmethod
    def non_blank_description(cls, value: str | None) -> str | None:
        if value is None:
            return value
        value = value.strip()
        if not value:
            raise ValueError("업무 설명은 공백만 입력할 수 없습니다.")
        return value


class NotificationPreferencesIn(BaseModel):
    due_soon_enabled: bool
    overdue_enabled: bool


class ImageEditIn(BaseModel):
    """Deliberately small safe edit surface for private task images."""

    direction: Literal["CLOCKWISE", "COUNTERCLOCKWISE"]
