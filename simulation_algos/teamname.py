"""
TODO: Rename this file with <name>.py where <name> is your team name *all* in lower case with underscores
e.g. awesome_theory_of_om.py
"""

from simulation_game.buyer import Buyer
from simulation_game.seller import Seller
from random import randint
import numpy as np
import scipy.stats as ss
import scipy.optimize as so
import time
import scipy
import scipy
from sympy.utilities.lambdify import lambdify
import sympy
from sympy import exp

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
            exp_array = self.trunc_exp_rv(0, price_h[t - 1], 1 / (exp_rate*1.0), size=num_buyers * n_samples)
        exp_array_matrix = np.reshape(exp_array, (n_samples, num_buyers))
        # create booolean array, True if reservation > price
        above_price = exp_array_matrix > price_h[t]
        # calculate the number customers with reservation higher than price for that sample (sum the row)
        num_sales = np.sum(above_price, axis=1)
        # can only sell as much as remaining inventory
        truncated_num_sales = np.minimum(num_sales, inventory_h[t])
        expected_sales = float(sum(truncated_num_sales)) / float(n_samples)
        return expected_sales

    def est_rate(self,t, inventory_h, price_h, num_buyers, reserve_price):
        r = sympy.symbols('r')
        k = inventory_h[t - 1] - inventory_h[t]
        for i in range(1, t + 1):
            k = inventory_h[i - 1] - inventory_h[i]
            if i == 1:
                tempfun = -1 * scipy.misc.comb(num_buyers, k) * exp(-r * price_h[0] * k) * (1 - exp(
                    -r * price_h[0])) ** (num_buyers - k)
            else:
                addfun = scipy.misc.comb(num_buyers - (inventory_h[0] - inventory_h[i]), k) * (exp(
                    -r * price_h[i - 1]) - exp(-r * price_h[i - 2])) ** k * (1 - exp(-r * price_h[i - 1])) ** (
                num_buyers - (inventory_h[0] - inventory_h[i]))
                tempfun = tempfun * addfun
        fun = lambdify(r, tempfun)
        print(tempfun)
        res = so.minimize(fun, x0=1/reserve_price, bounds=((0, 10),))
        return res
    #exp_rate=2

    def _get_decision_impl(self,t, inventory_h, price_h, reserve_price, b_t_1_n, horizon, num_buyers):
        if t == 0:
            rate = 1 / reserve_price
        else:
            res = self.est_rate(t, inventory_h, price_h, num_buyers, reserve_price)
            rate = res.x
        print("est rate", rate)
        if reserve_price > price_h[t]:
            if t+1==horizon: return 1
            elif inventory_h[0]>=num_buyers: return 0
            else:
                if inventory_h[0]>=.75*num_buyers:
                    alpha = .8
                elif inventory_h[0]>=.5*num_buyers:
                    alpha = .5
                else:
                    alpha = .1
                expected_num_purchase = self._expected_purchase(num_buyers, inventory_h, rate, price_h, 100, t)
                current_buyers=num_buyers-(inventory_h[0]-inventory_h[t])
                est_leftover_inventory = round(inventory_h[t] - expected_num_purchase)
                est_remaining_buyers = current_buyers - round(expected_num_purchase)

                return 0 if est_leftover_inventory > alpha * est_remaining_buyers else 1
        else:
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
