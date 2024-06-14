from django.db import models


# This class represents an api_simulation run containing multiple or one point(s)
# The id of this class is used to determine the position where the results are stored
# noinspection PyUnresolvedReferences
class SimulationRunModel(models.Model):
    # Get the points of this run (related_name='points' is used in SimulationPointModel) # TODO: check
    def get_points(self):
        return self.points.all()  # TODO: check

    # Get the finished points of this run
    def get_finished_points(self):
        return self.points.filter(_finished=True)  # TODO: check

    # Get the unfinished points of this run
    def get_unfinished_points(self):
        return self.points.filter(_finished=False)  # TODO: check

    # Check if the run is finished
    def is_finished(self):
        return self.get_unfinished_points().count() == 0

    # Get the path this run is stored in... # TODO: check is this should be here
    # noinspection PyMethodMayBeStatic
    def get_path(self):
        return None  # TODO: implement this function
    # TODO: getter
