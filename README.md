# Monitoring_App_Docker_Flask_Task
* This repository is for Implementation of a flask Application that provides API’s to monitor the server’s status (disks, memorys, and cpu), the application is implemeted by using docker and python to create a custom image for that app.

### How to run the application?
* Install the sqlite3 using this command 
```
$ docker run -it nouchka/sqlite3
```
* Install the app image using this command 
```
$ docker run yaseenasaliya/flask_monitoring_app:v1
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
