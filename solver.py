import heapq
    

def beam_search(input, task, beam_size, max_depth):
    current = [(10, "", input)]

    solutions = []

    # BFS
    for i in range(max_depth):
        next = []

        print(f"Round {i} all candidates: {current}")

        for (score, proposal, current_state) in current:

            print(f"Round {i} proposal: {proposal}, current_state: {current_state}, score: {score}")

            if current_state == "24":
                solutions.append((proposal, current_state))
                continue

            if abs(score) < 1:
                continue
            
            proposals, next_states = task.generate_proposals(current_state)
            for p, l in zip(proposals, next_states):
                score = task.evaluate(l)
                next.append((score, proposal + ';' + p, l))

                print(f"Round {i} candidate current: {current_state}, proposal: {proposal};{p}, next_state: {l}, score: {score}")

        current = sorted(next, reverse=True)[:beam_size]

    return solutions

if __name__ == "__main__":
    from task_24 import Game24
    task = Game24()

    solutions = beam_search("3 3 6 10", task, beam_size=5, max_depth=4)
    print(solutions)