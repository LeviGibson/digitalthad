from dataclasses import dataclass
from textwrap import indent
import requests
import json
import pandas as pd
import urllib
from pprint import pprint

#https://cloud.hasura.io/public/graphiql?endpoint=https%3A%2F%2Flive.worldcubeassociation.org%2Fapi

body = """
query MyQuery {
  competition(id: "4451") {
    competitors {
      results {
        attempts {
          result
        }
        round {
          competitionEvent {
            event {
              id
            }
          }
          number
        }
      }
      name
      registrantId
    }
  }
}
"""

url = 'https://live.worldcubeassociation.org/api'
r = requests.post(url, json={'query': body})

data = json.loads(r.text)['data']['competition']['competitors']

def get_results(regId, event, round):
    for point in data:
        if point['registrantId'] == regId:
            for r in point['results']:
                if r['round']['competitionEvent']['event']['id'] == event:
                    if r['round']['number'] == round:
                        return list(z['result'] for z in r['attempts'])
                