class ProgressMapperService:
    def __init__(self, enrollment):
        self.enrollment = enrollment
        self.course = enrollment.course
        self.progress_records = enrollment.progress_records

        # build lookup maps once (O(1) access)
        self.section_map = {
            section.id: section
            for section in self.course.sections
        }

    def map_progress(self):
        mapped_progress = []

        for progress in self.progress_records:
            record = {
                "id": progress.id,
                "trackable_type": progress.trackable_type,
                "trackable_id": progress.trackable_id,
                "status": progress.status,
                "completed_at": progress.completed_at,
                "created_at": progress.created_at,
            }

            # attach section details
            if progress.trackable_type == "section":
                record["section"] = self.section_map.get(
                    progress.trackable_id
                )

            # future: lessons
            # if progress.trackable_type == "lesson":
            #     record["lesson"] = lesson_map.get(progress.trackable_id)

            mapped_progress.append(record)

        return mapped_progress
