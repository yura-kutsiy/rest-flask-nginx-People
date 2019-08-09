Readme.md
This is a simple application which is aimed at understanding and putting together various pieces of the puzzle. 

Bird’s Eye View:
In this application, we use flask for creating the web app with connexion and swagger-ui for API documentation. 
We create RESTful API for requests and use a fast in-memory Redis server for database needs. 
JSON is used for the data interchange and is serialized and deserialized using python json module. 
Nginx acts as a reverse proxy for this app and Docker with user defined networks are used to containerize the application.

