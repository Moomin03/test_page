import base64
import requests
from nacl import public, encoding

class EnvEncrypy:
    def __init__(self, user_name, repo_name, token):
        self.user_name = user_name
        self.repo_name = repo_name
        self.token = token
        
    # Discord, Slack Webhook 알림 기능
    def discordwebhook_notifier(self, webhook_url: str):
        """Discord Webhook 알림 기능"""
        url = f'https://api.github.com/repos/{self.user_name}/{self.repo_name}/actions/secrets/public-key'
        headers = {'Authorization': f'token {self.token}'}
        resp = requests.get(url, headers=headers)
        pubkey_info = resp.json()
        key_id = pubkey_info['key_id']
        # 암호화할 값은 webhook_url이어야 함
        encrypted_value = self.encrypt(pubkey_info['key'], webhook_url)

        # Secret 등록(Repo -> Settings -> Secrets and variables -> Actions -> New repository secret 자동화)
        url2 = f'https://api.github.com/repos/{self.user_name}/{self.repo_name}/actions/secrets/{self.secret_discord}'
        payload = {
            "encrypted_value": encrypted_value,
            "key_id": key_id
        }
        resp2 = requests.put(url2, headers={**headers, 'Content-Type': 'application/json'}, json=payload)
    
    def slackwebhook_notifier(self, webhook_url: str):
        """Slack Webhook 알림 기능"""
        url = f'https://api.github.com/repos/{self.user_name}/{self.repo_name}/actions/secrets/public-key'
        headers = {'Authorization': f'token {self.token}'}
        resp = requests.get(url, headers=headers)
        pubkey_info = resp.json()
        key_id = pubkey_info['key_id']
        # 암호화할 값은 webhook_url이어야 함
        encrypted_value = self.encrypt(pubkey_info['key'], webhook_url)

        # Secret 등록(Repo -> Settings -> Secrets and variables -> Actions -> New repository secret 자동화)
        url2 = f'https://api.github.com/repos/{self.user_name}/{self.repo_name}/actions/secrets/{self.secret_slack}'
        payload = {
            "encrypted_value": encrypted_value,
            "key_id": key_id
        }
        resp2 = requests.put(url2, headers={**headers, 'Content-Type': 'application/json'}, json=payload)
        print("Slack 등록:", resp2.status_code, resp2.text)

    # webhook_url을 넣을 때, 암호화를 진행해야한다고 함
    def encrypt(self, public_key: str, secret_value: str) -> str:
        # public_key는 base64 인코딩된 문자열
        public_key = public.PublicKey(public_key, encoding.Base64Encoder())
        sealed_box = public.SealedBox(public_key)
        encrypted = sealed_box.encrypt(secret_value.encode("utf-8"))
        return base64.b64encode(encrypted).decode("utf-8")