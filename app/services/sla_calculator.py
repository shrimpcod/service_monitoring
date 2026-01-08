from datetime import datetime
from app.models.state import ServiceState, ServiceStatus

def calculate_sla(
        service_name: str,
        states: list[ServiceState],
        start_date: datetime,
        end_date: datetime,
) -> dict:

    total_seconds = (end_date - start_date).total_seconds()

    if total_seconds <= 0:
        return{"sla": 100.0, "downtime": 0.0}

    downtime_seconds = 0.0
    sorted_states = sorted(states, key=lambda x: x.created_at)

    for i in range(len(sorted_states)):
        current_state = sorted_states[i]

        segment_start = max(current_state.created_at, start_date)

        if i+1 < len(sorted_states):
            next_state_time = sorted_states[i+1].created_at
            segment_end = min(next_state_time, end_date)
        else:
            segment_end = end_date

        if segment_start < segment_end and current_state.status == ServiceStatus.not_working:
            downtime_seconds += (segment_end - segment_start).total_seconds()

    sla_percentage = ((total_seconds - downtime_seconds) / total_seconds) * 100

    return {
        "service_name": service_name,
        "start_date": start_date,
        "end_date": end_date,
        "sla_percentage": sla_percentage,
        "downtime_seconds": downtime_seconds,
    }
