FROM docker.io/library/python:3.9

RUN cd /home && git clone https://github.com/Dan-in-CA/SIP.git 
WORKDIR /home/SIP
EXPOSE 80
ENTRYPOINT ["python3", "/home/SIP/sip.py"]
