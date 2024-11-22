# SPDX-FileCopyrightText: 2024 Liv Dywan <liv.dywan@suse.com>
#
# SPDX-License-Identifier: EUPL-1.2

import re
import json
import requests
import os
import glob

class Job:
    uri: str

    def __init__(self, uri: str):
        self.uri = uri

    def fetch(self) -> {}:
        # Extract the test ID from the test URL
        match = re.search(r'/tests/(\d+)(?:#.*)?$', self.uri)
        if not match:
            raise ValueError(f"Invalid test URL: {self.uri}")

        host = 'https://openqa.opensuse.org'
        test_id = int(match.group(1))

        # If the job is cached we're good
        cached = os.path.join('dataset', f"**/{test_id}.txt")
        if glob.glob(cached):
            return

        # Fetch job result and logfile
        api_url = f"{host}/api/v1/experimental/jobs/{test_id}/status"
        print(f"Fetching {api_url}")
        response = requests.get(api_url)

        if response.status_code != 200:
            raise Exception(f"Failed to fetch test result: {response.status_code}")
        result = json.loads(response.content)['result']

        api_url = f"{host}/tests/{test_id}/file/autoinst-log.txt"
        print(f"Fetching {api_url}")
        response = requests.get(api_url)

        if response.status_code != 200:
            raise Exception(f"Failed to fetch test log: {response.status_code}")

        os.makedirs(os.path.join('dataset', result), exist_ok=True)
        cached = os.path.join('dataset', f"{result}/{test_id}.txt")
        with open(cached, 'w') as autoinst_log:
            autoinst_log.write(response.text)
