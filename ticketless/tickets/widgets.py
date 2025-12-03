from django import forms


class TicketTypeSelect(forms.Select):
    def __init__(self, *args, **kwargs):
        self.price_map = kwargs.pop("price_map", {})
        super().__init__(*args, **kwargs)

    def create_option(  # noqa: PLR0913
        self, name, value, label, selected, index, subindex=None, attrs=None
    ):
        option = super().create_option(
            name, value, label, selected, index, subindex=subindex, attrs=attrs
        )
        if value and str(value) in self.price_map:
            option["attrs"]["data-price"] = self.price_map[str(value)]
        return option
