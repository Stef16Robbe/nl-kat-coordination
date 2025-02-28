from typing import Dict, List

from scheduler import models


class MockKatalogusService:
    def __init__(self):
        self.organisations: Dict[str, models.Organisation] = {}

    def get_organisation(self, org_id: str) -> models.Organisation:
        """Get the organisation with the given id."""
        return self.organisations[org_id]

    def get_organisations(self) -> List[models.Organisation]:
        """Get all organisations."""
        return list(self.organisations.values())

    def get_new_boefjes_by_org_id(self, org_id: str) -> List[models.Boefje]:
        """Get all new Boefjes for the given organisation."""
        return []

    def flush_caches(self) -> None:
        """Flush the cache."""
        pass
