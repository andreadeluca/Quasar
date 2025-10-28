from quasar.core.task_decorator import task
from quasar.utils.logging_factory import get_logger

logger = get_logger(__name__)

    # --- LEVEL 1: ROOT TASKS ---
@task()
def setup_env():
    logger.debug("[setup_env] Setting up environment...")


@task()
def init_db():
    logger.debug("[init_db] Initializing database...")


# --- LEVEL 2: TASKS THAT DEPENDS FROM JUST ONE TASK ---
@task(depends_on=["setup_env"])
def load_config():
    logger.debug("[load_config] Loading configuration files...")


@task(depends_on=["init_db"])
def seed_db():
    logger.debug("[seed_db] Seeding initial data into database...")


# --- LEVEL: TASK THAT DEPENDS FROM MORE TASKS ---
@task(depends_on=["load_config", "seed_db"])
def start_services():
    logger.debug("[start_services] Starting background services (API, workers, schedulers...)")


# --- LEVEL: PARALLEL ---
@task(depends_on=["start_services"])
def run_integration_tests():
    logger.debug("[run_integration_tests] Running integration tests...")


@task(depends_on=["start_services"])
def build_frontend():
    logger.debug("[build_frontend] Building frontend application...")


@task(depends_on=["start_services"])
def prepare_artifacts():
    logger.debug("[prepare_artifacts] Preparing deployment artifacts...")


# --- LEVEL 5: TASKS CONVERGING ---
@task(depends_on=["run_integration_tests", "build_frontend", "prepare_artifacts"])
def deploy_staging():
    logger.debug("[deploy_staging] Deploying to staging environment...")


# --- LEVEL 6: ANOTHER BRANCH ---
@task(depends_on=["deploy_staging"])
def smoke_test():
    logger.debug("[smoke_test] Performing smoke tests on staging...")


@task(depends_on=["deploy_staging"])
def notify_team():
    logger.debug("[notify_team] Notifying team via Slack/Email...")


# --- LEVEL 7: FINAL TASK ---
@task(depends_on=["smoke_test", "notify_team"])
def promote_to_production():
    logger.debug("[promote_to_production] Promoting build to production 🎉")
