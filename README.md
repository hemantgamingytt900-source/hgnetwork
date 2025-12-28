PYTHON AND DISCORD INSTALL COMMANDS

```# 1. Update packages
sudo apt update

# 2. Install prerequisites
sudo apt install ca-certificates curl gnupg lsb-release -y

# 3. Add Docker’s official GPG key
sudo mkdir -p /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg

# 4. Set up the stable repository
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
  $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

# 5. Update package index
sudo apt update

# 6. Install Docker Engine, CLI, containerd, and Docker Compose plugin
sudo apt install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin -y

# 7. Verify Docker installation
docker --version
docker run hello-world```


```sudo apt install python3-pip -y```

```sudo apt update```
```sudo apt install python3 python3-pip -y```

```nano ipport.py```
```nano anti.py```

```python3 ipport.py```
```python3 anti.py```


