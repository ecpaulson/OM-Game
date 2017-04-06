from simulation_game.buyer import MyopicBuyer, FaultyBuyer
from simulation_game.seller import DummySeller
from simulation_game.simulation import simulate

import numpy as np
import numpy.random as rn

price_scale = 3
mc_trials = 100
x_0 = 3
horizon = 4


def test_simulation_game_with_two_teams_same_strategies():
    rn.seed(123)
    buyer1 = MyopicBuyer("Sarah")
    seller1 = DummySeller("Sarah")
    buyer2 = MyopicBuyer("Steve")
    seller2 = DummySeller("Steve")
    teams = [(buyer1, seller1), (buyer2, seller2)]
    mean_revenue, mean_cs = simulate(teams, horizon, x_0, mc_trials, price_scale)
    assert mean_revenue[0] == mean_revenue[1] and mean_revenue[0] > 0.
    assert mean_cs[0] == mean_cs[1] and mean_cs[0] > 0.


def test_simulation_game_with_two_teams_different_strategies():
    rn.seed(1234)
    buyer1 = MyopicBuyer("Sarah")
    seller1 = DummySeller("Sarah")
    buyer2 = MyopicBuyer("Steve")
    seller2 = DummySeller("Steve", constant_price=0.1)
    teams = [(buyer1, seller1), (buyer2, seller2)]
    mean_revenue, mean_cs = simulate(teams, horizon, x_0, mc_trials, price_scale)
    # with a very low selling price for team 2, the seller is undervaluing the product and hence makes less revenue
    assert mean_revenue[0] > mean_revenue[1] and np.all(mean_revenue > 0.)
    # with a very low selling price for team 2, the buyer is making a good deal a lot of the time and has higher
    # consumer surplus, on average
    assert mean_cs[0] > mean_cs[1] and np.all(mean_cs > 0.)


def test_simulation_game_with_three_teams():
    rn.seed(1234)
    buyer1 = MyopicBuyer("Sarah")
    seller1 = DummySeller("Sarah")
    buyer2 = MyopicBuyer("Steve")
    seller2 = DummySeller("Steve", constant_price=0.1)
    buyer3 = MyopicBuyer("Emanuel")
    seller3 = DummySeller("Emanuel", constant_price=1.)
    teams = [(buyer1, seller1), (buyer2, seller2), (buyer3, seller3)]
    mean_revenue, mean_cs = simulate(teams, horizon, x_0, mc_trials, price_scale)
    # with a very low selling price for team 2, the seller is undervaluing the product and hence makes less revenue
    # teams 1 and 3 have the same selling strategy, so should get the same sample mean revenue
    assert mean_revenue[2] == mean_revenue[0] and mean_revenue[0] > mean_revenue[1]
    assert np.all(mean_revenue > 0.)
    # with a very low selling price for team 2, the buyer is making a good deal a lot of the time and has higher
    # consumer surplus, on average
    assert mean_cs[0] > mean_cs[1]
    assert np.all(mean_cs > 0.)


def test_faulty_bots_scenario():
    rn.seed(1234)
    buyer1 = MyopicBuyer("Sarah")
    seller1 = DummySeller("Sarah")
    buyer2 = FaultyBuyer()
    seller2 = DummySeller("Basil")
    teams = [(buyer1, seller1), (buyer2, seller2)]
    # This code should terminate.. that's all we're testing
    simulate(teams, horizon, x_0, 1, price_scale)

test_simulation_game_with_two_teams_same_strategies()
test_simulation_game_with_two_teams_different_strategies()
test_simulation_game_with_three_teams()
test_faulty_bots_scenario()