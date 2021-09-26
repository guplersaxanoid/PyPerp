import requests
import json 

def getUsdcL1(address):
    faucetApiKey = "da2-h4xlnj33zvfnheevfgaw7datae"
    appSyncId = "izc32tpa5ndllmbql57pcxluua"
    faucet = f"https://{appSyncId}.appsync-api.ap-northeast-1.amazonaws.com/graphql"
    headers = {
        "Content-Type": "application/json",
        "X-Api-Key": faucetApiKey
    }
    body = {
        'query':f'mutation issue {{issue(holderAddr: "{address}"){{\
                txHashQuote\
                amountQuote\
            }}\
        }}'
    }
    r = requests.post(faucet, data=json.dumps(body), headers=headers)
    return r 
