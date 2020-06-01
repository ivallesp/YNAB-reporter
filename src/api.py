import logging
import ynab_client


from src.config import load_ynab_config


logger = logging.getLogger(__name__)


def fetch_transactions(ynab_cli, budget_name):
    """Downloads all the transactions of the budget specified and returns them
    in a list of dictionaries

    Args:
        ynab_cli (ynab_client): YNAB configured client with the credentials
        budget_name ([type]): name of the budget to query

    Returns:
        list: list of dictionaries, each dictionary representing a trnsaction
    """
    budget_id = get_ynab_budget_id_mapping(ynab_cli)[budget_name]
    trans_api = ynab_cli.TransactionsApi()

    # Dummy class to retrieve the raw output as the built-in method does not
    # return all the fields
    class RawResponse:
        swagger_types = []

    data, status, _ = trans_api.api_client.call_api(
        "/budgets/{budget_id}/transactions",
        "GET",
        path_params={"budget_id": budget_id},
        response_type=RawResponse,
        auth_settings=["bearer"],
    )
    data = data["data"]["transactions"]
    return data


def get_ynab_budget_id_mapping(ynab_client):
    """Build a mapping of YNAB budget names to internal ids

    Args:
        ynab_client (ynab_client): YNAB configured client with the credentials

    Returns:
        dict: Dictionary with budget names as keys and ids as values
    """
    response = ynab_client.BudgetsApi().get_budgets().data.budgets
    mapping = {budget.name: budget.id for budget in response}
    return mapping


def get_ynab_client():
    """Handles YNAB connection and returns the cli

    Returns:
        ynab_client: client ready to query the API
    """
    config = load_ynab_config()
    configuration = ynab_client.Configuration()
    configuration.api_key_prefix["Authorization"] = "Bearer"
    configuration.api_key["Authorization"] = config["ynab"]["api_key"]
    return ynab_client
