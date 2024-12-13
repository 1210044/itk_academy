import requests
from typing import Dict, Any, Callable, List
from wsgiref.simple_server import make_server


class WSGIApp:
    def __call__(self, environ: Dict[str, Any], start_response: Callable[[str, List[str]], None]) -> List[bytes]:
        self.client_path = environ["PATH_INFO"]
        response_body = self.get_body()

        if response_body:
            headers = [("Content-type", "application/json; charset=utf-8")]
            start_response("200 OK", headers)
            return [response_body.encode("utf-8")]
        
        start_response("404 Not Found", [("Content-type", "text/plain; charset=utf-8")])
        return [b"Not Found"]
    
    def run(self):
        with make_server("", 8000, self) as httpd:
            print("Serving on port 8000...")
            try:
                httpd.serve_forever()
            except KeyboardInterrupt:
                print("Shutting down server...")

    def get_body(self) -> str:
        currency = self.client_path.lstrip('/')
        if not currency:
            return ""

        url = f"https://api.exchangerate-api.com/v4/latest/{currency}"
        response = requests.get(url)

        if response.status_code == 200:
            return response.text
        return ""
            

if __name__ == "__main__":
    app = WSGIApp()
    app.run()