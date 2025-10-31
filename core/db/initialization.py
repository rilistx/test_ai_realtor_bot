from core.config.seeder import data_conditions, data_districts, data_microareas, data_streets

from core.db.models import ConditionModel, DistrictModel, MicroareaModel, StreetModel


async def init_db() -> None:
    conditions = await ConditionModel.first()

    if conditions is None:
        conditions = data_conditions

        for pk, name in conditions.items():
            await ConditionModel.create(
                id=pk,
                name=name.lower(),
            )

    # ###########################################
    districts = await DistrictModel.first()

    if districts is None:
        districts = data_districts

        for pk, name in districts.items():
            await DistrictModel.create(
                id=pk,
                name=name.lower(),
            )

    # ###########################################
    microareas = await MicroareaModel.first()

    if microareas is None:
        microareas = data_microareas

        for pk, name in microareas.items():
            await MicroareaModel.create(
                id=pk,
                name=name.lower(),
            )

    # ###########################################
    streets = await StreetModel.first()

    if streets is None:
        streets = data_streets

        for pk, name in streets.items():
            await StreetModel.create(
                id=pk,
                name=name.lower(),
            )
