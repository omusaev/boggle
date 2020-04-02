variable "profile" {
  default = "boggle"
}

variable "region" {
  default = "ca-central-1"
}

variable "instance" {
  default = "t2.micro"
}

variable "instance_count" {
  default = "1"
}

variable "public_key" {
  default = "./ssh/aws.pub"
}

variable "private_key" {
  default = "./ssh/aws.pem"
}

variable "ansible_user" {
  default = "ubuntu"
}

variable "ami" {
  default = "ami-e3189987"
}