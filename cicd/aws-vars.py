from dataclasses import dataclass

import boto3


@dataclass(frozen=True)
class Credentials:
    access_key_id: str
    secret_access_key: str
    session_token: str

    @classmethod
    def load(cls, profile_name: str = None) -> 'Credentials':
        session = boto3.Session(profile_name=profile_name)
        response = session.get_credentials()
        return cls(access_key_id=response.access_key,
                   secret_access_key=response.secret_key,
                   session_token=response.token)

    def export(self):
        print(f"export AWS_ACCESS_KEY_ID={self.access_key_id}")
        print(f"export AWS_SECRET_ACCESS_KEY={self.secret_access_key}")
        print(f"export AWS_SESSION_TOKEN={self.session_token}")


if __name__ == '__main__':
    credentials = Credentials.load()
    credentials.export()
