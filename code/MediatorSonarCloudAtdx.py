from ClassMediator import *


class MediatorSonarCloudAtdx(ClassMediator, ABC):

    def __init__(self, atdx_core, sonar_cloud):
        self.atdx = atdx_core
        self.sonar_cloud = sonar_cloud

    def notify(self, sender, event):
        pass
