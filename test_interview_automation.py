import subprocess
from subprocess import PIPE
from datetime import datetime
import requests
import json

def log(message):
    """
    logs the date and time
    :param message: String
    """
    datenow = datetime.today().strftime('%d-%m-%Y %H:%M:%S')
    print("{0} |  {1}".format(datenow, message))

class DockerMethod:

    def create_network(self,networkName):
        command = ["docker", "network", "create","-d", "bridge", networkName]
        self.command_execute(command)

    def add_network(self,networkName, containerName):
        command = ["docker", "network", "connect", networkName,containerName ]
        self.command_execute(command)

    def build_container_images(self, imagename, dockerfile):
        command = ['docker', 'build', '-t', 'test_interview_rails', '-f', '/Users/ezgovind/Documents/ruby/Dockerfile', "."]
        print(command)
        popen = subprocess.Popen(command, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        popen.wait(500)
        stdout, stderr = popen.communicate()
        error = stderr

        if error != None:
            error = error.replace("\n", "")
            log("An error occurred:" + error)
        else:
            log(" - Build is complete  " + str(stdout) )

    def run_container(self, networkName, containerName, port):
        command = ['docker', 'run', '-d', '--net', networkName, '--name', containerName,'-p',port, 'test_interview_rails','bin/rails','s','-b','0.0.0.0']
        print(command)
        popen = subprocess.Popen(command, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        popen.wait(500)
        stdout, stderr = popen.communicate()
        error = stderr
        if error != None:
            error = error.replace("\n", "")
            log("An error occurred:" + error)
        else:
            log(" - New container ID " + str(stdout))

    def run_container_with_exec(self, networkName, containerName, containerImage, execCommand, args):
        command = ["docker", "run", "-d", "--net", networkName, "--name", containerName]
        command.extend(args)
        command.append(containerImage)
        command.append(execCommand)
        self.command_execute(command)

    def command_execute(self, command):
        debugcommand = " - {0}".format(" ".join(command))
        log(debugcommand)
        popen = subprocess.Popen(command, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        popen.wait(500) # wait a little for docker to complete

    def clean_image(self):
        """
        Cleans the setup
        :return: None
        """
        command = ["docker", "images", "-q", "-f", "dangling=true"]
        image_ids = self.command_execute(command)
        if image_ids == None:
            log("No hanging container images to remove")
        else:
            for id in image_ids.stdout.readlines():
                id = id.decode("utf-8")
                id = id.replace("\n", "")

                log("Removing container image id " + id)
                command = ["docker", "rmi", "-f", str(id)]
                self.command_execute(command)

    def remove_container(self, containerName):
        command = ["docker", "rm", "-f", containerName]
        self.command_execute(command)
        log(" - Removed " + containerName)

    def command_execute_in_container(self, containerName, commandargs):
        command = ['docker','exec',containerName]
        for commandarg in commandargs:
            command.append(commandarg)
        popen = subprocess.Popen(command, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        popen.wait(500)
        stdout, stderr = popen.communicate()
        error = stderr
        if error != None:
            error = error.replace("\n", "")
            log("An error occurred:" + error)
        else:
            # id = popen.stdout.readline().decode("utf-8")
            # id = id.replace("\n", "")
            log("Able to reach the rubyrails server")
        return str(stdout)

networkNames = [
    "test-master",
    "test-bridge1",
    "test-bridge2",
    "test-bridge3",
    "test-bridge4",
    "test-bridge5"
]
containerImages = "test_interview_rails"
dockerFile = "/Users/ezgovind/Documents/ruby/Dockerfile"
containerNames = [
    "rails-master",
    "rails-node1",
    "rails-node2",
    "rails-node3",
    "rails-node4",
    "rails-node5"
]

print("################ Boots 6 environments, each with an instance of the rails app and a client that can curl #######################")
print("\n")
dockerMethod = DockerMethod()
dockerMethod.clean_image()
log("Removing containers.")

for containername in containerNames:
    dockerMethod.remove_container(containername)
dockerMethod.clean_image()
dockerMethod.build_container_images(containerImages, dockerFile)

for newtorkname in networkNames:
    log("Creating {0} network.".format(newtorkname))
    dockerMethod.create_network(newtorkname)

port = 3000
for i in range(0,len(containerNames)):
    local_port = str(port) +':3000'
    dockerMethod.run_container(networkNames[i], containerNames[i], local_port )
    port +=1

for i in range(1,len(containerNames)):
    dockerMethod.add_network(networkNames[i],containerNames[0])

print("################ Tests that the rails process is up ################## ")
print("\n")
port = 3000
for i in range(len(containerNames)):
    api_url = "http://localhost:"+str(port)
    # response = requests.request("GET", api_url)
    # print(response.text)
    response = requests.get(api_url)
    print(response.status_code)
    if (response.status_code ==200):
        log(" Ruby on Rail is up -  " + containerNames[i])
        print(" Ruby on Rail is up -  " + containerNames[i])
    else:
        log(" Ruby on Rail is not up -  " + containerNames[i])
        print(" Ruby on Rail is not up -  " + containerNames[i])
    port +=1

print("################ Tests that the client in each environment can successfully reach the rails app in the environment ################## ")
print("\n")

for i in range(len(containerNames)):
    commandargs = ['python3','client.py', containerNames[i]]
    output = dockerMethod.command_execute_in_container(containerNames[i],commandargs)
    print(output)
    if "200" in output:
        log(" Ruby on Rail is up -  " + containerNames[i])
        print(" Ruby on Rail is up -  " + containerNames[i])
    else:
        log(" Ruby on Rail is not up -  " + containerNames[i])
        print(" Ruby on Rail is not up -  " + containerNames[i])

print("################ Sets up the environments as 5 nodes and one master, so that each node can talk back and forth with the master but no node can talk to any other node ################## ")
print("\n")
for i in range(len(containerNames)):
    print("\n")
    print("################ "+containerNames[i] +"###################")
    for j in range(len(containerNames)):
        commandargs = ['python3','client.py', containerNames[i]]
        output = dockerMethod.command_execute_in_container(containerNames[j],commandargs)
        if "200" in output:
            print(f" Rails server can talk from { containerNames[i]}  to { containerNames[j]}")
        if 'Name or service not known' in output:
            print(f" Rails server cannot talk from { containerNames[i]}  to { containerNames[j]}")