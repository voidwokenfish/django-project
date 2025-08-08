import os

import pytest
from loguru import logger

BASE_DIR = os.path.dirname(__file__)

LOG_DIR = os.path.join(BASE_DIR, "logs")
os.makedirs(LOG_DIR, exist_ok=True)

LOG_FILE = os.path.join(LOG_DIR, "users_tests.log")
logger.add(
    LOG_FILE,
    rotation="500 KB",
    level="INFO",
    filter=lambda record: "users" in record["extra"].get("source", "")
)

@pytest.fixture
def test_log_data():
    return {}

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    if rep.when == "call":
        rep.test_log_data = getattr(item.funcargs.get("test_log_data", {}), "copy", lambda: {})()

@pytest.hookimpl(tryfirst=True)
def pytest_runtest_logreport(report):
    if report.when == "call":

        source = report.nodeid
        test_log_data = getattr(report, "test_log_data", None) or {}
        message = f"Тест: {source}, данные: {test_log_data}"

        if report.failed:
            logger.bind(source=source).error(f"Ошибка {message}")
            if report.longrepr:
                logger.bind(source=source).error(str(report.longrepr))
        elif report.skipped:
            logger.bind(source=source).warning(f"Пропущено {message}")
        else:
            logger.bind(source=source).success(f"Успешно {message}")