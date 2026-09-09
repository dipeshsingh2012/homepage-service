# Homepage Service (`homepage-service`)

> **Contentful GraphQL Proxy & Backend-For-Frontend (BFF) for Storefront Landing Pages**

`homepage-service` is a FastAPI-powered BFF service that interfaces with Contentful's Headless GraphQL API. It aggregates hero banners, category navigation modules, spatial AI hooks, and curated collection items for the e-commerce storefront.

---

## 🎯 Features

1. **Contentful GraphQL Proxy:** Securely queries Contentful CDN GraphQL endpoints with space credentials kept server-side.
2. **Resilient Local Mock:** Automatically returns high-fidelity fallback homepage content when Contentful environment variables are not configured.
3. **Spatial Qualifier Integration:** Serves configuration parameters for the storefront's "Shop by Counter Clearance" hero qualifier module.

---

## 🚀 API Endpoints

- `GET /api/v1/homepage` — Returns structured homepage landing sections (Hero, Categories, How It Works, Bestsellers).
- `POST /graphql` — Direct GraphQL pass-through query proxy to Contentful.
- `GET /api/v1/health` — Health check endpoint.
