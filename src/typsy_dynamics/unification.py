# 
# 
# def Block():
# 
#     def init(self):
#         pass
# 
#     def update(self):
#         ''' Performs the block function. '''
#         pass
# 
#     def finish(self):
#         pass
# 
#     def cleanup(self):
#         pass

# 
# class RobotInterface(PassiveRobotInterface):
#     ''' 
#         This is the basic class for robots. 
#         
#         Protocol notes:
#         
#         - new_episode() must be called before get_observations()
#     '''
# 
#     @abstractmethod
#     @contract(returns=EpisodeDesc)
#     def new_episode(self):
#         ''' 
#             Skips to the next episode. 
#             In real robots, the platform might return to start position.
#             
#             Guaranteed to be called at least once before get_observations().
#             
#             Should return an instance of EpisodeDesc.
#         '''
# 
#     @abstractmethod
#     @contract(commands='array', commands_source='str')
#     def set_commands(self, commands, commands_source):
#         ''' Send the given commands. '''
# 
#     @abstractmethod
#     @contract(returns=BootSpec)
#     def get_spec(self):
#         ''' Returns the sensorimotor spec for this robot
#             (a BootSpec object). '''
# 
#     @abstractmethod
#     @contract(returns=RobotObservations)
#     def get_observations(self):
#         ''' 
#             Get observations. Must return an instance of RobotObservations,
#             or raise either:
#             - RobotObservations.Finished => no more observations
#             - RobotObservations.NotReady => not ready yet
#         '''
