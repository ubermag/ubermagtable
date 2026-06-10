import ubermagtable as ut


def test_interact():
    table = ut.sample_data()

    # Only test whether it runs.
    @ut.interact(xlim=table.slider())
    def myplot(xlim):
        table.mpl(xlim=xlim)
