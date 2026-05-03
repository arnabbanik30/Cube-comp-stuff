import json
import sys


class Competitor:
    competitor_number_in_events = {}
    last_rank_in_events = {}
    total_competitors = 0

    def __init__(self, id, name, wcaId):
        self.id = int(id)
        self.name = name
        self.wcaId = wcaId
        self.result = {}
        self.adjusted_rank = {}

        if len(wcaId) == 0:
            self.first_timer = True
        else:
            self.first_timer = False


def usage():
    print("Usage: python extra_results_gen.py <input.json>")
    sys.exit(1)


def main():

    if len(sys.argv) < 2:
        usage()

    file_name = sys.argv[1]
    results_file = open(file_name)
    results_info = json.load(results_file)
    results_file.close()

    ## dictionary of all the competitor class instances
    all_competitors = {}

    # getting the competitor information
    for info in results_info["persons"]:
        temp = Competitor(info["id"], info["name"], info["wcaId"])
        all_competitors[temp.id] = temp

    Competitor.total_competitors = len(all_competitors)

    for event in results_info["events"]:
        eventId = event["eventId"]
        Competitor.competitor_number_in_events[eventId] = {}

        round_no = 0
        for round in event["rounds"]:
            round_no += 1
            Competitor.competitor_number_in_events[eventId][round_no] = len(
                round["results"]
            )
            last_rank = 4
            for result in round["results"]:
                personId = result["personId"]
                rank = result["position"]
                if rank == None:
                    continue
                if rank <= 3:
                    if result["best"] < 0 and result["average"] <= 0:
                        rank = 4
                        # print(f'{all_competitors[personId].name} -- event : {eventId} , round : {round_no} , rank : {rank}')
                # print(f'{all_competitors[personId].name} -- event : {eventId} , round : {round_no} , rank : {rank}')

                if all_competitors[personId].result.get(eventId) == None:
                    all_competitors[personId].result[eventId] = {}

                all_competitors[personId].result[eventId][round_no] = rank
                last_rank = max(last_rank, rank)
            if Competitor.last_rank_in_events.get(eventId) == None:
                Competitor.last_rank_in_events[eventId] = {}
            Competitor.last_rank_in_events[eventId][round_no] = last_rank

    for id, competitor in all_competitors.items():
        for eventId, rounds in Competitor.last_rank_in_events.items():
            if (
                competitor.result.get(eventId) == None
            ):  # it means that the competitor has not participated in this event.
                adjst_rank = 0
                for rank in rounds.values():
                    adjst_rank += rank + 1
                competitor.adjusted_rank[eventId] = adjst_rank
                continue

            if len(competitor.result[eventId]) == len(
                Competitor.last_rank_in_events[eventId]
            ):
                competitor.adjusted_rank[eventId] = list(
                    competitor.result[eventId].values()
                )[-1]
                continue
            i = len(Competitor.last_rank_in_events[eventId])
            j = len(competitor.result[eventId])

            # print(f'{competitor.name} -- {eventId} -- {i} -- {j}')
            adjst_rank = 0
            while i >= j:
                if i == j:
                    # print(f"{i}")
                    # print(competitor.result[eventId])
                    adjst_rank += competitor.result[eventId][i]
                else:
                    adjst_rank += Competitor.last_rank_in_events[eventId][i] + 1

                # print(f'{competitor.name} -- {eventId} -- round = {i} -- rank = {Competitor.last_rank_in_events[eventId][i] +1}')
                i -= 1
            competitor.adjusted_rank[eventId] = adjst_rank

    ## sum of ranks
    for id, competitor in all_competitors.items():
        competitor.sum_of_ranks = 0

        for eventId, rank in competitor.adjusted_rank.items():
            competitor.sum_of_ranks += rank

    ### eikhan theke dhanda shuru
    competitors_without_podium_list = []
    newcomer_list = []
    for competitor in all_competitors.values():
        ok = True
        for rank in competitor.adjusted_rank.values():
            if rank <= 3:
                ok = False
                break

        if ok == True:
            competitors_without_podium_list.append(competitor)
        if competitor.first_timer == True:
            newcomer_list.append(competitor)

    competitors_without_podium_list.sort(key=lambda x: x.sum_of_ranks)
    newcomer_list.sort(key=lambda x: x.adjusted_rank["333"])

    cnt = 0
    for competitor in competitors_without_podium_list:
        cnt += 1
        print(
            f"{cnt}. name = {competitor.name} -- sum of rank = {competitor.sum_of_ranks}"
        )
        # for event,rank in competitor.adjusted_rank.items():
        # print(f'\t{event} = {rank}')

    newcomer_cnt = 0
    for newcomer in newcomer_list:
        newcomer_cnt += 1
        print(
            f"{newcomer_cnt}. name = {newcomer.name} -- 3x3 rank = {newcomer.adjusted_rank['333']}"
        )


if __name__ == "__main__":
    main()
