import logging

class Module:
    def __init__(self, levels, inputs):
        self.levels = levels
        self.inputs = inputs
        self.iter = 0
        self.levels.sort(key=lambda x: x.index)

    def predict_flow(self):
        if self.iter < 10:
            self.iter += 1
        else:
            logging.error('Max iterations reached. Aborting')
            return

        logging.debug("---------- PREDICT FLOW --------------")

        for level in self.levels:
            for region in level.regions:
                pred = region.predict()
                for child in region.children:
                    child.setHyp(region.name, pred)

        logging.debug("---------- ERROR FLOW --------------")
        self.error_flow()


    def error_flow(self):
        lowest = True
        error = False

        for level in reversed(self.levels):
            if not lowest and not error:
                return
            for region in level.regions:
                if lowest:
                    for actual in self.inputs[region.name]:
                        if region.error(region.predict(), actual):
                            error = True
                            region.update(actual)
                else:
                    for child in region.children:
                        if region.error(region.predict(), child.hyp):
                            error = True
                            region.update(child.hyp)
            lowest = False
        self.predict_flow()
