import collections.abc

collections.Mapping = collections.abc.Mapping

from experta import *

# 1. Объявление класса фактов
class PlantFact(Fact):
    pass


# 2. Объявление класса движка ЭС
class PlantExpertSystem(KnowledgeEngine):
    def __init__(self):
        super().__init__()
        self.diagnoses = []
        self.fired_rules = []

    # Правило 1: Корневая гниль
    @Rule(PlantFact(leaves_wilt='да'), PlantFact(soil_wet='да'), PlantFact(roots_dark='да'))
    def diagnose_root_rot(self):
        self.fired_rules.append("Правило 1: Диагностика корневой гнили")
        self.diagnoses.append(
            "Корневая гниль. Решение: Срочно извлечь растение, удалить загнившие корни, обработать фунгицидом.")

    # Правило 2: Мучнистая роса
    @Rule(PlantFact(white_plaque='да'), PlantFact(high_humidity='да'), PlantFact(bad_ventilation='да'))
    def diagnose_powdery_mildew(self):
        self.fired_rules.append("Правило 2: Мучнистая роса")
        self.diagnoses.append(
            "Мучнистая роса. Решение: Удалить поражённые листья, обработать фунгицидом, снизить влажность.")

    # Правило 3: Хлороз
    @Rule(PlantFact(yellow_leaves='да'), PlantFact(green_veins='да'), PlantFact(in_shade='да'))
    def diagnose_chlorosis(self):
        self.fired_rules.append("Правило 3: Хлороз из-за нехватки света")
        self.diagnoses.append(
            "Хлороз. Решение: Переместить растение в освещённое место, внести железосодержащие удобрения.")

    # Правило 4: Ожог листьев
    @Rule(PlantFact(dry_spots='да'), PlantFact(direct_sun='да'))
    def diagnose_leaf_burn(self):
        self.fired_rules.append("Правило 4: Ожог листьев")
        self.diagnoses.append("Ожог листьев. Решение: Убрать из прямого солнца, обеспечить рассеянное освещение.")

    # Правило 5: Паутинный клещ
    @Rule(PlantFact(web_on_leaves='да'), PlantFact(light_dots='да'), PlantFact(dry_air='да'))
    def diagnose_spider_mite(self):
        self.fired_rules.append("Правило 5: Поражение паутинным клещом")
        self.diagnoses.append(
            "Паутинный клещ. Решение: Изолировать растение, обработать акарицидом, повысить влажность.")

    # Правило 8: Переувлажнение
    @Rule(PlantFact(yellow_bottom_leaves='да'), PlantFact(soil_wet_long='да'), PlantFact(no_bad_smell='да'))
    def diagnose_overwatering(self):
        self.fired_rules.append("Правило 8: Переувлажнение без гнили")
        self.diagnoses.append("Переувлажнение. Решение: Сократить полив, улучшить дренаж.")


# Вспомогательная функция с защитой от дурака
def ask_question(question_text):
    while True:
        answer = input(f"{question_text} (да/нет): ").strip().lower()
        if answer in ['да', 'нет']:
            return answer
        print("Ошибка ввода. Пожалуйста, введите 'да' или 'нет'.")


# Интерактивный запуск
def run_interactive():
    engine = PlantExpertSystem()
    engine.reset()

    print("--- Диагностика болезней комнатных растений ---")

    # Сбор фактов
    if ask_question("Листья вянут?") == 'да':
        engine.declare(PlantFact(leaves_wilt='да'))
        if ask_question("Почва постоянно влажная?") == 'да':
            engine.declare(PlantFact(soil_wet='да'))
            if ask_question("Наблюдается потемнение корней?") == 'да':
                engine.declare(PlantFact(roots_dark='да'))

    if ask_question("Есть сухие светлые пятна на листьях?") == 'да':
        engine.declare(PlantFact(dry_spots='да'))
        if ask_question("Растение находится под прямыми солнечными лучами?") == 'да':
            engine.declare(PlantFact(direct_sun='да'))

    if ask_question("Есть тонкая паутина на листьях?") == 'да':
        engine.declare(PlantFact(web_on_leaves='да'))
        engine.declare(PlantFact(light_dots=ask_question("Есть мелкие светлые точки?")))
        engine.declare(PlantFact(dry_air=ask_question("Воздух в помещении сухой?")))

    # Запуск вывода
    engine.run()

    print("\n--- Результаты диагностики ---")
    if engine.diagnoses:
        for d in engine.diagnoses:
            print(f"-> {d}")
        print("\nСработавшие правила (блок объяснения):")
        for rule in engine.fired_rules:
            print(f" - {rule}")
    else:
        print("Болезнь не распознана. Недостаточно симптомов или случай не описан в базе.")


if __name__ == "__main__":
    run_interactive()