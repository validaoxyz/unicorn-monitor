# Unicorn Monitoring

A professional monitoring setup for Unicorn using Prometheus, Grafana, and a custom consensus metric exporter. UwU.


## Features

- Custom Prometheus exporter for Unicorn validators.
- Pre-configured Grafana dashboards.
- Dockerized setup for easy deployment.

## Prerequisites

On the machine where you will be running the grafana+prometheus monitoring setup:

- Docker
- Docker Compose

To install:

```bash
sudo apt install -y docker docker-compose
```

On the machine that will be monitored (this can be the same machine), ensure that:

- you have `node-exporter` installed and running
- port `:26660` open on your `unicornd` binary
- [if the machine that will be monitored and the machine running the monitoring stack are different] ports `26660` and `9100` are accessible from your monitoring server

**To ensure that port `:26660` is opened:**

```bash
sed -i '/^prometheus[[:space:]]*=/c\prometheus = true' ~/.unicornd/config/config.toml && \
sed -i '/^prometheus-listen-addr[[:space:]]*=/c\prometheus-listen-addr = ":26660"' ~/.unicornd/config/config.toml
```

You'll then need to restart your `unicornd` process. If you're running `unicornd` as a `systemd` service:
```bash
sudo systemctl restart unicornd.service
```

Otherwise, restart the process according to your setup.

**To install node exporter:**
Install `node-exporter`
```bash
cd /tmp
wget https://github.com/prometheus/node_exporter/releases/download/v1.6.1/node_exporter-1.6.1.linux-amd64.tar.gz
sudo tar xvfz node_exporter-1.6.1.linux-amd64.tar.gz -C /usr/local/bin
cd ~/
```
Set up `systemd` as a process manager:
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

sudo systemctl daemon-reload
sudo systemctl enable node-exporter
sudo systemctl start node-exporter
```

## Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/yourusername/unicorn-monitoring.git
   cd unicorn-monitoring
   ```
2. **Set up environment variables:**

   Copy `.env.example` to `.env` and fill in the required values

   ```bash
   cp .env.example .env
   ```

   Edit `.env`:

   ```
   VALOPER=unicornvaloper...
   INSTANCE_IP=x.x.x.x
   ```

3. **Build and start the containers:**

   ```bash
   cd docker
   docker-compose up -d
   ```

4. **Access the services**:

   Grafana will now be running on port `:3000` on the server where you just did the above!
   To access your dashboard:
     - figure out your public IP
     - ensure that port `3000` is accessible to you on the firewall level
     - finally visit `http://<your-ip>:3000` and sign in with the credentials specified in your `.env` file in step 1)


## Configuration
* Grafana Dashboards:
  Dashboards are located in `grafana/dashboards/`

* Prometheus Configuration:
  Prometheus configuration files are in `prometheus/`

* Exporter:
  The exporter code is in `exporter/`

## Contributing

Contributions are welcome! Please submit a pull request or open an issue on GitHub.
