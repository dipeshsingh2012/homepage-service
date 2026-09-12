import httpx
from typing import Any, Optional
from fastapi import APIRouter, Body, HTTPException, Query
from src.config import settings
from src.services.contentful_client import ContentfulClient

router = APIRouter(prefix="/api/v1", tags=["Homepage & Content"])
client = ContentfulClient()


@router.get("/health", tags=["Health"])
async def health():
    return {"status": "ok", "service": "homepage-service", "version": "0.1.0"}


@router.get("/homepage")
async def get_homepage():
    """Returns structured CMS content for the landing page."""
    # Queries default GraphQL landing query
    query = """
    query GetHomepage {
      homepageCollection(limit: 1) {
        items {
          title
          heroHeadline
          heroSubheadline
        }
      }
    }
    """
    content = await client.execute_query(query)
    """Returns structured CMS content for the landing page with dynamic lanes."""
    # 1. Base default content (hero, how it works, fallback categories)
    content = client.get_default_homepage_content()

    # 2. Query dynamic lanes from content-service (:8006)
    try:
        async with httpx.AsyncClient(timeout=3.0) as http_client:
            res = await http_client.get(
                f"{settings.CONTENT_SERVICE_URL}/lanes",
                params={"placement": "homepage", "status": "active"},
            )
            if res.status_code == 200:
                lanes_data = res.json().get("items", [])
                content["lanes"] = lanes_data

                # Hydrate Category Tiles from category_lane
                for lane in lanes_data:
                    if lane.get("lane_type") == "category_lane":
                        content["categoryLane"] = {
                            "title": lane.get("title"),
                            "subtitle": lane.get("subtitle"),
                            "hasNavigationArrows": lane.get("has_navigation_arrows", True),
                            "items": [
                                {
                                    "id": item.get("id"),
                                    "title": item.get("title"),
                                    "imageUrl": item.get("image_url"),
                                    "href": item.get("target_url"),
                                    "badge": item.get("badge"),
                                }
                                for item in lane.get("items", [])
                            ],
                        }
                        # Also override featuredCategories for backwards compatibility
                        content["featuredCategories"] = [
                            {
                                "id": item.get("id"),
                                "title": item.get("title"),
                                "slug": item.get("target_url", "").replace("#/", ""),
                                "image": item.get("image_url"),
                                "description": item.get("subtitle") or item.get("title"),
                            }
                            for item in lane.get("items", [])
                        ]
                        break

                # Hydrate Product Slider from product_lane
                for lane in lanes_data:
                    if lane.get("lane_type") == "product_lane":
                        content["productLane"] = {
                            "title": lane.get("title"),
                            "subtitle": lane.get("subtitle"),
                            "hasNavigationArrows": lane.get("has_navigation_arrows", True),
                            "items": [
                                {
                                    "id": item.get("id"),
                                    "title": item.get("title"),
                                    "subtitle": item.get("subtitle"),
                                    "price": item.get("price") or "₹ 990",
                                    "imageUrl": item.get("image_url"),
                                    "productUrl": item.get("target_url"),
                                    "badge": item.get("badge"),
                                }
                                for item in lane.get("items", [])
                            ],
                        }
                        break
    except Exception as e:
        # Graceful fallback: return base content if content-service is unreachable
        pass

    return content


@router.get("/lanes")
async def get_lanes(placement: Optional[str] = Query("homepage"), status: Optional[str] = Query("active")):
    """Proxies and retrieves active lanes from content-service."""
    try:
        async with httpx.AsyncClient(timeout=3.0) as http_client:
            res = await http_client.get(
                f"{settings.CONTENT_SERVICE_URL}/lanes",
                params={"placement": placement, "status": status},
            )
            if res.status_code == 200:
                return res.json()
    except Exception:
        pass
    return {"items": [], "total": 0}


@router.post("/graphql")
async def graphql_proxy(
    query: str = Body(..., embed=True),
    variables: Optional[dict[str, Any]] = Body(None, embed=True),
):
    """Pass-through proxy for Contentful GraphQL queries."""
    result = await client.execute_query(query, variables)
    return result

