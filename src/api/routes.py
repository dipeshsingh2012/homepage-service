from typing import Any, Optional
from fastapi import APIRouter, Body, HTTPException
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
    return content


@router.post("/graphql")
async def graphql_proxy(
    query: str = Body(..., embed=True),
    variables: Optional[dict[str, Any]] = Body(None, embed=True),
):
    """Pass-through proxy for Contentful GraphQL queries."""
    result = await client.execute_query(query, variables)
    return result
