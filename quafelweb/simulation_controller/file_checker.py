

from typing import Any


class FileCheckerMiddleware:

  def __init__(self, get_response) -> None:
    self.get_response = get_response

  def __call__(self, request) -> Any:
    response = self.get_response(request)
    print("CALLED MIDDLE WARE")
    return response