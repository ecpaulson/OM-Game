"""
TODO: Rename this file with <name>.py where <name> is your team name *all* in lower case with underscores
e.g. awesome_theory_of_om.py
"""

from simulation_game.buyer import Buyer
from simulation_game.seller import Seller

# TODO: Replace the string "TeamName" below with your own team's name in camel case. For e.g. "AwesomeTheoryOfOM"
TEAM_NAME = "TeamName"


class TeamNameBuyer(Buyer):
    """
    Implementation of your buyer bot
    TODO: rename this class as <Name>Buyer where <Name> is your team name in camel case e.g. AwesomeTheoryOfOMBuyer
    """
    def get_name(self):
        """
        :return: name of the team
        """
        return TEAM_NAME

    def _get_decision_impl(self, t, inventory_h, price_h, reserve_price, b_t_1_n, horizon, num_buyers):
        """
        TODO: Fill in your code here -- right now this skeleton code makes the decision to never buy
        """
        return 0


class TeamNameSeller(Seller):
    """
    Implementation of your seller bot
    TODO: rename this class as <Name>Seller where <Name> is your team name in camel case e.g. AwesomeTheoryOfOMSeller
    """
    def get_name(self):
        """
        :return: name of the team
        """
        return TEAM_NAME

    def _get_price_impl(self, t, inventory_h, price_h, price_scale, horizon, num_buyers):
       """
        TODO: Fill in your code here -- right now this skeleton code always gives an arbitrary price
        """
       return 42/10.
