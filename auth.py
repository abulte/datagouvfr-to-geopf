import os
import sys
from dotenv import load_dotenv

load_dotenv()


def auth_headers() -> dict:
    token = os.getenv("GEOPF_TOKEN")
    if not token:
        print(
            "Missing GEOPF_TOKEN.\n"
            "Get one from the Swagger UI:\n"
            "  1. Go to https://data.geopf.fr/api/swagger-ui/index.html\n"
            "  2. Click 'Authorize', log in with your IdP\n"
            "  3. Open browser devtools → Network → any request → copy the Authorization header value\n"
            "  4. Set it: export GEOPF_TOKEN='<the token string>'\n"
        )
        sys.exit(1)
    return {"Authorization": f"Bearer {token}"}
