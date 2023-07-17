from collections import defaultdict
cases = int(input())

speakers = defaultdict(list)
understanders = defaultdict(list)

for i in range(cases):
    p_langs = input().split(" ");
    for idx, s in enumerate(p_langs):
        if idx == 0:
            continue
        elif idx == 1:
            speakers[s].append(p_langs[0])
        else:
            understanders[s].append(p_langs[0])

graph = defaultdict(list)
for lang, speakers_list in speakers.items():
    for speaker in speakers_list:
        for idx in range(len(speakers_list)):
            if speakers_list[idx] != speaker:
                graph[speaker].append(speakers_list[idx])

for lang, understanders_list in understanders.items():
    for understander in understanders_list:
        graph[understander].extend(speakers[lang])

def longest_circuit(graph: defaultdict, cur: str, start: str, visited: set):
    visited.add(cur)

    neighbors = graph[cur] if cur in graph else []
    if start in neighbors:
        visited.remove(cur)
        # print(f"Returned [1] here with cur={cur}, visited={visited}")
        return 1

    new_neighbors = [x for x in neighbors if x not in visited]
    if len(new_neighbors) == 0:
        visited.remove(cur)
         # print(f"Returned [2] here with cur={cur}, visited={visited}")
        return 0

    max_size = 0
    for neighbor in new_neighbors:
        cur_circuit = longest_circuit(graph, neighbor, start, visited)
        max_size = max_size if max_size >= cur_circuit else cur_circuit + 1

    visited.remove(cur)
    # print(f"Returned [3] here with cur={cur}, visited={visited}")
    return max_size


visited = set()
max_size = 0
for k in graph.keys():
    cur_circuit = longest_circuit(graph, k, k, visited)
    max_size = max_size if max_size >= cur_circuit else cur_circuit

print(graph)
print(cases - 1) if max_size == 0 else print(cases - max_size)
