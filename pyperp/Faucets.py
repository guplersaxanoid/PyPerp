"""Faucet related methods and data."""

import requests
import json


def get_usdc_l1(address):
    """
    Get USDC into rinkeby wallet using the USDC faucet host by Perp.

    Arguments:
    address -- The public address of the rinkeby wallet
    """
    faucet_api_key = "da2-h4xlnj33zvfnheevfgaw7datae"
    ID = "izc32tpa5ndllmbql57pcxluua"
    faucet = f"https://{ID}.appsync-api.ap-northeast-1.amazonaws.com/graphql"
    headers = {"Content-Type": "application/json", "X-Api-Key": faucet_api_key}
    body = {
        "query": f'mutation issue {{issue(holderAddr: "{address}"){{\
                txHashQuote\
                amountQuote\
            }}\
        }}'
    }
    r = requests.post(faucet, data=json.dumps(body), headers=headers)
    return r
