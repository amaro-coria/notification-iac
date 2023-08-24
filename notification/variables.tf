variable "db_name" {
  description = "The name of the database"
  type        = string
  default     = "your_db_name"
}

variable "db_user" {
  description = "The username to connect to the database"
  type        = string
  default     = "your_db_user"
}

variable "db_password" {
  description = "The password to connect to the database"
  type        = string
  default     = "your_db_password"
}

variable "db_host" {
  description = "The host of the database"
  type        = string
  default     = "your_db_host"
}

variable "db_port" {
  description = "The port of the database"
  type        = string
  default     = "your_db_port"
}

variable "sqs_queue_url_1" {
  description = "The URL of the SQS queue for channel 1"
  type        = string
  default     = "your_sqs_queue_url_1"
}

variable "sqs_queue_url_2" {
  description = "The URL of the SQS queue for channel 2"
  type        = string
  default     = "your_sqs_queue_url_2"
}

variable "sqs_queue_url_3" {
  description = "The URL of the SQS queue for channel 3"
  type        = string
  default     = "your_sqs_queue_url_3"
}
