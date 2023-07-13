from main.logger.custom_logging import log
from main.models.ondc_request import OndcDomain, OndcAction
from main.repository.db import get_first_ondc_request
from main.service.common import get_responses_from_client
from main.service.utils import make_request_over_ondc_network
from main.utils.decorators import check_for_exception
from main.utils.webhook_utils import post_on_bg_or_bap



def make_retail_issue_status_payload_request_to_client(issue_status_payload):
    return get_responses_from_client("client/issue_status", issue_status_payload)


@check_for_exception
def send_issue_status_payload_to_client(message):
    log(f"retail issue_status payload: {message}")
    issue_status_message_id = message['message_ids']['issue_status']
    issue_status_payload = get_first_ondc_request(
        OndcDomain.RETAIL, OndcAction('issue_status'), issue_status_message_id)
    resp, return_code = make_retail_issue_status_payload_request_to_client(
        issue_status_payload)
    log(f"Got response {resp} from client with status-code {return_code}")




@check_for_exception
def send_issue_status_response_to_bap(message):
    log(f"retail on_issue_status payload: {message}")
    on_issue_status_message_id = message['message_ids']['on_issue_status']
    on_issue_status_payload = get_first_ondc_request(
        OndcDomain.RETAIL, OndcAction('on_issue_status'), on_issue_status_message_id)
    bap_endpoint = on_issue_status_payload['context']['bap_uri']
    status_code = make_request_over_ondc_network(
        on_issue_status_payload, bap_endpoint, 'on_issue_status')
    log(f"Sent responses to bg/bap with status-code {status_code}")


