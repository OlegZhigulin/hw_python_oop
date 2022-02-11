from dataclasses import dataclass
from typing import Dict, Type


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""
    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float

    def get_message(self) -> str:
        return str(self)

    def __str__(self) -> str:
        return (f'Тип тренировки: {self.training_type}; '
                f'Длительность: {self.duration:.3f} ч.; '
                f'Дистанция: {self.distance:.3f} км; '
                f'Ср. скорость: {self.speed:.3f} км/ч; '
                f'Потрачено ккал: {self.calories:.3f}.')


class Training:
    """Базовый класс тренировки."""
    M_IN_KM: int = 1000
    LEN_STEP: float = 0.65
    H_IN_MIN: int = 60

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(self.__class__.__name__,
                           self.duration,
                           self.get_distance(),
                           self.get_mean_speed(),
                           self.get_spent_calories())


class Running(Training):
    """Тренировка: бег."""

    RUN_COEFF_CALORIE_MEAN_SPEED_MULTIPLC: int = 18
    RUN_COEFF_CALORIE_MEAN_SPEED_SHIFT: int = 20

    def get_spent_calories(self) -> float:

        return ((self.RUN_COEFF_CALORIE_MEAN_SPEED_MULTIPLC
                * self.get_mean_speed()
                - self.RUN_COEFF_CALORIE_MEAN_SPEED_SHIFT)
                * self.weight / self.M_IN_KM
                * self.duration * self.H_IN_MIN)


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    SPORT_WALK_COEFF_CALORIE: float = 0.035
    SPORT_WALK_COEFF_CALORIE_WEIGHT_MULTIPLC: float = 0.029

    def __init__(self,
                 action,
                 duration,
                 weight,
                 height
                 ) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        return ((self. SPORT_WALK_COEFF_CALORIE * self.weight + (
            self.get_mean_speed()**2 // self.height)
            * self.SPORT_WALK_COEFF_CALORIE_WEIGHT_MULTIPLC * self.weight)
            * self.duration * self.H_IN_MIN)


class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP: float = 1.38
    SWIM_COEFF_CALORIE_MEAN_SPEED_ADDITION: float = 1.1
    SWIM_COEFF_CALORIE_MULTIPLC: int = 2

    def __init__(self,
                 action,
                 duration,
                 weight,
                 length_pool,
                 count_pool
                 ) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return (self.length_pool * self.count_pool
                / self.M_IN_KM / self.duration)

    def get_spent_calories(self) -> float:
        return ((self.get_mean_speed()
                + self.SWIM_COEFF_CALORIE_MEAN_SPEED_ADDITION)
                * self.SWIM_COEFF_CALORIE_MULTIPLC
                * self.weight)


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    workout_type_classes: Dict[str, Type[Training]] = {
        'SWM': Swimming,
        'RUN': Running,
        'WLK': SportsWalking,
    }
    if workout_type in workout_type_classes:
        return workout_type_classes[workout_type](*data)

    raise ValueError('Данный вид тренировки отстутсвует, '
                     'проверьте правильность написания')


def main(training: Training) -> None:
    """Главная функция."""
    info: InfoMessage = training.show_training_info()
    print(info.get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
