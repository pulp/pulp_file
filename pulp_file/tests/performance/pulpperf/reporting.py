import datetime
import statistics

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


def tasks_min_max_table(tasks):
    """Return overview of tasks dates min and max in a table."""
    """
    out = "\n%11s\t%27s\t%27s\n" % ("field", "min", "max")
    for f in ("pulp_created", "started_at", "finished_at"):
        sample = [datetime.datetime.strptime(t[f], DATETIME_FMT) for t in tasks]
        out += "%11s\t%s\t%s\n" % (
            f,
            min(sample).strftime(DATETIME_FMT),
            max(sample).strftime(DATETIME_FMT),
        )
    return out
    """


def data_stats(data):
    """Return basic stats fetch from provided data."""
    return {
        "samples": len(data),
        "min": min(data),
        "max": max(data),
        "mean": statistics.mean(data),
        "stdev": statistics.stdev(data) if len(data) > 1 else 0.0,
    }


def fmt_data_stats(data):
    """
    Format data.

    https://stackoverflow.com/questions/455612/limiting-floats-to-two-decimal-points
    """
    return {
        "samples": data["samples"],
        "min": float("%.02f" % round(data["min"], 2)),
        "max": float("%.02f" % round(data["max"], 2)),
        "mean": float("%.02f" % round(data["mean"], 2)),
        "stdev": float("%.02f" % round(data["stdev"], 2)),
    }


def tasks_waiting_time(tasks):
    """Analyse tasks waiting time (i.e. started_at - _created)."""
    durations = []
    for t in tasks:
        diff = datetime.datetime.strptime(
            t["started_at"], DATETIME_FMT
        ) - datetime.datetime.strptime(t["pulp_created"], DATETIME_FMT)
        durations.append(diff.total_seconds())
    return fmt_data_stats(data_stats(durations))


def tasks_service_time(tasks):
    """Analyse tasks service time (i.e. finished_at - started_at)."""
    durations = []
    for t in tasks:
        diff = datetime.datetime.strptime(
            t["finished_at"], DATETIME_FMT
        ) - datetime.datetime.strptime(t["started_at"], DATETIME_FMT)
        durations.append(diff.total_seconds())
    return fmt_data_stats(data_stats(durations))


def print_fmt_experiment_time(label, start, end):
    """Print formatted label and experiment time."""
    print("\n-> {} => Experiment time (s): {}".format(label, (end - start).total_seconds()))


def report_tasks_stats(performance_task_name, tasks):
    """Print out basic stats about received tasks."""
    print(tasks_table(tasks, performance_task_name))
