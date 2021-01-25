# Fundamental settings
provider "aws" {
    region="eu-central-1"
}

# Spot instance for dashboard
resource "aws_spot_instance_request" "yt-dashboard" {
  ami           = "ami-1234"
  instance_type = "t2.micro"

  tags = {
    Name = "YTDashboard"
  }
}