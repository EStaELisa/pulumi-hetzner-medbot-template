# configure git
git config --global user.name "{{git_name}}"
git config --global user.email "{{git_email}}"

# Add GitHub to known hosts
ssh-keyscan -H github.com >> ~/.ssh/known_hosts

# load github ssh key
eval "$(ssh-agent -s)"
echo "Host github.com
  AddKeysToAgent yes
  IdentityFile /root/.ssh/id_pulumi_medbot_ed25519" > ~/.ssh/config

# set permissions for githuhb ssh key
chmod 600 /root/.ssh/id_pulumi_medbot_ed25519

# add github ssh key to ssh-agent
eval "$(ssh-agent -s)"
ssh-add /root/.ssh/id_pulumi_medbot_ed25519