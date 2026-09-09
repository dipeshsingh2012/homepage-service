from typing import Any, Optional
import httpx
from src.config import settings


class ContentfulClient:
    def __init__(
        self,
        space_id: Optional[str] = None,
        access_token: Optional[str] = None,
        environment: Optional[str] = None,
    ):
        self.space_id = space_id or settings.CONTENTFUL_SPACE_ID
        self.access_token = access_token or settings.CONTENTFUL_ACCESS_TOKEN
        self.environment = environment or settings.CONTENTFUL_ENVIRONMENT

    @property
    def endpoint_url(self) -> str:
        if not self.space_id:
            return ""
        return (
            f"https://graphql.contentful.com/content/v1/spaces/"
            f"{self.space_id}/environments/{self.environment}"
        )

    async def execute_query(
        self, query: str, variables: Optional[dict[str, Any]] = None
    ) -> dict[str, Any]:
        """Executes a GraphQL query against Contentful, or returns mock data if unconfigured."""
        if self.space_id and self.access_token:
            headers = {
                "Authorization": f"Bearer {self.access_token}",
                "Content-Type": "application/json",
            }
            payload = {"query": query, "variables": variables or {}}
            try:
                async with httpx.AsyncClient(timeout=10.0) as client:
                    resp = await client.post(
                        self.endpoint_url, json=payload, headers=headers
                    )
                    if resp.status_code == 200:
                        return resp.json()
            except Exception:
                pass  # Fall back to default mock structure on failure

        return self.get_default_homepage_content()

    def get_default_homepage_content(self) -> dict[str, Any]:
        """Returns structured JSON matching Contentful landing page content models."""
        return {
            "hero": {
                "headline": "Kitchen Appliances That Guaranteed Fit Your Counter",
                "subheadline": "Never return a coffee machine or blender because it's 2 cm too tall for your upper cabinets. Snap a photo, check fitment, and buy with confidence.",
                "ctaText": "Explore Space-Verified Appliances",
                "ctaLink": "#/collection",
                "backgroundImage": "https://images.unsplash.com/photo-1556911220-e15b29be8c8f?w=1600&auto=format&fit=crop&q=80",
                "spatialHook": {
                    "enabled": True,
                    "title": "Shop By Your Counter Clearance",
                    "description": "Have 45cm standard cabinets? We automatically filter for machines with ventilation clearance.",
                    "defaultClearanceCm": 48.0,
                },
            },
            "featuredCategories": [
                {
                    "id": "cat_espresso",
                    "title": "Espresso Machines",
                    "slug": "espresso_machine",
                    "image": "https://images.unsplash.com/photo-1514432324607-a09d9b4aefdd?w=600&auto=format&fit=crop&q=80",
                    "description": "Compact to prosumer espresso setups with bean hopper clearance checks.",
                },
                {
                    "id": "cat_blenders",
                    "title": "High-Performance Blenders",
                    "slug": "blender",
                    "image": "https://images.unsplash.com/photo-1570222094114-d054a817e56b?w=600&auto=format&fit=crop&q=80",
                    "description": "Check container height against low hanging upper kitchen cabinets.",
                },
                {
                    "id": "cat_mixers",
                    "title": "Stand Mixers",
                    "slug": "stand_mixer",
                    "image": "https://images.unsplash.com/photo-1594385208974-2e75f8d7bb48?w=600&auto=format&fit=crop&q=80",
                    "description": "Requires tilt-head vertical operating clearance before buying.",
                },
                {
                    "id": "cat_airfryers",
                    "title": "Air Fryers & Ovens",
                    "slug": "air_fryer",
                    "image": "https://images.unsplash.com/photo-1584269600464-37b1b58a9fe7?w=600&auto=format&fit=crop&q=80",
                    "description": "Requires safe rear & overhead heat ventilation clearance.",
                },
            ],
            "howItWorks": [
                {
                    "step": 1,
                    "title": "Snap a Kitchen Photo",
                    "description": "Use your phone camera to take a photo showing your countertop and hanging cabinets.",
                },
                {
                    "step": 2,
                    "title": "Spatial AI Measures Clearance",
                    "description": "Computer vision calculates the exact vertical clearance and usable surface drop zone.",
                },
                {
                    "step": 3,
                    "title": "Zero-Doubt Shopping",
                    "description": "Browse only the appliances guaranteed to fit under your cabinets with proper ventilation.",
                },
            ],
            "curatedProductIds": [
                "prod_breville_barista_touch",
                "prod_delonghi_dedica",
                "prod_breville_bambino",
                "prod_kitchenaid_artisan",
            ],
        }
