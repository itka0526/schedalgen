# pyright: reportAttributeAccessIssue = false

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
#                                    TODO                                     #
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
# ДОДЕЛАЙТЕ АЛГОРИТМ!!!
# ДОДЕЛАЙТЕ АЛГОРИТМ!!!
# ДОДЕЛАЙТЕ АЛГОРИТМ!!!
# ДОДЕЛАЙТЕ АЛГОРИТМ!!!
# ДОДЕЛАЙТЕ АЛГОРИТМ!!!

from typing import Any, Optional, Tuple

import matplotlib.pyplot as plt
import numpy as np
import random
from deap import algorithms
from deap import base
from deap import creator
from deap import tools

from schedalgen.problem import ScheduleProblem
from schedalgen.benchmark import ScheduleProblemBenchmark


class ScheduleProblemSolution:

    def __init__(
        self,
        hard_contraint_penalty: int,
        population_size: int,
        crossover_proba: float,
        mutation_proba: float,
        max_generations: int,
        hall_of_fame_size: int,
        tournament_size: int,
        random_seed: int = 52,
        schedule_problem: Optional[ScheduleProblem] = None,
        schedule_problem_benchmark: Optional[ScheduleProblemBenchmark] = None,
    ):
        self.hard_contraint_penalty = hard_contraint_penalty
        self.population_size = population_size
        self.crossover_proba = crossover_proba
        self.mutation_proba = mutation_proba
        self.max_generations = max_generations
        self.hall_of_fame_size = hall_of_fame_size
        self.tournament_size = tournament_size
        self.random_seed = random_seed
        self.schedule_problem = schedule_problem if schedule_problem is not None else ScheduleProblem()
        self.schedule_problem_benchmark = (
            schedule_problem_benchmark
            if schedule_problem_benchmark is not None
            else ScheduleProblemBenchmark(self.hard_constraint_penalty)
        )

        self.toolbox = base.Toolbox()

    def perform_algorithm(self) -> Tuple[Any, Any]:
        self._setup()
        population = self.toolbox.populationCreator(n=self.population_size)

        stats = tools.Statistics(lambda individual: individual.fitness.values)
        stats.register("min", np.min)
        stats.register("mean", np.mean)
        hall_of_fame = tools.HallOfFame(self.hall_of_fame_size)

        population, logbook = self._performGeneticAlgorithmWithElitism(
            population,
            self.toolbox,
            crossover_proba=self.crossover_proba,
            mutation_proba=self.mutation_proba,
            n_generations=self.max_generations,
            stats=stats,
            hall_of_fame=hall_of_fame,
            verbose=True,
        )
        return (hall_of_fame, logbook)

    def report_stats(self, hall_of_fame: Any, logbook: Any) -> None:
        best_individual = hall_of_fame.items[0]
        best_individual_string = "".join(map(str, best_individual))
        self.schedule_problem_benchmark.calculate_cost(best_individual_string)
        min_fitness_values, mean_fitness_values = logbook.select("min", "mean")
        self.schedule_problem.save_table(best_individual_string, "schedule.json")
        report = (
            "Solution report\n\n"
            f"Best fitness value: {best_individual.fitness.values[0]}\n"
            "Best individual stats\n"
            + self.schedule_problem_benchmark.get_violations_report()
            + "Schedule output file name: schedule.json"
        )
        print(report)

        _, axis = plt.subplots()
        max_value = np.max(np.concatenate([min_fitness_values, mean_fitness_values]))
        y_limit = int((max_value + 10) - (max_value % 10))
        axis.set_xlim(0, self.max_generations)
        axis.set_ylim(0, y_limit)
        axis.set_xlabel("Generation")
        axis.set_ylabel("Min/mean fitness value")
        axis.plot(min_fitness_values, color="red", linestyle="--")
        axis.plot(mean_fitness_values, color="blue")
        axis.set_title("Min and mean fitness over generations", fontsize=14)

        plt.tight_layout()
        plt.savefig("stats.png")

    def _performGeneticAlgorithmWithElitism(
        self,
        population,
        toolbox,
        crossover_proba,
        mutation_proba,
        n_generations,
        stats=None,
        hall_of_fame=None,
        verbose=__debug__,
    ):
        """This algorithm is similar to DEAP's ``eaSimple()`` algorithm, with the
        modification that halloffame is used to implement an elitism mechanism.
        The individuals contained in the ``halloffame`` are directly injected into
        the next generation and are not subject to the genetic operators of
        selection, crossover and mutation.
        """
        logbook = tools.Logbook()
        # fmt: off
        logbook.header = ['gen', 'nevals'] + (stats.fields if stats else [])
        # fmt: on

        # Evaluate the individuals with an invalid fitness
        invalid_individuals = [ind for ind in population if not ind.fitness.valid]
        fitnesses = toolbox.map(toolbox.evaluate, invalid_individuals)
        for ind, fit in zip(invalid_individuals, fitnesses):
            ind.fitness.values = fit

        if hall_of_fame is None:
            raise ValueError("halloffame parameter must not be empty!")

        hall_of_fame.update(population)
        record = stats.compile(population) if stats else {}
        logbook.record(gen=0, nevals=len(invalid_individuals), **record)
        if verbose:
            print(logbook.stream)

        # Begin the generational process
        for gen in range(1, n_generations + 1):
            # Select the next generation individuals
            offspring = toolbox.select(population, len(population) - len(hall_of_fame.items))
            # Vary the pool of individuals
            offspring = algorithms.varAnd(offspring, toolbox, crossover_proba, mutation_proba)
            # Evaluate the individuals with an invalid fitness
            invalid_offspring = [ind for ind in offspring if not ind.fitness.valid]
            fitnesses = toolbox.map(toolbox.evaluate, invalid_offspring)
            for ind, fit in zip(invalid_offspring, fitnesses):
                ind.fitness.values = fit

            # Add the best back to population
            offspring.extend(hall_of_fame.items)
            # Update the hall of fame with the generated individuals
            hall_of_fame.update(offspring)
            # Replace the current population by the offspring
            population[:] = offspring
            # Append the current generation statistics to the logbook
            record = stats.compile(population) if stats else {}
            logbook.record(gen=gen, nevals=len(invalid_offspring), **record)
            if verbose:
                print(logbook.stream)

        return population, logbook

    def calculateCost(self, individual) -> Tuple:
        individual_string = "".join(map(str, individual))
        cost = (self.schedule_problem_benchmark.calculate_cost(individual_string),)
        return cost

    def _setup(self) -> None:
        # РАБОАТЬ НАДО ТУТ!!!
        # РАБОАТЬ НАДО ТУТ!!!
        # РАБОАТЬ НАДО ТУТ!!!
        # РАБОАТЬ НАДО ТУТ!!!
        # РАБОАТЬ НАДО ТУТ!!!
        creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
        creator.create("Individual", list, fitness=creator.FitnessMin)
        self.toolbox.register("zeroOrOne", random.randint, 0, 1)
        self.toolbox.register(
            "individualCreator",
            tools.initRepeat,
            creator.Individual,
            self.toolbox.zeroOrOne,
            len(self.schedule_problem),
        )
        self.toolbox.register(
            "populationCreator",
            tools.initRepeat,
            list,
            self.toolbox.individualCreator,
        )
        self.toolbox.register("evaluate", self.calculateCost)
        self.toolbox.register("select", tools.selTournament, tournsize=self.tournament_size)
        # ВОТ ТУТ ОСОБЕННО!!!
        # ВОТ ТУТ ОСОБЕННО!!!
        # ВОТ ТУТ ОСОБЕННО!!!
        # ВОТ ТУТ ОСОБЕННО!!!
        # ВОТ ТУТ ОСОБЕННО!!!
        self.toolbox.register("mate", tools.cxTwoPoint)
        self.toolbox.register("mutate", tools.mutFlipBit, indpb=1.0 / len(self.schedule_problem))
        # ВОТ ТУТ ОСОБЕННО!!!
        # ВОТ ТУТ ОСОБЕННО!!!
        # ВОТ ТУТ ОСОБЕННО!!!
        # ВОТ ТУТ ОСОБЕННО!!!
        # ВОТ ТУТ ОСОБЕННО!!!
