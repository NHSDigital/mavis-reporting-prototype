import random


class MeasureFaker:
    def __init__(self, seed: str, organisation_type: str):
        self.rng = random.Random(seed)
        self.organisation_type = organisation_type

    def eligible_cohort_size(self) -> int:
        match self.organisation_type:
            case "region":
                return self.rng.randint(85000, 150000)
            case "provider":
                return self.rng.randint(7500, 12500)
            case "school":
                return self.rng.randint(500, 2000)
            case _:
                raise ValueError(f"Invalid organisation type: {self.organisation_type}")

    def measures(self, eligible_cohort_size: int) -> dict[str, int]:
        """
        Fakes a set of measure values for a given cohort size.
        """
        performance = self.rng.randint(85, 99)

        measures = {}

        sessions = round(eligible_cohort_size / 300)

        measures["sessions_completed"] = self.rng.randint(
            round(performance * sessions / 2 / 100),
            round(performance * sessions / 100),
        )

        measures["schools"] = sessions
        measures["schools_scheduled"] = round(performance / 100 * 0.92 * sessions)
        measures["schools_notified"] = round(performance / 100 * 0.9 * sessions)
        measures["schools_completed"] = round(performance / 100 * 0.8 * sessions)

        measures["consent_offered"] = round(eligible_cohort_size * 0.99)

        measures["consent_offered_percentage"] = round(
            measures["consent_offered"] / eligible_cohort_size * 100
        )

        consent_given = round(eligible_cohort_size * performance / 100)
        consent_refused = round((eligible_cohort_size - consent_given) / 3)
        measures["consent_given"] = consent_given
        measures["consent_given_percentage"] = round(
            consent_given / eligible_cohort_size * 100
        )
        measures["consent_refused"] = consent_refused
        measures["consent_refused_percentage"] = round(
            consent_refused / eligible_cohort_size * 100
        )

        measures["no_response"] = round(
            eligible_cohort_size - consent_given - measures["consent_refused"]
        )
        measures["no_response_percentage"] = round(
            measures["no_response"] / eligible_cohort_size * 100
        )

        measures["vaccinated"] = round(consent_given * performance / 100)
        measures["vaccinated_elsewhere"] = round(
            (measures["vaccinated"] * (1 - performance / 100)) / 2
        )
        measures["vaccinations"] = round(measures["vaccinated"] * 1.001)
        measures["uptake"] = round(
            (measures["vaccinated"] + measures["vaccinated_elsewhere"])
            / eligible_cohort_size
            * 100
        )

        return measures
