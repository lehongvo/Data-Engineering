#!/bin/bash
yum update -y
yum install -y httpd

# Start and enable Apache
systemctl start httpd
systemctl enable httpd

# Create index.html with our content
cat << 'EOH' > /var/www/html/index.html
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>My EC2 Web Server</title>
    <style>
      body {
        font-family: Arial, sans-serif;
        margin: 0;
        padding: 20px;
        background: #f0f2f5;
      }
      .container {
        max-width: 800px;
        margin: 0 auto;
        background: white;
        padding: 20px;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
      }
      h1 {
        color: #1a73e8;
        text-align: center;
      }
      p {
        line-height: 1.6;
        color: #333;
      }
    </style>
  </head>
  <body>
    <div class="container">
      <h1>Welcome to My EC2 Web Server</h1>
      <p>
        This page is being served from an EC2 instance running on LocalStack!
      </p>
      <p>Server Status: Running</p>
      <p>Time: <span id="time"></span></p>
    </div>
    <script>
      function updateTime() {
        document.getElementById("time").textContent =
          new Date().toLocaleString();
      }
      updateTime();
      setInterval(updateTime, 1000);
    </script>
  </body>
</html>
EOH
