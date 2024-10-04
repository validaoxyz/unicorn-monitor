```

                   ██╗   ██╗██╗    ██╗██╗   ██╗      ███╗   ███╗ ██████╗ ███╗   ██╗
                   ██║   ██║██║    ██║██║   ██║      ████╗ ████║██╔═══██╗████╗  ██║
                   ██║   ██║██║ █╗ ██║██║   ██║█████╗██╔████╔██║██║   ██║██╔██╗ ██║
                   ██║   ██║██║███╗██║██║   ██║╚════╝██║╚██╔╝██║██║   ██║██║╚██╗██║
                   ╚██████╔╝╚███╔███╔╝╚██████╔╝      ██║ ╚═╝ ██║╚██████╔╝██║ ╚████║
                    ╚═════╝  ╚══╝╚══╝  ╚═════╝       ╚═╝     ╚═╝ ╚═════╝ ╚═╝  ╚═══╝

                                        \.
                                        \'.      ;.
                                         \ '. ,--''-.~-~-'-,
                                          \,-' ,-.   '.~-~-~~,
                                        ,-'   (###)    \-~'~=-.
                                    _,-'       '-'      \=~-"~~',
                                   /o                    \~-""~=-,
                                   \__                    \=-,~"-~,
                                      """===-----.         \~=-"~-.
                                                  \         \*=~-"
                                                   \         "=====----
                                                    \
                                                     \
```
A monitoring solution for Unicorn validators using Prometheus, Grafana, and a custom consensus metrics exporter.

## Features

- Custom Prometheus exporter for Unicorn validators.
- Pre-configured Grafana dashboards.
- Dockerized setup for easy deployment.

## Prerequisites

Ensure the following are installed on the machine running the Grafana + Prometheus stack:

- Docker
- Docker Compose

Install with:

```bash
sudo apt install -y docker docker-compose
```
## Installation
### 1. Enable Required Services

On the machine to be monitored (this could be the same as your Prometheus server), ensure the Prometheus exporter and REST API server are listening on ports 26660 and 1317, respectively:


```bash
# Modify prometheus settings in config.toml
sed -i '/^prometheus[[:space:]]*=/c\prometheus = true' ~/.unicornd/config/config.toml && \
sed -i '/^prometheus-listen-addr[[:space:]]*=/c\prometheus-listen-addr = ":26660"' ~/.unicornd/config/config.toml && \

# Modify API settings in app.toml
sed -i '/^enable[[:space:]]*=/c\enable = true' ~/.unicornd/config/app.toml && \
sed -i '/^swagger[[:space:]]*=/c\swagger = false' ~/.unicornd/config/app.toml && \
sed -i '/^address[[:space:]]*=/c\address = "tcp://0.0.0.0:1317"' ~/.unicornd/config/app.toml
```

Restart the unicornd service:

```bash
sudo systemctl restart unicornd.service
```

Alternatively, restart the unicornd process based on your setup.

### 2. Install Node Exporter
Install Node Exporter to gather machine-level metrics:
```bash
curl -L https://github.com/prometheus/node_exporter/releases/download/v1.6.1/node_exporter-1.6.1.linux-amd64.tar.gz | sudo tar xvz -C /usr/local/bin --strip-components=1
```

Configure Node Exporter as a systemd service:
```bash
sudo tee /etc/systemd/system/node-exporter.service > /dev/null <<EOF
[Unit]
Description=Node Exporter

[Service]
User=ubuntu
Group=ubuntu
ExecStart=/usr/local/bin/node_exporter
Restart=always

[Install]
WantedBy=multi-user.target
EOF
```
Reload systemd configuration and start `node-exporter`:
```bash
sudo systemctl daemon-reload
sudo systemctl enable node-exporter
sudo systemctl start node-exporter
```

### 3. Setting up Grafana and Prometheus


1. **Clone the repository:**

   ```bash
   git clone https://github.com/yourusername/unicorn-monitoring.git
   cd unicorn-monitoring/docker
   ```
2. **Set up environment variables:**

   Copy `.env.sample` to `.env` and fill in the required values

   ```bash
   cp .env.sample .env
   ```

   Edit `.env`:

   ```
   VALOPER=unicornvaloper...
   INSTANCE_IP=x.x.x.x
   ```

3. **Build and start the containers:**

   ```bash
   bash generate-config.sh
   docker-compose up -d
   ```

4. **Access the services**:

   Grafana will be available on port 3000. To access it:
   To access your dashboard:
     - Ensure your firewall allows port `3000`
     - Visit `http://<your-ip>:3000` and log in using credentials from your `.env` file.

## Configuration

- **Grafana Dashboards**: Located in [grafana/dashboards/](grafana/dashboards).
- **Prometheus Configuration**: Files located in [prometheus/](prometheus/).
- **Exporter Code**: Located in [exporter/](exporter).

## Contributing

Contributions are welcome! Please submit a pull request or open an issue on GitHub.

