"""API client for communicating with backend server."""

import logging
from typing import List, Optional
import requests
from requests.exceptions import RequestException

from pybrowser.models import Team, Application, QuickLink, UserProfile
from pybrowser.auth import AuthenticationManager

logger = logging.getLogger(__name__)


class APIClient:
    """Client for backend API communication."""
    
    def __init__(self, base_url: str, auth_manager: AuthenticationManager):
        """
        Initialize API client.
        
        Args:
            base_url: Base URL for the API
            auth_manager: Authentication manager instance
        """
        self.base_url = base_url.rstrip("/")
        self.auth_manager = auth_manager
    
    def _get_headers(self) -> dict:
        """Get request headers with authentication."""
        token = self.auth_manager.get_token()
        if not token:
            raise ValueError("Not authenticated")
        
        return {
            "Authorization": f"Bearer {token.get('access_token')}",
            "Content-Type": "application/json",
        }
    
    def get_user_profile(self) -> Optional[UserProfile]:
        """
        Fetch authenticated user profile.
        
        Returns:
            UserProfile object or None on error
        """
        try:
            response = requests.get(
                f"{self.base_url}/api/user/profile",
                headers=self._get_headers(),
                timeout=10,
            )
            response.raise_for_status()
            data = response.json()
            return UserProfile(**data)
        except RequestException as e:
            logger.error(f"Failed to fetch user profile: {e}")
            return None
    
    def get_teams(self) -> List[Team]:
        """
        Fetch user's teams.
        
        Returns:
            List of Team objects
        """
        try:
            response = requests.get(
                f"{self.base_url}/api/teams",
                headers=self._get_headers(),
                timeout=10,
            )
            response.raise_for_status()
            data = response.json()
            return [Team(**team) for team in data.get("teams", [])]
        except RequestException as e:
            logger.error(f"Failed to fetch teams: {e}")
            return []
    
    def get_applications(self, team_id: str) -> List[Application]:
        """
        Fetch applications for a team.
        
        Args:
            team_id: Team identifier
            
        Returns:
            List of Application objects
        """
        try:
            response = requests.get(
                f"{self.base_url}/api/teams/{team_id}/applications",
                headers=self._get_headers(),
                timeout=10,
            )
            response.raise_for_status()
            data = response.json()
            return [Application(**app) for app in data.get("applications", [])]
        except RequestException as e:
            logger.error(f"Failed to fetch applications: {e}")
            return []
    
    def get_quick_links(self, application_id: str) -> List[QuickLink]:
        """
        Fetch quick links for an application.
        
        Args:
            application_id: Application identifier
            
        Returns:
            List of QuickLink objects
        """
        try:
            response = requests.get(
                f"{self.base_url}/api/applications/{application_id}/quick-links",
                headers=self._get_headers(),
                timeout=10,
            )
            response.raise_for_status()
            data = response.json()
            return [QuickLink(**link) for link in data.get("quick_links", [])]
        except RequestException as e:
            logger.error(f"Failed to fetch quick links: {e}")
            return []
