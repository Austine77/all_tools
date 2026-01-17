def create_study_plan(data):
    plan = []
    hours = data["hours"]
    subjects = data["subjects"]
    per_subject = hours // len(subjects)

    for subject in subjects:
        plan.append({
            "subject": subject,
            "hours": per_subject
        })

    return {"plan": plan}
