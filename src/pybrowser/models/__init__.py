"""Data models for PyBrowser application."""

from typing import List, Optional
from pydantic import BaseModel, HttpUrl


class QuickLink(BaseModel):
    """Model for quick access links."""
    
    id: str
    name: str
    url: HttpUrl
    icon: Optional[str] = None
    order: int = 0


class Application(BaseModel):
    """Model for team applications."""
    
    id: str
    name: str
    url: HttpUrl
    description: Optional[str] = None
    icon: Optional[str] = None
    quick_links: List[QuickLink] = []


class Team(BaseModel):
    """Model for user teams."""
    
    id: str
    name: str
    description: Optional[str] = None
    applications: List[Application] = []


class UserProfile(BaseModel):
    """Model for authenticated user profile."""
    
    id: str
    email: str
    name: str
    avatar: Optional[str] = None
