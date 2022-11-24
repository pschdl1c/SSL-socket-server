## SSL socket server
Simple implementation of client-server interaction using SSL authentication (for the server).

Quick start:  
`$ git clone https://github.com/pschdl1c/SSL-socket-server.git`  
`$ cd TPM`  
`$ conda create --name <env> --file requirements.txt`

_Generate a self-signed server certificate:_
`$ python gen_cert.py`

_Start the echo-server and clients:_
`$ python server.py`
`$ python client.py`