resource "aws_key_pair" "terraform_admin" {
  key_name   = "terraform_admin"
  public_key = file(var.public_key)
}

resource "aws_instance" "boggle" {
  count = var.instance_count

  ami           = var.ami
  instance_type = var.instance
  key_name      = aws_key_pair.terraform_admin.key_name

  vpc_security_group_ids = [
    aws_security_group.web.id,
    aws_security_group.ssh.id,
    aws_security_group.egress-tls.id,
    aws_security_group.ping-ICMP.id,
  ]

  connection {
    private_key = file(var.private_key)
    user        = var.ansible_user
    host        = self.public_ip
  }

  # Ansible requires Python to be installed on the remote machine as well as the local machine.
  provisioner "remote-exec" {
    inline = ["sudo apt-get -qq install python -y"]
  }
}

resource "aws_security_group" "web" {
  name        = "web"
  description = "Security group for web that allows web traffic from internet"

  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "sg-web"
  }
}

resource "aws_security_group" "ssh" {
  name        = "ssh"
  description = "Security group for nat instances that allows SSH and VPN traffic from internet"

  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "sg-ssh"
  }
}

resource "aws_security_group" "egress-tls" {
  name        = "egress-tls"
  description = "Default security group that allows inbound and outbound traffic from all instances in the VPC"

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "sg-egress-tls"
  }
}

resource "aws_security_group" "ping-ICMP" {
  name        = "ping"
  description = "Default security group that allows to ping the instance"

  ingress {
    from_port        = -1
    to_port          = -1
    protocol         = "icmp"
    cidr_blocks      = ["0.0.0.0/0"]
    ipv6_cidr_blocks = ["::/0"]
  }

  tags = {
    Name = "sg-ping"
  }
}