# Monitoring_App_Docker_Flask_Task
* This repository is for Implementation of a flask Application that provides API’s to monitor the server’s status (disks, memorys, and cpu), the application is implemeted by using docker and python to create a custom image for that app.

### How to run the application?
* Install the sqlite3 using this command 
```
$ docker run -it nouchka/sqlite3
```
* Install the app image using this command 
```
$ docker run -it --privileged -v /:/host -p 8080:80 yaseenasaliya/flask_monitoring_app:v1
```

### How to use it?
> In html pages go to then select go to statistics button
```
http://localhost:8080
```
> JSON
* To get disks usage 
```
http://172.17.0.2:5000/disk
```
* To get memory usage 
```
http://172.17.0.2:5000/memory
```
* To get cpu usage 
```
http://172.17.0.2:5000/cpu
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

> Here are some photos for collected usage
* Disks usage
![disks](https://user-images.githubusercontent.com/59315877/229504568-de9260bb-c77d-49cb-af58-ed285055e62d.png)
* Memory usage
![memory](https://user-images.githubusercontent.com/59315877/229504580-2240f30b-2f00-4e83-b384-a574fb597a34.png)
* CPU usage
![cpu](https://user-images.githubusercontent.com/59315877/229504541-b61a5ed4-7233-4808-b249-913765c72e5b.png)
