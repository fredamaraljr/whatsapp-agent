"""
User Management Module
Handles user identification, group assignment, and verification.
"""
from enum import Enum
from typing import Optional
from dataclasses import dataclass
from datetime import datetime
import sqlite3
import logging

logger = logging.getLogger(__name__)


class UserGroup(Enum):
    """Available user groups in the system."""
    ADMIN = "admin"
    MONITORI = "monitori"
    FPS = "fps"
    AVILA = "avila"
    FFL = "ffl"
    UNVERIFIED = "unverified"


@dataclass
class User:
    """User data model."""
    phone_number: str
    group: UserGroup
    verified: bool
    first_interaction: datetime
    last_interaction: datetime
    message_count: int = 0
    metadata: dict = None

    def __post_init__(self):
        if self.metadata is None:
            self.metadata = {}


class UserManager:
    """Manages user data, groups, and verification."""
    
    def __init__(self, db_path: str):
        self.db_path = db_path
        self._init_database()
    
    def _init_database(self):
        """Initialize the user database."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS users (
                        phone_number TEXT PRIMARY KEY,
                        user_group TEXT NOT NULL,
                        verified INTEGER NOT NULL,
                        first_interaction TEXT NOT NULL,
                        last_interaction TEXT NOT NULL,
                        message_count INTEGER DEFAULT 0,
                        metadata TEXT
                    )
                """)
                
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS interaction_log (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        phone_number TEXT NOT NULL,
                        timestamp TEXT NOT NULL,
                        message_type TEXT,
                        FOREIGN KEY (phone_number) REFERENCES users(phone_number)
                    )
                """)
                
                conn.commit()
                logger.info("User database initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize user database: {e}")
            raise
    
    def get_user(self, phone_number: str) -> Optional[User]:
        """Retrieve user by phone number."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "SELECT * FROM users WHERE phone_number = ?",
                    (phone_number,)
                )
                row = cursor.fetchone()
                
                if row:
                    return User(
                        phone_number=row[0],
                        group=UserGroup(row[1]),
                        verified=bool(row[2]),
                        first_interaction=datetime.fromisoformat(row[3]),
                        last_interaction=datetime.fromisoformat(row[4]),
                        message_count=row[5],
                        metadata=eval(row[6]) if row[6] else {}
                    )
                return None
        except Exception as e:
            logger.error(f"Error retrieving user {phone_number}: {e}")
            return None
    
    def create_user(self, phone_number: str, admin_phone: str) -> User:
        """Create a new user record."""
        now = datetime.now()
        
        # Check if this is the admin
        is_admin = phone_number == admin_phone
        group = UserGroup.ADMIN if is_admin else UserGroup.UNVERIFIED
        verified = is_admin  # Admin is auto-verified
        
        user = User(
            phone_number=phone_number,
            group=group,
            verified=verified,
            first_interaction=now,
            last_interaction=now,
            message_count=1
        )
        
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT INTO users (phone_number, user_group, verified, 
                                     first_interaction, last_interaction, message_count, metadata)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                """, (
                    user.phone_number,
                    user.group.value,
                    int(user.verified),
                    user.first_interaction.isoformat(),
                    user.last_interaction.isoformat(),
                    user.message_count,
                    str(user.metadata)
                ))
                conn.commit()
                logger.info(f"Created new user: {phone_number} (group: {group.value})")
        except Exception as e:
            logger.error(f"Error creating user {phone_number}: {e}")
            raise
        
        return user
    
    def update_user(self, user: User):
        """Update user information."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    UPDATE users 
                    SET user_group = ?, verified = ?, last_interaction = ?, 
                        message_count = ?, metadata = ?
                    WHERE phone_number = ?
                """, (
                    user.group.value,
                    int(user.verified),
                    user.last_interaction.isoformat(),
                    user.message_count,
                    str(user.metadata),
                    user.phone_number
                ))
                conn.commit()
                logger.info(f"Updated user: {user.phone_number}")
        except Exception as e:
            logger.error(f"Error updating user {user.phone_number}: {e}")
            raise
    
    def verify_user(self, phone_number: str, group: UserGroup):
        """Verify a user and assign them to a group."""
        user = self.get_user(phone_number)
        if user:
            user.verified = True
            user.group = group
            self.update_user(user)
            logger.info(f"Verified user {phone_number} as {group.value}")
    
    def increment_message_count(self, phone_number: str):
        """Increment the message count for a user."""
        user = self.get_user(phone_number)
        if user:
            user.message_count += 1
            user.last_interaction = datetime.now()
            self.update_user(user)
    
    def log_interaction(self, phone_number: str, message_type: str = "text"):
        """Log an interaction."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT INTO interaction_log (phone_number, timestamp, message_type)
                    VALUES (?, ?, ?)
                """, (phone_number, datetime.now().isoformat(), message_type))
                conn.commit()
        except Exception as e:
            logger.error(f"Error logging interaction: {e}")
    
    def get_user_stats(self) -> dict:
        """Get statistics about all users."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Total users
                cursor.execute("SELECT COUNT(*) FROM users")
                total_users = cursor.fetchone()[0]
                
                # Users by group
                cursor.execute("SELECT user_group, COUNT(*) FROM users GROUP BY user_group")
                users_by_group = {row[0]: row[1] for row in cursor.fetchall()}
                
                # Total messages
                cursor.execute("SELECT SUM(message_count) FROM users")
                total_messages = cursor.fetchone()[0] or 0
                
                # Recent interactions (last 24 hours)
                cursor.execute("""
                    SELECT COUNT(*) FROM interaction_log 
                    WHERE datetime(timestamp) > datetime('now', '-1 day')
                """)
                recent_interactions = cursor.fetchone()[0]
                
                return {
                    "total_users": total_users,
                    "users_by_group": users_by_group,
                    "total_messages": total_messages,
                    "recent_interactions_24h": recent_interactions
                }
        except Exception as e:
            logger.error(f"Error getting user stats: {e}")
            return {}
    
    def is_first_interaction(self, phone_number: str) -> bool:
        """Check if this is the user's first interaction."""
        user = self.get_user(phone_number)
        return user is None or user.message_count <= 1


# Verification questions for each group
VERIFICATION_QUESTIONS = {
    UserGroup.MONITORI: "Olá! Para melhor atendê-lo(a), você é cliente da Monitori?",
    UserGroup.FPS: "Olá! Para melhor atendê-lo(a), você estuda na Faculdade Pernambucana de Saúde (FPS)?",
    UserGroup.AVILA: "Olá! Para melhor atendê-lo(a), você trabalha na Ávila Digital?",
    UserGroup.FFL: "Olá! Para melhor atendê-lo(a), você pilota avião e está interessado em conhecimentos de aviação?",
}


def get_verification_question() -> str:
    """Get the initial verification question for new users."""
    return """Olá! Seja bem-vindo(a)! 👋

Para que eu possa oferecer o melhor atendimento, preciso saber um pouco mais sobre você.

Você é:
1️⃣ Cliente da Monitori
2️⃣ Estudante da FPS (Faculdade Pernambucana de Saúde)
3️⃣ Colaborador da Ávila Digital
4️⃣ Piloto ou interessado em aviação

Por favor, responda com o número da opção que melhor se aplica a você."""
