import heapq
import logging
import pandas as pd

def beam_search(input, task, beam_size, max_depth, logger):
    logger.info(f"input: {input}")
    
    current = [(10, "", input)]

    solutions = []

    # BFS
    for i in range(max_depth):
        next = []

        logger.info(f"Round {i} all candidates: {current}")

        for (score, proposal, current_state) in current:

            logger.info(f"Round {i} proposal: {proposal}, current_state: {current_state}, score: {score}")

            if current_state == "24":
                result = task.generate_cot_proposal(proposal, current_state)
                solutions.append(result)
                continue

            if score < 1:
                continue
            
            proposals, next_states = task.generate_proposals(current_state)
            for p, l in zip(proposals, next_states):
                score = task.evaluate(l)
                next.append((score, proposal + '\n' + p, l))

                logger.info(f"Round {i} candidate current: {current_state}, proposal: {";".join(proposal.split("\n"))};{p}, next_state: {l}, score: {score}")

        current = sorted(next, reverse=True)[:beam_size]

    return solutions

if __name__ == "__main__":
    logging.basicConfig(
        level=logging.DEBUG,  # Set the log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',  # Define the format of log messages
        filename='game_24.log',  # Log messages will be written to this file
        filemode='a'  # 'a' for append mode, 'w' for write mode (overwrites the file)
    )
    logger = logging.getLogger('my_logger')
    
    from task_24 import Game24
    task = Game24()

    data = pd.read_csv("data/24.csv")
    num_puzzle = 0
    num_correct= 0
    for puzzle in data["Puzzles"]:
        num_puzzle += 1
        solutions = beam_search(puzzle, task, beam_size=5, max_depth=4, logger=logger)

        if num_puzzle > 100:
            break

        for solution in solutions:
            if task.test(solution, puzzle) > 0:
                num_correct += 1
                break

        print(f"{num_correct} / {num_puzzle} = {num_correct/num_puzzle}")