from photon_platform.publish.global_conf import *
import geometor.seer_sessions as module

version = module.__version__

org = "geometor"
org_name = "GEOMETOR"

repo = "seer_sessions"
repo_name = "seer_sessions"

setup_globals(org, org_name, repo, repo_name)

site_title = "SEER Sessions"
project = site_title
html_title = f"{site_title} • {org_name}"
