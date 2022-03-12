# Webhook to Google Cloud Pubsub
This code has the simple mission of receiving a payload via HTTP 1.1 on any URL and place the content body in a pubsub topic.

![](documentation/run_to_pubsub.svg)

The webhook will listen to any url path and HTTP method (GET, POST, PUT, ...). As long that there's a body, the message will be sent to Pubsub. All the http message headers will be added in the PubsubMessage attributes, also 'request-path' and 'request-method' will be added with the path and method information.

The service account associated with the service that runs the container will be checked for permission `pubsub.topics.publish` on the configured topic before it starts to listen to HTTP calls. If the container fails to start the webserver, please check the logs because this is a possible reason of the container failing to start.

## Expected environment variables

|Environment Variable|Mandatory|Default|Description|
|--------------------|---------|-------|-----------|
|DEFAULT_RESPONSE|No|"OK"|string reponse that will be sent as response body on success(200) call of the webhook|
|PUBSUB_TOPIC|Yes||Topic name of the destination pubsub topic. Expected format regex ^projects\/[^/]+\/topics\/[^/]+$"|
