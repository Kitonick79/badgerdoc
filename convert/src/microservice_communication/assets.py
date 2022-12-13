from typing import List

import requests
from fastapi import Depends
from fastapi import Header
from requests import RequestException
from requests import Timeout
from tenant_dependency import TenantData
from tenant_dependency import get_tenant_info

from config import settings
from utils.common_utils import raise_request_exception

tenant = get_tenant_info(
    url=settings.keycloak_url, algorithm="RS256", debug=True
)


def upload_files(
        files: List,
        token: TenantData = Depends(tenant),
        current_tenant: str = Header(None, alias="X-Current-Tenant"),
):
    assets_url = settings.assets_service_url
    response = None
    try:
        response = requests.post(
            url=assets_url,
            headers={
                "X-Current-Tenant": current_tenant,
                "Authorization": token,
            },
            timeout=5,
            files=files
        )
    except (ConnectionError, RequestException, Timeout) as err:
        raise_request_exception(err)
    if response.status_code != 200:
        raise_request_exception(response.text)