from google.cloud import secretmanager


def get_secret(project_id: str, secret_id: str, version_id: str = "latest") -> str:
    """
    Access a secret from Google Secret Manager.

    Args:
        project_id: The Google Cloud project ID.
        secret_id: The ID of the secret to access.
        version_id: The version of the secret to access.

    Returns:
        The secret value.
    """
    client = secretmanager.SecretManagerServiceClient()
    name = f"projects/{project_id}/secrets/{secret_id}/versions/{version_id}"
    response = client.access_secret_version(request={"name": name})
    return response.payload.data.decode("UTF-8")
