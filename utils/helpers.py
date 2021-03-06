import os, yaml, logging, time
import logging.config
import logging
from constants import PROJECT_ROOT
from reports import ResultSummary


log = logging.getLogger("bender")


class ResultsAndLogs(object):
    def __init__(self):
        self._logs_root_dir = os.path.join(PROJECT_ROOT, 'logs')
        self._test_build = None
        self.logger_conf = os.path.join(PROJECT_ROOT, 'logger.yml')
        self._logger_name = "results"
        self.logger_dict = self.conf_to_dict()
        self._current_log_path = "/tmp/logs"
        self._current_log_file = "/tmp/logs"
        self._current_date = self.get_current_date()
        self._current_time = self.get_current_time()

    @property
    def test_build(self):
        return self._test_build

    @test_build.setter
    def test_build(self, val):
        self._test_build = val

    @property
    def logger_name(self):
        return self._logger_name

    @logger_name.setter
    def logger_name(self, val):
        self._logger_name = val

    @property
    def current_log_path(self):
        return self._current_log_path

    @property
    def current_log_file(self):
        return self._current_log_file

    def get_current_date(self):
        return time.strftime("%Y-%m-%d", time.localtime())

    def get_current_time(self):
        return time.strftime("%H-%M-%S")

    def conf_to_dict(self):
        return yaml.load(open(self.logger_conf))

    def get_actual_logger(self, test_case=''):
        log_file = os.path.join(PROJECT_ROOT, 'logs',
                                self._current_date,
                                self._current_time,
                                self._test_build, test_case,
                                self.logger_name)
        if not os.path.exists(log_file):
            os.system("mkdir -p {0}".format(os.path.dirname(log_file)))

        self._current_log_path = os.path.dirname(log_file)
        self._current_log_file = log_file

        self.logger_dict['logging']['handlers']['logfile'][
            'filename'] = log_file

        logging.config.dictConfig(self.logger_dict['logging'])

    def del_existing_logs(self, test_case=''):
        log_file = os.path.join(PROJECT_ROOT, 'logs',
                                self._current_date,
                                self._current_time,
                                self._test_build, test_case)
        if os.path.exists(log_file):
            os.system('rm -rf {}/*'.format(log_file))


results_logs = ResultsAndLogs()


def generate_final_results(expect_cases, results_logs):
    log_path = results_logs.current_log_path
    test_build = results_logs.test_build
    if test_build not in log_path:
        return
    final_path = os.path.join(
        log_path.split(test_build)[0], test_build)
    report = ResultSummary(expect_cases, final_path, test_build)
    report.run()


def yaml2dict(yaml_file):
    return yaml.load(open(yaml_file))
