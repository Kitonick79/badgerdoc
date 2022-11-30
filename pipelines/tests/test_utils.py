from unittest.mock import patch

import pytest

from src import utils


@pytest.mark.parametrize(
    ("prefix", "bucket", "expected"),
    (
        ("", "tenant", "tenant"),
        ("", "some-tenant", "some-tenant"),
        ("prefix", "prefix-tenant", "tenant"),
        ("prefix", "prefix-prefix-tenant", "prefix-tenant"),
    ),
)
def test_tenant_from_bucket(prefix: str, bucket: str, expected: str) -> None:
    with patch("src.config.S3_PREFIX", prefix):
        assert utils.tenant_from_bucket(bucket) == expected
