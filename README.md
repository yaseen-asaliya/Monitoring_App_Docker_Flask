# Monitoring_App_Docker_Flask_Task
* This repository is for Implementation of a flask Application that provides API’s to monitor the server’s status (disks, memorys, and cpu), the application is implemeted by using docker and python to create a custom image for that app.

### How to run the application?
#### Run it using `docker run`
* Install the app image using this command 
```
# docker run yaseenasaliya/flask_monitoring_app:v1
```


#### Run it using `docker compose`
* 


### How to use it?
> Go to localhost url
```
http://localhost
```


### How it was pushed on Docker Hub?
* Build image localy with `v1` tage
```
# docker build . -t yaseenasaliya/flask_monitoring_app:v1
```
* Login to docker hub using the this command
```
# docker login
```
* Push the image
```
# docker push yaseenasaliya/flask_monitoring_app:v1
```


## Database Side
* Pull mariadb docker image
```
# docker pull mariadb
```
* Create docker compose file `setup-database.yml` with mariadb database image and create a new user `yaseen` and database called `monitoring_app`
```
version: "3"

services:
  db:
    image: mariadb
    container_name: my_db
    env_file: .env
    ports:
      - "3306:3306"
```
* Create `.env` file 
```
MYSQL_ROOT_PASSWORD: root
MYSQL_DATABASE: monitoring_app
MYSQL_USER: yaseen
MYSQL_PASSWORD: yaseen
```
* Run a docker compose file 
```
# docker compose -f setup-database.yml up -d
```
* To connect to the database 
```
# mysql -P 3306 --protocol=tcp -u yaseen -pyaseen
```






> Here are some photos for collected usage
* Disks usage
![disks](https://user-images.githubusercontent.com/59315877/229504568-de9260bb-c77d-49cb-af58-ed285055e62d.png)
* Memory usage
![memory](https://user-images.githubusercontent.com/59315877/229504580-2240f30b-2f00-4e83-b384-a574fb597a34.png)
* CPU usage
![cpu](https://user-images.githubusercontent.com/59315877/229504541-b61a5ed4-7233-4808-b249-913765c72e5b.png)
