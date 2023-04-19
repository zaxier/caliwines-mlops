from packaged_poc.common import Workload


class AccessConfig(Workload):
    def _access_config(self):
        """Access the configuration in the conf file"""

        self.logger.info("Accessing the configuration in the conf file")
        self.logger.info(f"label_1: {self.conf['label_1']}")
        self.logger.info(f"label_2: {self.conf['label_2']}")
        self.logger.info(f"label_2_1: {self.conf['label_2']['label_2_1']}")
        self.logger.info(f"label_2_1: {self.conf['label_2']['label_2_2']}")

        print(self.conf)

        assert self.conf["label_1"] == "value_1"
        assert self.conf["label_2"]["label_2_1"] == "value_2_1"
        assert self.conf["label_2"]["label_2_2"] == "value_2_2"

    def launch(self):
        self.logger.info("Launching AccessConfigTask")
        self._access_config()
        self.logger.info("AccessConfigTask finished!")


# if you're using python_wheel_task, you'll need the entrypoint function to be used in setup.py
def entrypoint():  # pragma: no cover
    task = AccessConfig()
    task.launch()


# if you're using spark_python_task, you'll need the __main__ block to start the code execution
if __name__ == "__main__":
    entrypoint()
