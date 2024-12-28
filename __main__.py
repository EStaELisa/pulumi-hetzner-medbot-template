import pulumi
import pulumi_hcloud as hcloud
import pulumi_std as std
import pulumi_command as command
from pulumi_command import local
from jinja2 import Template

# context has the configuration values
config = pulumi.Config()

# upload ssh key to hetzner
ssh_key = hcloud.SshKey(
    "ssh-key",
    name="pulumi-ssh-key",
    public_key=std.file(input=config.require(key="ssh-key-public")).result,
)

# Create a Hetzner server instance
server = hcloud.Server(
    "medbot-server",
    name="medbot",
    image="ubuntu-22.04",
    server_type="cax41",
    public_nets=[
        {
            "ipv4_enabled": True,
            "ipv6_enabled": True,
        }
    ],
    datacenter="fsn1-dc14",
    labels={
        "project": "medbot",
        "managedBy": "pulumi",
    },
    ssh_keys=[ssh_key.id],
)

# The configuration of the SSH connection to the instance.
conn = command.remote.ConnectionArgs(
    host=server.ipv4_address,
    user="root",
    private_key=std.file(input=config.require(key="ssh-key-private")).result,
)

# Upload private key to server
copy_gh_ssh_key = command.remote.CopyToRemote(
    "copy-git-ssh-key",
    connection=conn,
    source=pulumi.asset.FileAsset(config.require(key="git-ssh-key")),
    remote_path="/root/.ssh/id_pulumi_medbot_ed25519",
)

# Ensure the SSH key is copied before running any other commands
depends_on = [copy_gh_ssh_key]

# Execute SSH command on the new server
scripts = {
    "update": "scripts/update.sh",
    "git": "scripts/git.sh",
    "git-clone": "scripts/git-clone.sh",
    "install-dependencies": "scripts/install-dependencies.sh",
}
for name, script in scripts.items():
    with open(script) as f:
        template = Template(f.read())
        file_content = template.render(
            git_name=config.require("git-user-name"),
            git_email=config.require("git-user-email"),
        )
        current_command = command.remote.Command(
            f"run-{name}",
            connection=conn,
            create=file_content,
            opts=pulumi.ResourceOptions(depends_on=depends_on), # Ensure the SSH key is copied before running any other commands
        )
        depends_on.append(current_command)
    

# Render the SSH config template and save it to ~/.ssh/ssh_config
def render_ssh_config(ipv4_address):
    with open('ssh_config.txt') as f:
        template = Template(f.read())
    ssh_config_content = template.render(hostname=ipv4_address)
    local.Command(
        "update-ssh-config",
        create=f'echo "{ssh_config_content}" >> ~/.ssh/config',
        delete=f'python3 remove_ssh_entry.py ~/.ssh/config hetzner',
    )
    
    local.Command(
        "known_host",
        create=f'ssh-keyscan {ipv4_address} >> ~/.ssh/known_hosts',
        delete=f'ssh-keygen -R {ipv4_address}',
        opts=pulumi.ResourceOptions(depends_on=depends_on),
    )

server.ipv4_address.apply(render_ssh_config) # process will only run after ip adress is available

pulumi.export("server_ip", server.ipv4_address)