"""
TODO: Rename this file with <name>.py where <name> is your team name *all* in lower case with underscores
e.g. awesome_theory_of_om.py
"""

from simulation_game.buyer import Buyer
from simulation_game.seller import Seller
from random import randint
import numpy as np
import scipy.stats as ss
import time

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

    def trunc_exp_rv(self,low, high, scale, size):
        rnd_cdf = np.random.uniform(ss.expon.cdf(x=low, scale=scale),
                                    ss.expon.cdf(x=high, scale=scale),
                                    size=size)
        return ss.expon.ppf(q=rnd_cdf, scale=scale)

    def _expected_purchase(self,num_buyers, inventory_h, exp_rate, price_h, n_samples, t):
        # NEED TO SAMPLE FROM TRUNCATED DISTR
        # generate sampled reservation prices and put in a n_samples x n_customers array
        # exp_array = np.random.exponential(2, size=num_buyers[t] * n_samples)
        if t == 0:
            exp_array = np.random.exponential(1/(exp_rate*1.0), size=num_buyers * n_samples)
        else:
            exp_array = self.trunc_exp_rv(0, price_h[t - 1], 1 / exp_rate, size=num_buyers * n_samples)
        exp_array_matrix = np.reshape(exp_array, (n_samples, num_buyers))
        # create booolean array, True if reservation > price
        above_price = exp_array_matrix > price_h[t]
        # calculate the number customers with reservation higher than price for that sample (sum the row)
        num_sales = np.sum(above_price, axis=1)
        # can only sell as much as remaining inventory
        truncated_num_sales = np.minimum(num_sales, inventory_h[t])
        expected_sales = float(sum(truncated_num_sales)) / float(n_samples)
        return expected_sales

    exp_rate=2

    def _get_decision_impl(self,t, inventory_h, price_h, reserve_price, b_t_1_n, horizon, num_buyers):
        if reserve_price > price_h[t]:
            print("res price>price")
            if t+1==horizon: return 1
            else:
                n = randint(0, 2)
                if n == 0:
                    alpha = .5
                elif n == 1:
                    alpha = .75
                else:
                    alpha = 1

                # current price is price_h[t]. Everyone with reservation price > price_h[t-1] has already bought.
                # Thus we are interested in the expected number of people with reservation price > price_h[t] given
                # that reservation price < price_h[t-1]
                # Is this the same as the expected number of buyers with reservation price between price_h[t] and price_h[t-1]?
                expected_num_purchase = self._expected_purchase(num_buyers, inventory_h, .5, price_h, 100, t)
                # Get vector of n reservation prices sampled from an exponential
                # Count number of res prices between price_h[t] and price_h[t-1]
                # Repeat a ton of times and take average

                est_leftover_inventory = inventory_h[t] - expected_num_purchase
                est_remaining_buyers = num_buyers - expected_num_purchase


                return 1 if est_leftover_inventory > alpha * est_remaining_buyers else 0
        else:
            print("res price too low")
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
