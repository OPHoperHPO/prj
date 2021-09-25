sudo docker build -t promotheus-front .
sudo docker run --rm -it -p 8080:80 promotheus-front
