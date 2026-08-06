"""Encrypted SQLite access for the Shared Work Calendar.

The SQLCipher key is never stored as plaintext.  On Windows it is protected by
DPAPI and can only be unsealed by the same Windows user account.
"""
from __future__ import annotations

import base64
import ctypes
from ctypes import wintypes
import os
import secrets
from contextlib import contextmanager
from pathlib import Path

from sqlcipher3 import dbapi2 as sqlite3

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = Path(os.getenv("WORK_CALENDAR_DB", BASE_DIR / "calendar.db"))
KEY_PATH = Path(os.getenv("WORK_CALENDAR_DB_KEY_FILE", BASE_DIR / ".calendar-db-key.dpapi"))


class _DATA_BLOB(ctypes.Structure):
    _fields_ = [("cbData", wintypes.DWORD), ("pbData", ctypes.POINTER(ctypes.c_byte))]


def _blob(data: bytes) -> tuple[_DATA_BLOB, ctypes.Array[ctypes.c_char]]:
    buffer = ctypes.create_string_buffer(data)
    return _DATA_BLOB(len(data), ctypes.cast(buffer, ctypes.POINTER(ctypes.c_byte))), buffer


def _dpapi(data: bytes, protect: bool) -> bytes:
    if os.name != "nt":
        raise RuntimeError("WORK_CALENDAR_DB_KEY를 안전한 비밀 저장소에서 제공해야 합니다.")
    source, source_buffer = _blob(data)
    result = _DATA_BLOB()
    crypt32 = ctypes.windll.crypt32
    kernel32 = ctypes.windll.kernel32
    if protect:
        ok = crypt32.CryptProtectData(ctypes.byref(source), "Shared Work Calendar DB", None, None, None, 0, ctypes.byref(result))
    else:
        ok = crypt32.CryptUnprotectData(ctypes.byref(source), None, None, None, None, 0, ctypes.byref(result))
    if not ok:
        raise OSError(ctypes.get_last_error(), "Windows DPAPI operation failed")
    try:
        return ctypes.string_at(result.pbData, result.cbData)
    finally:
        kernel32.LocalFree(result.pbData)


def database_key() -> bytes:
    """Return a 256-bit SQLCipher key from a DPAPI-protected local key file.

    An explicit key is accepted only for controlled recovery/automation. It must
    be hexadecimal and is intentionally not persisted by the application.
    """
    supplied = os.getenv("WORK_CALENDAR_DB_KEY")
    if supplied:
        try:
            key = bytes.fromhex(supplied)
        except ValueError as exc:
            raise RuntimeError("WORK_CALENDAR_DB_KEY는 64자리 16진수여야 합니다.") from exc
        if len(key) != 32:
            raise RuntimeError("WORK_CALENDAR_DB_KEY는 256비트여야 합니다.")
        return key
    if KEY_PATH.exists():
        return _dpapi(base64.b64decode(KEY_PATH.read_bytes()), protect=False)
    key = secrets.token_bytes(32)
    protected = _dpapi(key, protect=True)
    KEY_PATH.write_bytes(base64.b64encode(protected))
    return key


def connect(path: Path | str = DB_PATH) -> sqlite3.Connection:
    connection = sqlite3.connect(path)
    connection.row_factory = sqlite3.Row
    # hex form avoids SQL quoting and keeps the key outside SQL logs.
    connection.execute("PRAGMA key = \"x'%s'\"" % database_key().hex())
    connection.execute("PRAGMA foreign_keys = ON")
    return connection


@contextmanager
def db():
    connection = connect()
    try:
        yield connection
        connection.commit()
    except Exception:
        connection.rollback()
        raise
    finally:
        connection.close()
