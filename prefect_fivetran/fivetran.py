"""Module for running Fivetran data syncs."""

import asyncio
from typing import Any, Dict, List, Optional, Tuple, Union

from prefect import task

from prefect_fivetran.credentials import FivetranCredentials


@task
async def sync_task(
    connector_id: str,
    fivetran_credentials: "FivetranCredentials",
) -> List[Tuple[Any]]:
    """
    Executes a query against a Snowflake database.
    Args:
        connector_id: The id of the Fivetran connector to use in Prefect.
        fivetran_credentials: The credentials to use to authenticate.
    Returns:
        The output of `response.fetchall()`.
    Examples:
        Run a Fivetran connector in Prefect
        ```python
        from prefect import flow
        from prefect_fivetran import FivetranCredentials
        from prefect_fivetran import fivetran.sync
        @flow
        def fivetran_sync_flow():
            fivetran_credentials = FivetranCredentials(
                api_key="my_api_key",
                api_secret="my_api_secret",
            )
            result = fivetran.sync(
                connector_id="my_connector_id",
                fivetran_credentials=fivetran_credentials
            )
            return result
        fivetran_sync_flow()
        ```
    """
    async with fivetran_credentials.get_fivetran() as connection:
        response = await connection.sync(connector_id=connector_id)
