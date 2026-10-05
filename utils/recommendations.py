def recommend_crops(
    crop_data,
    soil_type="",
    season="",
    state=""
):
    """
    Recommend crops based on soil, season and state.
    """

    recommendations = []

    soil_type = soil_type.lower().strip()
    season = season.lower().strip()
    state = state.lower().strip()

    for row in crop_data:

        row_soil = str(
            row.get("soil_type", "")
        ).lower()

        row_season = str(
            row.get("season", "")
        ).lower()

        row_state = str(
            row.get("state", "")
        ).lower()

        soil_match = (
            not soil_type
            or soil_type in row_soil
        )

        season_match = (
            not season
            or season in row_season
        )

        state_match = (
            not state
            or state in row_state
        )

        if (
            soil_match
            and season_match
            and state_match
        ):
            recommendations.append(row)

    return recommendations