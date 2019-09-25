# MLwebapp
Python web app using Flask for Statistical Diagram Classification (CNN)</br>

## Model
We trained a CNN using keras. We are able to get ~90% training and testing accuracy.

## App
App writed using Flask framework on Python.

## Docker
App is packaged into dockerfile for easy deployment. </br>

It is also pushed to dockerhub, run the app by the command: (latest tagname: v0.3)
```
docker run -p 4000:80 hamesewe/statsclf:tagname
```
Web app is available at http://localhost:4000 after executing the command.
</br></br>
Dockerhub Link: [hamesewe/statsclf](https://hub.docker.com/r/hamesewe/statsclf)

## Demo
[~~http://chartmaster.cf~~](http://chartmaster.cf)
