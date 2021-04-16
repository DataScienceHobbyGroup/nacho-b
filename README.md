# nacho-b
New repo for the NachoBanana project


## Docker Instructions
### Prerequisites
1. Docker installed and runninig

### Docker build instructions
To build the image and give it a name run the following command:
```bash 
docker build -t ma_strat .
```

### Docker run instructions
To run the newly built image, rune the following command:
```bash
docker run ma_strat python /src/ma_strat.py
```