from abc import ABC, abstractmethod


class FilteringStrategy(ABC):
    @abstractmethod
    def apply(self, request, queryset):
        pass


class FilteringManager(ABC):
    def __init__(self, strategies=None):
        self.strategies = strategies

    def apply_filters(self, request, queryset):
        for filter in self.strategies:
            queryset = filter.apply(request, queryset)

        return queryset
