from time import perf_counter

from schedalgen.problem import ScheduleProblem
from schedalgen.benchmark import ScheduleProblemBenchmark


def main():
    schedule_problem = ScheduleProblem()
    schedule_problem_benchmark = ScheduleProblemBenchmark(
        10, problem=schedule_problem
    )

    total_schedules = schedule_problem.create_random_schedule()
    
    start_time = perf_counter()
    print(schedule_problem_benchmark.get_cost(total_schedules))
    end_time = perf_counter()
    print(f"Execution took {end_time - start_time} seconds.")


if __name__ == "__main__":
    main()
