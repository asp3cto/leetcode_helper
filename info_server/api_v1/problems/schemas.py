"""
Schemas for problems route
"""

from enum import Enum

from pydantic import BaseModel, computed_field


class DifficultyLevel(str, Enum):
    easy = "Easy"
    medium = "Medium"
    hard = "Hard"


class Topic(str, Enum):
    """I`m sorry..."""

    queue = "Queue"
    suffix_array = "Suffix Array"
    biconnected_component = "Biconnected Component"
    math = "Math"
    hash_function = "Hash Function"
    segment_tree = "Segment Tree"
    strongly_connected_component = "Strongly Connected Component"
    greedy = "Greedy"
    combinatorics = "Combinatorics"
    line_sweep = "Line Sweep"
    enumeration = "Enumeration"
    matrix = "Matrix"
    prefix_sum = "Prefix Sum"
    shell = "Shell"
    memoization = "Memoization"
    binary_indexed_tree = "Binary Indexed Tree"
    brainteaser = "Brainteaser"
    randomized = "Randomized"
    sorting = "Sorting"
    monotonic_stack = "Monotonic Stack"
    binary_tree = "Binary Tree"
    depth_first_search = "Depth-First Search"
    bit_manipulation = "Bit Manipulation"
    ordered_set = "Ordered Set"
    quickselect = "Quickselect"
    divide_and_conquer = "Divide and Conquer"
    heap_priority_queue = "Heap (Priority Queue)"
    rolling_hash = "Rolling Hash"
    array = "Array"
    binary_search_tree = "Binary Search Tree"
    merge_sort = "Merge Sort"
    counting_sort = "Counting Sort"
    eulerian_circuit = "Eulerian Circuit"
    interactive = "Interactive"
    data_stream = "Data Stream"
    database = "Database"
    game_theory = "Game Theory"
    binary_search = "Binary Search"
    probability_and_statistics = "Probability and Statistics"
    dynamic_programming = "Dynamic Programming"
    string_matching = "String Matching"
    hash_table = "Hash Table"
    graph = "Graph"
    shortest_path = "Shortest Path"
    geometry = "Geometry"
    union_find = "Union Find"
    monotonic_queue = "Monotonic Queue"
    simulation = "Simulation"
    two_pointers = "Two Pointers"
    doubly_linked_list = "Doubly-Linked List"
    linked_list = "Linked List"
    design = "Design"
    counting = "Counting"
    number_theory = "Number Theory"
    stack = "Stack"
    sliding_window = "Sliding Window"
    reservoir_sampling = "Reservoir Sampling"
    trie = "Trie"
    minimum_spanning_tree = "Minimum Spanning Tree"
    tree = "Tree"
    radix_sort = "Radix Sort"
    breadth_first_search = "Breadth-First Search"
    concurrency = "Concurrency"
    iterator = "Iterator"
    backtracking = "Backtracking"
    recursion = "Recursion"
    rejection_sampling = "Rejection Sampling"
    bitmask = "Bitmask"
    topological_sort = "Topological Sort"
    bucket_sort = "Bucket Sort"
    string = "String"


class ProblemSchemaBase(BaseModel):
    """
    Base class for problem schema
    """

    id: int
    question_title: str


class ProblemSchemaShort(ProblemSchemaBase):
    """
    Class with short problem schema for endpoints
    """

    difficulty_level: DifficultyLevel | None = None
    question_slug: str

    @computed_field
    @property
    def url(self) -> str:
        return get_url_from_problem_slug(self.question_slug)


class ProblemSchemaFull(ProblemSchemaShort):
    """
    Class with full problem schema for endpoints
    """

    question_text: str | None = None
    topic_tagged_text: list[str] | None = None
    success_rate: float | None = None
    total_submission: int | None = None
    total_accepted: int | None = None
    likes: int | None = None
    dislikes: int | None = None
    hints: str | None = None
    similar_questions_id: list[int] | None = None
    similar_questions_text: list[str] | None = None


def get_url_from_problem_slug(problem_slug: str):
    return f"https://leetcode.com/problems/{problem_slug}/description/"
