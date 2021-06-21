# destiny
DocumEnt STatIstics maNagement sYstem
## Setup by Docker
### Prerequisites
1. Docker is installed
### Build
1. Execute below command in this repository  
`$ docker build -t destiny .`
### Run
1. Start destiny server  
`$ ./destiny-docker.sh start`
2. Stop destiny server  
`$ ./destiny-docker.sh stop`
3. Enter container  
`$ ./destiny-docker.sh bash`
### Example
1. Try to use new gem
  * `echo "new_gem" >> Gemfile`
  * `./destiny-docker.sh bundle install`
  * `./destiny-docker.sh update`
  * `./destiny-docker.sh restart`

