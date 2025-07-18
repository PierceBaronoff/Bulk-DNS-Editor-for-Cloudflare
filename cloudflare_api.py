import requests

class CloudflareAPI:
    def __init__(self, api_token):
        self.api_token = api_token
        self.base_url = "https://api.cloudflare.com/client/v4"

    def _headers(self):
        return {
            "Authorization": f"Bearer {self.api_token}",
            "Content-Type": "application/json"
        }

    def validate_token(self):
        resp = requests.get(f"{self.base_url}/user/tokens/verify", headers=self._headers())
        return resp.status_code == 200

    def get_zones(self):
        response = requests.get(f"{self.base_url}/zones", headers=self._headers())
        return response.json().get('result', [])

    def find_records_by_ip(self, ip):
        matching_records = []
        for zone in self.get_zones():
            zone_id = zone['id']
            zone_name = zone['name']
            dns_records = requests.get(
                f"{self.base_url}/zones/{zone_id}/dns_records",
                headers=self._headers()
            ).json().get('result', [])
            for record in dns_records:
                if record.get('content') == ip:
                    matching_records.append({
                        'zone_name': zone_name,
                        'zone_id': zone_id,
                        'record_id': record['id'],
                        'name': record['name'],
                        'type': record['type'],
                        'ttl': record['ttl'],
                        'content': record['content']
                    })
        
        matching_records = []
        use_wildcard = '*' in ip
        pattern = re.compile(r'^' + re.escape(ip).replace('\*', '.*') + r'$') if use_wildcard else None
        for zone in self.get_zones():
            zone_id = zone['id']
            zone_name = zone['name']
            dns_records = requests.get(
                f"{self.base_url}/zones/{zone_id}/dns_records",
                headers=self._headers()
            ).json().get('result', [])
            for record in dns_records:
                record_ip = record.get('content')
                if use_wildcard and pattern.match(record_ip) or (not use_wildcard and record_ip == ip):
                    matching_records.append({
                        'zone_name': zone_name,
                        'zone_id': zone_id,
                        'record_id': record['id'],
                        'name': record['name'],
                        'type': record['type'],
                        'ttl': record['ttl'],
                        'content': record['content']
                    })
        return matching_records

    def update_record_ip(self, zone_id, record_id, new_ip):
        url = f"{self.base_url}/zones/{zone_id}/dns_records/{record_id}"
        record = requests.get(url, headers=self._headers()).json()['result']
        record['content'] = new_ip
        response = requests.put(url, json=record, headers=self._headers())
        return response.ok