from datetime import datetime as dt

date_time_format = "%Y-%m-%d %H:%M"
date_time_format_w_seconds = '%Y-%m-%d_%H-%M-%S'

today = dt.now().strftime(date_time_format)
now = dt.now().strftime(date_time_format_w_seconds)


script_path = os.path.abspath(__file__) # path to this script
script_dir = os.path.dirname(script_path) # directory of this script

log_dir = f"{script_dir}/logs_{dt.now().strftime(date_time_format)}"
