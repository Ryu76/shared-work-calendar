"""One-time, verified plaintext SQLite -> SQLCipher migration.

Run from backend: python migrate_to_sqlcipher.py
It creates a timestamped plaintext backup and replaces calendar.db only after
opening the encrypted copy with the application's DPAPI-protected key.
"""
from __future__ import annotations

import shutil
from datetime import datetime
from pathlib import Path

import sqlite3 as plaintext_sqlite

from database import DB_PATH, database_key, sqlite3


def main() -> None:
    if not DB_PATH.exists():
        raise SystemExit(f"Database not found: {DB_PATH}")
    stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    backup = DB_PATH.with_name(f"{DB_PATH.stem}.plaintext-backup-{stamp}{DB_PATH.suffix}")
    staged = DB_PATH.with_name(f"{DB_PATH.stem}.sqlcipher-staged{DB_PATH.suffix}")
    if staged.exists():
        staged.unlink()

    # Immutable recovery copy before any data movement.
    shutil.copy2(DB_PATH, backup)
    # SQLCipher's own export routine copies schema and data across the cipher
    # boundary. A stdlib sqlite3 backup cannot target a SQLCipher connection.
    source = sqlite3.connect(backup)
    try:
        source.execute("ATTACH DATABASE ? AS encrypted KEY \"x'%s'\"" % database_key().hex(), (str(staged),))
        source.execute("SELECT sqlcipher_export('encrypted')")
        source.execute("DETACH DATABASE encrypted")
    finally:
        source.close()

    target = sqlite3.connect(staged)
    try:
        target.execute("PRAGMA key = \"x'%s'\"" % database_key().hex())
        target.execute("PRAGMA cipher_integrity_check").fetchone()
        rows = target.execute("SELECT COUNT(*) FROM users").fetchone()[0]
        if rows < 1:
            raise RuntimeError("encrypted copy verification failed: users table is empty")
    finally:
        target.close()

    # Verify a no-key standard SQLite reader cannot read the staged file.
    try:
        plain_probe = plaintext_sqlite.connect(staged)
        try:
            plain_probe.execute("SELECT COUNT(*) FROM sqlite_master").fetchone()
        finally:
            plain_probe.close()
        raise RuntimeError("staged database is readable without a key; refusing replacement")
    except plaintext_sqlite.DatabaseError:
        pass

    staged.replace(DB_PATH)
    print(f"Encrypted database installed: {DB_PATH}")
    print(f"Recovery backup retained (protect/delete after offline backup): {backup}")


if __name__ == "__main__":
    main()
