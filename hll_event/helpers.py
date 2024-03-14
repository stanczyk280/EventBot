from datetime import datetime, timedelta


def filter_logs(logs, window_seconds=30):
    current_time = datetime.now()
    window_start_time = current_time - timedelta(seconds=window_seconds)

    filtered_logs = []
    for log in logs:
        log_timestamp = datetime.fromtimestamp(
            log.timestamp_ms / 1000
        )
        if window_start_time <= log_timestamp <= current_time:
            filtered_logs.append(log)

    return filtered_logs
