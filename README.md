# Challenge ML
This repository is used to store the code developed to solve the challenge proposed by ML data team.

The application has its functionality separated in three-tiers, following a microservice architecture:
 - UI tier – running on a nginx service
 - Logic tier – with Python component
 - Data tier – MySQL database to persist the data 


![img.png](img.png)

The structure of the project files is being design to isolate the files and configurations for each service. It does this by having a dedicated directory per service inside the project one. This is very useful to have a clean view of the components and to easily containerize each service. It also helps in manipulating service specific files without having to worry that we could modify by mistake other service files.

Project  
├─── web  
└─── app  
└─── db

To initialize the application, at the root directory of the project, it´s necessary to run the command docker-compose.

http://127.0.0.1/api/v1/resources/unload
http://127.0.0.1/api/v1/resources/load
