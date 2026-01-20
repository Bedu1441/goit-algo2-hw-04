from collections import deque, defaultdict
from typing import Dict, List, Tuple, Optional

class EdmondsKarp:
    def __init__(self):
        # capacity[u][v] = c
        self.capacity: Dict[str, Dict[str, int]] = defaultdict(dict)
        # adjacency list
        self.graph: Dict[str, List[str]] = defaultdict(list)

    def add_edge(self, u: str, v: str, cap: int) -> None:
        if cap < 0:
            raise ValueError("Capacity must be non-negative")
        if v not in self.graph[u]:
            self.graph[u].append(v)
        if u not in self.graph[v]:
            self.graph[v].append(u)

        # if multiple edges same (u,v) - сумуємо
        self.capacity[u][v] = self.capacity[u].get(v, 0) + cap
        # ensure reverse exists in capacity dict (for residual)
        self.capacity[v].setdefault(u, 0)

    def _bfs(self, s: str, t: str) -> Tuple[int, Dict[str, Optional[str]]]:
        parent: Dict[str, Optional[str]] = {s: None}
        q = deque([(s, float("inf"))])

        while q:
            u, flow = q.popleft()
            for v in self.graph[u]:
                if v not in parent and self.capacity[u].get(v, 0) > 0:
                    parent[v] = u
                    new_flow = min(flow, self.capacity[u][v])
                    if v == t:
                        return new_flow, parent
                    q.append((v, new_flow))

        return 0, parent

    def max_flow_with_log(
        self,
        s: str,
        t: str,
        terminals: Tuple[str, str],
        shops: List[str],
    ) -> Tuple[int, Dict[Tuple[str, str], int], List[str]]:
        """
        Повертає:
          max_flow,
          flows_terminal_shop[(terminal, shop)] = фактичний потік,
          log_steps: текстові кроки (augmenting paths)
        """
        total_flow = 0
        flow_ts: Dict[Tuple[str, str], int] = defaultdict(int)
        log_steps: List[str] = []

        while True:
            path_flow, parent = self._bfs(s, t)
            if path_flow == 0:
                break

            # відновлюємо шлях
            v = t
            path = []
            while v is not None:
                path.append(v)
                v = parent[v]
            path.reverse()  # s ... t

            # оновлюємо залишкові пропускні здатності
            total_flow += path_flow
            for i in range(len(path) - 1):
                u, v = path[i], path[i + 1]
                self.capacity[u][v] -= path_flow
                self.capacity[v][u] += path_flow

            # виділяємо Terminal і Shop з цього шляху (бо форма S->T->W->Shop->T)
            terminal_hit = None
            shop_hit = None
            for node in path:
                if node in terminals:
                    terminal_hit = node
                if node in shops:
                    shop_hit = node

            if terminal_hit and shop_hit:
                flow_ts[(terminal_hit, shop_hit)] += path_flow

            log_steps.append(f"Path: {' -> '.join(path)}, add flow = {path_flow}")

        return total_flow, flow_ts, log_steps


def build_logistics_network() -> Tuple[EdmondsKarp, str, str, Tuple[str, str], List[str]]:
    ek = EdmondsKarp()

    S = "SuperSource"
    T = "SuperSink"

    terminal1 = "Terminal 1"
    terminal2 = "Terminal 2"

    warehouses = ["Warehouse 1", "Warehouse 2", "Warehouse 3", "Warehouse 4"]
    shops = [f"Shop {i}" for i in range(1, 15)]

    # SuperSource -> Terminals (велика пропускна здатність)
    ek.add_edge(S, terminal1, 10**9)
    ek.add_edge(S, terminal2, 10**9)

    # Shops -> SuperSink (велика пропускна здатність)
    for shop in shops:
        ek.add_edge(shop, T, 10**9)

    # Terminals -> Warehouses (як у завданні)
    ek.add_edge(terminal1, "Warehouse 1", 25)
    ek.add_edge(terminal1, "Warehouse 2", 20)
    ek.add_edge(terminal1, "Warehouse 3", 15)

    ek.add_edge(terminal2, "Warehouse 3", 15)
    ek.add_edge(terminal2, "Warehouse 4", 30)
    ek.add_edge(terminal2, "Warehouse 2", 10)

    # Warehouses -> Shops
    ek.add_edge("Warehouse 1", "Shop 1", 15)
    ek.add_edge("Warehouse 1", "Shop 2", 10)
    ek.add_edge("Warehouse 1", "Shop 3", 20)

    ek.add_edge("Warehouse 2", "Shop 4", 15)
    ek.add_edge("Warehouse 2", "Shop 5", 10)
    ek.add_edge("Warehouse 2", "Shop 6", 25)

    ek.add_edge("Warehouse 3", "Shop 7", 20)
    ek.add_edge("Warehouse 3", "Shop 8", 15)
    ek.add_edge("Warehouse 3", "Shop 9", 10)

    ek.add_edge("Warehouse 4", "Shop 10", 20)
    ek.add_edge("Warehouse 4", "Shop 11", 10)
    ek.add_edge("Warehouse 4", "Shop 12", 15)
    ek.add_edge("Warehouse 4", "Shop 13", 5)
    ek.add_edge("Warehouse 4", "Shop 14", 10)

    return ek, S, T, (terminal1, terminal2), shops


def print_terminal_shop_table(flow_ts: Dict[Tuple[str, str], int], terminals: Tuple[str, str], shops: List[str]) -> None:
    print("\nТаблиця потоків Terminal -> Shop (фактичний потік):")
    print(f"{'Terminal':<12} {'Shop':<8} {'Flow':<6}")
    print("-" * 30)
    for term in terminals:
        for shop in shops:
            val = flow_ts.get((term, shop), 0)
            if val > 0:
                print(f"{term:<12} {shop:<8} {val:<6}")


def analyze(flow_ts: Dict[Tuple[str, str], int], terminals: Tuple[str, str], shops: List[str]) -> None:
    # 1) який термінал забезпечує найбільший потік
    terminal_totals = {term: 0 for term in terminals}
    shop_totals = {shop: 0 for shop in shops}
    for (term, shop), f in flow_ts.items():
        terminal_totals[term] += f
        shop_totals[shop] += f

    print("\nАналіз:")
    for term, total in terminal_totals.items():
        print(f"- {term} забезпечив загальний потік: {total}")

    top_terminal = max(terminal_totals, key=terminal_totals.get)
    print(f"Відповідь 1: найбільший потік дає {top_terminal}.")

    # 3) магазини з найменшим потоком
    min_flow = min(shop_totals.values()) if shop_totals else 0
    min_shops = [s for s, v in shop_totals.items() if v == min_flow]
    print(f"Відповідь 3: найменше товарів отримали: {min_shops} (потік={min_flow}).")

    # 2,4) “вузькі місця” — ребра з малими capacity,
    # які потенційно обмежують постачання (особливо 5,10 тощо).
    print("Відповідь 2/4: вузькі місця — ребра з малими пропускними здатностями (до Shop 13: cap=5),")
    print("а також обмежені виходи з терміналів до складів та зі складів до магазинів. Збільшення цих cap може підняти загальний потік.")


def main():
    ek, S, T, terminals, shops = build_logistics_network()

    max_flow, flow_ts, log_steps = ek.max_flow_with_log(S, T, terminals, shops)

    print(f"Максимальний потік у мережі: {max_flow}\n")

    print("Покрокові кроки Edmonds-Karp (augmenting paths):")
    for i, step in enumerate(log_steps, 1):
        print(f"{i:02d}. {step}")

    print_terminal_shop_table(flow_ts, terminals, shops)
    analyze(flow_ts, terminals, shops)

if __name__ == "__main__":
    main()

