import datetime

DATETIME_FMT = "%Y-%m-%dT%H:%M:%S.%fZ"


def parse_date_from_string(s, parse_format="%Y-%m-%dT%H:%M:%S.%fZ"):
    """Parse string to datetime object.
    :param s: str like '2018-11-18T21:03:32.493697Z'
    :param parse_format: str defaults to %Y-%m-%dT%H:%M:%S.%fZ
    :return: datetime.datetime
    """
    return datetime.datetime.strptime(s, parse_format)


def tasks_table(tasks, performance_task_name):
    """Return overview of tasks."""
    out = []
    for t in tasks:
        created_at = parse_date_from_string(t["pulp_created"])
        started_at = parse_date_from_string(t["started_at"])
        finished_at = parse_date_from_string(t["finished_at"])
        task_duration = finished_at - started_at
        waiting_time = started_at - created_at
        out.append(
            "\n-> {task_name} => Waiting time (s): {wait} | Service time (s): {service}".format(
                task_name=performance_task_name,
                wait=waiting_time.total_seconds(),
                service=task_duration.total_seconds(),
            )
        )
    return "\n".join(out)


def print_fmt_experiment_time(label, start, end):
    """Print formatted label and experiment time."""
    print("\n-> {} => Experiment time (s): {}".format(label, (end - start).total_seconds()))


def report_tasks_stats(performance_task_name, tasks):
    """Print out basic stats about received tasks."""
    print(tasks_table(tasks, performance_task_name))
