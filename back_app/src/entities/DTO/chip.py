from . import ma, post_load
from ..model.chip import Chip


class CreatChipSchema(ma.Schema):
    class Meta:
        model = Chip

    # def __load__(self, data):
    # super().load(data)

    @post_load
    def make_object(self, data, **kwargs):
        return Chip(**data)