# Pulumi Project

This project uses Pulumi to manage infrastructure on Hetzner Cloud.

## Prerequisites

- [Pulumi](https://www.pulumi.com/docs/get-started/install/)
- [Hetzner Cloud Account](https://www.hetzner.com/cloud)
- SSH keys for accessing the servers

## Setup

Configure your Pulumi stack:

```sh
pulumi config set hcloud:token <your-hcloud-token> --secret
pulumi config set hetzner_medbot:ssh-key-public /path/to/your/id_rsa.pub
pulumi config set hetzner_medbot:ssh-key-private /path/to/your/id_rsa
pulumi config set hetzner_medbot:git-ssh-key /path/to/your/id_pulumi_medbot_ed25519
pulumi config set hetzner_medbot:git-user-name "Your Name"
pulumi config set hetzner_medbot:git-user-email "your.email@example.com"
```

## Usage

1. Preview the changes:

    ```sh
    pulumi preview
    ```

2. Apply the changes:

    ```sh
    pulumi up
    ```

3. To destroy the stack:

    ```sh
    pulumi destroy
    ```
