output "app-url" {
  value = "http://${aws_instance.boggle.0.public_ip}"
}