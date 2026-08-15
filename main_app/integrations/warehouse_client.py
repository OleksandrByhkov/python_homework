"""Resilient HTTP client used by ProjectA to communicate with ProjectB."""
import logging
import os
import requests

logger = logging.getLogger(__name__)

class WarehouseError(RuntimeError):
    pass

class WarehouseClient:
    def __init__(self, base_url=None, token=None, timeout=3):
        self.base_url = (base_url or os.getenv("WAREHOUSE_API_URL", "http://warehouse:8001/api")).rstrip("/")
        self.token = token or os.getenv("WAREHOUSE_SERVICE_TOKEN", "")
        self.timeout = timeout

    def _request(self, method, path, **kwargs):
        headers = {"Authorization": f"Bearer {self.token}"} if self.token else {}
        url = f"{self.base_url}/{path.lstrip('/')}"
        try:
            response = requests.request(method, url, headers=headers, timeout=self.timeout, **kwargs)
            response.raise_for_status()
            return response.json()
        except (requests.Timeout, requests.ConnectionError) as exc:
            logger.exception("Warehouse service unavailable: %s", url)
            raise WarehouseError("Warehouse service is temporarily unavailable") from exc
        except requests.HTTPError as exc:
            logger.error("Warehouse API error status=%s body=%s", exc.response.status_code, exc.response.text[:500])
            raise WarehouseError(f"Warehouse rejected request ({exc.response.status_code})") from exc
        except ValueError as exc:
            logger.exception("Invalid JSON returned by warehouse: %s", url)
            raise WarehouseError("Invalid response from warehouse") from exc

    def get_stock(self, book_id): return self._request("GET", f"stocks/{book_id}/")
    def reserve(self, order_id, book_id, quantity): return self._request("POST", "reservations/", json={"order_id": str(order_id), "book_id": book_id, "quantity": quantity})
    def confirm(self, reservation_id): return self._request("POST", f"reservations/{reservation_id}/confirm/")
    def cancel(self, reservation_id): return self._request("POST", f"reservations/{reservation_id}/cancel/")
