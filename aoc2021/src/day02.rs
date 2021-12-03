#[aoc(day2, part1)]
pub fn solve_part1(input: &str) -> i32 {
    let mut pos = input.lines().fold((0, 0), |acc, l| {
        let mut parts = l.trim().split_whitespace();
        let dir = parts.next().unwrap();
        let x = parts.next().unwrap().parse::<i32>().unwrap();
        match dir {
            "forward" => (acc.0 + x, acc.1),
            "down" => (acc.0, acc.1 + x),
            "up" => (acc.0, acc.1 - x),
            _ => unreachable!(),
        }
    });

    pos.0 * pos.1
}

#[aoc(day2, part2)]
pub fn solve_part_1(input: &str) -> i32 {
    let pos = input.lines().fold((0, 0, 0), |acc, l| {
        let mut parts = l.trim().split_whitespace();
        let dir = parts.next().unwrap();
        let x = parts.next().unwrap().parse::<i32>().unwrap();
        match dir {
            "forward" => (acc.0 + x, acc.1 + x * acc.2, acc.2),
            "down" => (acc.0, acc.1, acc.2 + x),
            "up" => (acc.0, acc.1, acc.2 - x),
            _ => unreachable!(),
        }
    });

    pos.0 * pos.1
}
