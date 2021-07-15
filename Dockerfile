FROM docker.io/library/python:3.9

RUN cd /home && git clone https://github.com/Dan-in-CA/SIP.git 
WORKDIR /home/SIP
COPY plugins plugins
EXPOSE 80 20000
ENTRYPOINT ["python3", "-u", "/home/SIP/sip.py"]
